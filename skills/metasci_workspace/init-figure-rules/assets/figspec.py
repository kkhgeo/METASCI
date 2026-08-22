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
    python figspec.py audit   figure_spec.yaml fig1.svg   # verify rendered SVG against spec
    python figspec.py wire    figure_spec.yaml out        # render empty panel boxes

Requires matplotlib and pyyaml. The audit subcommand needs only the stdlib.
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

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
            "font.family": "sans-serif",
            "font.sans-serif": [t["font_family"], "Helvetica", "Liberation Sans", "DejaVu Sans"],
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

    def errorbar_kw(self, pid: str | None = None) -> dict:
        return dict(elinewidth=self.pt("errorbar", pid),
                    capsize=mm2pt(self.mm("errorbar_cap", pid)) / 2,  # capsize is half-width
                    capthick=self.pt("errorbar", pid))

    # ---------------------------------------------------------------- save
    def save(self, fig, basename: str) -> list[Path]:
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
    # Windows consoles default to a legacy codepage (cp949 here); the sheet and
    # audit output carry en dashes and Korean labels, so force UTF-8 on stdout.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    if len(argv) < 3:
        print(__doc__); return 1
    cmd, spec = argv[1], Spec.load(argv[2])
    if cmd == "sheet":
        print(spec.sheet())
    elif cmd == "audit":
        print(spec.audit_svg(argv[3]))
    elif cmd == "wire":
        print("wrote", [str(p) for p in spec.wireframe(argv[3] if len(argv) > 3 else "wireframe")])
    else:
        print(__doc__); return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
