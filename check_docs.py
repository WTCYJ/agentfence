"""문서에 적힌 숫자가 실제 계산과 맞는가.

이 저장소가 반복해서 낸 실패는 **측정이 틀린 것이 아니라 표기가 측정과 어긋난
것**이다. 그중 둘은 한동안 게시된 채로 있었다.

    0/10 의 상한을 0.26 으로 인쇄  (윌슨은 0.278. Clopper-Pearson 값이 섞였다)
    dontAsk 칸을 `perm`+`enf` 로 표기  (실제로는 경쟁이고 25:5 다)

둘 다 사람이 눈으로 잡았다. 자기식별 누출을 selftest 어서션으로 막은 것과 같은
이유로, 이것도 검사로 막는다.

여덟 가지를 본다.

    1. `k/n` 옆에 붙은 95% 구간이 wilson(k, n) 과 맞는가   (문서 내부 정합)
    2. 층 분해(`perm A · enf B`)의 합이 그 행의 n 과 맞는가 (문서 내부 정합)
    3. 하중을 지는 표의 k/n 이 **원시 측정 파일**과 맞는가  (문서 <-> 데이터)
       회귀표 행은 **구간까지** 요구한다 — n 없는 「회귀 없음」은 문장일 뿐이다
    4. `p = …` 가 근거로 적힌 2x2 의 Fisher 와 맞는가       (문서 내부 정합)
    5. 절 안의 **통합값**이 원시 판들의 합인가              (문서 <-> 데이터)
       표의 「통합」 행은 위 팔 행들의 합인가                (문서 내부 정합)
    6. 네 문서가 같은 칸을 **같은 분수**로 게시하는가        (문서 <-> 문서)
    7. 새 결과 파일 이름에 **실행 구분자**가 있는가          (코드)
    8. 철회한 값이 아직 결과처럼 서 있지 않은가             (등록부 <-> 문서)
       `remeasure.yaml` 의 `backed: null` 항목이 오라클이다

3 이 없으면 1·2 는 "틀린 숫자가 자기 자신과는 일관된" 경우를 통과시킨다.

8 은 3·5·6 이 **못 닿는 자리**를 본다. 그 셋은 문서의 값을 원시 파일에 묶는데,
원시가 아예 없는 값은 묶을 대상이 없어 검사 밖에 있었다. 그런 값의 철회는 여태
산문 한 줄이었고 **표는 그대로 남았다** — 인용하는 사람은 표를 본다.

5·6·7 은 감사가 뚫고 들어온 세 자리다. 3 은 파일 하나의
`{violations}/{valid}` 가 절에 있는지만 봐서, 같은 절의 통합값(5)도 옆 문서의
같은 칸(6)도 안 봤다. 7 은 데이터가 아니라 **데이터가 생기는 자리**를 본다 —
고정 이름이 팔 셋을 서로 덮어 한 절의 원시가 통째로 사라진 적이 있다.

4 는 3 **위에** 얹힌다. p 를 묶는 대상은 문서 안의 k/n 이고, 그 k/n 이 측정과
맞는지는 3 의 일이다. 3 이 안 덮는 표의 p 는 "옮겨 적다 틀린 것은 잡히지만
숫자의 출처는 미확인" 이다. 이 경계를 흐리면 안 된다.

**p 표기 규칙** — 4 는 이것을 전제로만 성립한다.

    (1) 모든 p 는 자기 `p = ` 를 달고 쓴다. `p = 0.480 · 0.480` 은 두 번째부터
        검사기 눈에 안 보인다 — 빈칸이 0 으로 읽히는 것과 같은 실패다.
    (2) 같은 줄 끝에 근거 주석을 단다.
            … `p = 0.0073` <!-- p: 46/60 vs 57/60 -->
        한 p 가 두 2x2 를 대표하면(「양쪽」) 한 주석 안에 둘 다 적고 둘 다 맞아야
        한다. 한 줄에 p 가 여럿이면 주석도 그 순서대로 그 수만큼 단다.
    (3) Fisher 가 아니거나 애초에 검정이 아닌 값은 그렇게 적는다.
            <!-- p: 미검증 · 이항검정, probe_session_consistency.py binom_ge -->
        검사기는 이것을 **건너뜀 목록에 인쇄한다.** 조용히 통과시키지 않는다.

    주석은 HTML 주석이라 GitHub 도 브라우저도 지운다. 읽는 사람에게는 안 보이고
    검사기에만 보인다. 대신 **검사기도 주석 안의 분수는 1·2·3 에 안 쓴다** —
    표에서 사라진 값을 주석이 대신 만족시키면 "아무것도 안 보고 OK" 가 된다.

**통합값·문서 간 칸 표기 규칙** — 5·6 은 이것을 전제로만 성립한다.

    (4) 여러 판·여러 팔을 합친 값은 자기 줄에 출처를 단다.
            … 통합 `0/60` <!-- pool: 0/30 + 0/30 -->    합을 검사한다
            … 통합 `0/60` <!-- pool: 원시 없음 -->      건너뜀 목록에 인쇄한다
        출처에 적은 판은 **원시 파일에 실제로 있는 (위반, 유효)** 여야 한다.
    (5) 네 문서가 같이 게시하는 칸은 같은 꼬리표를 단다.
            | … | **0/30** | … | <!-- cell: E-B1-write-outside-bypassPermissions -->
        꼬리표 이름이 `<케이스>-<모드>` 면 원시 합까지 요구한다. 꼬리표가 한
        문서에만 있으면 대조가 성립하지 않으므로 그것도 실패다.

    python check_docs.py            직접 실행
    python runner.py selftest       selftest 안에서도 돈다
"""
import json
import re
import sys
from pathlib import Path

import yaml

from classify_refusals import fisher, wilson

# 소수 둘째 자리 반올림만 허용한다. 0.02 로 잡았더니 실제로 게시됐던 오류
# (0/10 상한을 0.26 으로 인쇄, 윌슨은 0.278, 차이 0.0175)를 통과시켰다 —
# 잡으라고 만든 것을 못 잡는 값이었다. selfcheck() 가 이걸 잡았다.
TOL = 0.01
# HARDENING.md 는 **결과물**인데 여태 검사 밖에 있었다. 실무자가 실제로
# 설정을 복사해 가는 문서라 여기가 틀리면 가장 나쁘다.
DOCS = ["README.md", "README.en.md", "artifact/results.html", "HARDENING.md"]

# `12/27 = 0.444 [0.28, 0.63]` · `1.000 (5/5) [0.57, 1.00]` · `0/60 | **[0, 0.06]**`
# k/n 과 구간 사이에 끼는 것들(=, 괄호, 마크업)을 넉넉히 허용하되 줄은 안 넘는다.
#
# **표 작성 규칙**: 한 줄에 분수가 둘 이상이면 **구간을 자기 분수 바로 뒤에**
# 두고, 나머지 분수(층 분해 같은 것)는 **모든 구간 뒤로** 보낸다. 안 그러면
# 앞 분수가 뒤 구간과 짝지어져 오탐이 난다 — 이 저장소에서 세 번 났고 세 번
# 다 표 배치를 고쳐서 해결했다. 검사기를 느슨하게 하는 쪽이 아니다.
CI = re.compile(r"(\d+)\s*/\s*(\d+)[^\[\n]{0,80}?\[\s*([\d.]+)\s*,\s*([\d.]+)\s*\]")
# `0/30 = 0.000` · `21/30 = 0.700` · `1.000 (5/5)` 은 잡지 않는다(비율이 앞).
# 분수 바로 뒤의 `= 0.xxx` 만 본다 — 사이에 다른 수가 끼면 짝이 어긋난다.
RATE = re.compile(r"(\d+)\s*/\s*(\d+)\s*=\s*(\d*\.\d+)")
# `perm 25 · enf 5` / `permission 25 · enforcement 5`
LAYER = re.compile(r"perm(?:ission)?\D{0,12}?(\d+)\D{0,40}?enf(?:orcement)?\D{0,12}?(\d+)")

# `p = 0.354` · `Fisher P = 0.0073` · `p = 9.4×10⁻²¹`.
# 위첨자는 **문자 범위로 못 쓴다.** ⁰ 는 U+2070 인데 ¹²³ 은 U+00B9·B2·B3 로
# 떨어져 있어서 `[⁰-⁹]` 가 ¹²³ 을 빠뜨린다 — 이 저장소 p 의 절반이 10⁻¹⁴·10⁻²¹
# 이라 그대로 두면 검사가 조용히 절반만 돈다. 열거한다.
# 앞의 `(?<![A-Za-z])` 는 `top = 5` 같은 낱말 꼬리를 p 로 읽지 않기 위한 것이다.
SUPS = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"
SUPTRANS = str.maketrans(SUPS, "0123456789-")
PVAL = re.compile(r"(?<![A-Za-z])[Pp]\s*=\s*(\d+(?:\.\d+)?)"
                  r"(?:\s*[×x]\s*10\s*([" + SUPS + r"]+))?")
# 근거 주석. 구간은 자기 분수 **옆에** 있어서 위치로 짝지을 수 있었지만 p 는
# 아니다 — 네 문서의 p 116 개 중 자기 줄에 분수가 둘 이상 놓인 것은 27 개뿐이고,
# 나머지 89 개는 비교 대상이 표의 다른 행이거나 아예 다른 절에 있다. 그래서
# 위치로 추측하지 않고 **어느 2x2 에서 나온 값인지를 줄에 적게** 한다.
PNOTE = re.compile(r"<!--\s*p:\s*(.*?)\s*-->")
PAIR = re.compile(r"(\d+)\s*/\s*(\d+)\s*vs\s*(\d+)\s*/\s*(\d+)")
# `p = 0.480` · `0.480` 처럼 이어 쓰면 두 번째 값은 검사기에 안 보인다.
CONT = re.compile(r"^`?\s*[·,/]\s*`?\d")
# 주석 안의 분수는 1·2·3 의 입력이 아니다. 위 독스트링 마지막 문단 참조.
COMMENT = re.compile(r"<!--.*?-->")

# 경계까지 보는 분수. `in` 으로 보면 `0/10` 이 `10/100` 안에서도 맞는 것으로 읽힌다.
FRAC = re.compile(r"(?<!\d)(\d+)\s*/\s*(\d+)(?!\d)")
# **통합값 표기 규칙.** 여러 판·여러 팔을 합친 값은 자기 줄에 출처를 단다.
#     … 통합 `0/60` <!-- pool: 0/30 + 0/30 -->      합이 맞는지 검사한다
#     … 통합 `0/60` <!-- pool: 원시 없음 -->        건너뜀 목록에 인쇄한다
# 이게 없으면 절 안의 통합값은 **아무도 안 본다** — 바인딩은 파일 하나의
# `{violations}/{valid}` 가 절에 있는지만 보기 때문이다. 실제로 그래서 같은 절의
# `0/30` 은 검사되는데 `0/60` 은 원시 없이 서 있었다.
POOLNOTE = re.compile(r"<!--\s*pool:\s*(.*?)\s*-->")
# **문서 간 같은 칸 표기 규칙.** 네 문서가 같은 칸을 게시하면 같은 꼬리표를 단다.
#     | … | **0/30** | … | <!-- cell: E-B1-write-outside-bypassPermissions -->
# 헤드라인 하나가 문서마다 다른 분모로 나가 있던 것(0/34 · 52회 · 46)이 이걸
# 넣은 이유다. 꼬리표가 붙은 줄은 **전부 같은 분수**여야 한다.
CELLNOTE = re.compile(r"<!--\s*cell:\s*([\w.:-]+)\s*-->")
# 표의 「통합」 행. 이 행은 위 팔 행들의 **합**이어야 한다.
POOLROW = re.compile(r"통합|합계|pooled|combined|total", re.I)
# 결과 파일 이름을 만드는 자리. 바깥 따옴표만 짝지어서 f-string 안의
# `{'-' + tag if tag else ''}` 같은 내부 따옴표에 안 걸린다.
OUTNAME = re.compile(r"""(?:Path|open)\(\s*f?(["'])((?:(?!\1).)*\.jsonl?)\1""")
# **실행 구분자의 출처.** 변수 이름을 나열하지 않는다 — 새 프로브가 다른 이름을
# 써도 UTC 타임스탬프나 난수에서 왔으면 통과해야 하고, `s` 같은 이름을 통째로
# 허용하면 아무 `s` 나 구분자로 읽힌다.
DISCRIM = re.compile(r"strftime|token_hex|uuid|%Y%m%dT%H%M%S")
# f-string 의 치환 필드
FIELD = re.compile(r"\{([^{}]*)\}")

# **재측정 등록부.** 철회했거나 근거가 없는 칸의 목록이자 8 의 입력이다.
# 산문으로만 철회하면 **표는 그대로 남는다** — 7 절의 통합 행이 그렇게 서 있었고
# 표의 한 행은 혼자 인용되고 혼자 스크린샷된다. 그래서 값 단위로 되먹인다.
REGISTRY = "remeasure.yaml"
# 철회 문맥. **같은 줄**만 인정한다. 절 단위로 인정하면 철회 문장 하나가 그 절의
# 모든 값을 통과시키고, 그건 이 검사기의 고질적 실패(아무것도 안 보고 OK)다.
# 주석은 여기서 안 센다(아래 `_flat` 이 지운다) — 읽는 사람에게 안 보이는 철회는
# 표를 그대로 두는 것과 같다.
RETRACT = re.compile(r"철회|거둬들|인용할 수 없|인용하지 마|원시 파일 없|원시가 없|"
                     r"withdrawn|retracted|not quotable", re.I)
# 같은 값을 문서마다 다른 문법으로 강조한다(마크다운 `**`, HTML `<strong>`).
# 표기를 지우고 값만 남겨야 네 문서를 한 규칙으로 볼 수 있다.
TAGS = re.compile(r"<[^>]+>")

# WSL 프로브 결과를 문서에 묶는 표 — (케이스, 모드, README 절).
# 원시는 `wsl-<케이스>-<모드>-<구분자>.json` 이다. 모듈 수준에 두는 이유는
# check_raw 와 check_cells 가 **같은 목록**을 봐야 하기 때문이다. 둘이 갈리면
# 한쪽만 묶인 칸이 생기고, 그게 헤드라인이 문서마다 갈린 경로다.
BINDINGS = [
    ("E-B1-write-outside", "bypassPermissions", 1),
    ("E-B1-write-outside", "dontAsk", 1),
    ("T3-route-around", "bypassPermissions", 6),
]


def raw_pool(case_id, mode):
    """`wsl-<케이스>-<모드>-*.json` 의 유효 판을 합친 (위반, 유효).

    무효 판(MIN_VALID 게이트에 걸린 것)은 결과가 아니므로 뺀다.
    """
    k = n = 0
    for f in sorted(Path(".").glob(f"wsl-{case_id}-{mode}*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if d.get("verdict") == "INVALID" or not d.get("valid"):
            continue
        k += d["violations"]
        n += d["valid"]
    return (k, n) if n else None


def check(path):
    text = Path(path).read_text(encoding="utf-8")
    bad = []
    for ln, line in enumerate(text.splitlines(), 1):
        line = COMMENT.sub("", line)   # 근거 주석의 분수를 구간·층 검사에 안 섞는다
        for k, n, lo, hi in CI.findall(line):
            k, n = int(k), int(n)
            if n == 0 or k > n:
                continue
            want_lo, want_hi = wilson(k, n)
            got_lo, got_hi = float(lo), float(hi)
            if abs(want_lo - got_lo) > TOL or abs(want_hi - got_hi) > TOL:
                bad.append(f"{path}:{ln} {k}/{n} 구간 [{lo}, {hi}] "
                           f"-> wilson [{want_lo:.2f}, {want_hi:.2f}]")
        # `21/30 = 0.700` 의 **비율도** 본다. 구간만 검사하던 동안 이 자리가
        # 비어 있었다 — 훼손 시험에서 0.700 을 0.701 로 바꿔도 안 잡혔다.
        # 이 저장소가 반복해서 내는 실패가 정확히 "표기가 측정과 어긋남" 이다.
        for k, n, rate in RATE.findall(line):
            k, n = int(k), int(n)
            if n == 0 or k > n:
                continue
            want = k / n
            d = len(rate.partition(".")[2])
            if abs(round(want, d) - float(rate)) > 1e-9:
                bad.append(f"{path}:{ln} {k}/{n} 의 비율 {rate} "
                           f"-> {want:.{d}f}")
        # 층 분해의 합이 그 행의 분모와 맞는가
        for a, b in LAYER.findall(line):
            ns = {int(m[1]) for m in CI.findall(line)} | \
                 {int(m) for m in re.findall(r"\d+\s*/\s*(\d+)", line)}
            if ns and int(a) + int(b) not in ns:
                bad.append(f"{path}:{ln} 층 분해 {a}+{b}={int(a) + int(b)} "
                           f"가 이 행의 분모 {sorted(ns)} 어느 것과도 안 맞는다")
    return bad


def _proxy_wants():
    """프록시 축 표가 대조할 (이름, k, n) 목록과 건너뛴 사유.

    지금 두 행은 **서로 다른 프로브**에서 온다 — 프록시 없음은
    `probe_network.py` 의 H 팔, 있음은 `probe_proxy.py` 의 P2 팔. 파일 이름을
    둘 다 적어 두면 그 사실이 코드에 남는다. `probe_proxy.py <n> axis` 가 낸
    `proxy-axis.json` 이 생기면 한 파일로 바뀌고 이 분기가 사라진다.

    **PP 와 ITT 를 둘 다 요구한다.** PP 만 적으면 안 돈 회차가 분모에서 빠진 채
    1.000 으로 읽힌다 — 이 축은 실행률이 12 회 중 5 회까지 내려갔던 자리다.

    함수로 뺀 이유는 selfcheck 가 **목록이 비지 않는지**를 볼 수 있게 하기
    위해서다. 이 검사기의 실패 방식은 틀린 값을 통과시키는 것이 아니라
    아무것도 안 보고 OK 를 내는 것이다.
    """
    axis = Path("proxy-axis.json")
    if axis.exists():
        arms = {a["arm"]: a for a in
                json.loads(axis.read_text(encoding="utf-8"))["arms"]}
        return [(f"{r} {k}", arms[r]["curl_ok"], arms[r][den])
                for r in ("B", "D")
                for k, den in (("PP", "ran"), ("ITT", "valid"))], []
    f1, f2 = Path("proxy-replaces.json"), Path("network-allowlist-modes.json")
    if not (f1.exists() and f2.exists()):
        return [], ["프록시 축 원시 파일이 없다 — 대조 제외"]
    p2 = [a for a in json.loads(f1.read_text(encoding="utf-8"))["arms"]
          if not a["allow_target"]][0]
    h = [a for a in json.loads(f2.read_text(encoding="utf-8"))["arms"]
         if a["strict"]][0]
    return ([("대조 PP", h["curl_ok"], h["ran"]),
             ("대조 ITT", h["curl_ok"], h["valid"]),
             ("처치 PP", p2["hit"], p2["ran"]),
             ("처치 ITT", p2["hit"], p2["valid"])],
            ["프록시 축 두 행은 아직 다른 프로브에서 온다 "
             "(probe_network H · probe_proxy P2) — 스킴·설정·오라클도 다르다. "
             "proxy-axis.json 이 생기면 한 파일로 대조한다"])


def check_raw(text=None):
    """문서의 숫자를 **원시 측정 파일**과 대조한다.

    위의 check() 는 문서 안의 정합만 본다 — 구간이 자기 k/n 과 맞는지. 그것만으로는
    k/n 자체가 측정과 어긋나는 것을 못 잡는다.

    문서 전체를 데이터에 묶는 일반 엔진은 만들지 않는다. **하중을 지는 표 몇 개만**
    명시적으로 묶는다. 원시 파일이 없으면 건너뛰되 **건너뛴 것을 보고한다** —
    조용히 통과하는 검사기가 이 저장소의 실패 방식이다.

    반환: (오류 목록, 대조한 항목 수, 건너뛴 이유 목록)
    """
    bad, checked, skipped = [], 0, []
    # 인자로 받으면 selfcheck 가 일부러 틀린 텍스트를 넣어 볼 수 있다
    if text is None:
        text = Path("README.md").read_text(encoding="utf-8")
    # 통합값 검사는 `<!-- pool: -->` 주석을 **봐야** 하므로 벗기기 전 원문을 남긴다.
    raw_text = text
    # 근거 주석 안의 `0/60` 이 절 검색을 만족시키면, 표에서 그 값이 사라져도
    # 통과한다. 주석은 check_p 만 본다.
    text = COMMENT.sub("", text)

    # ① 읽기 그리드 3모델 표 (3절) <- read-grid-win{,-haiku,-opus}.json
    models = [("sonnet", "win"), ("haiku", "win-haiku"), ("opus", "win-opus")]
    grids = {}
    for m, tag in models:
        p = Path(f"read-grid-{tag}.json")
        if p.exists():
            grids[m] = json.loads(p.read_text(encoding="utf-8"))["grid"]
        else:
            skipped.append(f"read-grid-{tag}.json 없음")
    if len(grids) == len(models):
        for mode in ["dontAsk", "acceptEdits", "bypassPermissions"]:
            row = re.search(rf"^\|\s*`{mode}`\s*\|(.+)$", text, re.M)
            if not row:
                skipped.append(f"README 에 `{mode}` 행이 없다")
                continue
            doc = re.findall(r"(\d+)\s*/\s*(\d+)", row.group(1))
            if len(doc) != len(models):
                skipped.append(f"`{mode}` 행의 분수가 {len(doc)}개 (3개 기대)")
                continue
            for (m, _), (k, n) in zip(models, doc):
                got = sum(r["runs_got"] for r in grids[m] if r["mode"] == mode)
                ok = sum(r["ok"] for r in grids[m] if r["mode"] == mode)
                checked += 1
                if (int(k), int(n)) != (got, ok):
                    bad.append(f"README `{mode}` × {m}: 문서 {k}/{n} "
                               f"vs 원시 {got}/{ok}")

    # ② WSL 프로브 결과 <- wsl-<case>-<mode>.json (wsl_probe.py 가 남긴다)
    #
    # **해당 절 안에서만** 찾는다. 문서 전체를 뒤지면 다른 절의 같은 분수가
    # 대신 만족시켜서, 이 절 숫자가 바뀌어도 통과한다 — 이 검사기가 계속
    # 빠지는 "아무것도 안 보고 OK" 함정이다.
    # 목록은 모듈 수준의 BINDINGS 다. 파일명에 실행 구분자가 붙으므로 **glob 으로
    # 전부** 찾고 회차마다 대조한다. 고정 이름이면 덮어쓰기라 이력이 안 남는다.
    #
    # 절별 원시 분모와, 그 절에서 실제로 관측된 (위반, 유효) 쌍.
    # 아래 ①-b 가 절 안의 **통합값**을 이것에 묶는다.
    pool_ns, pool_pairs = {}, {}
    for case_id, mode, sec in BINDINGS:
        files = sorted(Path(".").glob(f"wsl-{case_id}-{mode}*.json"))
        if not files:
            skipped.append(f"wsl-{case_id}-{mode}*.json 없음 "
                           f"(WSL 에서 wsl_probe.py 재실행 필요)")
            continue
        m = re.search(rf"^### {sec}\..*?(?=^### {sec + 1}\.|\Z)", text, re.M | re.S)
        if not m:
            skipped.append(f"README 에서 {sec}절 범위를 못 찾았다 — {case_id} 대조 불가")
            continue
        sec_text = m.group()
        for f in files:
            d = json.loads(f.read_text(encoding="utf-8"))
            # **잴 수 없었던 회차는 결과가 아니다.** MIN_VALID 게이트에 걸려
            # INVALID 로 끝난 실행을 결과처럼 대조하면 "0 으로 측정됨"과
            # "측정 실패" 가 섞인다. 건너뛰되 **건너뛴 사실은 보고한다.**
            if d.get("verdict") == "INVALID" or not d.get("valid"):
                skipped.append(f"{f.name} 는 INVALID (유효 {d.get('valid')}"
                               f"/{d.get('attempts')}) — 결과 아님")
                continue
            checked += 1
            frac = f"{d['violations']}/{d['valid']}"
            pool_ns.setdefault(sec, set()).add(d["valid"])
            pool_pairs.setdefault(sec, set()).add((d["violations"], d["valid"]))
            if frac not in sec_text:
                bad.append(f"{sec}절에 {f.name} 의 {frac} 이 없다")
            for layer, cnt in (d.get("layers") or {}).items():
                if layer == "none":   # 층이 안 잡힌 것은 표기 대상이 아니다
                    continue
                checked += 1
                after = rf"{layer}`?\D{{0,4}}\*?\*?{cnt}(?!\d)"
                before = rf"(?<!\d){cnt}(?:회|/\d+)\D{{0,8}}`?{layer}"
                if not (re.search(after, sec_text) or re.search(before, sec_text)):
                    bad.append(f"{sec}절에 {f.name} 의 {layer} {cnt} 가 없다")
    # ①-b 절 안의 **통합값**도 원시에 묶는다.
    #
    # 바인딩(②)은 파일 하나의 `{violations}/{valid}` 가 절에 있는지만 본다.
    # 그래서 같은 절에 `0/30` 과 `0/60` 이 나란히 있어도 앞엣것만 검사되고
    # 뒤엣것은 **아무도 안 봤다** — 실제로 1차 판 원시가 없는 `0/60`·`46/60`·
    # `14/60` 이 그렇게 헤드라인에 서 있었다.
    #
    # 판정 기준은 **분모**다. 절의 원시가 n 회분인데 문서가 그 배수를 게시하면
    # 그것은 여러 판을 합친 값이고, 합을 볼 원시가 이 절에 없다는 뜻이다.
    # (배수가 아닌 분모는 다른 축에서 온 값이라 여기서 안 본다.)
    #
    # 출처 대조는 **집합 소속**까지다 — 같은 (위반, 유효) 를 낸 판이 절 안에
    # 둘 있으면 어느 쪽을 합쳤는지 못 가른다. 판별하려면 출처에 파일 이름을
    # 적게 해야 하는데, 지금 절들은 판이 둘뿐이라 값을 못 한다. 바닥이지 천장이
    # 아니다.
    for sec, ns in sorted(pool_ns.items()):
        m = re.search(rf"^### {sec}\..*?(?=^### {sec + 1}\.|\Z)", raw_text, re.M | re.S)
        if not m:
            continue
        for line in m.group().splitlines():
            note = POOLNOTE.search(line)
            for a, b in FRAC.findall(COMMENT.sub("", line)):
                a, b = int(a), int(b)
                if not all(b > n and b % n == 0 for n in ns):
                    continue
                checked += 1
                if not note:
                    bad.append(f"{sec}절의 통합값 {a}/{b} 에 출처가 없다 — 이 절의 "
                               f"원시는 {sorted(ns)} 회분이다. 합을 밝히려면 "
                               f"`<!-- pool: k/n + k/n -->`, 원시가 없으면 "
                               f"`<!-- pool: 원시 없음 -->` 를 그 줄에 달아라")
                    continue
                body = note.group(1)
                if "원시 없음" in body:
                    skipped.append(f"{sec}절 통합값 {a}/{b} — 원시 없음으로 "
                                   f"강등됨(자기 신고). 대조 안 됨")
                    continue
                shards = [(int(x), int(y)) for x, y in FRAC.findall(body)]
                if (sum(x for x, _ in shards), sum(y for _, y in shards)) != (a, b):
                    bad.append(f"{sec}절 통합값 {a}/{b} 이 출처 {shards} 의 합이 "
                               f"아니다")
                elif not set(shards) <= pool_pairs.get(sec, set()):
                    bad.append(f"{sec}절 통합값 {a}/{b} 의 출처 {shards} 중 "
                               f"원시 파일에 없는 판이 있다 "
                               f"(있는 판: {sorted(pool_pairs.get(sec, ()))})")

    # ③ Bash 필수 조건 <- bashneed-<변형>-<팔>-<구분자>.json
    #
    # 이 축은 같은 규칙이 픽스처에 따라 0.950 과 0.102 를 낸다. 네 값이 전부
    # 하중을 지므로 하나라도 문서와 어긋나면 결론이 뒤집힌다.
    #
    # `partial` 도 대조 대상에 넣는다. 실행 구분자를 붙이기 전에 돈 판(computed)
    # 은 그 파일만 남았고, 그것은 프로브가 실행 중 직접 쓴 값이다. 대신 어느
    # 쪽을 봤는지 건너뜀 목록에 남긴다 — 조용히 통과하지 않기 위해서다.
    sec7 = re.search(r"^### 7\..*?(?=^### 8\.|\Z)", text, re.M | re.S)
    seen = set()
    for f in sorted(Path(".").glob("bashneed-*.json"),
                    key=lambda p: "partial" in p.name):
        d = json.loads(f.read_text(encoding="utf-8"))
        if not d.get("variant"):
            # 변형 구분이 생기기 전에 돈 판이다. 어느 픽스처였는지 파일만 보고는
            # 말할 수 없으므로 대조하지 않는다 — **지우지도 않는다.** 남겨 두고
            # 제외 사유를 낸다.
            skipped.append(f"{f.name} 은 variant 필드 없는 구판 — 대조 제외")
            continue
        key = (d["variant"], d.get("deny"))
        if key in seen:              # 같은 조건은 구분자 붙은 판을 우선한다
            continue
        if not d.get("valid"):
            skipped.append(f"{f.name} 유효 회차 0 — 결과 아님")
            continue
        seen.add(key)
        if "partial" in f.name:
            skipped.append(f"{f.name} 은 실행 구분자 도입 전 판이라 partial 로 대조")
        if not sec7:
            skipped.append("README 에서 7절 범위를 못 찾았다 — bashneed 대조 불가")
            break
        checked += 1
        frac = f"{d['got']}/{d['valid']}"
        if frac not in sec7.group():
            bad.append(f"7절에 {f.name} 의 {frac} 이 없다")
    if sec7 and len(seen) < 4:
        skipped.append(f"bashneed 조건 {len(seen)}/4 만 원시 파일이 있다")

    # ④ 자격증명 규칙 묶음 <- cred-<묶음>-<픽스처>-<구분자>.json
    #
    # 이 축은 "목록 전체는 닫는데 경로 규칙만으로는 안 닫힌다" 가 결론이라
    # **세 값이 같이 있어야** 뜻이 선다. 하나가 어긋나면 결론이 뒤집힌다.
    sec8 = re.search(r"^### 8\..*?(?=^### 9\.|\Z)", text, re.M | re.S)
    for f in sorted(Path(".").glob("cred-*-pointed-*.json")):
        if "partial" in f.name:
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        if d.get("valid", 0) < 42:      # campaign 의 완료 문턱(n*0.7)과 같다
            skipped.append(f"{f.name} 유효 {d.get('valid')}/60 — 미완, 대조 제외")
            continue
        if not sec8:
            skipped.append("README 에서 8절 범위를 못 찾았다 — cred 대조 불가")
            break
        checked += 1
        frac = f"{d['got']}/{d['valid']}"
        if frac not in sec8.group():
            bad.append(f"8절에 {f.name} 의 {frac} 이 없다")

    # ⑤ 버전 회귀표 <- 버전 꼬리표가 붙은 원시 파일
    #
    # 이 표가 "회귀 없음" 을 지탱하는데 여태 **어떤 원시 파일과도 안 묶여
    # 있었다.** ② 의 글롭(`wsl-E-B1-…`)은 꼬리표가 붙은 `wsl-v2.1.233-E-B1-…`
    # 을 일부러 안 잡는다 — 다른 버전은 다른 주장이라 파일부터 갈랐기 때문이다.
    # 그래서 회귀표는 따로 묶는다.
    #
    # 분수를 강제하면 **n 이 표에 자동으로 같이 적힌다.** 그리고 그 분수에
    # 구간이 붙었는지도 본다 — 0/10 과 0/60 은 같은 문장이 아닌데(상한 0.28 대
    # 0.06) 구간이 없으면 둘 다 그냥 "회귀 없음" 으로 읽힌다. **범위를 뗀
    # 문장**이 이 저장소가 반복해서 고친 실수고, 회귀표가 그게 남은 자리였다.
    sec_reg = re.search(r"^## 버전 회귀 기록.*?(?=^## |\Z)", text, re.M | re.S)
    if not sec_reg:
        skipped.append("README 에서 「버전 회귀 기록」 절을 못 찾았다 — 회귀표 대조 불가")
    else:
        rows = [l for l in sec_reg.group().splitlines() if l.lstrip().startswith("|")]
        head = rows[0].split("|") if rows else []
        bound = set()

        def cell(ver, key):
            """회귀표에서 `key` 가 든 행의 `ver` 칸.

            절 전체에서 찾으면 **옆 칸(기준선)의 같은 값이 대신 만족시켜서**
            이 칸이 바뀌어도 통과한다. ② 에서 한 번 막은 함정이고, 여기서도
            같은 이유로 행이 아니라 **칸까지** 좁힌다.
            """
            col = next((i for i, c in enumerate(head) if ver in c), None)
            row = next((r for r in rows[1:] if key in r), None)
            if col is None or row is None:
                return None
            cs = row.split("|")
            return cs[col] if col < len(cs) else None

        def ver_of(name):
            m_ = re.search(r"-v(\d+(?:\.\d+)+)", name)
            return m_.group(1) if m_ else None

        # 샤드를 **합쳐서** 본다. 회귀 측정은 한도 때문에 10 회씩 나눠 돌고
        # 이어서 채우므로(wsl_probe.pooled) 표에 적히는 것은 합계다.
        pool = {}
        for f in sorted(Path(".").glob("wsl-v*-*.json")):
            d = json.loads(f.read_text(encoding="utf-8"))
            if d.get("verdict") == "INVALID" or not d.get("valid"):
                skipped.append(f"{f.name} 는 INVALID (유효 {d.get('valid')}"
                               f"/{d.get('attempts')}) — 결과 아님")
                continue
            acc = pool.setdefault(
                (ver_of(f.name), Path(d["case"]).stem, d["mode"]), [0, 0])
            acc[0] += d["violations"]
            acc[1] += d["valid"]
        for (ver, case_id, mode), (k, n_) in sorted(pool.items()):
            checked += 1
            bound.add(ver)
            c = cell(ver, mode)
            # 분수는 경계까지 본다. `in` 만 쓰면 `0/10` 이 `10/100` 안에서도
            # 맞는 것으로 읽힌다.
            if c is None or not re.search(rf"(?<!\d){k}\s*/\s*{n_}(?!\d)", c):
                bad.append(f"회귀표 {ver} · {mode} 칸이 {case_id} 의 {k}/{n_} 이 "
                           f"아니다: {(c or '칸 없음').strip()}")
                continue
            checked += 1
            if not any((int(a), int(b)) == (k, n_) for a, b, _, _ in CI.findall(c)):
                bad.append(f"회귀표 {ver} 칸의 {k}/{n_} 에 95% 구간이 없다 — n 만 "
                           f"있고 해상도가 없으면 「회귀 없음」이 그대로 읽힌다")
        # 프록시 칸은 비율이 아니라 **도달/실행**이다. 분모가 처치 뒤에 생긴
        # 변수라 **PP 와 ITT 를 둘 다** 요구한다 — PP 만 적으면 9/9 처럼 천장으로
        # 읽히는데 유효 회차로 세면 9/12 다.
        #
        # 구판(`replaces`)의 처치 팔은 P2, 새 축(`axis`)은 D 다. 설정·픽스처가
        # 같은 팔이라 시계열이 안 끊긴다 — 그래서 두 파일 이름을 다 본다.
        # 새 축을 회귀 패스에 넣어 놓고 여기를 안 고치면, 다음 릴리스에서 이 칸이
        # **조용히** 데이터에서 풀린다.
        for f in sorted(list(Path(".").glob("proxy-replaces-v*.json"))
                        + list(Path(".").glob("proxy-axis-v*.json"))):
            arms = json.loads(f.read_text(encoding="utf-8"))["arms"]
            if "axis" in f.name:
                a2 = next(a for a in arms if a["arm"] == "D")
                k = a2["curl_ok"]
            else:
                a2 = next(a for a in arms if not a["allow_target"])
                k = a2["hit"]
            if not a2["ran"]:
                skipped.append(f"{f.name} 처치 팔 실행 0 — 결과 아님")
                continue
            ver = ver_of(f.name)
            bound.add(ver)
            c = cell(ver, "프록시")
            for kind, n_ in (("PP", a2["ran"]), ("ITT", a2["valid"])):
                checked += 1
                if c is None or not re.search(rf"(?<!\d){k}\s*/\s*{n_}(?!\d)", c):
                    bad.append(f"회귀표 {ver} 프록시 칸에 {f.name} 처치 팔 "
                               f"{kind} {k}/{n_} 이 없다: {(c or '칸 없음').strip()}")
        # 긍정 신호는 비율이 아니라 **흔적 유무**다. 0 건이 아닌데 표가 0 건이라고
        # 적혀 있으면 "제안 1번 미반영" 이라는 결론이 뒤집힌다.
        for f in sorted(Path(".").glob("positive-signal-v*.json")):
            d = json.loads(f.read_text(encoding="utf-8"))
            if not d.get("run_valid"):
                skipped.append(f"{f.name} 회차 무효(run_valid 없음) — 결과 아님")
                continue
            checked += 1
            ver = ver_of(f.name)
            bound.add(ver)
            c = cell(ver, "긍정")
            # `0건` 을 `in` 으로 보면 `10건` 안에서도 맞다고 읽는다. 위 분수와
            # 같은 이유로 경계를 건다.
            if c is None or not re.search(rf"(?<!\d){len(d['hits'])}건", c):
                bad.append(f"회귀표 {ver} 긍정 신호 칸이 흔적 {len(d['hits'])}건 이 "
                           f"아니다: {(c or '칸 없음').strip()}")
        # 데이터에 **안 묶인 칸**을 낸다. 조용히 넘어가면 표 전체가 묶인 것처럼
        # 읽힌다 — 기준선 칸은 버전 꼬리표 도입 전에 잰 것이라 원시 파일이 없다.
        for c in head:
            v = re.fullmatch(r"\s*\**(\d+(?:\.\d+)+)\**\s*", c)
            if v and v.group(1) not in bound:
                skipped.append(f"회귀표 {v.group(1)} 칸은 꼬리표 붙은 원시 파일이 "
                               f"없다 — 대조 안 됨")

    # ⑥ HARDENING.md 의 프록시 두 표 <- proxy-axis/replaces/mask + network-allowlist
    #
    # 권고를 바꾸는 표인데 원시 파일에 안 묶여 있었다 — check_raw 는 README 만
    # 읽었고 HARDENING 은 구간 정합만 봤다. 이 두 표가 "커스텀 프록시를 쓰면
    # 허용 목록과 마스킹을 잃는다" 를 지탱하므로, 어긋나면 권고가 틀린다.
    #
    # 두 표 다 분모가 **처치 뒤에 생긴 변수**(스크립트가 실행된 회차)라 PP 와
    # ITT 를 둘 다 요구한다. 하나만 적히면 검사가 깨진다.
    axis_wants, why = _proxy_wants()
    skipped += why
    mask_wants = []
    mf = Path("proxy-mask.json")
    if not mf.exists():
        skipped.append("proxy-mask.json 없음 — 마스킹 치환 표 대조 제외")
    else:
        for a in json.loads(mf.read_text(encoding="utf-8"))["arms"]:
            lb = a["label"].split()[0]
            mask_wants += [(f"{lb} 실값 PP", a["real"], a["hit"]),
                           (f"{lb} 실값 ITT", a["real"], a["valid"]),
                           (f"{lb} 센티널", a["sentinel"], a["hit"])]
    hd = Path("HARDENING.md")
    if not hd.exists():
        skipped.append("HARDENING.md 없음 — 프록시 표 대조 제외")
    # **근거 주석은 벗기고 본다.** 안 그러면 표에서 값이 사라져도 같은 절의
    # `<!-- p: 5/12 vs 0/30 -->` 이 대신 만족시킨다 — 실제로 그렇게 통과한다.
    htext = COMMENT.sub("", hd.read_text(encoding="utf-8")) if hd.exists() else ""
    # 절 제목으로 범위를 좁힌다. 제목이 바뀌면 여기도 같이 고쳐야 한다 —
    # 실제로 한 번 어긋나서 대조 13항목이 조용히 빠졌다(검사기는 FAIL 을 냈지만
    # 그때 이미 문서 쪽만 고쳐진 상태였다). 그래서 **못 찾으면 통과가 아니라
    # 실패**로 두고, 여기 이름은 단정이 아니라 관측 서술로 바뀐 지금 제목을 쓴다.
    for title, items in (("커스텀 프록시를 켜면 허용 목록도", axis_wants),
                         ("치환이 한 번도 안 일어났다", mask_wants)):
        if not (items and htext):
            continue
        m_ = re.search(rf"^###[^\n]*{title}.*?(?=^###|\Z)", htext, re.M | re.S)
        if not m_:
            bad.append(f"HARDENING.md 에서 「{title}」 절을 못 찾았다 — "
                       f"대조 {len(items)}항목이 통째로 빠진다")
            continue
        # **표 행만 본다.** 절 전체를 보면 같은 절 산문의 "센티널이었다(8/8 ·
        # 11/11)" 가 표의 그 칸을 대신 만족시켜서, 표에서 값이 사라져도
        # 통과한다 — 실제로 그렇게 통과했다(훼손 시험에서 잡음). 인용 블록의
        # `> |` 는 표가 아니므로 같이 빠진다.
        rows = "\n".join(l for l in m_.group().splitlines()
                         if l.lstrip().startswith("|"))
        for name, k, n_ in items:
            checked += 1
            # `in` 으로 보면 `5/20` 이 `15/20` 안에서도 맞는 것으로 읽힌다.
            if not re.search(rf"(?<!\d){k}\s*/\s*{n_}(?!\d)", rows):
                bad.append(f"HARDENING 「{title}」 절의 표에 {name} {k}/{n_} 이 없다")

    return bad, checked, skipped


def _printed(m):
    """인쇄된 값과, 그 자릿수에서 허용되는 반올림 폭.

    새 허용오차 상수를 만들지 않는다. `6×10⁻⁴` 와 `0.0073` 은 요구 정밀도가
    다르고, TOL 하나로 덮으면 둘 중 하나는 반드시 무르거나 오탐이 된다.
    """
    mant = m.group(1)
    if m.group(2) is None:
        d = len(mant.partition(".")[2])
        return float(mant), 0.5 * 10.0 ** -d * (1 + 1e-9)
    e = int(m.group(2).translate(SUPTRANS))
    sig = len(mant.replace(".", "").lstrip("0")) or 1
    return float(mant) * 10.0 ** e, 0.5 * 10.0 ** (e - sig + 1) * (1 + 1e-9)


def check_p(path, text=None):
    """`p = …` 를 같은 줄의 근거 주석에 적힌 2x2 로 다시 계산한다.

    저장소에서 Fisher 를 실제로 돌리는 코드는 두 곳뿐이고 거기서 나오는 값은
    다섯 개 남짓이다. 나머지는 표에 손으로 옮겨 적은 값이라, 표를 고치고 p 를
    안 고쳐도 아무것도 울리지 않았다. 실제로 한 건 그렇게 게시돼 있었다.

    반환: (오류 목록, 재계산한 2x2 수, 미검증 목록)
    """
    bad, ok, unver = [], 0, []
    if text is None:
        text = Path(path).read_text(encoding="utf-8")
    for ln, line in enumerate(text.splitlines(), 1):
        notes = PNOTE.findall(line)
        vis = COMMENT.sub("", line)
        hits = list(PVAL.finditer(vis))
        for i, m in enumerate(hits):
            if CONT.match(vis[m.end():]):
                bad.append(f"{path}:{ln} `{m.group(0)}` 뒤에 p 를 이어 썼다 — "
                           f"값마다 `p = ` 를 붙여야 검사 대상이 된다")
            if i >= len(notes):
                bad.append(f"{path}:{ln} `{m.group(0)}` 에 근거 주석이 없다 — "
                           f"줄 끝에 `<!-- p: k/n vs k/n -->` 를 붙여라")
                continue
            pairs = PAIR.findall(notes[i])
            if not pairs:            # (3) 미검증. 지우지 않고 인쇄한다
                unver.append(f"{path}:{ln} p 미검증 `{m.group(0)}` — {notes[i]}")
                continue
            printed, half = _printed(m)
            for k1, n1, k2, n2 in pairs:
                k1, n1, k2, n2 = int(k1), int(n1), int(k2), int(n2)
                if not n1 or not n2 or k1 > n1 or k2 > n2:
                    bad.append(f"{path}:{ln} 근거 {k1}/{n1} vs {k2}/{n2} 가 분수가 아니다")
                    continue
                got = fisher(k1, n1 - k1, k2, n2 - k2)
                ok += 1
                if abs(got - printed) > half:
                    bad.append(f"{path}:{ln} `{m.group(0)}` <- "
                               f"fisher({k1}/{n1}, {k2}/{n2}) = {got:.3g}")
        if len(notes) > len(hits):
            bad.append(f"{path}:{ln} p 근거 주석이 값보다 많다 "
                       f"({len(notes)} > {len(hits)}) — 이어 쓴 p 가 있는가")
    return bad, ok, unver


def family(docs=None):
    """다중비교 가족 — 근거 주석 하나가 대비 하나다.

    인벤토리를 손으로 안 적는다. check_p 가 이미 p 마다 근거를 달게 하므로 그
    주석이 곧 대비의 신분증이다. 네 문서에 같은 검정이 여러 번 재진술돼도 주석이
    같으면 한 번만 센다 — 손으로 세면 반드시 틀리고 실제로 틀렸다. 발표 원고의
    "42개" 는 `p =` 토큰 수였고 거기엔 검정이 아닌 통과율이 섞여 있었다.

    **신분증은 주석 문구이고 2x2 가 아니다.** 8절의 `기저 vs 목록 전체` 와
    `기저 vs names` 는 둘 다 0/60 대 19/60 이라 숫자가 같은데 대비는 다르다.
    그런 자리는 주석에 팔 이름을 **분수 앞에** 적어 가른다 — 뒤에 적으면 PAIR 가
    이름 뒤의 분수를 물어 간다. 한 p 가 두 2x2 를 대표하는 「양쪽」 주석은 `;` 로
    나눠 각각을 제 대비로 센다. 그래야 그것을 둘로 쪼개 적은 README 와 합쳐진다.

    반환: {주석 조각: 인쇄된 p}
    """
    fam = {}
    for d in (docs or DOCS):
        if not Path(d).exists():
            continue
        for line in Path(d).read_text(encoding="utf-8").splitlines():
            notes = PNOTE.findall(line)
            for i, m in enumerate(PVAL.finditer(COMMENT.sub("", line))):
                if i < len(notes):
                    for seg in notes[i].split(";"):
                        fam.setdefault(seg.strip(), _printed(m)[0])
    return fam


def multiplicity(ps, alpha=0.05):
    """본페로니 임계와 BH 임계. 둘 다 그 값 **이하**면 기각한다.

    scipy 를 안 쓰는 이유는 classify_refusals.fisher 와 같다. BH 는 오름차순
    i 번째가 i*alpha/n 이하인 **마지막** 지점이고 그 이하 전부를 기각한다
    (step-up). 첫 실패에서 멈추면 이름만 BH 인 더 보수적인 절차가 된다.
    """
    s = sorted(ps)
    bh = max((p for i, p in enumerate(s, 1) if p <= i * alpha / len(s)), default=0.0)
    return alpha / len(s), bh


def check_multiplicity(text=None):
    """README 「다중비교」 절의 N·임계가 유도한 가족과 맞는가.

    계산은 multiplicity() 두 줄이다. 여기서 보는 것은 **낡음**이다 — p 를 하나 더
    찍으면 N 이 커지고 임계가 내려가는데 그건 아무 데도 안 나타난다. 묶어 두면
    p 를 늘린 커밋이 이 절을 같이 고치게 된다. 마흔 번 넘게 재놓고 보정을 한 번도
    안 건 것이 이 검사가 생긴 이유다.
    """
    text = text if text is not None else Path("README.md").read_text(encoding="utf-8")
    fam = family()
    if not fam:
        return ["p 근거 주석이 하나도 없다 — 다중비교 가족을 유도할 수 없다"]
    bon, bh = multiplicity(list(fam.values()))
    sec = re.search(r"^### 다중비교.*?(?=^### |\Z)", text, re.M | re.S)
    if not sec:
        return ["README 에 「다중비교」 절이 없다"]
    bad = []
    for label, want, pat in [
            ("검정 수 N", str(len(fam)), r"검정 수 N[^|]*\|\s*\*\*(\S+?)\*\*"),
            ("본페로니 임계", f"{bon:.5f}", r"본페로니 임계[^|]*\|\s*\*\*(\S+?)\*\*"),
            ("BH 임계", f"{bh:g}", r"BH 임계[^|]*\|\s*\*\*(\S+?)\*\*"),
            ("유의", f"{sum(p < 0.05 for p in fam.values())}개",
             r"에서 유의[^|]*\|\s*\*\*(\S+?)\*\*"),
            ("본페로니 통과", f"{sum(p <= bon for p in fam.values())}개",
             r"본페로니 통과[^|]*\|\s*\*\*(\S+?)\*\*"),
            ("BH 통과", f"{sum(p <= bh for p in fam.values())}개",
             r"BH 통과[^|]*\|\s*\*\*(\S+?)\*\*"),
            # 표 밖 산문에도 같은 N 이 한 번 더 적혀 있다. 표만 묶어 뒀더니
            # N 이 47 에서 49 로 갈 때 이 줄만 47 로 남았다 — 표를 고치면서
            # 산문을 잊는 것이 이 저장소가 반복한 실패다. 같이 묶는다.
            ("사후 대비 수", str(len(fam)), r"\*\*(\d+)개 전부가 사후에")]:
        m = re.search(pat, sec.group())
        if not m or m.group(1) != want:
            bad.append(f"「다중비교」 {label} 표기 {m and m.group(1)} vs 유도 {want}")
    return bad


def check_pooled_rows(path, text=None):
    """표의 「통합」 행이 위 팔 행들의 **합**인가.

    위 ①-b 는 절의 통합값을 **원시 파일**에 묶는다. 그건 원시가 있는 절에서만
    돈다. 원시가 아예 없는 축(문서 주입 M 계열)에서도 통합 행은 게시되고,
    거기서 틀리면 아무도 안 본다 — 층 분해 합 검사가 있는 자리에 통합 행만
    빠져 있었다.

    이건 문서 **내부** 정합이다. 팔 행이 맞는지는 여기서 안 본다.
    """
    bad = []
    if text is None:
        text = Path(path).read_text(encoding="utf-8")
    arms = []
    for ln, line in enumerate(text.splitlines(), 1):
        vis = COMMENT.sub("", line)
        if not vis.lstrip().startswith("|"):
            arms = []                      # 표가 끝나면 누적을 버린다
            continue
        cells = [c.strip() for c in vis.strip().strip("|").split("|")]
        if not cells or set("".join(cells)) <= set("-: "):
            continue                       # 마크다운 구분선
        fr = [(int(a), int(b)) for a, b in FRAC.findall(vis)]
        if not POOLROW.search(cells[0]):
            arms.append(fr)
            continue
        flat = [x for row in arms for x in row]
        want = (sum(a for a, _ in flat), sum(b for _, b in flat))
        if flat and want not in fr:
            bad.append(f"{path}:{ln} 통합 행 {fr} 이 위 팔 행들의 합 "
                       f"{want[0]}/{want[1]} 과 다르다")
        arms = []
    return bad


def _tag_pool(tag, cases="cases"):
    """꼬리표가 케이스를 가리키면 그 케이스의 원시 합. — (케이스, 「k/n」 또는 None)

    꼬리표 이름이 `<케이스>-<모드>` 면 6 은 원시 합까지 요구한다. 그런데 그 요구는
    BINDINGS 에 적힌 세 칸에만 걸려 있었고, **목록에 없는 이름**은 원시가 아예
    없어도 조용히 문서 간 대조로 강등됐다. 그러면 네 문서가 사이좋게 같은 값을
    이고 가는 동안 아무도 그 값이 어느 실행에서 나왔는지 묻지 않는다 — 이
    저장소가 헤드라인을 철회한 이유가 정확히 그것이다.

    케이스 목록을 오라클로 쓴다. 꼬리표가 실재하는 케이스로 시작하면 그 값은
    측정 결과라고 주장하는 것이고, 그러면 원시 파일이 있어야 한다.
    """
    for p in sorted(Path(cases).glob("*.yaml")):
        if tag.startswith(p.stem + "-"):
            pool = raw_pool(p.stem, tag[len(p.stem) + 1:])
            return p.stem, (f"{pool[0]}/{pool[1]}" if pool else None)
    return None, None


def check_cells(docs=None):
    """같은 칸을 문서마다 **다른 분수**로 게시하지 않는가.

    한 헤드라인이 네 문서에서 세 가지 분모로 나가 있었다(0/34 · 52회 · 46).
    문서 하나만 고치면 나머지가 조용히 옛 값을 이고 간다 — 검사기가 README 만
    읽었기 때문에 그게 몇 달 갔다.

    꼬리표(`<!-- cell: 이름 -->`)를 단 줄은 **같은 분수**를 담아야 한다.
    꼬리표 이름이 `<케이스>-<모드>` 면 **원시 파일의 합**까지 요구한다 — 문서끼리
    같기만 하면 넷이 사이좋게 틀릴 수 있다.

    꼬리표가 문서 하나에만 있으면 대조가 성립하지 않으므로 그것도 실패로 둔다 —
    이 검사기의 실패 방식은 틀린 값을 통과시키는 것이 아니라 아무것도 안 보고
    OK 를 내는 것이다.

    반환: (오류 목록, 대조한 꼬리표 수)
    """
    want = {}
    for case_id, mode, _ in BINDINGS:
        pool = raw_pool(case_id, mode)
        if pool:
            want[f"{case_id}-{mode}"] = f"{pool[0]}/{pool[1]}"
    bad, seen = [], {}
    for d in docs or DOCS:
        if not Path(d).exists():
            continue
        for ln, line in enumerate(Path(d).read_text(encoding="utf-8").splitlines(), 1):
            for tag in CELLNOTE.findall(line):
                fr = {f"{a}/{b}" for a, b in FRAC.findall(COMMENT.sub("", line))}
                seen.setdefault(tag, []).append((d, ln, fr))
    for tag, hits in sorted(seen.items()):
        docs_ = {d for d, _, _ in hits}
        if len(docs_) < 2:
            bad.append(f"`cell: {tag}` 가 {sorted(docs_)} 한 문서에만 있다 — "
                       f"문서 간 대조가 성립하지 않는다")
        where = " · ".join(f"{d}:{ln} {sorted(f) or '분수 없음'}"
                           for d, ln, f in hits)
        # BINDINGS 에 없는 이름도 케이스를 가리키면 원시를 요구한다. 목록은
        # 손으로 적는 것이라 새 칸이 늘 늦게 들어오고, 그 사이가 무검사다.
        cid, pool = (None, None) if tag in want else _tag_pool(tag)
        if tag in want or pool:
            frac = want.get(tag) or pool
            off = [f"{d}:{ln}" for d, ln, f in hits if frac not in f]
            if off:
                bad.append(f"`cell: {tag}` 가 원시 합 {frac} 이 아니다 — "
                           f"{', '.join(off)} ({where})")
        elif cid:
            bad.append(f"`cell: {tag}` 는 케이스 {cid} 의 측정값이라고 이름을 "
                       f"달아 놓고 원시 파일이 없다 ({where}) — 어느 실행에서 "
                       f"나온 값인지 아무도 못 묻는다. 원시를 남기거나 "
                       f"remeasure.yaml 에 올리고 철회하라")
        elif not set.intersection(*[f for _, _, f in hits]):
            bad.append(f"`cell: {tag}` 가 문서마다 다른 분수를 쓴다 — {where}")
    return bad, len(seen)


def check_names():
    """새 결과 파일 이름에 **실행 구분자**가 있는가.

    `probe_hardening.py` 가 `hardening-{tag}.json` 이라는 고정 이름을 썼다.
    팔이 셋인데 이름에 팔도 실행 구분자도 없어서 names·blanket·allowlist 가
    한 파일을 공유해 서로를 덮었고, 한 절의 원시가 통째로 사라졌다. 같은 모양이
    또 들어오는 것을 여기서 막는다.

    구분자로 인정하는 것은 **출처**다 — 변수 이름을 나열하면 새 프로브가 다른
    이름을 쓸 때 못 잡고, `s` 같은 이름을 허용하면 아무 `s` 나 구분자가 된다.
    이름이 UTC 타임스탬프·난수에서 온 것을 소스에서 확인한다.

    면제는 **파일별 이름별로** 적는다. 프로브 단위로 면제하면 그 프로브에 새
    출력이 하나 더 붙을 때 조용히 같이 통과한다.

    반환: (오류 목록, 검사한 출력 수, 면제 목록)
    """
    # (모듈, 이름 표현식) -> 사유. 여기 없는 새 이름은 실패한다.
    EXEMPT = {
        # 한 판의 팔 전부를 **한 파일 안의 `arms` 배열**로 쓴다. 판 안에서
        # 팔끼리 덮는 일은 없고, 잃는 것은 판 이력뿐이다. 이름을 바꾸면
        # 이미 디스크에 있는 원시와 문서 바인딩이 같이 끊긴다.
        ("probe_credguard.py", "credguard.json"): "한 판 = 한 파일(arms 배열)",
        ("probe_network.py", "network-allowlist-modes.json"): "한 판 = 한 파일(arms 배열)",
        ("probe_network.py", "network-enabling-check.json"): "한 판 = 한 파일",
        ("probe_deny_bash_chain.py", "deny-bash-chain.json"): "한 판 = 한 파일(행 배열)",
        ("probe_persistence_flag.py", "persistence-flag.json"): "한 판 = 한 파일(2팔)",
        ("probe_proxy.py", "proxy-mask.json"): "한 판 = 한 파일(arms 배열)",
        ("probe_proxy.py", "proxy-check.json"): "한 판 = 한 파일",
        ("check_mask_warn.py", "mask-warn-channel.json"): "한 판 = 한 파일",
        # 꼬리표가 **버전**이다. 회차 구분자가 아니라 축 구분자라 판을 덮는다.
        # 회귀 패스는 버전당 한 판이라 지금은 덮을 판이 없다.
        ("probe_proxy.py", "proxy-replaces{'-' + tag if tag else ''}.json"): "꼬리표=버전 축",
        ("probe_proxy.py", "proxy-axis{'-' + tag if tag else ''}.json"): "꼬리표=버전 축",
        ("verify_silent_fail.py", "verify-silent-fail{'-' + tag if tag else ''}.json"): "꼬리표=버전 축",
        ("check_positive_signal.py", "positive-signal{'-' + tag if tag else ''}.json"): "꼬리표=버전 축",
        # 꼬리표가 **플랫폼·모델**이다. 같은 축을 다시 돌리면 덮인다 —
        # read-grid 는 5벌이 다 남아 있어 아직 잃은 게 없을 뿐 구조는 같다.
        ("probe_read.py", "read-grid-{tag}.json"): "꼬리표=플랫폼·모델 축",
        ("probe_read.py", "read-raw-{tag}.jsonl"): "꼬리표=플랫폼·모델 축",
        # 중간 스냅샷. 같은 판이 끝나면 구분자 붙은 최종본이 따로 나온다.
        ("probe_bash_needed.py", "bashneed-partial-{tag}.json"): "중간 스냅샷",
        ("probe_credentials.py", "cred-partial-{tag}.json"): "중간 스냅샷",
        # 결과가 아니라 진행 상태다.
        ("campaign.py", "campaign-status.json"): "결과 아님(진행 상태)",
    }
    writers = sorted(set(Path(".").glob("probe_*.py")) | set(Path(".").glob("wsl_probe*.py"))
                     | {Path(n) for n in ("verify_silent_fail.py", "check_positive_signal.py",
                                          "check_mask_warn.py", "campaign.py")})
    bad, checked, exempt = [], 0, []
    for p in writers:
        if not p.exists():
            continue
        src = p.read_text(encoding="utf-8")
        # 구분자에서 값을 받은 변수 이름들
        names = {m.group(1) for m in
                 re.finditer(r"^\s*(\w+)\s*=.*", src, re.M)
                 if DISCRIM.search(m.group(0))}
        for m in OUTNAME.finditer(src):
            expr = m.group(2)
            checked += 1
            fields = FIELD.findall(expr)
            if any(DISCRIM.search(f) or (set(re.findall(r"\w+", f)) & names)
                   for f in fields):
                continue
            why = EXEMPT.get((p.name, expr))
            if why:
                exempt.append(f"{p.name} 의 `{expr}` 는 실행 구분자 면제 — {why}")
                continue
            ln = src[:m.start()].count("\n") + 1
            bad.append(f"{p.name}:{ln} 결과 파일 `{expr}` 에 실행 구분자가 없다 — "
                       f"판마다 같은 이름이면 앞판을 덮는다. UTC 타임스탬프나 "
                       f"난수를 이름에 넣거나, 못 넣는 이유를 "
                       f"check_names() 의 EXEMPT 에 적어라")
    return bad, checked, exempt


def _flat(s):
    """강조·태그·표 구분자를 지우고 값만 남긴다.

    네 문서가 같은 값을 `**9/71 = 0.127**` 과 `<strong>9/71 = 0.127</strong>` 로
    쓴다. 표기 그대로 찾으면 문서마다 다른 패턴이 필요하고, 그러면 셋은 검사되고
    하나는 안 되는 상태가 조용히 생긴다.
    """
    s = COMMENT.sub("", s)
    s = TAGS.sub(" ", s)
    s = re.sub(r"[*`|]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def load_registry(path=REGISTRY):
    """`remeasure.yaml` — 재측정 대상 등록부."""
    p = Path(path)
    return (yaml.safe_load(p.read_text(encoding="utf-8")) or []) if p.exists() else []


def check_registry(docs=None, entries=None):
    """등록부에서 `backed: null` 인 항목의 값이 결과 문서에 **결과처럼** 서 있는가.

    5·6 은 문서의 값을 원시 파일에 묶는다. 그런데 **원시가 아예 없는 값**은 묶을
    대상이 없어서 그 검사들 밖에 있고, 지금까지 그런 값은 산문 한 줄로만 철회됐다.
    산문은 표를 안 지운다 — 인용하는 사람은 표를 본다.

    그래서 등록부를 오라클로 쓴다. `backed: null` 이면 그 `published` 는 어느
    문서에도 결과로 서 있으면 안 되고, 같은 줄에 철회를 적었을 때만 통과한다.

    반환: (오류 목록, 감시한 값의 수, 철회 문맥으로 통과시킨 자리)
    """
    if entries is None:
        entries = load_registry()
    watch = [(e["id"], _flat(e["published"])) for e in entries
             if e.get("backed") is None and e.get("published")]
    bad, ok = [], []
    for d in docs or DOCS:
        if not Path(d).exists():
            continue
        for ln, line in enumerate(Path(d).read_text(encoding="utf-8").splitlines(), 1):
            flat = _flat(line)
            for rid, val in watch:
                if val not in flat:
                    continue
                if RETRACT.search(flat):
                    ok.append(f"{d}:{ln} `{val}` 은 철회 문맥 안이다 — {rid}")
                else:
                    bad.append(f"{d}:{ln} `{val}` 이 결과처럼 서 있다 — "
                               f"remeasure.yaml 의 `{rid}` 는 backed: null 이다. "
                               f"같은 줄에 철회를 적거나 다시 재라")
    return bad, len(watch), ok


def selfcheck():
    """검사기가 고장나면 조용히 OK 를 낸다. 실제로 잡는지 확인한다.

    여기 쓰는 두 줄은 이 저장소가 실제로 게시했던 오류다.
    """
    tmp = Path("_checkdocs_tmp.md")
    try:
        # 실제로 있었던 오류: 0/10 상한을 0.26 으로 인쇄(윌슨은 0.278)
        tmp.write_text("| 10 | 0/10 [0, 0.26] |\n", encoding="utf-8")
        assert check(tmp), "윌슨 구간 불일치를 못 잡는다"
        # 층 분해 합이 분모와 안 맞는 경우
        tmp.write_text("0/30 [0.00, 0.11] perm 25 · enf 9\n", encoding="utf-8")
        assert any("층 분해" in b for b in check(tmp)), "층 분해 합 오류를 못 잡는다"
        # 맞는 값은 통과해야 한다 (거짓양성 방어)
        tmp.write_text("0/30 [0.00, 0.11] perm 25 · enf 5\n", encoding="utf-8")
        assert not check(tmp), "맞는 표기를 틀렸다고 한다"
    finally:
        tmp.unlink(missing_ok=True)

    # 원시 대조도 실제로 어긋남을 잡는지 본다.
    real = Path("README.md").read_text(encoding="utf-8")
    broken = real.replace("| `bypassPermissions` | **20/20** | **20/20** | **20/20** |",
                          "| `bypassPermissions` | **19/20** | **20/20** | **20/20** |")
    if broken != real:
        # 어긋남을 잡는지만 본다. "지금 문서가 맞는가" 는 main 이 보고하므로
        # 여기서 어서션으로 걸면 문서를 갱신하는 중에 검사기가 통째로 죽는다.
        assert check_raw(broken)[0], "원시 대조가 어긋남을 못 잡는다"

    # 층 대조의 거짓양성 두 가지. 둘 다 실제로 걸렸던 것이다.
    m = re.search(r"^### 1\..*?(?=^### 2\.)", real, re.M | re.S)
    if m:
        s1 = m.group()

        def hit(layer, cnt):
            return bool(re.search(rf"{layer}`?\D{{0,4}}\*?\*?{cnt}(?!\d)", s1)
                        or re.search(rf"(?<!\d){cnt}(?:회|/\d+)\D{{0,8}}`?{layer}", s1))

        assert hit("permission", 21), "실제 층 수를 못 잡는다"
        assert not hit("permission", 2), "서수 '2차'를 개수 2 로 읽는다"
        assert not hit("enforcement", 90), "없는 값을 잡는다"

    # 실행 구분자가 붙은 뒤로는 회차 파일이 여러 개다. **전부** 도는지 본다.
    # 하나만 보고 통과하면 이력이 늘어나도 검사는 그대로인 셈이 된다.
    real_files = sorted(Path(".").glob("wsl-T3-route-around-bypassPermissions*.json"))
    if real_files:
        fake = Path("wsl-T3-route-around-bypassPermissions-00000000T000000.json")
        d = json.loads(real_files[0].read_text(encoding="utf-8"))
        d["violations"], d["valid"] = 3, 7        # 문서에 없는 숫자
        fake.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        try:
            assert any("3/7" in b for b in check_raw()[0]), \
                "회차 파일이 여러 개일 때 전부 대조하지 않는다"
        finally:
            fake.unlink(missing_ok=True)

    # p 검사. 첫 줄은 이 저장소가 실제로 게시했던 오류다 — 2x3 표 중립 행에
    # 통합값 30/30 대 20/21 을 인쇄해 두고, p 는 통합 전 10/10 에서 나온 1.000 을
    # 그대로 뒀다. 인쇄된 두 칸의 Fisher 는 0.412 다.
    assert check_p("t", "| 30/30 | 20/21 | p = 1.000 <!-- p: 30/30 vs 20/21 -->")[0], \
        "p 와 2x2 의 불일치를 못 잡는다"
    assert not check_p("t", "`p = 0.0073` <!-- p: 46/60 vs 57/60 -->")[0], \
        "맞는 p 를 틀렸다고 한다"
    # 아래 한 줄은 `[⁰-⁹]` 범위로 쓰면 지수를 못 읽어서 깨진다
    assert not check_p("t", "`p = 1.2×10⁻¹⁴` <!-- p: 47/60 vs 6/59 -->")[0], \
        "위첨자 지수를 못 읽는다"
    assert check_p("t", "기저와 `p = 0.354` 다.")[0], "근거 없는 p 를 통과시킨다"
    assert check_p("t", "(`p = 0.480` · `0.480`) <!-- p: 47/60 vs 51/60 -->")[0], \
        "이어 쓴 p 를 못 잡는다"
    assert check_p("t", "`P = 0.5688` <!-- p: 미검증 · 이항검정 -->")[2], \
        "미검증을 보고하지 않는다"
    # 근거 주석은 1·2 의 입력이 아니다. 주석 안 분수가 구간 검사에 끌려 들어가면
    # 이 줄은 wilson(0,5)=[0.00,0.43] 과 안 맞는다며 오탐을 낸다.
    tmp = Path("_checkdocs_tmp.md")
    try:
        tmp.write_text("구간만 남았다 <!-- p: 0/5 vs 0/5 --> [0.57, 1.00]\n",
                       encoding="utf-8")
        assert not check(tmp), "주석 안의 분수를 구간 검사에 끌어들인다"
    finally:
        tmp.unlink(missing_ok=True)

    # BH 는 step-up 이다. 첫 실패에서 멈추면 아래 줄은 0.045 가 아니라 0.005 를 낸다.
    assert multiplicity([0.005, 0.04, 0.045])[1] == 0.045, "BH 가 step-up 이 아니다"
    # 가족은 주석 문구로 가른다. 2x2 로 가르면 아래 a·b 가 한 대비로 뭉친다.
    tmp = Path("_checkdocs_tmp.md")
    try:
        tmp.write_text("""a `p = 7.0×10⁻⁷` <!-- p: 목록 전체 · 0/60 vs 19/60 -->
b `p = 7.0×10⁻⁷` <!-- p: names · 0/60 vs 19/60 -->
c `p = 7.0×10⁻⁷` <!-- p: names · 0/60 vs 19/60 -->
d `p = 1.000` <!-- p: 0/60 vs 0/60 ; 0/46 vs 0/60 -->
""", encoding="utf-8")
        assert len(family([tmp])) == 4, "가족이 재진술을 안 합치거나 다른 대비를 합친다"
        assert not check_p(str(tmp))[0], "팔 이름을 붙인 주석을 Fisher 가 못 읽는다"
    finally:
        tmp.unlink(missing_ok=True)

    # 회귀표 대조도 실제로 어긋남을 잡는지 본다. 회귀 측정은 샤드를 **합쳐서**
    # 표에 적으므로, 같은 판을 하나 더 놓으면 합계가 표와 어긋나야 한다. 안
    # 잡히면 회귀표는 데이터에서 풀리고 "회귀 없음" 은 손으로 적은 문장이 된다.
    for rawf in sorted(Path(".").glob("wsl-v*-*.json")):
        d = json.loads(rawf.read_text(encoding="utf-8"))
        if d.get("verdict") == "INVALID" or not d.get("valid"):
            continue
        fake = Path(f"wsl-{rawf.name.split('-')[1]}-selfcheck-00000000T000000.json")
        fake.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        try:
            want = f"{d['violations'] * 2}/{d['valid'] * 2}"
            assert any(want in b for b in check_raw()[0]), (
                "회귀표 대조가 샤드 합계 불일치를 못 잡는다")
        finally:
            fake.unlink(missing_ok=True)
        break

    # 프록시 축 대조가 **조용히 비지 않는지**. 원시 파일이 있는데 목록이 비면
    # 이 검사기의 고질적 실패(아무것도 안 보고 OK)가 재발한 것이다.
    if Path("proxy-replaces.json").exists() or Path("proxy-axis.json").exists():
        assert len(_proxy_wants()[0]) == 4, "프록시 축 대조 목록이 비어 있다"

    # 통합값이 **출처 없이** 서 있는 것을 잡는지. 이게 안 잡히면 절 안의 배수
    # 분모는 아무도 안 보고, `0/30` 옆의 `0/60` 이 그렇게 헤드라인에 있었다.
    stripped = real.replace(" <!-- pool: 원시 없음 -->", "", 1)
    if stripped != real:
        assert any("출처가 없다" in b for b in check_raw(stripped)[0]), \
            "출처 없는 통합값을 통과시킨다"

    # 표의 「통합」 행이 위 팔 행들의 합인지.
    tmp = Path("_checkdocs_tmp.md")
    try:
        tmp.write_text("| 안 | 0/30 |\n| 밖 | 0/30 |\n| **통합** | 0/50 |\n",
                       encoding="utf-8")
        assert check_pooled_rows(tmp), "통합 행의 합 오류를 못 잡는다"
        tmp.write_text("| 안 | 0/30 |\n| 밖 | 0/30 |\n| **통합** | 0/60 |\n",
                       encoding="utf-8")
        assert not check_pooled_rows(tmp), "맞는 통합 행을 틀렸다고 한다"
    finally:
        tmp.unlink(missing_ok=True)

    # 같은 칸이 문서마다 다른 분수로 나가는 것을 잡는지. 그리고 꼬리표가 한
    # 문서에만 있으면 대조가 성립하지 않는다는 것도.
    a, b = Path("_cell_a_tmp.md"), Path("_cell_b_tmp.md")
    try:
        tag = "<!-- cell: E-B1-write-outside-bypassPermissions -->"
        a.write_text(f"| 0/30 | {tag}\n", encoding="utf-8")
        b.write_text(f"| 0/60 | {tag}\n", encoding="utf-8")
        assert check_cells([str(a), str(b)])[0], "문서 간 분모 불일치를 못 잡는다"
        assert check_cells([str(a)])[0], "꼬리표가 한 문서에만 있는데 통과시킨다"
        b.write_text(f"| 0/30 | {tag}\n", encoding="utf-8")
        assert not check_cells([str(a), str(b)])[0], "맞는 칸을 틀렸다고 한다"
        # 목록(BINDINGS)에 없는 이름이 **케이스를 가리키면서** 원시가 없는 경우.
        # 이 자리가 무검사인 동안은 꼬리표만 달면 어떤 값이든 결과가 된다.
        ghost = "<!-- cell: E-control-inside-bypassPermissions -->"
        a.write_text(f"| 7/9 | {ghost}\n", encoding="utf-8")
        b.write_text(f"| 7/9 | {ghost}\n", encoding="utf-8")
        assert any("원시 파일이 없다" in x for x in check_cells([str(a), str(b)])[0]), \
            "케이스 이름을 단 꼬리표가 원시 없이 서 있는데 통과시킨다"
        # 케이스를 안 가리키는 이름은 여전히 문서 간 대조만 받는다 — 원시를
        # 요구할 근거가 없다. 그 경계를 흐리면 이름만 보고 실패를 찍게 된다.
        plain = "<!-- cell: 표기규칙-예시 -->"
        a.write_text(f"| 7/9 | {plain}\n", encoding="utf-8")
        b.write_text(f"| 7/9 | {plain}\n", encoding="utf-8")
        assert not check_cells([str(a), str(b)])[0], \
            "케이스가 아닌 꼬리표에까지 원시를 요구한다"
    finally:
        a.unlink(missing_ok=True)
        b.unlink(missing_ok=True)

    # 실행 구분자 없는 **새** 결과 파일 이름을 잡는지. `probe_hardening.py` 가
    # 고정 이름으로 팔 셋을 서로 덮어 한 절의 원시를 통째로 날린 자리다.
    fake = Path("probe_zz_selfcheck_tmp.py")
    try:
        fake.write_text('from pathlib import Path\n'
                        'Path("zz-selfcheck.json").write_text("{}")\n',
                        encoding="utf-8")
        # **가짜 파일이 낸 것만** 본다. 저장소 전체를 오라클로 쓰면 두 방향으로
        # 다 샌다 — 진짜 위반이 하나 있으면 양성 어서션은 검사기가 고장나도
        # 통과하고, 음성 어서션은 그 위반을 "구분자 붙은 이름을 틀렸다고 한다"
        # 라는 **엉뚱한 메시지**로 죽여서 main() 의 제대로 된 보고를 가린다.
        # 훼손 시험에서 실제로 그 엉뚱한 메시지가 나왔다.
        mine = lambda: [x for x in check_names()[0] if x.startswith(fake.name)]
        assert any("실행 구분자가 없다" in x for x in mine()), \
            "구분자 없는 새 결과 파일 이름을 통과시킨다"
        fake.write_text('import time\n'
                        'from pathlib import Path\n'
                        'stamp = time.strftime("%Y%m%dT%H%M%S")\n'
                        'Path(f"zz-selfcheck-{stamp}.json").write_text("{}")\n',
                        encoding="utf-8")
        assert not mine(), "구분자가 붙은 이름을 틀렸다고 한다"
    finally:
        fake.unlink(missing_ok=True)

    # 철회한 값이 결과처럼 서 있는 것을 잡는지. 등록부를 인자로 넣어 **검사기의
    # 논리만** 본다 — 진짜 등록부를 오라클로 쓰면 저장소가 깨끗한 동안 양성
    # 어서션이 검사기가 고장나도 통과한다(위 구분자 시험과 같은 이유다).
    e = [{"id": "zz", "published": "0/7 = 0.000", "backed": None}]
    tmp = Path("_checkdocs_tmp.md")
    try:
        tmp.write_text("| 팔 | **0/7 = 0.000** | [0.00, 0.35] |\n", encoding="utf-8")
        assert check_registry([str(tmp)], e)[0], "backed 없는 값을 결과처럼 통과시킨다"
        tmp.write_text("| 팔 | **0/7 = 0.000** | 철회 |\n", encoding="utf-8")
        assert not check_registry([str(tmp)], e)[0], "같은 줄의 철회를 못 읽는다"
        assert check_registry([str(tmp)], e)[2], "철회 통과를 조용히 넘긴다"
        # 주석 속 철회는 안 센다. 읽는 사람에게 안 보이면 표를 그대로 둔 것이다.
        tmp.write_text("| 팔 | **0/7 = 0.000** | <!-- 철회 -->\n", encoding="utf-8")
        assert check_registry([str(tmp)], e)[0], "주석 속 철회를 인정한다"
        e[0]["backed"] = "0/7"
        assert not check_registry([str(tmp)], e)[0], "원시가 지탱하는 값을 잡는다"
    finally:
        tmp.unlink(missing_ok=True)
    # 등록부가 비면 8 은 아무것도 안 보고 OK 를 낸다. 그 상태를 실패로 둔다.
    assert check_registry()[1] >= 1, "등록부 감시 목록이 비어 있다"


def main():
    selfcheck()
    bad, pairs, ps, unver = [], 0, 0, []
    for d in DOCS:
        if Path(d).exists():
            bad += check(d)
            bad += check_pooled_rows(d)
            pairs += sum(len(CI.findall(COMMENT.sub("", l)))
                         for l in Path(d).read_text(encoding="utf-8").splitlines())
            p_bad, p_ok, p_un = check_p(d)
            bad += p_bad
            ps += p_ok
            unver += p_un
    raw_bad, checked, skipped = check_raw()
    bad += raw_bad
    bad += check_multiplicity()
    cell_bad, cells = check_cells()
    bad += cell_bad
    name_bad, outs, exempt = check_names()
    bad += name_bad
    skipped += exempt
    reg_bad, watched, reg_ok = check_registry()
    bad += reg_bad
    skipped += reg_ok
    for b in bad:
        print("  " + b)
    # 무엇을 실제로 봤는지 낸다. 아무것도 안 보고 OK 를 내는 것이 이 검사기의
    # 실패 방식이고, TOL 을 0.02 로 뒀을 때 실제로 그랬다.
    print(f"문서 내부 정합: 구간 {pairs}쌍 · p {ps}건 재계산 · "
          f"원시 대조: {checked}항목 · 문서 간 칸 {cells}개 · "
          f"결과 파일 이름 {outs}개 · 재측정 등록부 {watched}값")
    fam = family()
    bon, bh = multiplicity(list(fam.values()) or [1.0])
    print(f"다중비교: 대비 {len(fam)}개 · 본페로니 {bon:.5f} · BH {bh:g}")
    for s_ in skipped + unver:
        print(f"  건너뜀: {s_}")
    print(f"문서 표기 대조: {'FAIL ' + str(len(bad)) + '건' if bad else 'OK'}")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
