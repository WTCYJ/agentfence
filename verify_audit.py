"""감사가 지적한 수치를 직접 재계산한다. 감사도 틀릴 수 있다.

2026-09-10 정정 — 아래 A10 절과 2x3 절이 다루는 다섯 값
(`29/82` · `18/18` · `30/30` · `20/21` · 그 합 `50/51`)은 **원시 파일이
없다.** 디스크 전역과 git 이력 전수에서 `modelaxis-*.json` ·
`pathnaming-*.json` 이 0 건이고 한 번도 커밋된 적이 없다. 그래서 게시
문서(README 3절)에서 **검증 가능한 원본 부재로 제외**됐다.

이 스크립트가 하는 것은 **인쇄된 2x2 의 산술 재계산까지**다. k/n 자체를
원시에서 다시 세는 것이 아니다 — 셀 원시가 없다. 여기 나오는 p 를 근거로
결론을 세우지 마라. 추적 사슬과 재측정 명령은 `remeasure.yaml` 의
`pathcue-*` 일곱 항목에 있다.
"""
import json

import read_table as R
from classify_refusals import fisher, wilson

print("=== A6 · 윌슨 상한 ===")
for k, n in [(0, 10), (0, 30), (0, 100)]:
    print(f"  wilson({k},{n}) 상한 = {wilson(k, n)[1]:.4f}")

print("\n=== A4 · 내장 Read 의 밖 표적 시도/거부 (dontAsk + acceptEdits) ===")
for tag in ["win", "wsl"]:
    tries = dens = 0
    for line in open(f"read-raw-{tag}.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if r["mode"] not in ("dontAsk", "acceptEdits") or r["status"] != "ok":
            continue
        for a in r["attempts"]:
            if a["tool"] != "Read":
                continue
            if R.targets_outside("Read", a["input"]):
                tries += 1
                dens += a["denied"]
    print(f"  {tag}: 시도 {tries} · 거부 {dens}")

print("\n=== A0 · MIN_VALID 게이트가 A팔을 무효로 만드는가 ===")
n, valid = 10, 7
print(f"  len(valid)={valid} < n*MIN_VALID={n * 0.7} ?  -> {valid < n * 0.7}")
print("  (False 이면 INVALID 가 아니다 — 감사의 해당 주장은 틀렸다)")

print("\n=== A10 · 고지 경로 조건 sonnet 통합 (원시 파일 없음 · 제외됨) ===")
sess = [(12, 27), (10, 25), (7, 30)]
k, m = sum(a for a, _ in sess), sum(b for _, b in sess)
lo, hi = wilson(k, m)
# "검증 가능한" 이었다 — 세 판 모두 원시가 없다는 것이 2026-09-10 에 확인됐다.
print(f"  3세션 통합 {k}/{m} = {k / m:.3f} [{lo:.2f}, {hi:.2f}] (원시 파일 없음)")
print(f"  세션 내역: {sess}")
lo2, hi2 = wilson(30, 30)
print(f"  중립 경로 통합 30/30 = 1.000 [{lo2:.2f}, {hi2:.2f}] (원시 파일 없음)")
print(f"  구간 분리: {hi < lo2}")

print("\n=== 2x3 설계 · 정확검정 (네 칸 모두 원시 파일 없음 · 제외됨) ===")

# 경로 효과 (sonnet): 고지 29/82 vs 중립 30/30
print(f"  경로 효과  sonnet 29/82 vs 30/30   p = {fisher(29, 53, 30, 0):.3e}")
# 모델 효과, 고지 경로: sonnet 29/82 vs haiku+opus 18/18
print(f"  모델 효과(고지)  29/82 vs 18/18     p = {fisher(29, 53, 18, 0):.3e}")
# 모델 효과, 중립 경로. sonnet 중립은 **세 세션 통합 30/30** 이다 — 바로 위에서
# 그렇게 인쇄하고, 경로 효과 줄도 29/82 대 30/30 으로 계산한다. 10/10 은 통합
# 전의 한 세션 값이라, 여기서 나온 p = 1.000 이 README 2x3 표에 그대로 실렸다.
# 표가 인쇄하는 두 칸(30/30 · 20/21)의 Fisher 는 0.412 다.
print(f"  모델 효과(중립)  30/30 vs 20/21     p = {fisher(30, 0, 20, 1):.3f}")
