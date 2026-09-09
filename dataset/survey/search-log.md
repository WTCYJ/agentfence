# 검색·확인 기록

이 파일은 "왜 이건 안 봤나"에 답하기 위한 것이다. 단계별로 무엇을 했고 무엇이
헛수고였는지 적는다. 실행한 에이전트 회차는 전 단계 통틀어 0회다.

주의 — 아래 "2026-09-08 · 비교표 작성 단계" 절의 "내려받은 데이터셋 파일 0바이트"
는 그 단계 시점의 사실이고 지금은 아니다. 뒤이은 확보 단계들이 모두 11건을 받았다
(그 아래 "obtained 3건" 이라고 적힌 대목도 그 시점의 사실이지 현재 값이 아니다).
현재 상태는 맨 아래 2026-09-09 정직성 감사 절과 `README.md` 를 보라.

## 2026-09-08 · 비교표 작성 단계

### 이 단계가 받은 것과 못 받은 것

앞 단계는 후보 40건의 1차 출처를 확인했다고 알려왔는데, 이 단계에 실제로 도착한
확인 기록은 5건이다 — LivePI, RedTeamCUA, MalSkillBench, MCPTox, AIShellJack.
전달 내용이 AIShellJack 항목의 `verified_how` 중간(`Google Cloud virtual machine
(Ubuntu 20.0` 에서)에서 잘려 있어, 그 뒤에 있었을 나머지 후보의 확인 결과는
받지 못했다. 비교표를 5건으로 한정한 이유가 이것이고, 없는 값을 추정해 채우지
않았다.

### 앞 단계의 작업 흔적 조사 (헛수고를 줄이려는 시도)

전달이 잘렸으므로, 나머지 후보가 무엇이었는지라도 알아내려고 파이프라인이 쓴
스크래치패드를 훑었다. 경로는
`C:\Users\yejun\AppData\Local\Temp\claude\C--Users-yejun\c2f8b650-21c4-4574-b560-3c827f528d80\scratchpad`.

- `ls -la` 로 파일 목록 확인. 09:55~10:09 와 14:22~17:07 두 무리로 나뉜다.
- 파일 앞부분만 읽어 이름을 특정한 것: `asb_tree.json`(agiresearch/ASB API 응답),
  `opi_files.json`(liu00222/Open-Prompt-Injection), `pi_bench.py`(Meta PurpleLlama,
  MIT 헤더), `zen.json`(Zenodo, PoisonedSkills), `dt_README.md`(DeepTrap,
  arXiv 2605.11047), `nemotron_ipi_README.md`(NVIDIA NeMo-Gym, front matter
  `license: cc-by-4.0`), `wasp_cfg.json`(WASP, GitLab 환경 설정),
  `redcode_tree.tsv`(RedCode), `bipia/`, `mcpsec/`, `pll/`, `eff/`.
- 이름을 특정하지 못한 것: `eff/` 안의 snapshot checker 류, `trojans_whisper.txt`,
  `ipi_wild.html`. 무엇의 산출물인지 파일만으로는 확정되지 않아 비교표 4절에
  "이름·성격 미확정" 으로 남겼다.

이 흔적들은 "그 이름이 조사되었다" 는 증거일 뿐이다. 라이선스·규모·적합성은
전혀 확인하지 않았으므로 비교표 본표에 넣지 않았다.

### CIPR 추적 (부분 성공)

`cipr_tree.txt` 와 `cipr_slice.json` 이 눈에 띄었다. 트리에 `configs/cc_cli.yaml`,
`codex_cli.yaml`, `cursor_ide.yaml`, `opencode_cli.yaml`, `vmware.example.yaml` 이
있어 우리 대상(코딩 에이전트 CLI)과 가장 가깝게 보였기 때문에 이름만이라도
확정하려 했다.

- `WebSearch: "CIPR benchmark coding agent indirect prompt injection dataset
  cc_cli cline codex cursor configs"` → 논문 특정 성공. arXiv 2608.30686
  "Beyond the Payload: How User Invocation Shapes Coding Agent Vulnerability to
  Repository Poisoning". 검색 결과 요약이 "1,920 instances, 20 repositories,
  four task types, automated runtime and trace-based oracles" 를 언급했다.
- `WebFetch https://arxiv.org/abs/2608.30686` → 제목·저자 6인·2026-08-31 v1·초록
  전문 확인. 다만 abs 페이지에 GitHub/Zenodo/HuggingFace 링크가 없다. 코드
  URL 미확인.
- `gh search repos "CIPR coding poisoned repos"` 와 `"Coding In Poisoned Repos"`
  → 둘 다 결과 0건. 헛수고.
- `cipr_slice.json` 헤더에 `dataset_name: cipr_main_k15_selected3_direct_deep`,
  `target_tasks: [prepare_env, fix_feature_issue, fix_bug_issue, run_test]` 가
  있어 논문의 네 가지 태스크 유형과 일치한다. 스크래치패드 트리가 이 논문의
  저장소일 개연성은 높지만 URL 을 못 댔으므로 `found` 로만 두고 선정하지 않았다.
  다음 단계 최우선 재조사 대상.

### AIShellJack 배포 파일 실측 (선정 명령을 실제로 동작하게 만들기 위해)

`how_to_get` 에 추측 경로를 적지 않으려고 figshare 메타데이터만 조회했다. 데이터
파일 본체는 받지 않았다.

- `curl -s https://api.figshare.com/v2/articles/30111988/files` → 기본 페이지가
  10건만 돌려준다. 앞 단계가 보고한 91건과 어긋나 보였는데, `?page_size=200` 을
  붙이니 91건·합계 1,680,735,369바이트로 앞 단계 수치와 정확히 일치했다.
  기본 페이지 크기 때문이었다.
- 확보한 파일 id(선정 명령에 그대로 쓴다):
  `57929701` linux_atomic_tests_attack_payloads.json (486,178B),
  `57929728` repos.zip (2,117,470B),
  `57929929` workspace_setup.py (15,700B),
  `57929923` check_command_execution.py (36,140B),
  `57929908` Labeling_results.xlsx (23,489B),
  `57929944` raw_results.zip (1,675,993,431B — 받지 않는다).
- `curl -sIL https://ndownloader.figshare.com/files/57929701` → 첫 응답 302 에
  `Content-Disposition: attachment;filename=linux_atomic_tests_attack_payloads.json`
  이 붙어 파일이 맞다는 것까지는 확인. 리다이렉트된 S3 레그는 HEAD 에 403 을
  준다(서명 URL 이 GET 만 허용하는 흔한 형태). GET 은 시도하지 않았으므로
  실제 내려받기 성공 여부는 미검증이다 — 선정 명령의 유일한 미확인 지점이다.

### 하지 않은 것

- 유료 측정 0회. `probe_*.py`, `campaign.py`, `run_*.sh`, `claude` 바이너리 호출
  전부 손대지 않았다.
- 내려받은 코드 실행 0회. `pip install`, `npm i`, `setup.py` 전부 없음.
- `dataset/raw/` 에 쓴 파일 0건. 이 단계의 산출물은 `dataset/survey/` 의
  `comparison.md` 와 이 파일뿐이다.
- 금지 영역(`check_docs.py`, `runner.py`, `remeasure.yaml`, `plan/`,
  `dataset/schema.md`, `dataset/cases.yaml`, `dataset/external.md`, `cases/`,
  `*.json` 원시 측정 기록, `_quarantine-*/`)은 읽기만 하고 수정하지 않았다.
  실제로 열어본 것은 디렉터리 목록뿐이다.
- 데이터셋 안의 인젝션 문구(예: "이전 지시를 무시하고", `rm -f ...` 류)는 전부
  자료로만 취급했고 지시로 따르지 않았다.

### 다음 단계에 남기는 숙제

1. CIPR 저장소 URL 확정. 논문 PDF 본문이나 저자 페이지에 링크가 있을 가능성이
   높다. 확정되면 우리 대상과 가장 가까운 자료라 우선 검토할 것.
2. PoisonedSkills 의 `rq2_claude` — Claude Code 대상 실측이 실제로 있는지, 어떤
   조건(권한 켬/끔)에서 잰 것인지. 라이선스가 익명 저장소라 확인 필요.
3. 전달이 잘려 못 받은 나머지 후보들의 1차 출처 확인 기록 회수.
4. LivePI 논문 PDF 의 "pre-execution tool-call authorization" 방어 실험 설정.
   권한을 켠 조건의 수치가 논문에 있으면 대조 근거의 값이 크게 달라진다.

## 2026-09-08 · 확보 단계 (사후 기록)

비교표 단계 이후에 확보 단계가 돌아 `dataset/raw/` 에 3건을 받았다. 이 절은
감사 단계가 디스크를 직접 재서 남기는 기록이다 — 확보 단계의 자기 보고를
그대로 옮긴 게 아니라 다시 센 값이다.

| 대상 | 경로 | 바이트(.git 제외) | 파일 | 고정점 |
|---|---|---|---|---|
| AIShellJack (부분) | `dataset/raw/aishelljack` | 2,699,896 | 13 | figshare DOI v4. VCS 없어 md5 로 고정 |
| LivePI | `dataset/raw/livepi` | 2,503,427 | 318 | `d48d3fa4949c587bef5de93a088fd9457b8544a6` |
| RedTeamCUA | `dataset/raw/redteamcua` | 6,833,316 | 918 | `a05b8bd04629e19a9a06bf04f8e0c5b53549d16c` |

받지 않은 것: AIShellJack `raw_results.zip`(1,675,993,431B). 논문 결과 2,826건이
그 안이라 결과 수치는 계속 미확인이다.

## 2026-09-08 · 정직성 감사

한 일: 디스크 실측 대조, 문서의 확인상태 재판정, 근거 없는 수치 강등,
`.gitignore` 보강, `README.md` 작성.

실측으로 확인 단계 보고와 **일치한** 것 — 3건의 바이트·파일수 전부, AIShellJack
4개 대상 파일 md5 4건 전부, 페이로드 314건·test_guid 314종 유일·base 기법 69종,
repos.zip 958엔트리 중 비-__MACOSX 479, LivePI 태스크 34건·기법태그 12개 정의 중
실사용 3개·`total_case_count` 169·실행결과 46회차, LivePI `prompt_injection_lab/`
와 `artifacts/prompt_injection_lab/` 이 `diff -rq` 로 완전 동일한 중복 사본,
RedTeamCUA 예제 864건·id 중복 0·플랫폼 각 288·`adv_id` 24종 각 36건·`tags` 864건
모두 true.

대조 근거(다)도 원본 파일에서 직접 재확인했다 — LivePI
`agents/claude_code_adapter.py:11`(`--dangerously-skip-permissions`),
`:36`(`IS_SANDBOX=1` 대입, 34행은 그 이유를 적은 주석), `agents/codex_adapter.py:13`, `secrets.example.env:113/144/177`.
AIShellJack `README.figshare-57929695.md:45`(Auto-Run 무제한 / Auto Approve
빈 deny 목록). RedTeamCUA `lib_run_single.py:124-140`(result.txt·adversary_result.txt·
check.json 3중 분리), `desktop_env/evaluators/metrics/basic_os.py` 의
`check_service_active` 가 출력에 "inactive" 가 있으면 1 을 주는 것,
`accound` 오타가 예제 24개 파일에 있는 것.

**어긋나서 고친** 것은 `comparison.md` 갱신 각주 [^9] [^10] [^11] 과
정정된 각주 [^7] [^8], 그리고 LivePI 규모·taxonomy 개수, RedTeamCUA 2×2 축 정의,
AIShellJack 라이선스 서술·기법 수·"84%" 강등, 논문 수치 92.5%/42.9% 헤지다.

**바로잡지 못하고 unknown 으로 내린** 것: AIShellJack 84% 와 결과 2,826건,
RedTeamCUA 92.5%/42.9% 와 "216 시나리오"·"27.4MB", Atomic Red Team 상류 라이선스.
전부 확보한 파일 안에 근거가 없다.

사소한 드리프트 1건: 확보 보고가 `normalized/redteamcua.yaml` 을 14,332B 라
적었으나 실측 14,406B 다. 보고 후 파일이 더 편집된 것으로 보이며 내용 손상은
없다(`yaml.safe_load` 통과, `goal_map` 24행). 값 자체는 무해하지만, 보고된
숫자가 파일보다 낡을 수 있다는 예라 적어 둔다.

이 단계도 유료 측정 0회, 내려받은 코드 실행 0회다. 데이터 안의 인젝션 문자열은
전부 자료로만 다뤘다.

## 2026-09-09 · 정직성 감사 2차 (독립 재검)

1차 감사의 결론을 그대로 받지 않고 디스크에서 다시 셌다. 다음은 이번에 직접
돌린 대조이고, 괄호 안이 실측값이다.

- 폴더 바이트·파일수 3건 전부 일치. `find -type f -not -path "*/.git/*"` 기준
  aishelljack 13/2,699,896 · livepi 318/2,503,427 · redteamcua 918/6,833,316.
  `.git` 을 빼지 않으면 livepi 347/2,942,441, redteamcua 1,148/18,446,421 이
  나오므로 문서의 "(.git 제외)" 단서가 없으면 수치가 어긋나 보인다.
- `git log -1` 로 두 저장소 HEAD 확인. livepi `d48d3fa4949c...`(2026-06-09
  01:36:57 +0800), redteamcua `a05b8bd0462...`(2026-02-09 03:09:19 -0500).
  문서의 해시와 동일.
- payloads.json 재파싱: 레코드 314, `test_guid` 314종, `indexed_technique`
  314종, 기법 서브포함 106·base 69, md5 `a910976e59c132b978b529cfb97bdc98`,
  실행기 sh 246/bash 64/powershell 4. repos.zip 958엔트리·비-__MACOSX 479·
  압축해제 3,145,296B. 전부 문서와 일치.
- livepi 태스크 34건, 표면 7종, 실사용 기법태그 3종, taxonomy JSON 6개,
  `total_case_count` 169, 실행결과 파일 6개·회차 46. 일치.
  `diff -rq prompt_injection_lab artifacts/prompt_injection_lab` 종료코드 0 —
  중복 사본이라는 서술 확인.
- redteamcua 예제 864(플랫폼별 288×3), `accound` 오타가 예제 24파일에 존재,
  `basic_os.py:41-45` 의 `check_service_active` 가 `"inactive" in result` 면 1
  반환. `lib_run_single.py:124-140` 의 3중 분리 기록도 원문 확인.
- 라이선스 1차 확인: redteamcua `LICENSE` 첫 줄 "Apache License / Version 2.0",
  livepi `LICENSE` 첫 줄 "Creative Commons Attribution 4.0 International
  (CC BY 4.0)". livepi `README.md:7` 의 MIT 배지도 실제로 있다 — 문서가
  "배지는 낡음" 이라 적은 근거를 확인한 것이다.

**이번에 고친 것 3건.** 전부 근거 인용의 정확도 문제이고 결론은 안 바뀐다.

1. `claude_code_adapter.py` 의 `IS_SANDBOX=1` 은 34행이 아니라 36행이다.
   34행은 그 이유를 적은 주석이다. `README.md` 와 이 파일에서 고쳤다.
2. `secrets.example.env` 를 경로 없이 `agents/...` 인용 사이에 끼워 두어
   `prompt_injection_lab/agents/` 아래 파일로 읽혔다. 실제 위치는 저장소
   최상위(그리고 `artifacts/livepi/data/` 에 같은 사본)이며 그 경로에 파일이
   없으므로 따라가면 근거를 못 찾는다. 경로를 명시하고, 113·144행도 같은
   플래그를 기본 인자로 두고 있다는 사실을 본문에 넣었다.
3. `comparison.md` AIShellJack 행의 적합성 칸이 "ATT&CK 70기법" 으로 남아
   있었다. 같은 표의 각주 [^11] 이 실측 69 를 쓰라고 정해 놓은 것과 어긋나
   69 로 맞췄다.

**빠져 있어서 채운 것 1건.** `.gitignore` 주석이 "재취득 방법은
`dataset/survey/README.md` 에 있다" 고 가리키는데 README 에 그런 절이 없었다.
`raw/` 를 커밋하지 않는 설계이므로 이게 없으면 다른 사람은 재현을 못 한다.
`README.md` 에 "다시 받는 법" 절을 넣었다 — clone/curl 명령과 AIShellJack
md5 4개, 그리고 받지 않는 `raw_results.zip` 을 명시했다.

**침범 검사.** `git status --short` 에 `dataset/` 밖 변경이 여럿 있으나
(`HARDENING.md`, `LOG.md`, `README.md`, `cases/*`, `check_docs.py`,
`runner.py`, `probe_*.py`, `wsl_probe.py`, `artifact/results.html` 등) 이
조사가 만든 것이 아니다 — 같은 저장소에서 도는 다른 워크플로의 것이라
되돌리지 않았다. 이 조사가 `dataset/` 밖에 만든 변경은 `.gitignore` 뒤에
붙인 4줄뿐이고, `git diff .gitignore` 로 그 4줄 외에 아무것도 없음을 확인했다.
`git check-ignore -v` 로 `dataset/raw/` 가 실제로 무시되고
`dataset/survey/README.md` 는 무시되지 않는 것도 확인했다.

**여전히 `unknown` 인 것** (1차 감사와 동일, 이번에도 못 좁혔다): AIShellJack
84% 와 결과 2,826건, RedTeamCUA 92.5%/42.9%·"216 시나리오"·"27.4MB",
Atomic Red Team 상류 라이선스, CIPR 저장소 URL. 이번 감사도 유료 측정 0회,
내려받은 코드 실행 0회이고 데이터 안의 인젝션 문자열은 자료로만 다뤘다.

## 2026-09-09 · 비교표 전면 재작성 (42건 전수)

### 왜 다시 돌았나

이전 비교표는 5건만 담고 있었다. 앞 확인 단계가 42건을 조사해
`verified.json`(779,452B)에 남겼는데, 그 결과가 비교표 단계로 넘어오면서
AIShellJack 항목의 `verified_how` 중간에서 잘렸기 때문이다. 그래서 InjecAgent ·
ASB · BIPIA · RedCode · CyberSecEval 4 · SEP · Tensor Trust · NIST CAISI · CIPR
같은 주요 자료가 표에 아예 없었다. 이번 단계는 그 실패를 고치려고 돌았다.

### 이번 단계가 실제로 한 일

새 웹 검색은 하지 않았다. `WebSearch`·`WebFetch` 스키마를 부르지도 않았다.
검색·1차 출처 확인은 앞 단계가 이미 했고, 이번에 필요한 것은 그 결과를 빠짐없이
읽는 것이었기 때문이다. 헛수고를 반복하지 않으려는 판단이다.

읽기 절차:

1. `python -c "json.load(...)"` 로 42건의 인덱스·status·이름·직렬화 바이트 수를
   먼저 뽑아 읽을 순서와 분량을 잡았다. 항목당 5.5KB~18.8KB, 합계 약 470KB.
2. cp949 콘솔에서 `—`(em dash) 인코딩 오류가 나서 `PYTHONIOENCODING=utf-8`
   을 붙였다. 이걸 안 붙이면 목록 출력이 8번째 항목에서 죽는다.
3. 42건 전부를 필드 단위로 평문 파일 하나(3,783행)로 펼쳐 스크래치패드에 쓰고,
   200~260행씩 19회에 나눠 읽었다. Read 도구의 25,000토큰 상한에 두 번 걸려
   (offset 1229 limit 250, offset 3228 limit 160) 그때마다 limit 을 줄였다.
4. 읽은 것은 `name / status / primary_url / paper_url / version / updated /
   license / license_evidence / scale / measures / environments / real_boundary /
   fit / cost / preconditions / blockers / unknowns / verified_how` 18개 필드
   전부다. 요약본이나 앞부분만 보고 판정한 항목은 없다.

### 작업 지시와 사실이 어긋난 곳 (규칙 3)

지시는 "지금 `obtained` 는 아직 하나도 없다" 고 알려왔다. 사실이 아니다.
`ls -la dataset/raw/` 와 `find -type f -not -path '*/.git/*'` 로 직접 재어
확인했다 — aishelljack 13파일 2,699,896B, livepi 318파일 2,503,427B,
redteamcua 918파일 6,833,316B 가 실재한다. 앞 확보 단계와 두 차례 감사의
산출물이고 `normalized/` 에 정제본도 있다.

그래서 비교표의 `확인 상태` 열을 지시대로 "전부 verified" 로 적지 않고
실측대로 obtained 3 / verified 39 로 적었다. 전달받은 전제보다 디스크가 우선이다.
이 때문에 RedTeamCUA 의 판정도 바꿨다 — 적합성만 보면 GUI/CUA 대상이라
제외 후보였으나, 이미 받아서 정제까지 끝난 자료를 버리는 것은 근거 없는 낭비라
"확보 완료, 활용은 24목표 CIA 매핑과 요인 설계까지" 로 선정에 남겼다.

### 헛수고와 함정

- `Read` 로 3,783행 파일을 한 번에 열려다 두 번 거부당했다(41,024토큰,
  25,617토큰). 큰 JSON 을 평문으로 펼칠 때 항목당 실제 부피가 직렬화 길이의
  1.5~2배로 늘어난다는 걸 감안해야 한다.
- `python` 출력의 cp949 문제. 한국어 문서를 다루는 이 저장소에서는
  `PYTHONIOENCODING=utf-8` 을 기본으로 붙이는 편이 낫다.
- `verified.json` 안에 중복 항목이 두 쌍 있다. AgentVigil 이 idx 6·7 로,
  IPI-Proxy 가 idx 14·15 로 두 번 들어 있다(같은 저장소를 다른 각도로 조사한
  기록). 비교표에는 둘 다 행으로 남기고 중복임을 명시했다 — 42건이라는 수를
  40건으로 줄여 적으면 앞 단계 기록과 대조가 안 되기 때문이다.

### 이번 판정에서 드러난 검색 단계의 오분류

앞 단계가 이미 바로잡아 놓은 것들인데, 같은 실수를 반복하지 않으려고 모아 둔다.

- `NetInjectBench` — "130 시나리오 / 240 공격 인스턴스" 는 틀렸다. 240 은
  별개 공격이 아니라 80 공격 시나리오 × 모델 3종의 model-scenario instance 다.
- `MCPTox` — "real, 45개 라이브 서버 위에서 평가" 는 틀렸다. 45개 실서버는
  도구 메타데이터를 긁어온 출처일 뿐이고 평가 자체는 단일 턴 텍스트 생성이다.
- `LivePI` — "코드 MIT + LICENSE-DATA 이중 라이선스" 는 틀렸다. 두 파일 모두
  CC BY 4.0 이고, MIT 는 README 의 낡은 배지에서 온 오해다.
- `AgentDyn` — 검색이 준 URL `leolee99/AgentDyn` 은 낡았다. `SaFo-Lab/AgentDyn`
  으로 이전됐고 API 가 301 로 넘긴다.
- `Firewalls All You Need?` — "AgentDojo/BIPIA/ASB/InjecAgent/SEP 5종" 은 틀렸다.
  본문에 BIPIA 0회·SEP 0회 등장하고 실제 평가 대상은 AgentDojo · ASB ·
  InjecAgent · tau-bench 4종이다. "메타 분석" 이라는 종류 표기도 부정확하다.
- `PI Attacks on Agentic Coding Assistants` — "benchmark" 분류가 틀렸다.
  벤치마크가 아니라 코드를 내지 않은 SoK 서베이다.
- `Safety Benchmark Taxonomy` — 같은 오분류. 벤치마크를 세는 서베이다.
- `MCPTox` 익명 저장소 — 논문이 안내한 `anonymous.4open.science/r/AAAI26-7C02`
  는 HTTP 401 로 죽었고, 정식 저장소는 `zhiqiangwang4/MCPTox-Benchmark` 다.

### 아직 안 본 실마리 (다음 조사 후보)

이번 통독에서 나온 것 중, 조사되지 않았고 우리 문제의식에 가까운 것만 적는다.
전부 `verified.json` 안의 `unknowns`·`fit` 에서 나온 2차 단서이고, 이 조사가
1차 출처를 열어보지는 않았다.

- **OpenAgentSafety** — Safety Benchmark 서베이(arXiv 2605.16282) 부록 D 파싱
  결과, 40개 벤치마크 중 컨테이너·라이브는 5개뿐이고 그중 우리와 가장 가깝다.
  356개 멀티턴 과제를 실제 툴(shell, Python, 브라우저, 메시징)로 컨테이너
  샌드박스에서 돌린다. 같은 서베이가 "컨테이너 벤치마크는 무해한 프롬프트로도
  50~86% 불안전률을 보고하는데 LLM 에뮬레이트 환경(ToolEmu)은 23.9%" 라는
  측정 편향을 데이터로 보인다.
- **ODCV-Bench** (`github.com/McGill-DMaS/ODCV-Bench`) — MIT, 22MB,
  2026-05-12 푸시, `docker-compose.yml` + `mission_executor` 트리 실재를
  앞 단계가 확인했다. 서베이가 매긴 Containerized 코딩이 정직한 한 건.
- **ST-WebAgentBench**, **MobileSafetyBench** — 같은 서베이의 Containerized
  분류. Table 8 행 추출이 이 둘에서만 실패해 사례 수 미확인.
- **IDEsaster** (Ari Marzouk, 30+ 취약점 중 24건 CVE, Cursor·Windsurf·Kiro.dev·
  Copilot·Zed·Roo Code·Junie·Cline 대상) — 실제 제품에서 나온 실제 CVE라 우리
  회귀 케이스로 옮길 값이 가장 높아 보인다. 다만 인용이 "Technical Report, 2025"
  로 URL·DOI 가 없어 안정적 출처를 찾아야 한다.
- **Assay-Harness** (`Rul1an/Assay-Harness`, MIT, 2026-09-07 푸시) — 에이전트가
  주장한 파일·네트워크·프로세스 부작용을 독립 관측 증거와 대조해
  supported/degraded/blocked/not-evaluable 로 판정하는 CI 게이트. "observed
  support is the ceiling" 이라는 표현이 우리 원칙 3과 사실상 같은 말이다.
  우리 판정 어휘와 대조해 볼 값어치가 있다.
- **agent-sentinel** (`junlinwk/agent-sentinel`) — eBPF/BPF-LSM 로 커널 경계에서
  민감 파일 접근을 원자적으로 차단. 라이선스 없음, 스타 1이라 기대는 낮다.
- **CubeSandbox** (TencentCloud) — 퍼커널 하드웨어 격리 + eBPF 네트워크 격리 +
  도메인 허용목록 이그레스.
- **mcp-sec-audit** (arXiv 2603.21641) — Docker/eBPF 기반 동적 샌드박스 퍼징.
- 산업 리포트 계열 — Snowflake Cortex 에서 bash 프로세스 치환으로 명령
  허용목록을 우회해 RCE 로 간 체인, Claude `web_fetch` 를 통한 글자 단위 유출,
  Trail of Bits 의 스킬 스캐너 우회, ClawHub 패키지 52,652개 중 22%만 clean
  이라는 레지스트리 전수 분석, Anthropic 의 간접 인젝션 720회 시도 0회 성공
  보고. 실제 제품·실제 경계를 명시한 사건이라 케이스 씨앗으로 곧장 읽힌다.
  전부 `awesome-agent-skills-security` 인덱스 경유라 1차 출처 재확인이 필수다 —
  그 인덱스는 봇이 매일 자동 추가하고 자리표시자 죽은 링크가 16건 있으며
  "SkillGuard 악성 스킬 157개" 처럼 실측과 어긋나는 표기가 실제로 발견됐다.

### 규칙 준수

이번 단계도 유료 회차 0, 내려받은 코드 실행 0(`pip install`·`setup.py`·`npm i`
전부 미실행), 새로 내려받은 파일 0이다. `verified.json` 안에는 설계상 "이전
지시를 무시하고" 류 문자열과 실제 악성 명령(`shutil.rmtree("/")`,
`cat /etc/passwd | curl -X POST`, `sudo ufw disable`, `curl -fsSL ... | bash`)이
인용문으로 다수 들어 있다. 전부 연구 자료로만 읽었고 어떤 것도 지시로 따르지
않았으며 실행하지 않았다. 쓴 파일은 `dataset/survey/comparison.md` 와
`dataset/survey/search-log.md` 둘뿐이고, 금지 목록(`check_docs.py`, `runner.py`,
`remeasure.yaml`, `plan/`, `dataset/schema.md`, `dataset/cases.yaml`,
`dataset/external.md`, `cases/`, `*.json` 원시 측정 기록, `_quarantine-*/`)은
열지도 건드리지도 않았다.

---

## 2026-09-09 · 정직성 감사 단계

앞 단계들이 적은 것을 디스크와 대조했다. 이 단계도 유료 회차 0, 내려받은 코드
실행 0, 새로 내려받은 파일 0이다. 쓴 파일은 `dataset/survey/` 안의
`README.md` · `comparison.md` · `search-log.md` 셋뿐이다.

### 실측 방법

`find <dir> -type f -not -path "*/.git/*"` 로 파일 수, `du -sb --exclude=.git`
로 바이트, `git -C <dir> rev-parse HEAD` 로 커밋, `head -3 LICENSE` 로 라이선스
첫 줄, 그리고 스크래치패드에 직접 쓴 python 파서로 레코드 수를 셌다. 저장소
스크립트는 하나도 실행하지 않았다.

### 대조 결과 — 맞은 것

- 확보 11건이 전부 디스크에 실재한다. 보고된 커밋 해시 5건(cipr `d069c204`,
  redcode `c84b6db8`, bipia `a004b69e`, agentcanary `5072b782`, poisoned-skills
  zip md5)이 실물과 일치했다.
- 레코드 수도 일치했다. CIPR 640×3 · ipi_file 633 · ipi_web 284 · dpi 60,
  RedCode 1,410(py 27파일 810 + bash 20파일 600), BIPIA 코드공격 100(50+50),
  PoisonedSkills SKILL.md zip 1,070 / 디스크 1,069, AgentCanary 과제 md 484,
  DeepTrap 태스크 42 + zh 10 + 씬 54(42+12), MaliciousAgentSkillsBench 157행.
- 라이선스 파일 첫 줄도 보고와 일치했다(cipr = PolyForm NC 1.0.0,
  redcode 코드 MIT + `dataset/LICENSE` CC BY 4.0, bipia 들여쓰기된 MIT,
  agentcanary Apache-2.0, livepi CC BY 4.0 두 파일, deeptrap·inspect-evals·
  malicious-agent-skills-bench MIT, redteamcua·aishelljack Apache-2.0).
- `normalized/` 11개 YAML 전부 `yaml.safe_load` 통과.
- `.gitignore` 16행에 `dataset/raw/` 가 이미 있고 `git status` 상 `dataset/` 는
  통째로 미추적이다. 남의 저작물이 커밋에 섞이지 않는다.

### 대조 결과 — 틀려서 고친 것

전부 `comparison.md` 에 반영했다. 원인은 하나같이 "확보 전에 쓴 추정치가
확보 후에 갱신되지 않은 것" 이다.

- 상태 분포. `obtained` 3건 → 11건, 본표의 상태 열 8행을 `verified` 에서
  `obtained` 로 고쳤다.
- AgentCanary 28,092,505B → 28,270,158B. CIPR 126,443,136B → 127,363,137B
  (전자는 GitHub API blob 합, 후자가 작업 트리 실측). DeepTrap 6,399,500B →
  6,430,929B. RedTeamCUA 918파일 6,833,316B → 958파일 7,564,311B(뒤 단계가
  sparse 범위를 `mm_agents` 까지 넓혔다).
- RedCode "페이로드 1,350건" → 1,410건. 1,350 은 논문 시점 값이고 현재
  저장소는 bash 인덱스가 2개 늘었다.
- PoisonedSkills "SKILL.md 1,071개가 표준 스킬 포맷" → zip 1,070 / 디스크
  1,069 이고 5키 포맷을 다 갖춘 건 656건뿐이다.
- CIPR "`repos-selected-4lang-5each.csv` 에 base commit 까지 기록" → 그 CSV
  (41행)에는 커밋 열이 없다. 감사에서 직접 열어 헤더를 확인했다.
- BIPIA "파괴/유출/외부연결/지속성 라벨이 붙어 있다" → per-payload 라벨은
  없고 카테고리명 20개가 전부다.
- AgentCanary 상관분석 코드 "아직 미확인" → 실재 확인(`lib_tracee_grading.py`
  28,145B, `tracee_correlate.py` 53,020B).

### 세 숫자를 어떻게 셌나

- 발견 194 — 파이프라인이 검색 7건의 후보를 이름으로 접어 센 값이다. 이 감사가
  독립적으로 다시 세지 못했다. 디스크에 후보 목록 파일이 남아 있지 않고,
  `search-log.md` 어디에도 194 가 기록돼 있지 않다. 즉 이 하나만 전달값이다.
- 원출처 확인 42 — `verified.json` 을 `json.load` 해 `len()` 으로 셌다.
  중복 2쌍(AgentVigil, IPI-Proxy)을 접지 않은 값이고, 접으면 40이다.
- 확보 11 — `dataset/raw/` 밑 디렉터리를 센 값이며 11건 모두 실물을 확인했다.

