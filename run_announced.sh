#!/bin/sh
# 고지 경로(`agentfence-E-B1-write-outside-`)의 haiku·opus 재측정.
#
# 이 칸은 9월 23일 재측정에서 유일하게 안 잰 칸이다(옛 값 18/18, 원본부재).
# probes.yaml 의 pathcue-announced-others 블로커가 "probe_model_axis 로 재되,
# 접두사를 구 값으로 명시하라"고 적어 둔 그 측정이다.
#
# 예산: 남은 재측정 예산 안에서 돈다. 고지 경로는 실행이 억제될 수 있어
# (sonnet 27/30 거절) 비싼 모델의 재시도 상한을 낮춘다 — haiku n=10, opus n=7.
# opus 는 호출당 ~$0.15 이라 상한 3n=21 이 최악치를 $3.13 으로 묶는다.
#
#   sh run_announced.sh
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

DOLLAR_CAP="${DOLLAR_CAP:-3.6}"
STAMP="$(date -u +%Y%m%dT%H%M%S)"

echo "# 고지 경로 haiku·opus 재측정 · $VER · 달러 상한 \$$DOLLAR_CAP"
"${AGENTFENCE_CLAUDE:-claude}" --version 2>&1 | head -1
echo

spent() {
    python3 - "$STAMP" <<'PY'
import json, sys, glob
stamp = sys.argv[1]
tot = 0.0
for f in glob.glob(f"run-log/announced-{stamp}-*-ledger.jsonl"):
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

# 인자: 모델 · 유효목표 n · 예산 backstop(회차수). backstop 은 상한 3n 보다
# 크게 잡는다 — 관문이 회차 도중 트리면 프로브가 죽어 결과 파일을 못 쓴다.
# 실질 정지는 run_case 의 상한 3n 이다.
run_model() {
    model="$1"; ncap="$2"; backstop="$3"
    used="$(spent)"
    over="$(python3 -c "print(1 if float('$used') >= float('$DOLLAR_CAP') else 0)")"
    if [ "$over" = "1" ]; then
        echo "== [$model] 건너뜀 — 이미 \$$used 로 상한 \$$DOLLAR_CAP 도달"
        return 0
    fi
    rid="announced-${STAMP}-${model}-v${VER}"
    log="run-log/${STAMP}-announced-${model}-v${VER}.log"
    echo "== [$model] 시작 (n $ncap · backstop $backstop · 지금까지 \$$used) → $rid"
    AGENTFENCE_BUDGET="$backstop" AGENTFENCE_RUN_ID="$rid" \
        python3 probe_model_axis.py announced "$model" "$ncap" 2>&1 | tee "$log" \
        || echo "   [$model] 종료코드 $? (관문 정지 포함)"
    echo "== [$model] 끝 — 누적 \$$(spent)"
    echo
}

run_model haiku 10 35
run_model opus   7 25

echo "=== 전체 끝 — 총 \$$(spent) (상한 \$$DOLLAR_CAP) ==="
