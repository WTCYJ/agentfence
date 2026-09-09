#!/bin/sh
# run_chain.sh 가 띄운 로그가 완성될 때까지 기다렸다가 읽는다.
# 완료 표지는 프로브가 마지막에 찍는 파일명이다.
#
#     sh ./wait_chain.sh [로그파일]      안 주면 가장 최근 것
#
# 파일명을 박아 두면 run_chain.sh 와 **두 파일이 함께 굳는다.** 실제로 그랬다.
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
F="${1:-$(ls -t run-log/*-deny-chain.out 2>/dev/null | head -1)}"
[ -n "$F" ] || { echo "로그가 없다 — run_chain.sh 를 먼저 띄운다"; exit 2; }
echo "지켜보는 로그: $F"
i=0
while [ $i -lt 200 ]; do
    if grep -q "deny-bash-chain.json" "$F" 2>/dev/null; then
        echo "=== 완료 ==="
        break
    fi
    if ! pgrep -f probe_deny_bash_chain.py > /dev/null 2>&1; then
        echo "=== 프로세스 없음 (죽었거나 끝남) ==="
        break
    fi
    i=$((i + 1))
    sleep 20
done
tail -28 "$F"
