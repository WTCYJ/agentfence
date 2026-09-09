# 최종 측정 기록

이 폴더는 측정을 돌린 기록을 그대로 쌓는다. 요약하지 않고, 실패한 실행도 지우지
않는다. 실패 기록을 지우면 "왜 이 칸이 비어 있는가"에 답할 수 없게 된다.

파일 이름은 `<시각>-<무엇>.log` 이고 시각은 실행을 시작한 때다.

## 돌리는 법

로그인 상태부터 확인한다. 이 문이 없으면 만료된 세션으로 60회를 돌리고 전부
무효를 결과 0 으로 착각하게 된다.

    wsl -d Ubuntu-24.04 -- sh /mnt/c/Users/yejun/agentfence/run_final.sh preflight

통과하면 두 가지를 돌린다. 둘 다 중간에 끊겨도 앞 회차가 남고, 같은 명령을 다시
부르면 이어 돈다.

    wsl -d Ubuntu-24.04 -- sh /mnt/c/Users/yejun/agentfence/run_final.sh regress
    wsl -d Ubuntu-24.04 -- sh /mnt/c/Users/yejun/agentfence/run_final.sh proxy

## 이번에 재려는 것

| 항목 | 지금 값 | 목표 | 왜 |
|---|---|---|---|
| 파일 쓰기 차단 (2.1.233) | 10회 중 0회 | 60회까지 쌓기 | 값의 폭이 0.28 에서 0.06 으로 좁아진다 |
| 접속 경로 실험 | 서로 다른 스크립트에서 나온 두 줄 | 한 스크립트 2x2 | 지금 비교는 조건이 하나만 다른 것이 아니다 |

위 `regress` 는 `VER` 기본값이 2.1.233 이라 2.1.233 칸에 쌓인다. 회귀표
왼쪽의 2.1.220 기준선 칸(0/30 · 상한 0.11)은 다른 칸이고 `.versions/2.1.220/`
이 없어 지금 못 돈다 — `remeasure.yaml` 의 `baseline-2.1.220` 을 보라.


## 기록에 남겨야 할 것

- 실행한 명령과 시각
- 고정한 버전과 실제 바이너리 경로
- 표준 출력 전체 (요약하지 않는다)
- 만들어진 결과 파일 이름
- 중간에 끊겼으면 어디서 왜 끊겼는지

## 로그인이 필요할 때

세션이 만료되면 preflight 가 `OAuth session expired` 로 막는다. 아래를 사람이
직접 실행해 로그인한다.

    wsl -d Ubuntu-24.04
    export PATH=$HOME/node-v22.11.0-linux-x64/bin:$PATH
    /mnt/c/Users/yejun/agentfence/.versions/2.1.233/node_modules/.bin/claude

실행하면 대화형 화면이 뜨고 `/login` 으로 로그인한다. 끝나면 preflight 를 다시
돌려 통과하는지 본다.
