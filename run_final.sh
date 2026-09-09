#!/bin/sh
# 최종 측정을 한 번에 돌리고 전부 기록한다.
#
# `wsl -- sh -c "..."` 로 여러 줄을 넘기면 인용이 깨진다. 이 저장소가 이미 겪은
# 문제라 셸 조각을 넘기지 않고 파일로 둔다.
#
#     wsl -d Ubuntu-24.04 -- sh /mnt/c/Users/yejun/agentfence/run_final.sh preflight
#     wsl -d Ubuntu-24.04 -- sh /mnt/c/Users/yejun/agentfence/run_final.sh regress
#     wsl -d Ubuntu-24.04 -- sh /mnt/c/Users/yejun/agentfence/run_final.sh proxy
set -e
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$HERE"

# 노드와 고정 버전. PATH 에 claude 가 없으면 프로브가 첫 줄에서 죽는다.
if [ -x "$HOME/node-v22.11.0-linux-x64/bin/node" ]; then
    PATH="$HOME/node-v22.11.0-linux-x64/bin:$PATH"
    export PATH
fi
VER="${VER:-2.1.233}"
PINNED="$HERE/.versions/$VER/node_modules/.bin/claude"
if [ -x "$PINNED" ]; then
    AGENTFENCE_CLAUDE="$PINNED"
    export AGENTFENCE_CLAUDE
fi
PYTHONIOENCODING=utf-8
export PYTHONIOENCODING

echo "# 버전 고정: $VER"
echo "# 바이너리: ${AGENTFENCE_CLAUDE:-(PATH 의 claude)}"
"${AGENTFENCE_CLAUDE:-claude}" --version 2>&1 | head -1
echo

case "$1" in
preflight)
    # 측정 가능 여부를 한 회차로 판별한다. 로그인 안 됨과 한도 초과를 가른다.
    python3 preflight.py
    ;;
regress)
    # 헤드라인 칸을 60 회까지 누적한다. 한도에 걸려도 앞 샤드가 남고
    # 같은 명령을 다시 부르면 이어 돈다.
    sh ./run_regression.sh "$VER"
    ;;
proxy)
    # 프록시 축 2x2. 한 스크립트 안에서 조건만 바꾼 대비다.
    # 12 = 하중 12x2 + 게이트 5x2 = 34 회차. remeasure.yaml 의 proxy-axis-2x2
    # 가 적은 cost_runs 와 같은 값이다 — 기본값이 30 이던 동안 이 갈래는
    # 등록부 견적의 2.4 배(80 회차)를 썼다.
    python3 probe_proxy.py "${N:-12}" axis
    ;;
*)
    echo "쓰임: run_final.sh {preflight|regress|proxy}" >&2
    exit 2
    ;;
esac
