"""figspec — draw matplotlib figures from figure_spec.yaml.

Units: thickness/text in pt, lengths in mm. Inches and pixels never appear in
user-facing code.

Usage in a plotting script
--------------------------
    from figspec import Spec
    S = Spec.load("figure_spec.yaml")
    fig = S.canvas()
    ax = S.panel(fig, "a")
    ax.plot(x, y, color=S.color("impacted"), lw=S.pt("data"))
    S.style(ax, "a")
    S.save(fig, "fig1")

Command line
------------
    python figspec.py sheet   figure_spec.yaml            # print the parameter sheet
    python figspec.py audit   figure_spec.yaml fig1.pdf   # verify the exported PDF against the spec
    python figspec.py wire    figure_spec.yaml out        # render empty panel boxes

Requires matplotlib, pyyaml, and pymupdf (for audit).
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Windows consoles default to a legacy codepage (cp949 here). Every printed line
# from this module — the collision check a plotting script triggers, the sheet,
# the audit — carries Korean labels and en dashes, so force UTF-8 once at import
# instead of only on the command-line path.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

MM_PER_IN = 25.4
PT_PER_IN = 72.0
PT_PER_MM = PT_PER_IN / MM_PER_IN  # 2.8346


def mm2in(v: float) -> float:
    return v / MM_PER_IN


def mm2pt(v: float) -> float:
    return v * PT_PER_MM


def pt2mm(v: float) -> float:
    return v / PT_PER_MM


class Spec:
    def __init__(self, data: dict, path: Path | None = None):
        self.d = data
        self.path = path

    # ---------------------------------------------------------------- load
    @classmethod
    def load(cls, path: str | Path = "figure_spec.yaml") -> "Spec":
        import yaml

        p = Path(path)
        with open(p, encoding="utf-8") as f:
            return cls(yaml.safe_load(f), p)

    def _panel(self, pid: str) -> dict:
        for p in self.d["panels"]:
            if str(p["id"]) == str(pid):
                return p
        raise KeyError(f"panel '{pid}' not in spec")

    def _get(self, section: str, key: str, pid: str | None = None):
        if pid is not None:
            ov = self._panel(pid).get("overrides") or {}
            if key in ov:
                return ov[key]
        return self.d[section][key]

    # --------------------------------------------------------------- units
    def pt(self, name: str, pid: str | None = None) -> float:
        """Line thickness in pt: data, axis, errorbar, grid, ticks, minor_ticks."""
        table = {
            "data": ("lines", "data_pt"),
            "axis": ("lines", "axis_pt"),
            "errorbar": ("lines", "errorbar_pt"),
            "grid": ("lines", "grid_pt"),
            "ticks": ("ticks", "width_pt"),
            "minor_ticks": ("ticks", "minor_width_pt"),
            "marker_edge": ("markers", "edge_pt"),
        }
        sec, key = table[name]
        return float(self._get(sec, key, pid))

    def fs(self, name: str, pid: str | None = None) -> float:
        """Font size in pt: axis_label, tick_label, legend, annotation, panel_label."""
        return float(self._get("text", f"{name}_pt", pid))

    def mm(self, name: str, pid: str | None = None) -> float:
        """Length in mm: errorbar_cap, tick_length, tick_pad, handle_length ..."""
        table = {
            "errorbar_cap": ("lines", "errorbar_cap_mm"),
            "tick_length": ("ticks", "length_mm"),
            "minor_tick_length": ("ticks", "minor_length_mm"),
            "tick_pad": ("ticks", "pad_mm"),
            "handle_length": ("legend", "handle_length_mm"),
            "handle_text_gap": ("legend", "handle_text_gap_mm"),
        }
        sec, key = table[name]
        return float(self._get(sec, key, pid))

    @property
    def font_fallback(self) -> list[str]:
        """Families that supply glyphs the spec font lacks. Spec key text.font_fallback."""
        return list(self.d["text"].get("font_fallback") or ["DejaVu Sans"])

    def color(self, role: str) -> str:
        return self.d["colors"]["roles"][role]

    def site_marker(self, site: str) -> str:
        """Marker glyph for a site/group, from spec.markers_by_site."""
        return self.d.get("markers_by_site", {}).get(str(site), "o")

    @property
    def palette(self) -> list[str]:
        return list(self.d["colors"]["roles"].values())

    def marker(self, pid: str | None = None) -> dict:
        return dict(
            markersize=float(self._get("markers", "size_pt", pid)),
            markeredgewidth=float(self._get("markers", "edge_pt", pid)),
            alpha=float(self._get("markers", "alpha", pid)),
        )

    # -------------------------------------------------------------- canvas
    def rc(self) -> dict:
        t, l, k, lg, c = (self.d[s] for s in ("text", "lines", "ticks", "legend", "colors"))
        return {
            # Arial has no ⁺ ⁻ and no subscript digits. matplotlib only walks a
            # fallback chain when font.family is a LIST of families; with
            # font.family="sans-serif" the missing glyphs land on LastResort and
            # export as placeholder boxes.
            "font.family": [t["font_family"], *self.font_fallback],
            "font.sans-serif": [t["font_family"], *self.font_fallback, "Helvetica", "Liberation Sans"],
            "font.size": t["axis_label_pt"],
            "axes.labelsize": t["axis_label_pt"],
            "axes.titlesize": t["axis_label_pt"],
            "xtick.labelsize": t["tick_label_pt"],
            "ytick.labelsize": t["tick_label_pt"],
            "legend.fontsize": t["legend_pt"],
            "axes.linewidth": l["axis_pt"],
            "lines.linewidth": l["data_pt"],
            "grid.linewidth": l["grid_pt"],
            "grid.color": l["grid_color"],
            "xtick.major.size": mm2pt(k["length_mm"]),
            "ytick.major.size": mm2pt(k["length_mm"]),
            "xtick.major.width": k["width_pt"],
            "ytick.major.width": k["width_pt"],
            "xtick.minor.size": mm2pt(k["minor_length_mm"]),
            "ytick.minor.size": mm2pt(k["minor_length_mm"]),
            "xtick.minor.width": k["minor_width_pt"],
            "ytick.minor.width": k["minor_width_pt"],
            "xtick.major.pad": mm2pt(k["pad_mm"]),
            "ytick.major.pad": mm2pt(k["pad_mm"]),
            "xtick.direction": k["direction"],
            "ytick.direction": k["direction"],
            "axes.spines.top": k["top_right_spines"],
            "axes.spines.right": k["top_right_spines"],
            "axes.edgecolor": c["spine"],
            "text.color": c["text"],
            "axes.labelcolor": c["text"],
            "xtick.color": c["spine"],
            "ytick.color": c["spine"],
            "xtick.labelcolor": c["text"],
            "ytick.labelcolor": c["text"],
            "legend.frameon": lg["frame"],
            "legend.handlelength": mm2pt(lg["handle_length_mm"]) / t["legend_pt"],
            "legend.handletextpad": mm2pt(lg["handle_text_gap_mm"]) / t["legend_pt"],
            "legend.labelspacing": lg["row_gap_pt"] / t["legend_pt"],
            "axes.prop_cycle": _cycler(self.palette),
            # Illustrator round-trip
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.bbox": "standard",  # never 'tight': keep the artboard fixed
            "savefig.pad_inches": 0,
            "figure.dpi": 72,
            "savefig.dpi": 72,
        }

    def canvas(self):
        import matplotlib as mpl
        import matplotlib.pyplot as plt

        mpl.rcParams.update(self.rc())
        cv = self.d["canvas"]
        fig = plt.figure(figsize=(mm2in(cv["width_mm"]), mm2in(cv["height_mm"])))
        fig.patch.set_facecolor(cv["background"])
        return fig

    def panel(self, fig, pid: str, label: bool = True):
        """Create an axes at the panel's mm box. Returns the axes."""
        cv = self.d["canvas"]
        p = self._panel(pid)
        W, H = cv["width_mm"], cv["height_mm"]
        ax = fig.add_axes([p["x_mm"] / W, p["y_mm"] / H, p["w_mm"] / W, p["h_mm"] / H])
        ax.set_gid(f"panel-{pid}")
        if label:
            t = self.d["text"]
            x = (p["x_mm"] + t["panel_label_dx_mm"]) / W
            y = (p["y_mm"] + p["h_mm"] + t["panel_label_dy_mm"]) / H
            txt = fig.text(x, y, str(pid), fontsize=self.fs("panel_label"),
                           fontweight=t["panel_label_weight"], ha="left", va="bottom")
            txt.set_gid(f"label-{pid}")
        return ax

    def style(self, ax, pid: str | None = None):
        """Re-apply spec values to one axes (needed when per-panel overrides exist)."""
        k = self.d["ticks"]
        ax.tick_params(
            which="major",
            length=mm2pt(self.mm("tick_length", pid)),
            width=self.pt("ticks", pid),
            pad=mm2pt(self.mm("tick_pad", pid)),
            direction=k["direction"],
            labelsize=self.fs("tick_label", pid),
        )
        if k["minor"]:
            ax.minorticks_on()
            ax.tick_params(which="minor", length=mm2pt(self.mm("minor_tick_length", pid)),
                           width=self.pt("minor_ticks", pid), direction=k["direction"])
        for sp in ax.spines.values():
            sp.set_linewidth(self.pt("axis", pid))
        ax.xaxis.label.set_fontsize(self.fs("axis_label", pid))
        ax.yaxis.label.set_fontsize(self.fs("axis_label", pid))
        if self.d["lines"]["grid"]:
            ax.grid(True, linewidth=self.pt("grid", pid), color=self.d["lines"]["grid_color"])
        lay = self.d.get("layout", {})
        if pid is not None and lay.get("shared_x_rows"):
            p = self._panel(pid); ymin = min(q["y_mm"] for q in self.d["panels"])
            if p["y_mm"] > ymin + 0.5:
                ax.tick_params(labelbottom=False); ax.set_xlabel("")
        if pid is not None and lay.get("shared_y_cols"):
            p = self._panel(pid); xmin = min(q["x_mm"] for q in self.d["panels"])
            if p["x_mm"] > xmin + 0.5:
                ax.tick_params(labelleft=False); ax.set_ylabel("")
        leg = ax.get_legend()
        if leg is not None:
            for t in leg.get_texts():
                t.set_fontsize(self.fs("legend", pid))
        return ax

    # ------------------------------------------------ legend / annotations
    def legend(self, ax, pid: str, **kw):
        """Place the legend from spec: global legend.loc, per-panel panels[].legend
        {loc, dx_mm, dy_mm, ncol, title}. dx/dy shift the anchor in mm."""
        g = self.d["legend"]; p = self._panel(pid); lg = p.get("legend") or {}
        loc = lg.get("loc", g.get("loc", "best"))
        dx, dy = float(lg.get("dx_mm", 0)), float(lg.get("dy_mm", 0))
        opts = dict(loc=loc, ncol=lg.get("ncol", 1), title=lg.get("title"),
                    fontsize=self.fs("legend", pid), frameon=g["frame"])
        if dx or dy:
            # anchor = the corner implied by loc, shifted by mm in axes fraction
            W, H = p["w_mm"], p["h_mm"]
            corner = {"upper right": (1, 1), "upper left": (0, 1), "lower right": (1, 0), "lower left": (0, 0),
                      "center right": (1, .5), "center left": (0, .5), "upper center": (.5, 1), "lower center": (.5, 0)}.get(loc, (1, 1))
            opts["bbox_to_anchor"] = (corner[0] + dx / W, corner[1] + dy / H)
        opts.update(kw)
        leg = ax.legend(**opts)
        if leg is not None:
            leg.set_gid(f"legend-{pid}")
        return leg

    def annotate(self, ax, pid: str):
        """Draw every inline text and arrow declared for this panel in the spec.
        Positions are mm from the panel's bottom-left corner."""
        p = self._panel(pid); W, H = p["w_mm"], p["h_mm"]
        for i, a in enumerate(p.get("annotations") or []):
            t = ax.text(a["x_mm"] / W, a["y_mm"] / H, a["text"], transform=ax.transAxes,
                        fontsize=float(a.get("pt", self.fs("annotation", pid))),
                        color=a.get("color", self.d["colors"]["text"]),
                        ha=a.get("ha", "left"), va=a.get("va", "bottom"),
                        fontweight=a.get("weight", "normal"), rotation=a.get("rotation", 0))
            t.set_gid(f"note-{pid}-{i}")
        for i, r in enumerate(p.get("arrows") or []):
            ax.annotate("", xy=(r["to_mm"][0] / W, r["to_mm"][1] / H), xytext=(r["from_mm"][0] / W, r["from_mm"][1] / H),
                        xycoords="axes fraction", textcoords="axes fraction",
                        arrowprops=dict(arrowstyle=r.get("style", "->"), lw=float(r.get("pt", self.pt("data"))),
                                        color=r.get("color", self.d["colors"]["text"]), shrinkA=0, shrinkB=0))

    def check_collisions(self, fig) -> list[str]:
        """Overlapping text boxes (labels, ticks, legend, notes). Returns messages in mm."""
        fig.canvas.draw(); r = fig.canvas.get_renderer(); items = []
        def add(name, art):
            try:
                bb = art.get_window_extent(r)
            except Exception:
                return
            if bb.width > 0 and bb.height > 0 and art.get_visible() and (getattr(art, "get_text", lambda: "x")() != ""):
                items.append((name, bb))
        for ax in fig.axes:
            gid = ax.get_gid() or "ax"
            add(f"{gid}:xlabel", ax.xaxis.label); add(f"{gid}:ylabel", ax.yaxis.label)
            xl, yl = sorted(ax.get_xlim()), sorted(ax.get_ylim())
            for k, tk in enumerate(ax.xaxis.get_major_ticks()):
                if xl[0] <= tk.get_loc() <= xl[1]: add(f"{gid}:xtick{k}", tk.label1)
            for k, tk in enumerate(ax.yaxis.get_major_ticks()):
                if yl[0] <= tk.get_loc() <= yl[1]: add(f"{gid}:ytick{k}", tk.label1)
            for k, t in enumerate(ax.texts): add(f"{gid}:note{k}('{t.get_text()[:12]}')", t)
            if ax.get_legend(): add(f"{gid}:legend", ax.get_legend())
        for t in fig.texts: add(f"fig:'{t.get_text()[:12]}'", t)
        out = []
        px2mm = 25.4 / fig.dpi
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                a, b = items[i][1], items[j][1]
                ox = min(a.x1, b.x1) - max(a.x0, b.x0); oy = min(a.y1, b.y1) - max(a.y0, b.y0)
                if ox > 0.3 / px2mm and oy > 0.3 / px2mm:  # ignore < 0.3 mm touches
                    out.append(f"{items[i][0]} ↔ {items[j][0]}  겹침 {ox*px2mm:.1f} × {oy*px2mm:.1f} mm")
        return out

    def audit_pdf(self, pdf_path: str | Path) -> str:
        """Audit the exported PDF against the spec: canvas mm, font sizes/family,
        5 pt floor, stroke widths, text kept as text (not outlines)."""
        try:
            import pymupdf
        except ImportError:
            return "[XX] pymupdf 없음: pip install pymupdf"
        page = pymupdf.open(pdf_path)[0]
        rep, ok = [], True
        # canvas
        w, h = round(pt2mm(page.rect.width), 1), round(pt2mm(page.rect.height), 1)
        cw, ch = self.d["canvas"]["width_mm"], self.d["canvas"]["height_mm"]
        good = abs(w - cw) < 0.2 and abs(h - ch) < 0.2; ok &= good
        rep.append(f'[{"OK" if good else "XX"}] 캔버스 {w} × {h} mm (스펙 {cw} × {ch})')
        # text
        spans = [sp for b in page.get_text("dict")["blocks"] for l in b.get("lines", []) for sp in l["spans"] if sp["text"].strip()]
        if not spans:
            return "결과: 불일치\n" + "\n".join(rep) + "\n[XX] PDF에 텍스트 객체 없음 — 글자가 윤곽선으로 변환됨"
        rep.append(f"[OK] 텍스트 객체 {len(spans)}개 유지 (편집 가능)")
        fams = sorted({sp["font"] for sp in spans})
        norm = lambda s: s.lower().replace(" ", "").replace("-", "")
        allowed = [self.d["text"]["font_family"], *self.font_fallback]
        unexpected = [f for f in fams if not any(norm(a) in norm(f) for a in allowed)]
        good = not unexpected; ok &= good
        rep.append(f'[{"OK" if good else "XX"}] 글꼴 {fams} (스펙 {self.d["text"]["font_family"]}'
                   f' + 폴백 {self.font_fallback})' + (f"  ← 예상 밖: {unexpected}" if unexpected else ""))
        placeholder = [f for f in fams if "lastresort" in norm(f)]
        if placeholder:
            ok = False
            rep.append(f"[XX] 자리표시자 글꼴 {placeholder} — 이 글리프는 네모 상자로 인쇄된다. "
                       "폴백 글꼴에 없는 문자다")
        t = self.d["text"]
        want_fs = {float(t[k]) for k in ("axis_label_pt", "tick_label_pt", "legend_pt", "annotation_pt", "panel_label_pt")}
        for p in self.d["panels"]:
            for k, v in (p.get("overrides") or {}).items():
                if k in t: want_fs.add(float(v))
            for a in p.get("annotations") or []:
                if "pt" in a: want_fs.add(float(a["pt"]))
        got_fs = sorted({round(sp["size"], 1) for sp in spans})
        extra = [v for v in got_fs if not any(abs(v - w_) < 0.15 for w_ in want_fs)]
        good = not extra; ok &= good
        rep.append(f'[{"OK" if good else "XX"}] 글자 크기 실측 {got_fs} pt / 스펙 {sorted(want_fs)}' + (f"  ← 스펙에 없는 값: {extra}" if extra else ""))
        small = [v for v in got_fs if v < 5]
        if small: ok = False; rep.append(f"[XX] 5 pt 미만 글자: {small}")
        # strokes
        l, k, m = self.d["lines"], self.d["ticks"], self.d["markers"]
        want_sw = {float(l["axis_pt"]), float(l["data_pt"]), float(l["errorbar_pt"]), float(k["width_pt"]), float(m["edge_pt"])}
        if l["grid"]: want_sw.add(float(l["grid_pt"]))
        if k["minor"]: want_sw.add(float(k["minor_width_pt"]))
        for p in self.d["panels"]:
            for kk, v in (p.get("overrides") or {}).items():
                if kk.endswith("_pt") and kk not in t: want_sw.add(float(v))
            for r in p.get("arrows") or []:
                if "pt" in r: want_sw.add(float(r["pt"]))
        got_sw = sorted({round(dr["width"], 2) for dr in page.get_drawings() if dr.get("width") and dr["type"] in ("s", "fs")})
        extra = [v for v in got_sw if not any(abs(v - w_) < 0.03 for w_ in want_sw)]
        good = not extra; ok &= good
        rep.append(f'[{"OK" if good else "XX"}] 선 두께 실측 {got_sw} pt / 스펙 {sorted(want_sw)}' + (f"  ← 스펙에 없는 값: {extra}" if extra else ""))
        return "결과: " + ("스펙과 일치" if ok else "불일치 항목 있음") + "\n" + "\n".join(rep)

    def errorbar_kw(self, pid: str | None = None) -> dict:
        return dict(elinewidth=self.pt("errorbar", pid),
                    capsize=mm2pt(self.mm("errorbar_cap", pid)) / 2,  # capsize is half-width
                    capthick=self.pt("errorbar", pid))

    # ---------------------------------------------------------------- save
    def save(self, fig, basename: str) -> list[Path]:
        hits = self.check_collisions(fig)
        print("충돌 없음" if not hits else "텍스트 충돌:\n  " + "\n  ".join(hits))
        out = []
        for fmt in self.d["export"]["formats"]:
            p = Path(f"{basename}.{fmt}")
            kw = {"bbox_inches": None, "pad_inches": 0, "facecolor": fig.get_facecolor()}
            if fmt in ("png", "tiff", "tif", "jpg"):
                kw["dpi"] = self.d["export"]["raster_dpi"]
            fig.savefig(p, **kw)
            out.append(p)
        return out

    # --------------------------------------------------------------- sheet
    def sheet(self) -> str:
        """Human-readable parameter sheet (Korean labels, pt/mm units)."""
        d = self.d
        rows: list[tuple[str, str, str]] = []
        A = rows.append
        cv = d["canvas"]
        A(("캔버스", "폭 × 높이", f'{cv["width_mm"]} × {cv["height_mm"]} mm'))
        for p in d["panels"]:
            A(("패널", f'{p["id"]} 위치·크기', f'x {p["x_mm"]}, y {p["y_mm"]}, w {p["w_mm"]}, h {p["h_mm"]} mm'))
            if p.get("overrides"):
                A(("패널", f'{p["id"]} 예외', ", ".join(f"{k}={v}" for k, v in p["overrides"].items())))
        for p in d["panels"]:
            if p.get("legend"):
                lg = p["legend"]; A(("범례", f'{p["id"]} 위치', f'{lg.get("loc", d["legend"]["loc"])}, 이동 dx {lg.get("dx_mm", 0)} / dy {lg.get("dy_mm", 0)} mm'))
            for i, a in enumerate(p.get("annotations") or []):
                A(("인라인", f'{p["id"]}-{i} "{a["text"][:14]}"', f'x {a["x_mm"]}, y {a["y_mm"]} mm, {a.get("pt", d["text"]["annotation_pt"])} pt, {a.get("ha", "left")}'))
            for i, r in enumerate(p.get("arrows") or []):
                A(("화살표", f'{p["id"]}-{i}', f'{r["from_mm"]} → {r["to_mm"]} mm'))
        t = d["text"]
        A(("글자", "글꼴", t["font_family"]))
        for k, lab in (("axis_label_pt", "축 제목"), ("tick_label_pt", "눈금 라벨"), ("legend_pt", "범례"),
                       ("annotation_pt", "주석"), ("panel_label_pt", "패널 라벨")):
            A(("글자", lab, f'{t[k]} pt'))
        A(("글자", "패널 라벨 굵기·오프셋", f'{t["panel_label_weight"]}, dx {t["panel_label_dx_mm"]} / dy {t["panel_label_dy_mm"]} mm'))
        l = d["lines"]
        for k, lab in (("axis_pt", "축 테두리"), ("data_pt", "데이터 선"), ("errorbar_pt", "오차막대"), ("grid_pt", "격자선")):
            A(("선", lab, f'{l[k]} pt'))
        A(("선", "오차막대 캡 폭", f'{l["errorbar_cap_mm"]} mm'))
        A(("선", "격자", f'{"on" if l["grid"] else "off"} ({l["grid_color"]})'))
        k = d["ticks"]
        A(("눈금", "길이 / 두께", f'{k["length_mm"]} mm / {k["width_pt"]} pt'))
        A(("눈금", "방향", k["direction"]))
        A(("눈금", "눈금–라벨 간격", f'{k["pad_mm"]} mm'))
        A(("눈금", "보조눈금", f'{"on" if k["minor"] else "off"} ({k["minor_length_mm"]} mm / {k["minor_width_pt"]} pt)'))
        A(("눈금", "위·오른쪽 테두리", "on" if k["top_right_spines"] else "off"))
        m = d["markers"]
        A(("마커", "크기 / 테두리 / 투명도", f'{m["size_pt"]} pt / {m["edge_pt"]} pt / {m["alpha"]}'))
        lg = d["legend"]
        A(("범례", "테두리", "on" if lg["frame"] else "off"))
        A(("범례", "핸들 길이 / 핸들–글자 간격", f'{lg["handle_length_mm"]} mm / {lg["handle_text_gap_mm"]} mm'))
        A(("범례", "행 간격", f'{lg["row_gap_pt"]} pt'))
        c = d["colors"]
        A(("색", "역할", ", ".join(f"{r} {h}" for r, h in c["roles"].items())))
        A(("색", "글자 / 테두리", f'{c["text"]} / {c["spine"]}'))
        e = d["export"]
        A(("내보내기", "형식 / 래스터 DPI", f'{", ".join(e["formats"])} / {e["raster_dpi"]}'))
        w1 = max(len(r[0]) for r in rows)
        w2 = max(len(r[1]) for r in rows)
        lines = [f'{"범주":<{w1}}  {"항목":<{w2}}  값', "-" * (w1 + w2 + 30)]
        lines += [f"{a:<{w1}}  {b:<{w2}}  {c}" for a, b, c in rows]
        return "\n".join(lines)

    # --------------------------------------------------------------- audit
    def audit_svg(self, svg_path: str | Path) -> str:
        """Compare the rendered SVG with the spec. Reports in pt/mm."""
        tree = ET.parse(svg_path)
        root = tree.getroot()
        rep = []
        ok = True

        def num(s):
            return float(re.match(r"[-\d.]+", s).group())

        # canvas
        w_pt, h_pt = num(root.get("width")), num(root.get("height"))
        cw, ch = self.d["canvas"]["width_mm"], self.d["canvas"]["height_mm"]
        got = (round(pt2mm(w_pt), 1), round(pt2mm(h_pt), 1))
        good = abs(got[0] - cw) < 0.2 and abs(got[1] - ch) < 0.2
        ok &= good
        rep.append(f'[{"OK" if good else "XX"}] 캔버스 {got[0]} × {got[1]} mm (스펙 {cw} × {ch})')

        # font sizes & stroke widths present in file
        fsizes, strokes = {}, {}
        for el in root.iter():
            st = el.get("style", "") or ""
            for attr_name, store in (("font-size", fsizes), ("stroke-width", strokes)):
                v = el.get(attr_name)
                if v is None:
                    m = re.search(attr_name + r"\s*:\s*([\d.]+)", st)
                    v = m.group(1) if m else None
                if v is not None:
                    key = round(float(re.match(r"[\d.]+", v).group()), 2)
                    store[key] = store.get(key, 0) + 1
        t = self.d["text"]
        want_fs = {float(t[k]) for k in ("axis_label_pt", "tick_label_pt", "legend_pt", "annotation_pt", "panel_label_pt")}
        for p in self.d["panels"]:
            for k, v in (p.get("overrides") or {}).items():
                if k.endswith("_pt") and k in t:
                    want_fs.add(float(v))
        extra_fs = sorted(set(fsizes) - want_fs)
        good = not extra_fs
        ok &= good
        rep.append(f'[{"OK" if good else "XX"}] 글자 크기 실측 {sorted(fsizes)} pt / 스펙 {sorted(want_fs)}'
                   + (f"  ← 스펙에 없는 값: {extra_fs}" if extra_fs else ""))
        small = [s for s in fsizes if s < 5]
        if small:
            ok = False
            rep.append(f"[XX] 5 pt 미만 글자 존재: {small}")

        l, k, m = self.d["lines"], self.d["ticks"], self.d["markers"]
        want_sw = {float(l["axis_pt"]), float(l["data_pt"]), float(l["errorbar_pt"]), float(k["width_pt"]), float(m["edge_pt"])}
        if l["grid"]:
            want_sw.add(float(l["grid_pt"]))
        if k["minor"]:
            want_sw.add(float(k["minor_width_pt"]))
        for p in self.d["panels"]:
            for kk, v in (p.get("overrides") or {}).items():
                if kk.endswith("_pt") and kk not in t:
                    want_sw.add(float(v))
        extra_sw = sorted(set(strokes) - want_sw)
        good = not extra_sw
        ok &= good
        rep.append(f'[{"OK" if good else "XX"}] 선 두께 실측 {sorted(strokes)} pt / 스펙 {sorted(want_sw)}'
                   + (f"  ← 스펙에 없는 값: {extra_sw}" if extra_sw else ""))

        # text editable?
        has_text = any(el.tag.endswith("}text") or el.tag == "text" for el in root.iter())
        ok &= has_text
        rep.append(f'[{"OK" if has_text else "XX"}] 텍스트 객체 {"유지됨 (편집 가능)" if has_text else "없음 — 윤곽선으로 변환됨"}')

        # panel groups
        gids = {el.get("id") for el in root.iter() if el.get("id")}
        missing = [f'panel-{p["id"]}' for p in self.d["panels"] if f'panel-{p["id"]}' not in gids]
        good = not missing
        ok &= good
        rep.append(f'[{"OK" if good else "XX"}] 패널 그룹 id ' + ("모두 존재" if good else f"누락 {missing}"))

        rep.insert(0, "결과: " + ("스펙과 일치" if ok else "불일치 항목 있음"))
        return "\n".join(rep)

    def wireframe(self, basename: str):
        fig = self.canvas()
        for p in self.d["panels"]:
            ax = self.panel(fig, p["id"])
            ax.set_xticks([]); ax.set_yticks([])
            ax.text(0.5, 0.5, f'{p["w_mm"]} × {p["h_mm"]} mm', ha="center", va="center",
                    transform=ax.transAxes, fontsize=self.fs("annotation"), color="#999999")
        return self.save(fig, basename)


def _cycler(colors):
    from cycler import cycler
    return cycler(color=colors)


def main(argv):
    if len(argv) < 3:
        print(__doc__); return 1
    cmd, spec = argv[1], Spec.load(argv[2])
    if cmd == "sheet":
        print(spec.sheet())
    elif cmd == "audit":
        f = argv[3]
        print(spec.audit_pdf(f) if f.lower().endswith(".pdf") else spec.audit_svg(f))
    elif cmd == "wire":
        print("wrote", [str(p) for p in spec.wireframe(argv[3] if len(argv) > 3 else "wireframe")])
    else:
        print(__doc__); return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
