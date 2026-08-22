#!/usr/bin/env python3
"""Parse, validate, filter and visualize meta-writing-mapping outline.md files.

No third-party dependency. outline.md remains the source of truth; queue and HTML
are derived views. Supports format 1.1 plus best-effort legacy tables/vertical blocks.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from datetime import date
import html
import json
from pathlib import Path
import re
import sys
from typing import Sequence

ACTIVE = {"detected", "surfaced", "decided", "reopened"}
ARCHIVED = {"resolved", "superseded"}
PRIORITY = {"blocker": 0, "high": 1, "medium": 2, "low": 3, "mechanical": 4}
GLOBAL_PARTIAL_CODES = {"duplicate-node", "duplicate-decision", "parse-warning", "resolved-under-blocker"}
KNOWN_FUNCTIONS = {
    "Background", "Lit-Review", "Gap", "Question", "Purpose", "Scope", "Contribution",
    "Study-Area", "Design", "Sample", "Procedure", "Instrument", "Statistical", "Quality",
    "Overview", "Finding", "Comparison", "Trend", "Pattern", "Anomaly", "Summary",
    "Interpretation", "Mechanism", "Lit-Comparison", "Agreement", "Disagreement",
    "Limitation", "Implication", "Future", "Conclusion",
}
KNOWN_RELATIONS = {
    "Continuation", "Contrast", "Cause-Effect", "Specification", "Generalization",
    "Sequence", "Concession", "Problem-Solution", "Evidence-Claim", "Question-Answer",
}
EVIDENCE_REQUIRED = {"Overview", "Finding", "Comparison", "Trend", "Pattern", "Anomaly", "Statistical", "Quality"}


@dataclass
class Link:
    id: str
    role: str = "unspecified"


@dataclass
class Node:
    id: str
    section: str = ""
    status: str = "proposed"
    function: str = ""
    claim: str = ""
    predecessors: list[Link] = field(default_factory=list)
    evidence: list[Link] = field(default_factory=list)
    ledger: list[Link] = field(default_factory=list)
    axes: dict[str, str] = field(default_factory=dict)
    core_contribution: str = ""
    decisions: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    order: int = 0
    legacy: bool = False


@dataclass
class Decision:
    id: str
    status: str = "detected"
    priority: str = "medium"
    scope: str = "manuscript"
    title: str = ""
    recommendation: str = ""
    reason: str = ""
    alternatives: list[str] = field(default_factory=list)
    impacts: list[str] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    resolution_criterion: str = ""
    history: list[str] = field(default_factory=list)
    order: int = 0


@dataclass
class InventoryItem:
    id: str
    kind: str
    status: str
    scope: str = "manuscript"


@dataclass
class Issue:
    level: str
    code: str
    message: str
    scope: str = "manuscript"


@dataclass
class Outline:
    title: str = ""
    metadata: dict[str, str] = field(default_factory=dict)
    nodes: list[Node] = field(default_factory=list)
    decisions: list[Decision] = field(default_factory=list)
    evidence_inventory: list[InventoryItem] = field(default_factory=list)
    ledger_inventory: list[InventoryItem] = field(default_factory=list)
    parse_warnings: list[str] = field(default_factory=list)
    format_version: str = "legacy"


# 구형 파일에서 단락 블록이 **없는** 영역. 단락을 담는 `## ` 제목은 사용자가
# 원고마다 자유롭게 짓는다(`## 제1부 — …`처럼). 그래서 허용 목록이 아니라 제외
# 목록으로 판별한다. 규격이 이름을 정한 쪽은 이 메타 영역들뿐이다.
NON_COMPOSITION_AREAS = (
    "미해결", "근거 노트", "Ledger 착지", "사용자 결정", "문서 관계",
    "결정 대장", "근거 인벤토리", "Ledger 인벤토리", "해소",
)

# 미해결 항목의 머리줄. 열 0에서 시작하고 번호 뒤에 `.`/`)`가 있거나 `#`이 앞에
# 붙어야 한다. 들여쓴 이어진 줄(`   3장 전반에 깔린다`)이 새 결정으로 잡혀 진짜
# 항목과 ID가 충돌하던 결함을 막는다.
LEGACY_DECISION = re.compile(
    r"^(?:[-*]\s+)?(?:\\?#\s*(?P<hash>\d+)|(?P<num>\d+)\s*[.)])\s*(?P<body>.+)$"
)

NODE_SCALAR = {"상태": "status", "기능": "function", "한 줄 논지": "claim", "Core message 기여": "core_contribution"}
NODE_LIST = {"앞 단락": "predecessors", "근거": "evidence", "Ledger": "ledger", "축": "axes", "메모": "notes"}
DEC_SCALAR = {"상태": "status", "우선순위": "priority", "범위": "scope", "제목": "title", "추천": "recommendation", "근거": "reason", "해소 기준": "resolution_criterion"}
DEC_LIST = {"대안": "alternatives", "영향": "impacts", "의존": "depends_on", "이력": "history"}


def _utf8() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _link(raw: str) -> Link:
    raw = raw.strip()
    if raw in {"", "—", "-"}:
        return Link("—", "none")
    left, *right = [part.strip() for part in raw.split("|", 1)]
    return Link(left, right[0] if right and right[0] else "unspecified")


def _csv(raw: str) -> list[str]:
    return [item.strip() for item in re.split(r"\s*[,;]\s*", raw) if item.strip() and item.strip() not in {"—", "-"}]


def _inventory(raw: str) -> InventoryItem | None:
    if not re.match(r"^\s*-\s+", raw):
        return None
    parts = [p.strip() for p in re.sub(r"^\s*-\s+", "", raw).split("|")]
    if not parts or not parts[0]:
        return None
    return InventoryItem(parts[0], parts[1] if len(parts) > 1 else "unspecified", parts[2] if len(parts) > 2 else "available", parts[3] if len(parts) > 3 else "manuscript")


def _heading_scope(text: str, major: str = "") -> tuple[str, str]:
    clean = re.sub(r"[*_`]", "", text).strip()
    low = clean.lower()
    if "introduction" in low or "서론" in clean: major = "INTRO"
    elif "method" in low or "방법" in clean: major = "METHODS"
    elif "result" in low or "결과" in clean: major = "RESULTS"
    elif "discussion" in low or "고찰" in clean or "논의" in clean: major = "DISCUSSION"
    elif "conclusion" in low or "결론" in clean: major = "CONCLUSION"
    m = re.match(r"^(\d+(?:\.\d+)*)\b", clean)
    if m:
        number = m.group(1)
        if not major:
            major = {"1": "INTRO", "2": "METHODS", "3": "RESULTS", "4": "DISCUSSION", "5": "CONCLUSION"}.get(number.split(".")[0], "SECTION")
        return f"{major}.{number}", major
    return major or re.sub(r"\W+", "_", clean.upper()).strip("_") or "SECTION", major


def _is_structured(out: Outline) -> bool:
    """형식 1.1로 볼 수 있는가.

    선언된 포맷 버전이 1.1이거나, 노드 하나라도 구조 필드를 채웠으면 1.1이다.
    제목만 있고 나머지가 빈 노드는 구형 파일의 산문 소제목(`#### 구조 원리` 등)이
    `## 구성` 아래에 있어 노드로 오인된 것이다. 그 오탐이 legacy 폴백을 막았다.
    """
    if out.metadata.get("포맷 버전", "").startswith("1.1"):
        return True
    return any(
        n.function or n.claim or n.predecessors or n.evidence or n.ledger or n.core_contribution
        for n in out.nodes
    )


def parse_outline(path: str | Path) -> Outline:
    text = Path(path).read_text(encoding="utf-8").replace("\r\n", "\n")
    lines = text.splitlines()
    out = Outline()
    area = section = major = ""
    metadata_open = True
    node: Node | None = None
    decision: Decision | None = None
    active: tuple[str, str] | None = None
    node_order = decision_order = 0

    for line in lines:
        line = line.rstrip()
        if line.startswith("# Outline"):
            out.title = line.split("—", 1)[1].strip() if "—" in line else line.lstrip("# ").strip()
            continue
        if metadata_open:
            m = re.match(r"^-\s*([^:]+):\s*(.*)$", line)
            if m:
                out.metadata[m.group(1).strip()] = m.group(2).strip()
                if m.group(1).strip() == "포맷 버전": out.format_version = m.group(2).strip()
                continue
        if line.startswith("## "):
            metadata_open = False; area = line[3:].strip(); section = ""; node = None; decision = None; active = None; continue
        if line.startswith("### ") and not line.startswith("#### "):
            section = line[4:].strip(); _, major = _heading_scope(section, major); node = None; decision = None; active = None; continue
        if line.startswith("#### "):
            entry = line[5:].strip(); active = None
            if area == "구성":
                node_order += 1; node = Node(entry, section=section, order=node_order); out.nodes.append(node); decision = None
            elif area == "결정 대장":
                decision_order += 1; decision = Decision(entry, order=decision_order); out.decisions.append(decision); node = None
            continue
        if area == "근거 인벤토리" and node is None and decision is None:
            item = _inventory(line)
            if item: out.evidence_inventory.append(item)
            continue
        if area == "Ledger 인벤토리" and node is None and decision is None:
            item = _inventory(line)
            if item: out.ledger_inventory.append(item)
            continue

        field_match = re.match(r"^\s*-\s*([^:]+):\s*(.*)$", line)
        nested = re.match(r"^\s{2,}-\s+(.*)$", line)
        if node:
            if field_match:
                label, value = field_match.group(1).strip(), field_match.group(2).strip(); active = None
                if label in NODE_SCALAR: setattr(node, NODE_SCALAR[label], value)
                elif label == "결정": node.decisions = _csv(value)
                elif label in NODE_LIST:
                    active = ("node", NODE_LIST[label])
                    if value: _append_node(node, NODE_LIST[label], value)
                continue
            if nested and active and active[0] == "node": _append_node(node, active[1], nested.group(1)); continue
        if decision:
            if field_match:
                label, value = field_match.group(1).strip(), field_match.group(2).strip(); active = None
                if label in DEC_SCALAR: setattr(decision, DEC_SCALAR[label], value)
                elif label in DEC_LIST:
                    active = ("decision", DEC_LIST[label])
                    if value: getattr(decision, DEC_LIST[label]).append(value)
                continue
            if nested and active and active[0] == "decision": getattr(decision, active[1]).append(nested.group(1).strip()); continue

    if not out.nodes or not _is_structured(out):
        # 오탐으로 만들어진 껍데기 노드를 버리고 다시 읽는다. 남겨두면 legacy 결과에
        # 섞여 단락 수가 부풀고, 그 상태로 errors=0 이 나가 조용한 오통과가 된다.
        out.nodes.clear(); out.decisions.clear()
        out.evidence_inventory.clear(); out.ledger_inventory.clear()
        return _parse_legacy(text, out)
    if out.format_version == "legacy": out.format_version = out.metadata.get("포맷 버전", "1.1")
    return out


def _append_node(node: Node, field_name: str, raw: str) -> None:
    raw = raw.strip()
    if field_name in {"predecessors", "evidence", "ledger"}: getattr(node, field_name).append(_link(raw))
    elif field_name == "axes":
        if "=" in raw:
            key, value = [part.strip() for part in raw.split("=", 1)]; node.axes[key] = value
        else: node.notes.append(f"[축 파싱 실패] {raw}")
    elif field_name == "notes": node.notes.append(raw)


def _parse_legacy(text: str, out: Outline) -> Outline:
    out.format_version = "legacy"
    out.parse_warnings.append("legacy parse: 1.1 구조 노드를 찾지 못해 구형 형식을 추정했습니다.")
    area = scope = ""; major = ""; node: Node | None = None; node_order = dec_order = 0; counts: dict[str, int] = {}; imported = 0

    def uid(local: str) -> str:
        base = f"{scope}.{local}"; n = counts.get(base, 0); counts[base] = n + 1
        return base if n == 0 else f"{base}_{n+1}"

    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("## "): area = line[3:].strip(); node = None; continue
        if area.startswith("미해결"):
            m = LEGACY_DECISION.match(line)
            if m:
                number = int(m.group("hash") or m.group("num")); body = m.group("body").strip()
                dec_order += 1; imported += 1
                out.decisions.append(Decision(
                    id=f"D-{number:03d}", status=_legacy_status(body), priority=_legacy_priority(body),
                    scope=_legacy_scope(body), title=body,
                    reason="legacy 미해결 항목 — 추천안과 영향 분석이 아직 구성되지 않음",
                    history=[f"legacy | imported | #{number} {body}"], order=dec_order,
                ))
            continue
        if area.startswith(NON_COMPOSITION_AREAS): continue
        if line.startswith("### "): scope, major = _heading_scope(line[4:].strip(), major); node = None; continue
        if line.startswith("|") and line.count("|") >= 6:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not cells or cells[0] in {"단락", "---", ""} or set(cells[0]) <= {"-", ":"}: continue
            node_order += 1; node = Node(uid(cells[0]), section=scope, function=cells[1], claim=cells[2], core_contribution=cells[5] if len(cells)>5 else "", order=node_order, legacy=True)
            if len(cells)>3 and cells[3] not in {"", "—", "-"}: node.predecessors.append(_legacy_pred(cells[3], scope, major))
            if len(cells)>4: node.evidence.extend(Link(x) for x in _csv(cells[4]))
            out.nodes.append(node); continue
        m = re.match(r"^\s*(P\d+)\s*\|\s*(.+)$", line)
        if m:
            parts = [p.strip() for p in m.group(2).split("|")]; layer = function = claim = ""
            if parts:
                first = parts[0].strip("[]")
                if first in KNOWN_FUNCTIONS: function = first; claim = " | ".join(parts[1:])
                else:
                    layer = first
                    if len(parts)>1 and parts[1] in KNOWN_FUNCTIONS: function = parts[1]; claim = " | ".join(parts[2:])
                    else: claim = " | ".join(parts[1:] if len(parts)>1 else parts)
            node_order += 1; node = Node(uid(m.group(1)), section=scope, function=function, claim=claim.strip(), order=node_order, legacy=True)
            if layer: node.axes["epistemic-layer"] = layer
            out.nodes.append(node); continue
        if node:
            m = re.match(r"^\s*←\s*(.+)$", line)
            if m:
                # `← — (섹션 첫 단락)`은 앞 단락이 없다는 표기지 간선이 아니다.
                # 그대로 넣으면 존재하지 않는 노드를 가리켜 오탐 경고가 난다.
                head = m.group(1).lstrip()
                if not re.search(r"P\d+", head) and head.startswith(("—", "–", "-")): continue
                node.predecessors.append(_legacy_pred(m.group(1), scope, major)); continue
            m = re.match(r"^\s*(근거|Ledger\s*착지|기여|메모|해석|⚠[^:]*):\s*(.*)$", line)
            if m:
                label, value = m.group(1), m.group(2).strip()
                if label == "근거": node.evidence.extend(Link(x) for x in _csv(value))
                elif label.startswith("Ledger"): node.ledger.extend(Link(x) for x in _csv(value))
                elif label == "기여": node.core_contribution = value
                else: node.notes.append(f"{label}: {value}")
                continue
            if line.strip() and not line.lstrip().startswith(("#", "|", "`", "```")):
                body = line.strip()
                # 구형 방언은 한 줄 논지를 `P` 줄이 아니라 바로 다음 줄에 두기도 한다.
                # 그대로 비워두면 규격상 "아직 설계되지 않은 단락"으로 잘못 판정된다.
                if not node.claim: node.claim = body
                else: node.notes.append(body)

    for n in out.nodes:
        for note in n.notes:
            for m in re.finditer(r"(?:미해결\s*)?#(\d+)", note):
                did = f"D-{int(m.group(1)):03d}"
                if did not in n.decisions: n.decisions.append(did)
    out.parse_warnings.append(f"legacy parse로 단락 {len(out.nodes)}개를 추출했습니다. 자유문 필드는 수동 확인이 필요합니다.")
    if imported: out.parse_warnings.append(f"legacy 미해결 {imported}건을 결정 대장으로 가져왔습니다. 추천·영향은 대화에서 보강해야 합니다.")
    return out


def _legacy_pred(raw: str, scope: str, major: str) -> Link:
    rel = re.search(r"\[([^\]]+)\]", raw); role = rel.group(1) if rel else "unspecified"
    clean = re.sub(r"\[[^\]]+\]", "", raw).strip(); m = re.search(r"(?:(\d+(?:\.\d+)*)\s*)?(P\d+)", clean)
    if not m: return Link(clean or "—", role)
    subsection, para = m.group(1), m.group(2)
    return Link(f"{major or scope.split('.')[0]}.{subsection}.{para}" if subsection else f"{scope}.{para}", role)


def _legacy_status(body: str) -> str:
    low = body.lower()
    if "해소" in body or "완료" in body or "resolved" in low: return "resolved"
    if "보류" in body or "deferred" in low: return "deferred"
    if "재개방" in body or "reopened" in low: return "reopened"
    return "detected"


def _legacy_priority(body: str) -> str:
    low = body.lower()
    if "core message" in low or "핵심 메시지" in body or "전체를 막" in body or "블로커" in body: return "blocker"
    if any(x in body for x in ("섹션 경계", "전체 구조", "연구 질문", "결과-고찰")): return "high"
    if any(x in body for x in ("각주", "p값", "p 값", "정밀도", "오기", "오탈자", "번호", "표기")): return "mechanical"
    return "medium"


def _legacy_scope(body: str) -> str:
    low = body.lower()
    if "core message" in low or "핵심 메시지" in body: return "manuscript"
    m = re.search(r"(?:(\d+(?:\.\d+)*)\s*)?(P\d+)", body)
    if m and m.group(1):
        num = m.group(1); major = {"1":"INTRO","2":"METHODS","3":"RESULTS","4":"DISCUSSION","5":"CONCLUSION"}.get(num.split('.')[0],"SECTION")
        return f"{major}.{num}.{m.group(2)}"
    if "introduction" in low or "서론" in body: return "INTRO"
    if "method" in low or "방법" in body: return "METHODS"
    if "result" in low or "결과" in body: return "RESULTS"
    if "discussion" in low or "고찰" in body or "논의" in body: return "DISCUSSION"
    if "conclusion" in low or "결론" in body: return "CONCLUSION"
    return "manuscript"


def _dupes(values: Sequence[str]) -> set[str]:
    seen, dup = set(), set()
    for value in values:
        if value in seen: dup.add(value)
        seen.add(value)
    return dup


def _usage(nodes: Sequence[Node], attr: str) -> dict[str, list[tuple[str,str]]]:
    result: dict[str, list[tuple[str,str]]] = {}
    for node in nodes:
        for link in getattr(node, attr):
            if link.id not in {"", "—", "-"}: result.setdefault(link.id, []).append((node.id, link.role))
    return result


def _common_scope(ids: Sequence[str]) -> str:
    if not ids: return "manuscript"
    parts = [x.split(".") for x in ids]; common=[]
    for col in zip(*parts):
        if len(set(col))==1: common.append(col[0])
        else: break
    if common and re.fullmatch(r"P\d+", common[-1]): common.pop()
    return ".".join(common) or "manuscript"


def validate(out: Outline) -> list[Issue]:
    issues: list[Issue] = []
    node_ids = [n.id for n in out.nodes]; decision_ids = [d.id for d in out.decisions]
    for x in _dupes(node_ids): issues.append(Issue("error","duplicate-node",f"중복 단락 ID: {x}",x))
    for x in _dupes(decision_ids): issues.append(Issue("error","duplicate-decision",f"중복 결정 ID: {x}",x))
    node_set, decision_set = set(node_ids), set(decision_ids)
    provisional = out.metadata.get("지도 상태","").lower()=="provisional"
    for node in out.nodes:
        for pred in node.predecessors:
            if pred.id not in {"","—","-"} and pred.id not in node_set:
                external = provisional or pred.id.upper().startswith("EXTERNAL.")
                issues.append(Issue("info" if external else "warn", "external-predecessor" if external else "missing-predecessor", f"{node.id}의 경계 앞 단락 {pred.id}는 현재 지도 밖에 있습니다." if external else f"{node.id}가 존재하지 않는 앞 단락 {pred.id}를 참조합니다.", node.id))
        if node.function in EVIDENCE_REQUIRED and not node.evidence: issues.append(Issue("warn","evidence-empty",f"{node.id} [{node.function}]에 근거가 없습니다.",node.id))
        if not node.claim: issues.append(Issue("warn","claim-empty",f"{node.id}에 한 줄 논지가 없습니다.",node.id))
        if not node.core_contribution: issues.append(Issue("info","contribution-empty",f"{node.id}에 Core message 기여가 없습니다.",node.id))
        if node.function and node.function not in KNOWN_FUNCTIONS: issues.append(Issue("info","custom-function",f"{node.id}가 사용자 정의 기능 [{node.function}]를 씁니다.",node.id))
        for pred in node.predecessors:
            if pred.role not in {"none","unspecified"} and pred.role not in KNOWN_RELATIONS: issues.append(Issue("info","custom-relation",f"{node.id}가 사용자 정의 관계 [{pred.role}]를 씁니다.",node.id))
        for did in node.decisions:
            if did and did not in decision_set: issues.append(Issue("warn","missing-decision",f"{node.id}가 존재하지 않는 결정 {did}을 참조합니다.",node.id))

    omitted = {n.id for n in out.nodes if n.status=="omitted"}
    euse, luse = _usage(out.nodes,"evidence"), _usage(out.nodes,"ledger")
    for item in out.evidence_inventory:
        places = euse.get(item.id,[])
        if not places: issues.append(Issue("warn","evidence-unassigned",f"근거 {item.id}가 어느 단락에도 배정되지 않았습니다.",item.scope))
        first=[nid for nid,role in places if role=="first-report"]
        if len(first)>1: issues.append(Issue("error","evidence-first-report-duplicate",f"{item.id} first-report 중복: {', '.join(first)}",_common_scope(first)))
        if places and all(nid in omitted for nid,_ in places): issues.append(Issue("warn","evidence-omitted-only",f"{item.id}가 omitted 단락에만 있습니다.",item.scope))
    for item in out.ledger_inventory:
        places=luse.get(item.id,[])
        if not places: issues.append(Issue("error" if "required" in item.status else "warn","ledger-unassigned",f"Ledger {item.id}가 배정되지 않았습니다.",item.scope)); continue
        first=[nid for nid,role in places if role=="first-report"]
        if "first-report-required" in item.status and not first: issues.append(Issue("error","ledger-first-report-missing",f"Ledger {item.id}에 first-report가 없습니다.",item.scope))
        if len(first)>1: issues.append(Issue("error","ledger-first-report-duplicate",f"Ledger {item.id} first-report 중복: {', '.join(first)}",_common_scope(first)))
        if places and all(nid in omitted for nid,_ in places): issues.append(Issue("error","ledger-omitted-only",f"Ledger {item.id}가 omitted 단락에만 있습니다.",item.scope))

    for d in out.decisions:
        for dep in d.depends_on:
            if dep not in {"","—","-"} and dep not in decision_set: issues.append(Issue("warn","missing-dependency",f"{d.id}가 존재하지 않는 의존 결정 {dep}을 참조합니다.",d.scope))
        if d.status=="resolved" and not d.history: issues.append(Issue("info","resolved-without-history",f"{d.id}는 resolved이지만 이력이 없습니다.",d.scope))
    for warning in out.parse_warnings: issues.append(Issue("warn","parse-warning",warning,"manuscript"))
    return issues


def scope_nodes(out: Outline, scope: str) -> tuple[list[Node], set[str]]:
    active=[n for n in out.nodes if n.status!="omitted"]
    if scope in {"","manuscript","all"}: core=active
    elif "," in scope:
        requested={x.strip() for x in scope.split(",")}; core=[n for n in active if n.id in requested]
    else:
        s=scope.upper(); core=[n for n in active if n.id.upper()==s or n.id.upper().startswith(s+".")]
    ids={n.id for n in core}; boundary=set()
    if scope not in {"","manuscript","all"}:
        for n in core:
            boundary.update(p.id for p in n.predecessors if p.id not in ids and p.id not in {"","—","-"})
        for n in active:
            if n.id not in ids and any(p.id in ids for p in n.predecessors): boundary.add(n.id)
    return sorted([n for n in active if n.id in ids or n.id in boundary],key=lambda n:n.order), boundary


def decision_queue(out: Outline, scope: str, include_deferred: bool=False) -> list[Decision]:
    candidates=[d for d in out.decisions if d.status not in ARCHIVED and (d.status in ACTIVE or (include_deferred and d.status=="deferred"))]
    if scope in {"","manuscript","all"}: queue=candidates[:]
    else:
        nodes,boundary=scope_nodes(out,scope); visible={n.id for n in nodes if n.id not in boundary}; normalized=scope.upper(); queue=[]
        for d in candidates:
            ancestor=d.priority=="blocker" and (d.scope=="manuscript" or normalized==d.scope.upper() or normalized.startswith(d.scope.upper()+"."))
            same=d.scope.upper()==normalized or d.scope.upper().startswith(normalized+".") or normalized.startswith(d.scope.upper()+".")
            impacted=any(i in visible or any(n.startswith(i+".") or i.startswith(n+".") for n in visible) for i in d.impacts)
            if ancestor or same or impacted: queue.append(d)
        ids={d.id for d in queue}; changed=True
        while changed:
            changed=False
            for d in candidates:
                if d.id not in ids and d.status=="reopened" and any(dep in ids for dep in d.depends_on): queue.append(d); ids.add(d.id); changed=True
    return sorted(queue,key=lambda d:(PRIORITY.get(d.priority,99),d.order,d.id))


def filtered_issues(issues: Sequence[Issue], out: Outline, scope: str) -> list[Issue]:
    if scope in {"","manuscript","all"}: return list(issues)
    nodes,_=scope_nodes(out,scope); visible={n.id for n in nodes}; s=scope.upper(); result=[]
    for i in issues:
        x=i.scope.upper(); global_ok=i.scope=="manuscript" and i.code in GLOBAL_PARTIAL_CODES
        if global_ok or x==s or x.startswith(s+".") or s.startswith(x+".") or i.scope in visible: result.append(i)
    return result


def to_dict(out: Outline, issues: Sequence[Issue]) -> dict[str,object]:
    return {"title":out.title,"metadata":out.metadata,"format_version":out.format_version,"nodes":[asdict(x) for x in out.nodes],"decisions":[asdict(x) for x in out.decisions],"evidence_inventory":[asdict(x) for x in out.evidence_inventory],"ledger_inventory":[asdict(x) for x in out.ledger_inventory],"issues":[asdict(x) for x in issues],"generated":date.today().isoformat()}


def queue_markdown(out: Outline, scope: str) -> str:
    q=decision_queue(out,scope); lines=[f"# 결정 대기열 — {scope}",""]
    if not q: return "\n".join(lines+["활성 결정이 없습니다.",""])
    for d in q:
        lines += [f"## {d.id} · {d.priority} · {d.scope}","",f"**{d.title or '(제목 없음)'}**","",f"- 상태: {d.status}",f"- 추천: {d.recommendation or '—'}",f"- 근거: {d.reason or '—'}",f"- 대안의 비용: {'; '.join(d.alternatives) if d.alternatives else '—'}",f"- 영향: {', '.join(d.impacts) if d.impacts else '—'}","","판정: 추천 채택 / 대안 채택 / 부분 수정 / 보류",""]
    return "\n".join(lines)


def render_dashboard(out: Outline, issues: Sequence[Issue], path: str|Path) -> None:
    data=json.dumps(to_dict(out,issues),ensure_ascii=False).replace("</","<\\/"); title=html.escape(out.title or "Outline dashboard")
    doc=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>body{{margin:0;font-family:system-ui,sans-serif;background:#f6f7f9;color:#17191d}}header{{position:sticky;top:0;background:#fff;border-bottom:1px solid #ddd;padding:16px 22px;z-index:2}}main{{padding:20px}}select,input,button{{padding:7px 9px;border:1px solid #ccd0d8;border-radius:7px;background:#fff}}.tabs{{margin-top:10px;display:flex;gap:6px;flex-wrap:wrap}}.tabs .active{{background:#315efb;color:#fff}}.panel{{display:none}}.panel.active{{display:block}}.card{{background:#fff;border:1px solid #d9dde5;border-radius:10px;padding:14px;margin-bottom:10px}}.badge{{display:inline-block;padding:2px 7px;border-radius:999px;background:#e8ebf1;font-size:12px;margin-right:5px}}.blocker{{background:#fee2e2}}.high{{background:#ffedd5}}.medium{{background:#fef3c7}}.low{{background:#dcfce7}}.mechanical{{background:#e5e7eb}}.scroll{{overflow:auto;background:#fff;border:1px solid #ddd;border-radius:10px}}table{{border-collapse:collapse;min-width:700px;width:100%}}th,td{{border:1px solid #ddd;padding:6px;font-size:12px}}th{{background:#eef1f5}}svg text{{font-family:system-ui,sans-serif}}.muted{{color:#69717d}}.error{{border-left:5px solid #dc2626}}.warn{{border-left:5px solid #f59e0b}}.info{{border-left:5px solid #3b82f6}}</style></head><body>
<header><h2>{title}</h2><label>범위 <input id="scope" list="scopeOptions" value="manuscript" size="34"><datalist id="scopeOptions"></datalist></label> <button id="applyScope">적용</button> <label>축 <select id="axis"></select></label><div class="tabs"><button class="active" data-tab="queue">결정 대기열</button><button data-tab="graph">논리 그래프</button><button data-tab="matrix">근거 매트릭스</button><button data-tab="validation">검증 결과</button><button data-tab="archive">해소 기록</button></div></header>
<main><section id="queue" class="panel active"></section><section id="graph" class="panel"><div id="graphbox" class="scroll"></div></section><section id="matrix" class="panel"></section><section id="validation" class="panel"></section><section id="archive" class="panel"></section></main>
<script>const D={data},P={{blocker:0,high:1,medium:2,low:3,mechanical:4}},A=new Set(['detected','surfaced','decided','reopened']);
const S=document.getElementById('scope'),X=document.getElementById('axis');function e(s){{return String(s??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}}[c]))}}
const scopes=new Set(['manuscript']);D.nodes.forEach(n=>{{let p=n.id.split('.');for(let i=1;i<p.length;i++)if(!/^P\\d+$/.test(p[i-1]))scopes.add(p.slice(0,i).join('.'));if(/^P\\d+$/.test(p.at(-1)))scopes.add(p.slice(0,-1).join('.'))}});[...scopes].sort().forEach(s=>document.getElementById('scopeOptions').append(new Option(s,s)));D.nodes.forEach(n=>document.getElementById('scopeOptions').append(new Option(n.id,n.id)));const axes=new Set;D.nodes.forEach(n=>Object.keys(n.axes||{{}}).forEach(k=>axes.add(k)));if(!axes.size)axes.add('function');axes.forEach(x=>X.add(new Option(x,x)));
function core(scope){{return D.nodes.filter(n=>n.status!=='omitted'&&(scope==='manuscript'||n.id===scope||n.id.startsWith(scope+'.')))}}function select(scope){{let c=core(scope),ids=new Set(c.map(n=>n.id)),b=new Set;if(scope!=='manuscript'){{c.forEach(n=>(n.predecessors||[]).forEach(p=>{{if(p.id!=='—'&&!ids.has(p.id))b.add(p.id)}}));D.nodes.forEach(n=>{{if(!ids.has(n.id)&&(n.predecessors||[]).some(p=>ids.has(p.id)))b.add(n.id)}})}}return{{core:ids,boundary:b,nodes:D.nodes.filter(n=>n.status!=='omitted'&&(ids.has(n.id)||b.has(n.id))).sort((a,b)=>a.order-b.order)}}}}
function queue(){{let scope=S.value,z=select(scope),q=D.decisions.filter(d=>A.has(d.status)&&(scope==='manuscript'||(d.priority==='blocker'&&(d.scope==='manuscript'||scope===d.scope||scope.startsWith(d.scope+'.')))||d.scope===scope||d.scope.startsWith(scope+'.')||scope.startsWith(d.scope+'.')||(d.impacts||[]).some(i=>z.core.has(i)||[...z.core].some(n=>n.startsWith(i+'.')||i.startsWith(n+'.')))));let ids=new Set(q.map(d=>d.id)),chg=true;while(chg){{chg=false;D.decisions.forEach(d=>{{if(!ids.has(d.id)&&d.status==='reopened'&&(d.depends_on||[]).some(x=>ids.has(x))){{q.push(d);ids.add(d.id);chg=true}}}})}}q.sort((a,b)=>(P[a.priority]??99)-(P[b.priority]??99)||a.order-b.order);document.getElementById('queue').innerHTML=q.length?q.map((d,i)=>`<div class="card"><span class="badge ${{e(d.priority)}}">${{e(d.priority)}}</span><span class="badge">${{e(d.status)}}</span> <span class="muted">${{e(d.id)}} · ${{e(d.scope)}}</span><h3>${{e(d.title)}}</h3><p><b>추천</b> ${{e(d.recommendation||'—')}}</p><p><b>근거</b> ${{e(d.reason||'—')}}</p><p><b>대안 비용</b> ${{e((d.alternatives||[]).join('; ')||'—')}}</p><p><b>영향</b> ${{e((d.impacts||[]).join(', ')||'—')}}</p>${{i===0?'<p><b>판정</b> 추천 채택 / 대안 채택 / 부분 수정 / 보류</p>':''}}</div>`).join(''):'<div class="card">활성 결정이 없습니다.</div>'}}
function color(v){{let f={{observation:'#dbeafe','관찰':'#dbeafe','observation-to-interpretation':'#fef3c7','관찰→해석':'#fef3c7',interpretation:'#dcfce7','해석':'#dcfce7'}};if(f[v])return f[v];let h=0;for(let c of v)h=(h*31+c.charCodeAt(0))>>>0;return`hsl(${{h%360}} 65% 88%)`}}
function graph(){{let z=select(S.value),nodes=z.nodes;if(!nodes.length){{document.getElementById('graphbox').innerHTML='<div class="card">노드 없음</div>';return}}let rows=new Map,pos=new Map,count={{}};nodes.forEach(n=>{{let r=n.id.split('.')[0];if(!rows.has(r))rows.set(r,rows.size);let y=rows.get(r),i=count[y]||0;count[y]=i+1;pos.set(n.id,{{x:60+i*220,y:60+y*140}})}});let w=Math.max(900,...[...pos.values()].map(p=>p.x+200)),h=Math.max(360,rows.size*140+100),svg=`<svg width="${{w}}" height="${{h}}"><defs><marker id="a" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#64748b"/></marker></defs>`;nodes.forEach(n=>(n.predecessors||[]).forEach(p=>{{if(!pos.has(p.id))return;let a=pos.get(p.id),b=pos.get(n.id);svg+=`<path d="M ${{a.x+170}} ${{a.y+30}} C ${{a.x+205}} ${{a.y+30}}, ${{b.x-35}} ${{b.y+30}}, ${{b.x}} ${{b.y+30}}" fill="none" stroke="#64748b" marker-end="url(#a)"/><text x="${{(a.x+b.x+170)/2}}" y="${{(a.y+b.y)/2+15}}" font-size="9">${{e(p.role)}}</text>`}}));nodes.forEach(n=>{{let p=pos.get(n.id),v=X.value==='function'?n.function:(n.axes||{{}})[X.value]||'unspecified',op=z.boundary.has(n.id)?.45:1;svg+=`<g opacity="${{op}}"><rect x="${{p.x}}" y="${{p.y}}" width="170" height="60" rx="8" fill="${{color(v)}}" stroke="#475569"/><text x="${{p.x+8}}" y="${{p.y+17}}" font-size="10" font-weight="700">${{e(n.id)}}</text><text x="${{p.x+8}}" y="${{p.y+33}}" font-size="9">${{e(n.function)}}</text><text x="${{p.x+8}}" y="${{p.y+49}}" font-size="9">${{e((n.claim||'').slice(0,38))}}</text></g>`}});document.getElementById('graphbox').innerHTML=svg+'</svg>'}}
function table(items,nodes,field,label){{let ids=new Set(items.map(i=>i.id));nodes.forEach(n=>(n[field]||[]).forEach(x=>ids.add(x.id)));return`<h3>${{label}}</h3><div class="scroll"><table><tr><th>${{label}}</th>${{nodes.map(n=>`<th>${{e(n.id)}}</th>`).join('')}}</tr>${{[...ids].sort().map(id=>`<tr><th>${{e(id)}}</th>${{nodes.map(n=>`<td>${{e((n[field]||[]).filter(x=>x.id===id).map(x=>x.role).join(', '))}}</td>`).join('')}}</tr>`).join('')}}</table></div>`}}
function matrix(){{let z=select(S.value),n=z.nodes.filter(x=>z.core.has(x.id));document.getElementById('matrix').innerHTML=table(D.evidence_inventory,n,'evidence','근거 × 단락')+table(D.ledger_inventory,n,'ledger','Ledger × 단락')}}function validation(){{let s=S.value,z=select(s),g=new Set(['duplicate-node','duplicate-decision','parse-warning','resolved-under-blocker']),x=D.issues.filter(i=>s==='manuscript'||(i.scope==='manuscript'&&g.has(i.code))||i.scope===s||i.scope.startsWith(s+'.')||s.startsWith(i.scope+'.')||z.core.has(i.scope));document.getElementById('validation').innerHTML=x.length?x.map(i=>`<div class="card ${{e(i.level)}}"><b>${{e(i.code)}}</b><p>${{e(i.message)}}</p><span class="muted">${{e(i.scope)}}</span></div>`).join(''):'<div class="card">검증 이슈 없음</div>'}}function archive(){{let x=D.decisions.filter(d=>['resolved','superseded','deferred'].includes(d.status));document.getElementById('archive').innerHTML=x.length?x.map(d=>`<div class="card"><span class="badge">${{e(d.status)}}</span> ${{e(d.id)}}<h3>${{e(d.title)}}</h3><p>${{e((d.history||[]).join(' / '))}}</p></div>`).join(''):'<div class="card">보관 결정 없음</div>'}}function render(){{queue();graph();matrix();validation();archive()}}S.onchange=render;document.getElementById('applyScope').onclick=render;X.onchange=graph;document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.tabs button,.panel').forEach(x=>x.classList.remove('active'));b.classList.add('active');document.getElementById(b.dataset.tab).classList.add('active')}});render();</script></body></html>'''
    Path(path).write_text(doc,encoding="utf-8")


def main(argv: list[str]|None=None) -> int:
    _utf8(); p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("lint");a.add_argument("outline");a.add_argument("--json-out")
    a=sub.add_parser("queue");a.add_argument("outline");a.add_argument("--scope",default="manuscript");a.add_argument("--json",action="store_true")
    a=sub.add_parser("dashboard");a.add_argument("outline");a.add_argument("--out",required=True)
    args=p.parse_args(argv)
    try:
        out=parse_outline(args.outline); issues=validate(out)
        if args.cmd=="lint":
            errors=sum(i.level=="error" for i in issues);warnings=sum(i.level=="warn" for i in issues);print(f"format={out.format_version} nodes={len(out.nodes)} decisions={len(out.decisions)} errors={errors} warnings={warnings}")
            for i in issues: print(f"- [{i.level.upper()}] {i.code}: {i.message}")
            if args.json_out: Path(args.json_out).write_text(json.dumps(to_dict(out,issues),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            return 2 if errors else 1 if warnings else 0
        if args.cmd=="queue":
            q=decision_queue(out,args.scope);print(json.dumps([asdict(x) for x in q],ensure_ascii=False,indent=2) if args.json else queue_markdown(out,args.scope),end="" if not args.json else "\n");return 0
        render_dashboard(out,issues,args.out);print(f"dashboard written: {args.out}");return 0
    except (OSError,UnicodeError,ValueError) as exc:
        print(f"ERROR: {exc}",file=sys.stderr);return 3

if __name__=="__main__": raise SystemExit(main())
