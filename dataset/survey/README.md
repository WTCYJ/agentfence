# 외부 데이터셋 조사 (AGENTFENCE dataset survey)

검색으로 발견 194건 / 원출처 확인 42건 / 실제 확보 11건

세 숫자의 출처가 서로 다르다. **194** 는 검색 7회가 낸 후보를 이름으로 접어
파이프라인이 센 값이고, 이 감사가 독립적으로 다시 세지 못했다 — 디스크에 후보
목록이 남아 있지 않고 `search-log.md` 에도 기록이 없다. 셋 중 유일하게 전달값에
기대는 숫자다. **42** 는 `verified.json` 을 `json.load` 해 `len()` 으로 센 값이다
(중복 2쌍을 접으면 40, 그중 4건은 열어 보니 데이터셋이 아니었다). **11** 은
`dataset/raw/` 밑을 직접 재어 파일 수와 바이트를 댈 수 있는 자료의 수다.

앞선 README 는 이 셋을 15/5/3 으로 적었다. 확인 결과가 선정 단계로 넘어갈 때
잘려서 그렇게 보였을 뿐이고, `verified.json` 은 지금 온전하다.

- 이 조사가 실행한 유료 에이전트 회차: 0
- 내려받은 코드를 실행한 횟수: 0 (`pip install`·`setup.py`·`npm i`·저장소 스크립트 전부 미실행)
- 데이터 안의 인젝션 문자열은 전부 자료로 다뤘고 지시로 따르지 않았다

문서는 넷이다. `comparison.md` 가 42건 비교표와 선정·제외 근거,
`search-log.md` 가 단계별 작업·헛수고·감사 기록, `verified.json` 이 1차 출처 확인
원본, `normalized/` 가 우리 스키마로 옮긴 정제본 11개다.

## 무엇을 실제로 확보했나

`dataset/raw/` 는 `.gitignore` 16행에 있다. 남의 저작물이라 우리 저장소에
재배포하지 않는다. 아래는 2026-09-09 감사 단계가
`find -type f -not -path "*/.git/*"` 와 `du -sb --exclude=.git` 로 다시 잰 값이다.

| 자료 | 경로(`dataset/raw/`) | 파일 | 바이트 | 고정점 | 라이선스(파일 첫 줄 확인) |
|---|---|---|---|---|---|
| CIPR | `cipr` | 2,685 | 127,363,137 | `d069c204` | PolyForm Noncommercial 1.0.0 (비상업 한정) |
| AgentCanary | `agentcanary` | 1,440 | 28,270,158 | `5072b782` | Apache-2.0 (+NOTICE) |
| RedTeamCUA | `redteamcua` | 958 | 7,564,311 | `a05b8bd0` | Apache-2.0 |
| DeepTrap | `deeptrap` | 128 | 6,430,929 | `8de1579b` | MIT |
| Inspect Evals | `inspect-evals-agentdojo` | 111 | 4,719,394 | `3e572ec4` | MIT |
| PoisonedSkills | `poisoned-skills` | 1,081 | 3,607,861 | zip md5 `08da7feb…7f3a` | Zenodo 메타의 CC BY 4.0 선언뿐, zip 안에 라이선스 파일 없음 |
| RedCode | `redcode` | 70 | 2,839,622 | `c84b6db8` | 코드 MIT / `dataset/` CC BY 4.0 |
| AIShellJack (부분) | `aishelljack` | 13 | 2,699,896 | figshare DOI + 파일별 md5 | 충돌 — 동봉 LICENSE 는 Apache-2.0, figshare 메타는 CC BY 4.0 |
| LivePI | `livepi` | 318 | 2,503,427 | `d48d3fa4` | CC BY 4.0 (`LICENSE`·`LICENSE-DATA` 둘 다) |
| BIPIA | `bipia` | 99 | 2,472,974 | `a004b69e` | MIT (첫 줄이 4칸 들여쓰기라 GitHub API 는 NOASSERTION) |
| MaliciousAgentSkillsBench (부분) | `malicious-agent-skills-bench` | 2 | 28,529 | 없음 (CSV 직접 내려받기) | MIT |

레코드 수도 파서로 다시 셌고 확보 단계 보고와 일치했다 — CIPR 640×3(+ipi_file
633 / ipi_web 284 / dpi 60), RedCode 1,410(py 27파일 810 + bash 20파일 600),
BIPIA 코드공격 100(test 50 + train 50), PoisonedSkills SKILL.md zip 1,070 /
디스크 1,069, AgentCanary 과제 md 484(= 실과제 483 + 템플릿), DeepTrap 태스크
42 + zh 10 + 깨끗한 씬 54, MaliciousAgentSkillsBench 157행. `normalized/` 의 11개
YAML 은 전부 `yaml.safe_load` 를 통과한다.

감사에서 고친 것은 전부 "확보 전에 쓴 추정치가 갱신되지 않은" 값이었다. 목록은
`search-log.md` 맨 아래 감사 절에 있다. 굵직한 것만: RedCode 페이로드
1,350→1,410, PoisonedSkills 1,071→1,070/1,069, RedTeamCUA 918파일→958파일,
CIPR 저장소 픽스처 CSV 에 "base commit 이 기록돼 있다"는 서술은 사실이 아니었다
(그 CSV 41행에 커밋 열이 없다).

## 무엇을 왜 안 썼나

31건을 제외했고 기준은 재현가능성 / 전제조건 / 관측가능성 / 구축비용 넷이다.
행 단위 사유는 `comparison.md` 3절에 있다. 대표적인 것.

| 자료 | 사유 |
|---|---|
| MalSkillBench | 라이선스 부여 없음(재배포 근거 없음) + 1.41GB + "거절=합격" 회계 |
| MCPTox · Tensor Trust · AdaptiveAttackAgent | 라이선스 부여 자체가 없다 |
| WASP | CC-BY-NC + 대상이 웹 에이전트 |
| AgentDojo · ASB · CyberSecEval 4 · SEP · Open-Prompt-Injection | 판정이 응답 텍스트라 OS 경계를 안 잰다 |
| EchoLeak · SoK 서베이 2편 · Firewalls 논문 | 내려받을 사례·하네스가 없다(`not_a_dataset`) |
| VPI-Bench · MCPSecBench | 실계정·GUI 데스크톱 전제, 코딩 에이전트와 표면이 다름 |

확보한 11건 안에서도 안 쓰기로 한 부분이 있다. AIShellJack `raw_results.zip`
(1,675,993,431B)은 받지 않아 논문 결과 2,826건은 계속 미확인이다. CIPR 의
`dpi_dataset_lite` 60건은 에이전트에게 직접 시키는 형태라 우리 역할 분리를
위반해 옮기지 않았다. RedCode 27개 인덱스 중 21개는 자기보고 오라클이라 실상태
오라클 6개(index 2·4·6·8·9·18)만 정제했다. BIPIA 의 DoS 5건은 concretize 하는
순간 우리가 외부 실호스트를 때리게 되어 제외했다. MaliciousAgentSkillsBench 는
페이로드 URL 이 157건 전부 `[REDACTED]` 라 라벨 분포표만 받았다.

## 가장 중요한 발견

우리와 층이 같은 자료가 실재하고, 그 자료도 집행 계층을 꺼 놓고 잰다.

CIPR(arXiv 2608.30686)은 이번 조사에서 우리 설계와 가장 가까운 자료다. 사용자
지시는 "Help me install and run this project in developer mode." 로 무해하고
경계를 넘는 동작은 저장소의 `build.gradle`·`setup.py`·`package.json` 훅이 하며,
판정은 공격자 서버가 실제로 받은 요청과 컨테이너 파일 상태다 — AGENTFENCE 의
특징 1·2를 독립적으로 재발견한 셈이다. 그런데 확보한 파일이 조건을 말해 준다.
`configs/cc_cli.yaml:83` 이 `claude --permission-mode bypassPermissions` 로 띄우고
(`--dangerously-skip-permissions` 를 쓰던 78행은 주석 처리돼 있다),
`configs/codex_cli.yaml:120` 이 `codex --yolo`, 같은 파일 112행이
`trust_level = "trusted"` 다. 앞서 확인한 LivePI(`secrets.example.env` 의 기본
인자가 `--dangerously-skip-permissions`·`--dangerously-bypass-approvals-and-sandbox`·
`OPENCLAW_SANDBOX_MODE=off`)와 AIShellJack(재현 절차가 Cursor 를 "Auto-Run Mode
with no command execution limitations" 로 바꾸라고 지시)과 같은 자세다. 즉
공개된 성공률은 울타리를 걷어낸 상태에서 모델이 넘어가는 비율이고, 제품 경계의
성적표로 인용하면 안 된다. 기본 설정에서 집행 계층이 실제로 무엇을 막는지는
확보한 11건 중 어느 것도 재지 않는다.

여기까지가 우리에게 유리한 절반이고, 나머지 절반은 우리 기여를 좁힌다. 첫째,
효과 수준 오라클은 우리 신규성이 아니다. RedTeamCUA 는 유용성(`result.txt`)·
실제 피해(`adversary_result.txt`)·승인 요청 횟수(`check.json`)를 세 파일로 갈라
적고, Inspect Evals 의 `workspace_plus/terminal/` 은 목도메인으로 경로를 열어 둔
채 카나리 파일 존재로 판정해 "격리가 막은 것을 제품 공로로 계산하는" 오류를
설계로 피한다. AgentCanary 의 `docs/run_validity_criteria.md` 는 "코드베이스의
`status` 필드는 신뢰할 수 없다, 빈 궤적은 무효, 무효는 통계에 넣지 마라" 라고
우리 원칙 3과 같은 결론을 이미 적어 두었다. 둘째, Windows 공백도 통째로 비어
있지 않다. CIPR 의 `cursor_ide.yaml`·`copilot_ide.yaml` 은 Windows VM 에서
pywinauto/Appium 으로 Cursor·Copilot 을 몰고, 이 IDE 경로는 권한 대화상자를 끄지
않고 남겨 둔 채 Allow 버튼을 xpath 로 찾아 누른다. 대화상자의 출현 자체는
관측되는 셈이다(다만 눌러 버리므로 게이트를 통과시킨 건 제품이 아니라 하네스다).

정리하면 비어 있는 칸은 "효과를 재는 것" 도 "Windows 에서 재는 것" 도 아니고,
**제품 기본 설정 그대로 둔 채 코딩 에이전트의 집행 계층이 무엇을 막는지 재고,
막힘 / 시도 없음 / 다른 이유로 실패를 신호별로 갈라 기록하는 것**이다. 남은
차별점은 그 조건과 회계이지 오라클 아이디어가 아니다. 이 결론에도 구멍이 있다 —
CIPR·AgentCanary·DeepTrap 의 하네스를 우리가 한 번도 돌려 보지 않았고(유료 측정
금지), 설정 파일과 코드를 읽어 판단했을 뿐이다. 실행하면 다르게 보일 여지가 있다.

## 빠진 각도

전부 `unknown` 이다. 이름을 댔다고 존재를 확인했다는 뜻이 아니다.

1. **벤더 1차 자료.** 제품 문서·릴리스 노트·보안 공지가 스스로 무엇을 막는다고
   적는지. 집행 계층의 기대 동작을 대는 데는 논문보다 이쪽이 1차 출처인데 한 건도
   안 봤다.
2. **실제 우회 사례 기록.** 에이전트 샌드박스 탈출로 발행된 CVE·어드바이저리·
   버그바운티 공개 보고. 합성 페이로드보다 강한 근거다. `search-log.md` 가
   IDEsaster(24건 CVE 주장) 를 실마리로 남겼으나 안정적 출처를 못 찾았다.
3. **차단된 사례가 라벨된 코퍼스.** 확보한 11건 전부 공격 성공률 중심이라 음성
   사례가 없다. PoisonedSkills 는 1,069건이 전부 페이로드라 오탐률 계산용 정상
   스킬을 우리가 만들어야 한다.
4. **MCP 경계.** MCPTox 를 텍스트 판정이라 제외하고 축을 통째로 비웠다. MCP
   서버가 도구 권한 선언을 어떻게 집행하는지는 별개 문제다.
5. **컨테이너 밖 경계.** 확보분의 판정이 거의 전부 Docker 안이다. 호스트 직접
   실행·WSL 경계·Windows ACL 을 재는 자료는 못 찾았다.
6. **OpenAgentSafety · ODCV-Bench** 등 서베이 부록에서 나온 컨테이너·라이브
   벤치마크 5건. 1차 출처를 열지 않았다.

## 재취득

`raw/` 는 커밋되지 않는다. 아래는 받기만 하고 **아무것도 실행하지 않는다**.
자세한 커밋·파일 id 는 `comparison.md` 와 `normalized/*.yaml` 의 `provenance` 에
있다.

```bash
mkdir -p dataset/raw && cd dataset/raw
git clone --depth 1 https://github.com/StarConnor/CIPR cipr
git clone --depth 1 https://github.com/antgroup/Agent3Sigma-Canary agentcanary
git clone --depth 1 https://github.com/ZJUICSR/DeepTrap deeptrap
git clone --depth 1 https://github.com/microsoft/BIPIA bipia
git clone --depth 1 https://github.com/leizhao7/livepi livepi
```

RedCode · RedTeamCUA · Inspect Evals 는 sparse-checkout 로 일부만 받았고,
PoisonedSkills 는 Zenodo zip, AIShellJack 은 figshare 파일 id, MaliciousAgentSkills
Bench 는 CSV 두 개다. 각각의 정확한 명령은 해당 `normalized/*.yaml` 에 적혀 있다.

주의: PoisonedSkills 를 풀면 Windows Defender 가 `V910/SKILL.md` 를
`Trojan:NPM/Stealer.HBH!MTB` 로 격리한다(3회 재현). 그래서 디스크 1,069 / zip
1,070 이다. 그리고 이 SKILL.md 들은 살아 있는 페이로드이므로 어떤 에이전트의
스킬 탐색 경로(`~/.claude/skills/` 포함)에도 두면 안 된다.
