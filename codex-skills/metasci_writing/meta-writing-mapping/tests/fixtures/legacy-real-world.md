# Outline — Legacy real-world layout (fixture)

- **Core message:** 구형 `outline.md`가 실제로 쓰이는 모양을 재현한 회귀 픽스처.
- **원고 언어:** English
- **최종 갱신:** 2026-08-22

이 파일은 실사용 원고에서 관찰된 네 가지 구조를 담는다. 내용은 중립 placeholder이고
구조만 실제와 같다. 각 구조가 1.1.0 이전 파서를 어떻게 무너뜨렸는지는 아래 주석 참조.

---

## 문서 관계

| 파일 | 역할 |
|---|---|
| `Methods_Outline.md` | Methods 준거 |

---

## 구성

### 1. Introduction — `미설계`

현행 미착수.

### 3. Results and Discussion — **통합 섹션**

<!-- (1) 아래 두 `####`는 산문 소제목이다. 1.1 파서가 이것을 단락 노드로 오인하면
     `if not out.nodes` 폴백이 막혀 legacy 본문 전체가 사라진다. -->

#### 구조 원리

두 성과가 대등하므로 대칭으로 짠다.

#### 층 구조 규칙 (통합 섹션 운용)

| 태그 | 운용 |
|---|---|
| `[관찰]` | 사실 보고만 |

---

<!-- (2) 단락 블록이 `## 구성`이 아니라 사용자가 지은 `## 제N부` 아래에 있다.
     영역 게이트가 `구성`만 허용하면 단락이 하나도 안 잡힌다. -->

## 제1부 — 첫째 묶음

### 3.1 First subsection

```
P1 | [관찰] | Overview
   The first placeholder claim sentence sits on the line after the P line.
   ← — (섹션 첫 단락)
   근거: Fig. 1, Table 1
   기여: 무대 설치

P2 | [관찰→해석] | Trend
   The second placeholder claim, again on the following line.
   ← P1 [Continuation]
   근거: Fig. 2
   Ledger 착지: placeholder metric  ← 첫 보고
   기여: 경향 제시
```

## 제2부 — 둘째 묶음

### 3.4 Fourth subsection — **경첩**

```
P1 | [관찰] | Comparison
   A third placeholder claim.
   ← 3.1 P2 [Question-Answer]
   근거: Fig. 3, Table 2
   Ledger 착지: another placeholder  ← 첫 보고
   기여: 두 묶음을 잇는다

P2 | [해석] | Interpretation
   A fourth placeholder claim.
   ← P1 [Evidence-Claim]
   근거: Fig. 3
   기여: 함의
   메모: 자유문은 메모로 보존된다
```

---

## Ledger 착지 대조표

| Ledger 항목 | 착지 단락 |
|---|---|
| placeholder metric | 3.1 P2 |

---

## 근거 노트

### Fig. 1 — placeholder
→ 배정: 3.1 P1

---

## 미해결

<!-- (3) 2번 항목의 이어진 줄이 `3장 …`으로 시작한다. 열 0 고정과 구분자 요구가
     없으면 이 줄이 결정 #3으로 잡혀 진짜 3번과 ID가 충돌한다.
     10번은 결번이다 — 은퇴한 항목의 번호는 당기지 않는다. -->

1. **첫째 미결** — placeholder 결정 하나
2. **둘째 미결** — 용어 불일치
   3장 전반에 깔린다
3. **셋째 미결** — placeholder 결정 셋

## 사용자 결정 기록 (※ 규칙과 충돌하나 저자가 확정)

- **통합 섹션 채택** (2026-08-22). placeholder 근거.
