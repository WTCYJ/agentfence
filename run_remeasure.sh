#!/bin/sh
# 세 재측정 대상을 한 번에 돌리되, 예산 상한을 구조로 지킨다.
#
# 관문(runner.budget_gate)은 장부 하나(run_id) 단위로만 상한을 건다. 이 스크립트는
# 그 위에 **전역 달러 상한**을 얹는다 — 프로브를 하나 돌릴 때마다 오늘 장부 전체의
# cost_usd 를 더해 보고, DOLLAR_CAP 을 넘겼으면 다음 프로브를 시작하지 않는다.
#
# 이렇게 하는 이유: run_case 는 유효 회차 n 을 채울 때까지 최대 3n 번 재시도한다.
# 무효율이 높은 팔(고지 경로 sonnet 은 ~35%)은 재시도가 많아 회차 수만으로는 비용을
# 못 맞춘다. 그래서 회차 상한(AGENTFENCE_BUDGET)과 달러 상한을 둘 다 건다.
#
#   sh run_remeasure.sh
set -e
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$HERE"

if [ -x "$HOME/node-v22.11.0-linux-x64/bin/node" ]; then
    PATH="$HOME/node-v22.11.0-linux-x64/bin:$PATH"; export PATH
fi
VER="${VER:-2.1.270}"
PINNED="$HERE/.versions/$VER/node_modules/.bin/claude"
[ -x "$PINNED" ] && { AGENTFENCE_CLAUDE="$PINNED"; export AGENTFENCE_CLAUDE; }
PYTHONIOENCODING=utf-8; export PYTHONIOENCODING
AGENTFENCE_TAG="v$VER"; export AGENTFENCE_TAG

DOLLAR_CAP="${DOLLAR_CAP:-16.0}"
STAMP="$(date -u +%Y%m%dT%H%M%S)"

echo "# 버전 고정: $VER · 달러 상한: \$$DOLLAR_CAP"
"${AGENTFENCE_CLAUDE:-claude}" --version 2>&1 | head -1
echo

# 오늘 태운 비용의 합을 장부에서 읽는다. run_remeasure 로 만든 장부만 센다.
spent() {
    python3 - "$STAMP" <<'PY'
import json, sys, glob
stamp = sys.argv[1]
tot = 0.0
for f in glob.glob(f"run-log/remeasure-{stamp}-*-ledger.jsonl"):
    for line in open(f, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            tot += json.loads(line).get("cost_usd") or 0
        except Exception:
            pass
print(f"{tot:.4f}")
PY
}

# 한 프로브를 돌린다. 먼저 전역 상한을 확인하고, 넘겼으면 건너뛴다.
# 인자: 라벨 · 회차상한(AGENTFENCE_BUDGET) · 명령...
run_probe() {
    label="$1"; cap="$2"; shift 2
    used="$(spent)"
    over="$(python3 -c "print(1 if float('$used') >= float('$DOLLAR_CAP') else 0)")"
    if [ "$over" = "1" ]; then
        echo "== [$label] 건너뜀 — 이미 \$$used 로 상한 \$$DOLLAR_CAP 도달"
        return 0
    fi
    rid="remeasure-${STAMP}-${label}-v${VER}"
    log="run-log/${STAMP}-${label}-v${VER}.log"
    echo "== [$label] 시작 (회차 상한 $cap · 지금까지 \$$used) → $rid"
    AGENTFENCE_BUDGET="$cap" AGENTFENCE_RUN_ID="$rid" \
        python3 "$@" 2>&1 | tee "$log" || echo "   [$label] 종료코드 $? (관문 정지 포함)"
    echo "== [$label] 끝 — 누적 \$$(spent)"
    echo
}

# 순서: 등록부가 지탱하는 것부터. 회차 상한은 유효 목표 + 재시도 여유다.
run_probe names-A   60  probe_hardening.py 41 names
run_probe names-BO  45  probe_hardening.py 15 haiku,opus
run_probe pathname  65  probe_path_naming.py
run_probe modelaxis 50  probe_model_axis.py
run_probe session   55  probe_session_consistency.py 12 4

echo "=== 전체 끝 — 총 \$$(spent) (상한 \$$DOLLAR_CAP) ==="
