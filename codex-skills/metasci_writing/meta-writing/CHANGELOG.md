# CHANGELOG — meta-writing (metasci_writing / finalized)

## 1.1.0 (2026-07-23)

`Writing_Principles_Extraction` 원리 은행(27개 소스, 대표 원리 185개) 대조 검토 결과를 반영.
은행을 통째로 이식하지 않고, 검토가 지목한 **구조적 공백 6개와 규범 충돌 4건**만 처리했다.
(검토 원본: `Z:\KKH_Research\META_SCI\Writing_Principles_Extraction\`)

**1. 인용 오귀속(misattribution) 차단 — 최대 공백이었음.**
기존 검증은 인용의 *존재*와 *형식*만 봤고, 인용된 문헌이 실제로 그 주장을 하는지는
어디서도 확인하지 않았다. Phase 4에 `Step 3: Claim-Source 내용 일치 검증`을 신설하고
검증 보고서에 `Claim-Source Fidelity` 표를 추가했다. 판정은 지지됨/과장됨/확인불가/
반대됨 4종이며, 과장은 자동 약화, 나머지는 표기 후 보고한다.

**2. 2차 인용 규율.**
Loop 2가 Knowledge 마크다운에서 뽑는 Claim-Citation 쌍은 간접 정보인데, 이를 그대로
본문에 쓰면 읽지 않은 문헌을 인용하게 된다. 스킬 아키텍처에서 직접 나오는 위험이라
`Constraints > Citation Strictness`와 검증 Step 3에 원문 추적 의무를 명시했다.
미확보 시 간접 인용 명시 또는 `[unverified secondary citation]`.

**3. 표절·패러프레이즈 규율 신설 (기존 0건).**
Knowledge·PDF 원문을 직접 읽어 문장을 만드는 스킬인데 관련 규칙이 한 줄도 없었다.
Phase 3에 `Source Language Discipline`을 추가 — 원문 문장 이식 금지, 직접인용은
따옴표+출처, 재서술 시 범위·강도·강조 이동 금지, reporting verb 다양화.

**4. Phase 3.5 개고 단계 신설.**
Phase 3(작성) 다음이 곧바로 Phase 4(인용 검증)여서 원고 자체의 논리·초점·잉여를
점검하는 슬롯이 없었다. 전역(Core message 기여 심사, 단락 삭제 테스트, 순서·커버리지)
→ 국소(문장 분할, 밀도, reporting verb, 용어 일관성) 2단 패스로 신설.
`writing_template.md`에 `Loop 5-0 골격 확정`을 넣어 산문화 전에 단락별 논지를 고정한다.

**5. 규범 충돌 4건 정합화.**
- **표·본문 중복**: `meta-rewriting/section-checklists.md`는 이미 중복을 위반으로 잡는데
  이 스킬 템플릿은 그 중복을 생성하고 있었다. Results에 명시 규칙 추가 —
  표 전체 재서술 금지, 논지에 필요한 핵심 수치 1-2개는 허용.
- **Results의 해석**: 구조 블록의 "가능한 원인 참조"를 삭제하고 원인·기전 해석을
  Discussion 소관으로 이관. `results_style: data-only | with-comparison` 분기 신설.
  평가어("Notably", "Surprisingly") 금지, 예시 문형에서도 제거.
- **`remains unclear`**: 전환어 표는 유지하되, 갭 진술을 그 표현으로 *끝내지 말고*
  결과·영향 + 인용을 덧붙이라는 단서를 Introduction 규칙에 추가.
- **능동태**: 일괄 적용 대신 섹션별 태 정책 표를 신설 (Methods·Abstract 방법 요약은
  수동 유지, Results·Discussion은 능동 권장).

**6. Figure 판독 수치의 불확실성 표기.**
Loop 3은 이미지에서 값의 범위를 뽑으라 지시하는데 검증은 그림 번호와 파일 존재만
확인해, 잘못 읽은 수치가 PASS를 통과했다. 판독 수치에 정확/근사 등급을 부여하고
근사값은 `~` 표기 + 저자 확인 대상으로 남긴다. 원자료가 있으면 그것을 우선한다.

**7. G) AI Assistance Log 출력 추가.**
저널 disclosure 요구에 대응. 개입 층위, 수행/미수행 작업, 저자 확인 필요 항목,
제출용 disclosure 초안을 출력한다. 함께 C) Main Text를 "AI 생성 초안 — 저자 검증 필요"로
프레이밍하고, E)·F)를 자기 보고로 격하해 PASS가 품질 보증이 아님을 명시했다.

**8. 기타 섹션 규칙 보강.**
Introduction(첫 문장 접근성·연구질문 명시·선행연구 개관 상한), Methods(설계 명시·비관례
방법 정당화·통계 필수 기재·윤리 정보 생성 금지), Discussion(연구질문 응답으로 시작·갭
되짚기·범위 이동 금지·외교적 비판), Abstract(독립성·조립 절차), 공통(reporting verb 표·
약어·소스 우선순위).

**채택하지 않은 것 (검토 판정에 따름):**
- 불릿·목록으로 가독성 확보 — 출처가 연구제안서 맥락이며, 저널 본문에 적용하면 산문
  출력 형식이 무너진다.
- "초기 초고와 핵심 사고는 사람이 하고 AI는 보조에 한정" — 규칙으로 넣으면 스킬이 자기
  작업을 부정하게 된다. 대신 출력 프레이밍(C 초안 명시, G 로그)으로 흡수했다.
- 은행 185개 중 적용 불가 50개(사람 습관·협업·투고 행위)와 이미 커버된 46개는 제외.

> ⚠️ 이 버전부터 GitHub `kkhgeo/METASCI` 의 `skills/metasci_writing/meta-writing`과
> 내용이 갈라진다. 1.0.1 원본은 `~/.claude/skills_backup/meta-writing_v1.0.1_pre-principles/`
> 에 보관되어 있다.

## 1.0.1
`skills/metasci_writing/`에 큐레이션된 **완성형(finalized) 본**.
`skills/writing/meta-writing` v1.0.0에서 다음 3가지를 수정했다.

1. **APA 7 인용 표기 정정.**
   본문 인용은 소스 유형과 무관하게 단일 `(Author, Year)` 형식만 사용한다.
   소스 유형 구분 기호(`*`=PDF, `†`=Web)를 본문·References에 붙이지 않는다.
   References는 저자 알파벳순 단일 목록. `Retrieved from`·접근일은 DOI 없이
   내용이 수시로 바뀌는 웹 페이지에만 쓴다. 소스 유형은 내부 추적용
   (Source Summary / 검증 보고서)으로만 기록한다.

2. **검증 후 수정의 안전장치.**
   기존 정보 재포맷은 자동, 새 사실(누락 참고문헌/필드) 추가는 검증된
   원본이 있을 때만 + 사용자 확인 후 수행한다. 없으면 `[missing]`으로
   남기며, DOI·URL·연도·저자를 추론하거나 지어내지 않는다.

3. **자가 품질점수 → 검증 상태.**
   검증 보고서 말미의 `X/10` 자가 채점을 제거하고
   `PASS / ISSUES FOUND` 상태 + 수정항목 목록으로 대체했다.

## 1.0.0
기반 버전 (`skills/writing/meta-writing` 참조): My Data vs Knowledge 분리,
writing.local.md 프로젝트 설정, 5-Loop 프로세스, 서브에이전트 병렬 처리,
progressive-disclosure 참조 파일 구조.
