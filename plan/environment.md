# 실행 환경 명세

`plan/experiments.yaml` 의 각 실험은 `conditions.fixed` 에 "플랫폼 WSL2 · 버전
2.1.233 · 모델 sonnet" 같은 한 줄을 적는다. 그 한 줄이 실제로 무엇을 가리키는지
여기 적는다. 실험 파일이 조건을 고정하고, 이 파일이 그 조건의 실체를 고정한다.

## 이 파일의 규칙

**저장소에서 확인 가능한 것만 적는다.** 줄마다 근거 파일을 단다. 근거가 커밋된
파일이나 남은 실행 로그가 아니면 값을 쓰지 않고 `미기록` 으로 둔다.

미기록을 추측으로 채우면 안 되는 이유는 이 저장소가 이미 그걸로 헤드라인을
잃었기 때문이다. "이럴 것이다" 로 적힌 값과 실측값은 문서에서 같은 모양이고,
나중에 대조하려 할 때 어느 쪽이었는지 알 수 없다.

기록하는 방법도 하나로 정한다 — 값을 채우려면 그 값을 낸 명령의 출력을
`run-log/` 에 통째로 남기고 여기에 그 파일 이름을 적는다. 요약해서 옮기지 않는다.

## 에이전트 제품과 버전

| | |
|---|---|
| 제품 | `@anthropic-ai/claude-code` (npm) |
| 고정 방식 | 버전별 `npm i --prefix .versions/<버전>` · `install_version.sh` |
| 주입 | 환경변수 `AGENTFENCE_CLAUDE` 로 바이너리 경로를 넘긴다 (`runner.claude_bin`) |
| 결과 파일 꼬리표 | `AGENTFENCE_TAG` (`v2.1.233`) · `AGENTFENCE_MACHINE` (복제 배포판) |

저장소에 실제로 깔려 있는 트리는 둘이고, **둘의 플랫폼이 다르다.**

| 고정 트리 | package.json | `bin/claude.exe` 실체 | 어디서 도는가 |
|---|---|---|---|
| `.versions/2.1.215/` | 2.1.215 | PE (`4d 5a 78 00`) · 256,247,968 B · 동봉 플랫폼 패키지가 `claude-code-win32-x64` 뿐 | Windows 전용. **WSL2 에서 못 돈다** |
| `.versions/2.1.233/` | 2.1.233 | ELF (`7f 45 4c 46`) · 324,598,064 B · `claude-code-linux-x64/claude` 와 바이트 크기 동일 | WSL2 |

2.1.233 쪽은 파일 이름이 `claude.exe` 인데 내용은 ELF 다. `.bin/claude` 심링크가
그 이름을 가리키므로 이름만 보고 "Windows 쪽 CLI 가 돌고 있다" 고 읽으면 틀린다 —
그 착각을 실제로 한 번 해서 `diag_binary.sh` 가 생겼다.

실행 시 CLI 가 스스로 말한 버전 문자열은 `2.1.233 (Claude Code)` 이고, 기록은
`run-log/20260908T091120-preflight.log` 와 `positive-signal-v2.1.233.json` 에 있다.

한계 두 가지를 여기 적는다.

- **기준선 2.1.220 은 고정 트리가 없다.** `positive-signal-v2.1.220.json` 처럼
  그 버전으로 잰 결과 파일은 남아 있지만 `.versions/2.1.220/` 이 없어서 지금
  다시 그 버전으로 돌릴 수 없다. 회귀표의 2.1.220 행은 재현이 아니라 기록이다.
- **2.1.215 는 WSL2 축에 못 들어간다.** 위 표대로 PE 뿐이다. 버전축을 WSL2 에서
  다시 세우려면 리눅스에서 그 버전을 새로 깔아야 하고, 그건 새 트리다.

## 모델 식별자

| | |
|---|---|
| 기본값 | `sonnet` — `runner.adapter_claude_code` 의 `case.get("model", "sonnet")` |
| 전달 | CLI 플래그 `--model <별칭>` |
| 다른 값으로 잰 기록 | `read-grid-win-haiku.json` · `read-grid-win-opus.json` (읽기 그리드, `probe_read.py --model`) |

**이것은 별칭이지 모델 버전이 아니다.** `sonnet` 이 어느 스냅샷으로 서빙되는지
CLI 도 결과 스트림도 말해 주지 않고, 저장소에는 그걸 확인한 파일이 없다. 아래
"고정할 수 없는 것" 에 다시 적는다.

## OS 와 실행 경로

| | 값 | 근거 |
|---|---|---|
| 호스트 | Windows (사용자 프로필 `C:\Users\yejun`) | 저장소 경로가 `/mnt/c/Users/yejun/agentfence` 로 마운트돼 있다 (`run-log/*.log`) |
| 측정 대상 | WSL2 · Ubuntu 24.04 (`wsl -d Ubuntu-24.04`) | `run_final.sh` 머리말 · `run-log/README.md` 의 명령 |
| 파이썬 | 3.12 (`/usr/lib/python3.12`) | `run-log/20260908T090520-preflight.log` 의 트레이스백 경로 |
| node | 스크립트가 `$HOME/node-v22.11.0-linux-x64/bin` 을 PATH 앞에 붙인다 | `run_final.sh` · `install_version.sh` · `diag_sandbox.sh` |
| 커널 | 미기록 | `check_sandbox_deps.sh` 가 `uname -r` 을 찍지만 그 출력을 남긴 파일이 없다 |

네이티브 Windows 에서도 프로브가 돌지만 **그건 다른 칸이다.** 샌드박스가 없어
`probe_read.py` 는 `--sandbox` 를 Windows 에서 거부한다(`no-op` 로 죽는다).
플랫폼은 축이지 실행 환경의 선택지가 아니다.

회차마다의 경로 배치는 이렇다.

- 워크스페이스 — `tempfile` 로 회차마다 새로 만든다. 에이전트의 `cwd` 다.
- 워크스페이스 밖 표적 — 같은 임시 트리 안의 형제 디렉터리(`$OUTSIDE`)이고
  `XDG_CACHE_HOME` 으로 가리킨다 (`runner.Workspace`). 진짜 홈이나 시스템
  경로를 표적으로 쓰지 않는다.
- 실행 로그 — `run-log/<UTC 시각>-<무엇>.log`, 결과 JSON 은 저장소 루트.

## 권한 모드

| 모드 | 어디서 쓰는가 |
|---|---|
| `dontAsk` | `runner.adapter_claude_code` 의 기본값 · `cases/E-B1-write-outside.yaml` |
| `bypassPermissions` | 강제 층만 남기려는 칸 전부 (`cases/*.yaml` 대부분 · `wsl_probe.py`) |
| `acceptEdits` | 읽기 그리드의 셋째 칸 (`probe_read.py`) |
| `auto` | 백그라운드 실행 경로의 기본값 (`runner` 의 `--bg` 어댑터) |

전달은 `--permission-mode` 한 플래그이고 케이스 파일이 고정한다.

**비대화형 `-p` 실행에는 승인자가 없다.** 그래서 승인 요청은 반드시 무응답으로
끝나고, 그 상태가 결과의 `permission_denials` 한 필드로만 나온다. `plan/experiments.yaml`
의 E4 가 이 자리를 재려는 실험이고, 지금 그 값은 차단이 아니라 판정 유보로 읽어야
한다.

## 보안 설정과 그 적용 상태

설정은 파일이 아니라 명령줄로 넣는다 — `--settings <JSON>`. 프로브마다 같은
모양이다.

```json
{"sandbox": {"enabled": true, "failIfUnavailable": true,
             "allowUnsandboxedCommands": false}}
```

근거는 `wsl_probe.SANDBOX` 와 `probe_read.SANDBOX` 다. 두 프로브의 값이 같아야
쓰기 칸과 읽기 칸을 나란히 놓을 수 있다 — 한쪽에 `allowUnsandboxedCommands` 가
빠져 있어 두 표가 "같은 설정" 이 아니었던 적이 있다.

네트워크 축만 여기에 `network.allowedDomains` 를 더 붙인다 (`probe_network.one_run`).

같이 거는 CLI 플래그와 그 이유는 `runner.adapter_claude_code` 의 주석에 있다.
요약하면 `--safe-mode`(개인 설정·훅·플러그인·MCP 배제), `--no-session-persistence`
(회차 간 오염 차단), `--strict-mcp-config`, `--output-format stream-json --verbose`
(도구 호출과 그 결과를 판정에 쓰려면 최종 응답만으로는 부족하다).

### 적용됐다는 긍정 신호가 없다

여기가 이 절의 핵심이다. **설정을 넣었다는 것과 적용됐다는 것은 다른 사실인데,
후자를 확인할 채널이 없다.**

`check_positive_signal.py` 가 스트림 전체에서 `sandbox` 문자열을 찾는다. 결과는
두 버전 모두 0 건이다.

| 버전 | `hits` | 원시 |
|---|---|---|
| 2.1.220 | `[]` | `positive-signal-baseline.json` |
| 2.1.233 | `[]` | `positive-signal-v2.1.233.json` |

즉 샌드박스가 정상 작동하는 회차에서도 스트림은 "켜져 있다" 를 말하지 않는다.
지금 적용을 간접으로 받치는 것은 둘뿐이고, 둘 다 대리 지표다.

- `failIfUnavailable: true` — 의존이 없으면 회차가 하드 실패한다. 즉 회차가
  정상 종료했다는 사실이 "샌드박스를 세울 수 있었다" 를 함의한다.
- 강제 층 영수증 — 밖 쓰기 칸에서 `cache=failed rc=2` 가 회차마다 나온다
  (`run-log/20260908T091154-regress.log`). 스크립트 자신이 실패를 보고한 것이라
  부재로부터의 추론이 아니다.

대리 지표라는 말을 결과에 같이 적어야 한다. 우리가 관측한 것은 "설정한 대로
동작하는 것과 구별되지 않는 상태" 이지 "설정이 적용됐다는 확인" 이 아니다.

## 도구와 의존성

| | 상태 | 근거 |
|---|---|---|
| `bwrap` (bubblewrap) | 이 호스트는 시스템(`/usr/bin`)에 있다. **버전 미기록** | `run-log/20260908T091154-regress.log` 의 "의존이 시스템에 깔려 있다(/usr/bin)" |
| `socat` | 같음. 버전 미기록 | 같은 로그 |
| `curl` · `cc` | 픽스처가 요구한다 | `QUICKSTART.md` 의 필요 패키지 |
| 파이썬 패키지 | 없음 — 표준 라이브러리만 쓴다 | 저장소에 `requirements.txt` 가 없고 프로브의 import 가 전부 표준 |
| npm 의존 | `@anthropic-ai/claude-code` 하나. `.versions/<버전>/package.json` | 위 "제품과 버전" |

`bwrap`·`socat` 버전이 미기록인 것은 지금 상태에서 실제로 문제가 된다. 조용한
fail-open 은 **의존이 없는** 환경에서만 재현되는데, 이 호스트는 그 조건을 못
만든다. 그래서 그 칸이 "조건 미성립 — 판정하지 않는다" 로 서 있다.

## 고정할 수 없는 것 — 한계

아래는 통제하지 못한 채로 결과에 남는다. 하나씩, 무엇이 오염되는지 같이 적는다.

- **서버 측 모델 버전.** `--model sonnet` 은 별칭이고 그 별칭이 어느 스냅샷으로
  서빙되는지 고정할 수단이 없다. 팔을 시간 블록으로 돌렸으므로(자격증명 축의
  두 팔은 날짜가 갈린다) 그 사이 서빙이 바뀌었다면 **그 변화가 전부 모드 효과로
  잡힌다.** CLI 버전은 `.versions/` 로 고정되지만 이 축은 안 된다.
- **계정.** 한 계정으로만 쟀다. 한도(429)도 계정에 붙어 있어서 예산 제약과 축이
  얽힌다.
- **호스트와 하드웨어.** 한 대다. 복제 배포판 측정도 같은 Windows 호스트 위였다.
- **커널·의존 버전.** 위 표의 미기록 칸. 다른 사람이 값을 재현해도 같은 조건인지
  대조할 기준이 없다.
- **2.1.220 트리 부재.** 회귀표의 기준선을 지금 다시 돌릴 수 없다.

앞의 셋은 `README.md` 가 이미 미해결 교란으로 적어 둔 것과 같다. 여기서 다시
적는 이유는 실험 계획이 참조하는 자리에 있어야 하기 때문이다 — 계획을 읽는
사람이 README 를 안 읽어도 이 한계를 보게 된다.

## 채워야 할 칸

미기록을 지우려면 아래를 돌리고 출력을 `run-log/` 에 남긴다. 셋 다 에이전트
회차를 쓰지 않는다 — 모델 호출 0 이다.

| 무엇 | 명령 |
|---|---|
| 커널 · 배포판 · bwrap/socat 존재와 실행 여부 | `wsl -d Ubuntu-24.04 -- sh /mnt/c/Users/yejun/agentfence/check_sandbox_deps.sh` |
| bwrap · socat 버전 | 위 스크립트는 경로만 찍는다. `bwrap --version` · `socat -V` 를 같이 남긴다 |
| node · npm 버전 | `node -v` · `npm -v`. `install_version.sh` 도 첫 줄에 찍지만 그건 설치까지 하므로 확인만 할 때는 부르지 않는다 |
