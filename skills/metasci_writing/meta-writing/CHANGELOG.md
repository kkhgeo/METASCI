# CHANGELOG — meta-writing (metasci_writing / finalized)

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
