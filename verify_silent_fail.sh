#!/bin/sh
# 복제 배포판에서 제보 전 검증을 돌린다.
#
# 인라인 셸은 Windows PATH 의 괄호에서 깨진다 — 스크립트 파일로 넘긴다.
#
#     wsl -d Ubuntu -- sh ./verify_silent_fail.sh
set -e
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PATH="$HOME/bwrap-local/usr/bin:$PATH"
export PATH
LD_LIBRARY_PATH="$(ls -d "$HOME"/bwrap-local/usr/lib/*-linux-gnu 2>/dev/null | tr '\n' ':')${LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
# **이미 걸려 있으면 존중한다.** 무조건 덮어쓰던 동안, 고정 버전을 걸고
# 이 스크립트를 불러도 재는 것은 전역 설치였고 결과 파일 이름만
# AGENTFENCE_TAG 를 따랐다 — 이름과 내용이 다른 버전일 수 있었다.
: "${AGENTFENCE_CLAUDE:=$HOME/node-v22.11.0-linux-x64/bin/claude}"
export AGENTFENCE_CLAUDE
PYTHONIOENCODING=utf-8
export PYTHONIOENCODING
echo "기준: bwrap=$(command -v bwrap) socat=$(command -v socat)"
exec python3 verify_silent_fail.py
