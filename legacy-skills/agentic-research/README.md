# Agentic Research Framework

Kosmos 논문(Mitchener et al., 2025)에서 영감을 받은 자율적 데이터 기반 과학적 발견 프레임워크.

## 아키텍처

```
연구 목표 + 데이터셋
        ↓
┌─── 오케스트레이터 ───┐
│                       │
│  ┌─ 데이터 분석 에이전트 (Python/R 코드 실행)
│  │
│  ├─ 문헌 검색 에이전트 (web_search + 논문 탐색)
│  │
│  └─ 세계 모델 (JSON 상태 관리)
│                       │
│  사이클 1 → 2 → ... → N
└───────────────────────┘
        ↓
  추적 가능한 연구 보고서
```

## Kosmos와의 매핑

| Kosmos 컴포넌트 | 이 프레임워크 | 역할 |
|---|---|---|
| World Model | `world_model.json` | 에이전트 간 컨텍스트 공유, 가설 추적 |
| Data Analysis Agent | `orchestrator.py` + Python 스크립트 | 코드 생성 및 실행 |
| Literature Search Agent | web_search 통합 | 문헌 검색 및 검증 |
| Report Generator | `generate_report.py` | 추적 가능한 보고서 생성 |
| Discovery Cycles | `update_world_model.py` | 반복적 가설-검증 사이클 |

## 사용법

### Claude Code에서

```bash
# 1. 세션 초기화
python scripts/init_world_model.py \
  --objective "연구 목표" \
  --dataset /path/to/data.csv \
  --output /path/to/session/

# 2. 데이터셋 프로파일링
python scripts/profile_dataset.py \
  --dataset /path/to/data.csv \
  --session /path/to/session/

# 3. 사이클 계획
python scripts/orchestrator.py --session /path/to/session/ --action plan

# 4. 사이클 시작
python scripts/update_world_model.py --session /path/to/session/ --action start_cycle

# 5. 분석 수행 후 발견 기록
python scripts/update_world_model.py --session /path/to/session/ \
  --action add_finding --data '{"finding_id":"f001",...}'

# 6. 가설 추가
python scripts/update_world_model.py --session /path/to/session/ \
  --action add_hypothesis --data '{"hypothesis_id":"h001",...}'

# 7. 체크포인트 평가
python scripts/orchestrator.py --session /path/to/session/ --action checkpoint

# 8. 보고서 생성
python scripts/generate_report.py --session /path/to/session/
```

### Claude.ai 대화에서

SKILL.md를 읽은 Claude가 자동으로:
1. 연구 목표와 데이터셋을 파싱
2. 세계 모델을 초기화
3. 각 사이클에서 분석 코드를 작성/실행하고 web_search로 문헌 탐색
4. 세계 모델을 갱신하며 가설을 추적
5. 최종 보고서를 생성

## 파일 구조

```
agentic-research/
├── SKILL.md                           # 메인 스킬 (Claude가 읽음)
├── scripts/
│   ├── init_world_model.py            # 세션 초기화
│   ├── profile_dataset.py             # 데이터셋 프로파일링
│   ├── update_world_model.py          # 상태 관리 (가설, 발견, 사이클)
│   ├── orchestrator.py                # 사이클 계획 및 태스크 생성
│   └── generate_report.py             # 추적 가능한 보고서 생성
├── references/
│   ├── world_model_spec.md            # 세계 모델 전체 스키마
│   ├── report_template.md             # 보고서 구조 템플릿
│   └── domain_geoscience.md           # 지구과학 도메인 가이드
└── templates/
    └── world_model_template.json      # 빈 세계 모델 템플릿
```

## 핵심 원칙

1. **추적 가능성 (Traceability)**: 모든 진술에 코드 또는 문헌 근거
2. **구조화된 상태 (Structured State)**: 세계 모델로 컨텍스트 유지
3. **병렬 탐색 (Parallel Exploration)**: 복수 가설 동시 추적
4. **반복적 심화 (Iterative Deepening)**: 각 사이클이 이전 발견 위에 구축
5. **보수적 주장 (Conservative Claims)**: 데이터 기반 vs. 해석적 진술 구분
6. **인간 참여 (Scientist-in-the-Loop)**: 체크포인트에서 연구자 리뷰

## 의존성

- Python 3.8+
- pandas, numpy, scipy
- matplotlib (시각화)
- 도메인별: scikit-learn, pyrolite (지구화학), 등
