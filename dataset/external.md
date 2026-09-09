# 외부 데이터셋 — 무엇을 받았고, 무엇을 확인했나

11 건을 받았다. 목록·파일수·바이트·고정점은 `dataset/survey/README.md`,
자료별 정제본은 `dataset/survey/normalized/*.yaml`, 42 건 비교표와 제외 사유는
`dataset/survey/comparison.md` 에 있다. 원본 체크아웃은 `dataset/raw/` 이고
`.gitignore` 로 막혀 있다 — 남의 저작물이라 재배포하지 않는다.

이 문서는 그 조사의 요약이 아니다. **받기 전에 정해 둔 규칙**이고, 여기에 그
규칙이 11 건에 실제로 적용됐는지 대조한 결과를 붙인다.

> 2026-09-09 까지 이 문서 3 행은 "아직 아무것도 받지 않았다. `dataset/raw/` 는
> 비어 있다" 였다. 계획 시점에 쓰였고, 뒤이은 조사 단계들이 이 파일을 수정 금지
> 목록에 올려 읽기만 했다(`survey/search-log.md` 의 각 단계 "하지 않은 것" 절).
> 그래서 확보가 끝난 뒤에도 계획 시점 문장이 남았다. 두 문서는 커밋 `b5d205c`
> 하나로 같이 들어왔으므로 `git log` 로는 앞뒤가 안 갈리고, 순서는 `search-log.md`
> 안에만 있다.

## 지금 확보한 것

세 숫자의 근거가 서로 다르다(`survey/README.md` 도 같은 구분을 한다).

- **11** — 이 문서를 고치며 다시 셌다. `dataset/raw/` 하위 디렉터리 11 개,
  `survey/normalized/*.yaml` 11 개. 둘이 1:1 로 붙는다.
- **42** — `survey/verified.json` 을 `json.load` 해 `len()` 으로 센 값. 42 다.
- **194** — 검색이 낸 후보 수. **재확인하지 못했다.** 후보 목록이 디스크에
  남아 있지 않다. 인용할 때 이 사실을 같이 적어야 한다.

받은 11 건과 라이선스 근거는 아래 대조표에 있다.

### AgentDojo — 원본은 안 받았다. 포트를 받았다

원 AgentDojo 는 제외했다. 도구가 인메모리 객체이고 판정이 그 객체 상태라
OS 경계를 안 잰다(`comparison.md` 본표 #5 와 3.1 절). 대신 US AISI 의 Inspect Evals
포트를 sparse 로 받았고, 샘플 1,014 개 중 컨테이너에서 실제로 도는 것은
`workspace_plus-u40-i14` · `u41-i14` 두 조합뿐이다(전체의 0.2%,
`normalized/inspect-evals-agentdojo.yaml`). `comparison.md` 본표 #20 은 같은 칸을
"샌드박스 70" 이라 적는다 — 두 값이 어긋나고, 샘플 id 를 대는 정제본 쪽을 따랐다.

앞 판이 옮겨 적은 "사용자 태스크 97 · 보안 케이스 629" 는 논문 값이다. 소스를
직접 센 값은 **user 86 / injection 27 / 조합 567** 이다(`comparison.md` 본표 #5).
우리 `docs/40-prior-art-gap.md` 는 논문 쪽 숫자를 들고 있다.

### InjecAgent — 1 차 출처를 열었고, 안 받았다

MIT(파일명이 `LICENCE`), HEAD `f19c9f2c`(2024-07-02), 24 파일, 설정당 케이스
1,054. 제외 사유는 도구 330 개가 JSON 스키마뿐이고 관측(Observation)이
f-string 으로 위조된다는 것이다(`comparison.md` 본표 #19 와 3.1 절). 설계에서
빌릴 것(S1/S2 2 단 분리, invalid 회계)만 인용한다.

## 라이선스와 재배포 조건을 어떻게 확인하는가

받기 전에 이 순서로 확인한다. 확인 전 기본값은 `unknown` 이고, `unknown` 인
자료는 저장소에 커밋하지 않는다.

1. 저장소 루트의 라이선스 파일. 코드 라이선스가 데이터 라이선스와 같은지 —
   MIT 코드에 CC BY-NC 데이터가 붙어 있는 조합이 흔하다.
2. 데이터 디렉터리에 별도 라이선스·`DATA_LICENSE`·README 고지가 있는지.
3. 논문의 라이선스는 데이터의 라이선스가 아니다. arXiv 의 CC 표시는 원고에만
   걸린다. 배포 플랫폼(figshare · Zenodo · HF)의 메타데이터 선언도 라이선스
   파일이 아니다 — 같은 함정의 다른 얼굴이다.
4. 파생물 조항. 우리는 원본을 그대로 쓰지 않고 경계 표적을 바꿔 변형할
   것이므로, 변형 허용 여부와 변형물 재배포 조건을 따로 본다.
5. 재배포를 피하는 쪽이 기본이다. 원문을 커밋하는 대신 **받아 오는 스크립트와
   내용 해시**를 남기면 라이선스 판단이 필요 없어지는 경우가 많다.
6. 출처 표기 요구(attribution)와 상업적 이용 제한이 우리 공개 방식(MIT 저장소 ·
   공개 아티팩트)과 충돌하는지.

### 확인 결과를 어디에 적는가

앞 판은 결과를 `dataset/cases.yaml` 의 `provenance.license` 에 적는다고 했다.
지금 확보분의 결과는 거기 없다 — `survey/normalized/*.yaml` 의 `license` 와
`comparison.md` 라이선스 열에 있다. `cases.yaml` 은 우리 사례 10 건뿐이고
외부 항목이 아직 하나도 없기 때문이다.

외부 사례를 실행 케이스로 승격하는 시점에 두 가지가 필요하다.

- `schema.md` 의 `provenance.origin` 열거에 `external` 이 없다(지금은
  `changelog` · `docs` · `cve` · `design` · `measurement`). 아래 통합 규칙이
  요구하는 값이므로 승격 전에 열거를 늘려야 한다.
- 정제본의 라이선스 문장을 케이스 항목으로 **옮겨 적는** 것이 아니라, 어느
  정제본을 가리키는지 적는다. 두 벌로 갈라 놓으면 어긋난다(`schema.md` 서두).

## 절차를 11 건에 대조한 결과

각 항목의 라이선스가 어느 파일에서 나왔는지, 위 6 단계 중 무엇이 비어 있는지.
근거는 전부 `normalized/*.yaml` 과 `comparison.md` 에서 읽었다.

| 자료 | 라이선스 | 근거 | 빈칸 |
|---|---|---|---|
| AgentCanary | Apache-2.0 | `LICENSE` + `NOTICE`(PinchBench MIT) | 없음 — 원문을 안 옮겨 §4(b) 변경 고지가 아직 안 걸린다 |
| AIShellJack | Apache-2.0(동봉) ↔ CC BY 4.0(figshare 메타) | 동봉 `LICENSE` 첫 줄 | 충돌은 동봉본 우선으로 정리됐다. figshare 메타를 따를 때의 개작 표시는 아래 (1) |
| BIPIA | MIT | `LICENSE`(4 칸 들여쓰기) + `NOTICE.md` | 없음 — 컨텍스트가 CC BY-SA 4.0 이라 페이로드만 가져오기로 4 를 실제로 적용했다 |
| CIPR | PolyForm Noncommercial 1.0.0 | `LICENSE` Required Notice | 6 — 아래 (3) |
| DeepTrap | MIT | `LICENSE` + HF 카드 front matter | 없음 — 조건이 저작권 고지뿐이다 |
| Inspect Evals | MIT | `LICENSE`(UK AISI) | 상류 AgentDojo/ETH 가 `NOTICE` 에 없다(원본 문제, 기록됨) |
| LivePI | CC BY 4.0 | `LICENSE` · `LICENSE-DATA` (README 배지 MIT 는 틀림) | 4 — 아래 (1) |
| MaliciousAgentSkillsBench | MIT | `LICENSE` 첫 줄 | 5 — 아래 (5) |
| PoisonedSkills | 데이터 CC BY 4.0(선언만) / 하네스 코드 라이선스 없음 | Zenodo 레코드 메타. **zip 안에 라이선스 파일 없음** | 1 · 6 — 아래 (2). 코드는 OSI 라이선스가 없어 벤더링 불가, 설계만 참고 |
| RedCode | 코드 MIT / 데이터 CC BY 4.0 | `LICENSE` + `dataset/LICENSE` | 4 — 아래 (1) |
| RedTeamCUA | Apache-2.0 / 데이터셋 설정 CC-BY-4.0 | `LICENSE` + croissant 메타 | 4 — 아래 (1) |

단계별로 보면 이렇다. **1 단계**(라이선스 파일 실물)는 PoisonedSkills 를 뺀
10 건에서 파일과 첫 줄을 짚을 수 있다. **2 단계**(데이터 쪽 별도 라이선스·고지)가
실제로 기록된 것은 7 건이다 — RedCode(`dataset/LICENSE`) · LivePI(`LICENSE-DATA`) ·
BIPIA(`NOTICE.md`) · RedTeamCUA(croissant 메타) · DeepTrap(HF 카드) ·
AgentCanary(`NOTICE`) · Inspect Evals(`NOTICE`). 나머지 4 건은 데이터 전용
라이선스가 원본에 따로 없어서인지 안 본 것인지 **기록만으로는 안 갈린다.**
**3 단계**는 어느 항목도 논문 라이선스를 근거로 삼지 않았다. 다만 두 건
(AIShellJack · PoisonedSkills)이 배포 플랫폼 메타데이터에 기댄다.

빈칸은 다섯이다. **없는 확인을 했다고 적지 않기 위해 그대로 남긴다.**

1. **CC BY 4.0 자료의 개작 표시 의무가 무기록이다.** LivePI · RedCode(데이터) ·
   RedTeamCUA(데이터셋 설정) · PoisonedSkills, 그리고 figshare 메타를 따르면
   AIShellJack 까지. CC BY 4.0 은 개작물에 "변경했음"을 밝히라고 요구한다.
   `normalized/*.yaml` 의 `transform` 이 무엇을 바꿨는지 적기는 하지만, 그것이
   라이선스 의무의 이행이라고 어디에도 안 적혀 있고 공개 산출물(README · 아티팩트)
   에 그 표시가 붙는지도 정한 바 없다. 4 단계에서 가장 큰 구멍이다.
2. **PoisonedSkills 는 attribution 대상이 미확정이다.** zip 안에 라이선스 파일이
   없고, Zenodo `creators[0].name` 이 `annoymous`(원문 오타), 코드 저장소는
   `anonymous.4open.science` 다. 익명 심사용 아티팩트라 CC BY 의 핵심 의무를
   이행할 상대가 없다. 인용처가 확정되기 전에는 표기를 확정할 수 없으므로,
   이 자료에서 나온 것을 공개 산출물에 싣기 전에 그것부터 정해야 한다.
3. **CIPR 의 비상업 조항과 우리 루트 `LICENSE` 의 관계가 안 적혀 있다.**
   저장소 루트는 MIT("Copyright (c) 2026 WTCY")이고 예외 표기가 없는데,
   `normalized/cipr.yaml` 은 PolyForm Noncommercial 원본의 파생 요약이다. 그
   파일 머리에 Required Notice 를 달아 둔 것이 지금의 유일한 대응이고, 저장소
   전체를 MIT 로 제공한다는 선언과 어떻게 양립하는지는 미기재다.
4. **재취득 명령이 고정점을 강제하지 않는다.** `survey/README.md` 의 재취득
   블록은 `git clone --depth 1 <url>` 뿐이고 기록된 커밋을 `checkout` 하지
   않는다. 기본 브랜치가 움직이면 다른 트리를 받는다. 5 단계가 말한 "해시로
   고정" 이 명령 수준에서는 안 걸려 있다.
5. **한 자료의 고정점 기재가 문서마다 다르다.** MaliciousAgentSkillsBench 는
   `survey/README.md` 와 `comparison.md` 표가 "고정점 없음" 이라 적었는데,
   `normalized/malicious-agent-skills-bench.yaml` 에는 커밋 `f7d28b1a` 와
   CSV md5 `2b2a0f4c…` 가 있다. 정제본 쪽이 더 구체적이다. 함께 받은 `LICENSE`
   파일에는 바이트만 있고 해시가 없다.

## 이 자료가 검증하는 것

- 모델 층의 주입 감수성에 대한 **외부 기준선**. 우리 M 계열(문서에 심긴 지시)의
  성공률이 낮게 나올 때, 그것이 경계 때문인지 우리 페이로드가 약해서인지를
  가를 참조점이 생긴다.
- 공격 페이로드의 형태 목록. 우리가 안 써 본 전달 경로를 고르는 재료.
- 우리 설계 원칙의 **외부 독립 근거**. 역할 분리(원칙 2)를 CIPR · LivePI 의
  `code_carried` 표면이 먼저 구현해 놓았고, 미관측을 결과로 세지 않는다(원칙 3)
  는 AgentCanary 의 `docs/run_validity_criteria.md` 가 같은 결론을 적어 두었다.
  효과 수준 오라클도 우리 신규성이 아니다(RedTeamCUA 의 3 파일 분리).
- 선행 연구와의 비교 가능성.

## 이 자료가 검증하지 못하는 것

여기가 핵심이다. 앞 판은 "둘 다 시뮬레이션이라 실제 경계를 안 잰다" 고 적었는데,
그건 AgentDojo · InjecAgent 에 대한 서술이었고 지금 확보분에는 그대로 안 맞는다.
11 건 중 판정이 실제 OS 상태인 것이 여럿이다 — CIPR, RedTeamCUA, LivePI(스냅샷이
설 때), RedCode 27 개 인덱스 중 6 개, Inspect Evals 의 컨테이너 조합 2 개.

못 재는 이유가 다르다.

**집행 계층을 켠 채로 실제 부수효과를 보는 회차가 11 건 어디에도 없다.** 실상태
오라클을 가진 쪽은 울타리를 걷고 잰다 — CIPR 은 `configs/cc_cli.yaml:83` 이
`claude --permission-mode bypassPermissions`, `configs/codex_cli.yaml:120` 이
`codex --yolo` 에 같은 파일 112 행이 `trust_level = "trusted"` 다. LivePI 는
`secrets.example.env` 의 기본 인자가 `--dangerously-skip-permissions` ·
`--dangerously-bypass-approvals-and-sandbox` 다. AIShellJack 은 재현 절차가
Cursor 를 "Auto-Run Mode with no command execution limitations" 로 바꾸라고
지시한다. 반대쪽도 있다 — PoisonedSkills 의 `rq2` 는 집행 계층을 켠 채 진짜
`claude` CLI 를 돌리지만 판정이 stdout 정규식과 LLM 심판이고, 같은 저장소의
oracle 쪽만 sha1 스냅샷·허니토큰을 보면서 `--dangerously-skip-permissions` 를
켠다. **두 반쪽이 한 회차에서 만나는 실행이 그 저장소에 없다**
(`comparison.md` 2.4 절). 그 빈칸이 이 저장소가 서는 자리다. 공개된 성공률을
제품 경계의 성적표로 인용하면 안 되는 이유도 같다.

- 평가 대상이 대체로 제품이 아니라 모델이다. 표적도 안 겹친다 — AgentCanary 는
  OpenClaw · Hermes · NanoClaw, DeepTrap 은 OpenClaw CLI 다. Claude Code 를 직접
  띄우는 것은 CIPR 과 PoisonedSkills 인데, 전자는 위 설정으로 뜨고 후자는
  실상태 오라클과 갈라져 있다.
- 버전축이 없다. 우리 주장이 "CHANGELOG 에 귀속된 시나리오가 릴리스 버전을
  따라 아직 통하는가" 인데, 그 축을 이 자료들은 갖고 있지 않다.
- 차단된 사례가 라벨된 코퍼스가 없다. 11 건 전부 공격 성공률 중심이라 음성
  사례가 없고, 오탐률을 재려면 정상 자극을 우리가 만들어야 한다.
- 컨테이너 밖 경계가 비어 있다. 판정이 거의 전부 Docker 안이고, 호스트 직접
  실행 · WSL 경계 · Windows ACL 을 재는 자료는 조사에서 못 찾았다.
- 설정 경계(B4)는 호스트 재시작 뒤 신뢰되어 실행되는 파일이 있는지의 문제이고,
  컨테이너 회차에는 그 "나중" 이 없다.

즉 이 자료들이 재는 것은 사슬의 앞칸이다. 이 저장소가 재는 것은 모델 층 ·
권한 층 · 강제 층이 이어진 사슬이고, 어느 층이 막았는지를 대조군으로 가른다
(`cases/SCHEMA.md`).

## 통합 규칙

- 외부 사례는 자기 `family_id` 를 받고, 우리 계열과 섞지 않는다.
- `provenance.origin: external` 로 구분하고 `ref` 에 받은 커밋·릴리스 태그와
  받은 날짜를 적는다. 원본 버전을 못 고정하면 받지 않는다.
- 외부 사례의 결과를 경계 헤드라인 수치에 합치지 않는다. 같은 표에 놓을 때는
  무엇을 재는 값인지 열 이름으로 갈라 적는다.
- 우리 하네스로 돌리려면 시뮬레이션 도구를 실제 부작용으로 바꾸는 번역이
  필요하다. 그 번역은 원 데이터가 아니므로 `transform` 에 무엇을 바꿨는지 남기고,
  번역 뒤 결과를 원 벤치마크 점수와 비교하지 않는다.
- 원본이 집행 계층을 끈 조건에서 잰 수치는 우리 수치와 같은 열에 놓지 않는다.
  조건이 다르면 그건 비교가 아니라 착시다.
