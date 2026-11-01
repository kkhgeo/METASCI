# Output Formats

모든 Stage의 출력 형식을 정의한다.

---

## Stage Transition Prompts

### Stage 1-A → Stage 1-B

```
Stage 1-A 자체 진단 교정이 완료되었습니다.
승인하시면 Stage 1-B (논증 구조 Monte Carlo)로 진행합니다.

Stage 1-B에서는 N개 레퍼런스의 논증 패턴(Dim 3)을 각각 독립 적용하여
최적의 논증 구조를 찾습니다.
```

### Stage 1-B → Stage 2

```
Stage 1-B 논증 구조 교정이 완료되었습니다.
승인하시면 Stage 2 (스타일 Monte Carlo)로 진행합니다.

Stage 2에서는 N개 레퍼런스의 스타일(톤, 문장구조, 어휘, 전환표현, 인용)을
각각 독립 적용하여 최적의 스타일을 융합합니다.
내용과 논증 구조는 변경하지 않습니다.
```

---

## Final Draft

```
================================================================
  FINAL DRAFT — META-REWRITING-LOOP
  References: N papers | Stages: 1-A → 1-B → 2
================================================================

[최종 교정본 전문]

================================================================
```

---

## Session Log

```
================================================================
  SESSION LOG — META-REWRITING-LOOP
  Date: [YYYY-MM-DD]
================================================================

References:
  A: [source, confidence]
  B: [source, confidence]
  C: [source, confidence]

Stage 1-A (Self-Diagnosis):
  Issues found: N (Major: N, Minor: N)
  Changes applied: N
  User deferred: N

Stage 1-B (Argumentation Monte Carlo):
  Candidates: N
  Rounds: N
  Champion map: D-1=[X], D-2=[X], D-3=[X], D-4=[X], D-5=[X]
  Final avg score: X.X/10
  Fusion status: [success / fallback to best individual]

Stage 2 (Style Monte Carlo):
  Candidates: N
  Rounds: N
  Champion map: D-1=[X], D-2=[X], D-4=[X], D-5=[X], D-6=[X]
  Final avg score: X.X/10
  Fusion status: [success / fallback to best individual]

Preservation check: [PASS / FAIL]
Output files: [list]
================================================================
```

---

## File Output Structure

```
Rewrite_{topic}/
├── blueprints/
│   ├── blueprint_A.md          # Blueprint A (6 dimensions)
│   ├── blueprint_B.md          # Blueprint B
│   └── blueprint_C.md          # Blueprint C
├── stage1a_diagnosis.md        # Self-diagnosis report
├── stage1a_pre_corrected.md    # Pre-corrected draft
├── stage1b_evaluation.md       # Cross-eval table + Champion map
├── stage1b_fusion.md           # Fusion argumentation guide
├── stage1b_corrected.md        # Structure-corrected draft
├── stage2_evaluation.md        # Cross-eval table + Champion map
├── stage2_fusion_blueprint.md  # Fusion style blueprint
├── final_draft.md              # Final rewritten draft
└── session_log.md              # Complete session log
```
