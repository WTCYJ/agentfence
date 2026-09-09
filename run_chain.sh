#!/bin/sh
# 서브에이전트 도구 분포까지 세는 체인 진단을 **세션과 분리해** 돌린다.
#
# `wsl ... -- bash -lc '...'` 로 인라인 실행하면 두 가지가 물린다.
#   ① Windows PATH 의 괄호·인용이 셸을 깨뜨린다 (실제로 세 번 당했다)
#   ② Claude Code 세션이 끝나면 프로세스가 같이 죽는다 —
#      30분 넘게 돌던 측정이 그렇게 날아갔다
#
# 스크립트 파일 + nohup 으로 둘 다 피한다.
#
#     wsl -d Ubuntu-24.04 -- sh ./run_chain.sh
set -e
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
export PYTHONIOENCODING=utf-8
# 출력 이름에 **실행 구분자**를 넣는다. `deny-chain5.out` 은 손으로 번호를
# 붙여 돌리던 시절의 숫자가 그대로 굳은 것이고, 그대로 두면 같은 축을 다시
# 돌릴 때 앞 판의 콘솔 기록을 덮는다 — 이 프로브는 JSON 에 행 배열만 남기므로
# .out 이 유일한 회차 이력인 경우가 많다.
mkdir -p run-log
OUT="run-log/$(date -u +%Y%m%dT%H%M%S)-deny-chain.out"
nohup python3 -u probe_deny_bash_chain.py 10 > "$OUT" 2>&1 &
echo "기동 pid=$!  -> $OUT"
