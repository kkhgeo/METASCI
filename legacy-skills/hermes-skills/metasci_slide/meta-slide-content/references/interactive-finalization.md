# Interactive Finalization

Use this reference when building a presentation with the user step by step. Confirm the high-level structure first, then draft all slide details in one batch for efficient review.

## Default Interaction Model

Work in approval gates:

1. **Promise Gate**: audience, purpose, delivery setting, deck promise.
2. **Structure Gate**: narrative spine, section order, approximate slide count.
3. **Topic Gate**: slide topics, slide jobs, and keyword titles.
4. **Batch Detail Gate**: lead statements, body blocks, figure/table/source choices, captions, and speaker notes for all slides.
5. **Revision Gate**: apply user feedback by slide number.
6. **Lock Gate**: save approved wording and mark slide status as `user-approved` or `locked`.

Do not move past the first three gates until the user accepts them or explicitly asks to skip. After the Topic Gate is approved, draft the detailed content for all slides together rather than asking for approval slide by slide.

## How to Ask

Ask about only the current gate. Prefer concrete alternatives.

Good:

```text
슬라이드 구성은 이 순서로 확정할까요?
01 연구 배경
02 정보 분절 문제
03 온톨로지 기반 통합
04 지식그래프 구축 절차
05 정책 질의 활용
```

Good:

```text
제목까지 확정되었으니, 다음 단계에서는 전체 슬라이드의 리드문구, 불렛, 그림/표 후보, 캡션을 한 번에 초안으로 정리하겠습니다.
```

Avoid:

```text
슬라이드 01의 불렛을 확정했습니다. 이제 슬라이드 02로 넘어갈까요?
```

Use slide-by-slide approval only when the user explicitly asks for line editing or when a slide is too complex to resolve in the batch.

## Batch Detail Draft

After the Topic Gate is approved, draft details for every slide in one response or artifact:

1. Keep the approved slide topic, job, and keyword title unchanged.
2. Draft one final lead statement per slide.
3. Draft 2-4 body blocks per slide.
4. Select evidence objects: figure, table, quote, source excerpt, or none.
5. Draft captions or source notes.
6. Add speaker notes only when needed.
7. Mark unresolved items as `Open Question`.
8. Ask the user to approve all, or request revisions by slide number.

Use a compact review format:

```text
Slide 03
Title:
Lead Statement:
Body Blocks:
- Label: Content
- Label: Content
Figure/Table:
Caption:
Open Question:
```

## Revision Pass

When the user responds, revise only the named slides unless the requested change affects the whole structure.

Use concise status reporting:

```text
Updated: slides 03, 05
Still unresolved: slide 07 figure source
Ready to save: slides 01-06, 08-10
```

If the user edits wording, treat the user's wording as authoritative unless it conflicts with source fidelity.

## Revision Rules

- Keep a slide in `draft` until the title, lead statement, bullets, and evidence choice are accepted.
- Mark unresolved source claims as `Open Question`.
- If a slide becomes overloaded, suggest a split before finalizing.
- If a figure or table is required but not available, mark it as `unresolved` with the needed source.
- Do not rewrite approved wording unless the user asks or a source conflict is discovered.

## Status Labels

- `draft`: proposed but not reviewed.
- `revised`: changed after user feedback.
- `user-approved`: wording accepted by the user.
- `locked`: accepted and should not be changed without explicit permission.
