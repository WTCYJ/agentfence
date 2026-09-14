"""문서에 적힌 숫자가 실제 계산과 맞는가.

이 저장소가 반복해서 낸 실패는 **측정이 틀린 것이 아니라 표기가 측정과 어긋난
것**이다. 그중 둘은 한동안 게시된 채로 있었다.

    0/10 의 상한을 0.26 으로 인쇄  (윌슨은 0.278. Clopper-Pearson 값이 섞였다)
    dontAsk 칸을 `perm`+`enf` 로 표기  (실제로는 경쟁이고 25:5 다)

둘 다 사람이 눈으로 잡았다. 자기식별 누출을 selftest 어서션으로 막은 것과 같은
이유로, 이것도 검사로 막는다.

열일곱 가지를 본다.

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
    9. 영어 요약의 분수가 한국어 결과 문서에도 있는가        (문서 <-> 문서)
       `README.en.md` 는 요약이라 자기 출처가 없다 — 없으면 영어에만 사는 값이다
   10. `dataset/` 의 색인·정제본·확보 표가 실제와 맞는가       (문서 <-> 데이터)
       색인 <-> `cases/*.yaml` 1:1 · `schema.md` 가 요구하는 칸 ·
       확보 표 <-> `dataset/raw/` 의 실제 파일 수와 바이트
   11. 결과 파일의 버전 꼬리표가 파일 안 `agent_version` 과 같은가 (이름 <-> 내용)
   12. 개발용(`split: dev`) 계열에서 나온 칸이 그 표기 없이 서 있지 않은가 (색인 <-> 문서)
       `dataset/cases.yaml` 의 계열 split 이 오라클이다
   13. 정제본이 스키마 v1 한 갈래인가 (데이터 <-> 마이그레이션 표)
       최상위 `meta`·중첩 `provenance`·옛 칸 이름이 **재발하면** 실패한다
   14. 라이선스 고지와 상업 배포 판정이 세 자리에서 같은가 (LICENSE <-> NOTICE <-> 정제본)
       MIT 본문은 바이트 동일해야 한다
   15. 회차를 태우는 파일 전부가 `probes.yaml` 에 분류돼 있는가 (등록부 <-> 코드)
       게시근거인데 원시가 0 건인 프로브를 **건너뜀에 인쇄한다**
   16. 게시된 p 하나하나가 `p-family.yaml` 에 가설·원본·가족과 함께 있는가 (문서 <-> 등록부)
   17. 봉인 문서가 봉인 표시를 달고, 그것을 가리키는 **현행 줄**도 같이 다는가
       봉인은 인용 금지이지 **검사 면제가 아니다** — 봉인 문서의 p 도 4 를 받는다
   그리고 프록시 축 두 줄이 **다른 프로토콜**에서 왔다는 사실이 표에 붙어 있는가

3 이 없으면 1·2 는 "틀린 숫자가 자기 자신과는 일관된" 경우를 통과시킨다.

9 는 6 이 **꼬리표 붙은 칸만** 본다는 데서 온다. 꼬리표도 구간도 p 주석도 없는
영어 분수는 1·2·3·4·6·8 을 전부 빠져나간다 — 철회 사고 때 `README.en.md` 가
철회 전 수치를 이고 두 검사를 통과한 경로가 정확히 그것이다.

10 은 여태 `dataset/` 이 **어느 검사에도 안 걸려 있던** 자리다. 색인은 손으로
쓴 메타데이터 층이고, 확보 표의 파일 수·바이트는 감사가 한 번 재고 굳은 값이다 —
다시 세는 사람이 없으면 그 표에는 "쟀다" 는 서명만 남는다. `dataset/raw/` 는
`.gitignore` 라 없을 수 있는데, 그때는 **건너뛴 사실을 인쇄한다.** 조용히
통과시키는 것이 이 검사기의 고질적 실패다.

11 은 3 이 버전을 **파일 이름에서만** 읽는다는 데서 온다. 이름표와 실제 바이너리가
어긋나도 3 은 못 잡는다. 옛 원시에는 그 칸이 없으므로 소급하지 않고 건너뜀으로
인쇄한다 — 없는 것을 채워 넣지 않는다.

7 은 등록부(`remeasure.yaml`)가 부르는 프로브가 **결과 파일을 쓰는지**도 본다.
이름 검사는 이미 있는 쓰기 지점만 훑으므로, 쓰기가 아예 없는 프로브는 통째로
검사 밖이었다 — `fail-open-rate` 가 그렇게 원시 없이 헤드라인이 됐다.

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

**12~17 이 못 잡는 것** — 같이 적어 둔다. 장식이 되지 않게 경계를 분명히 한다.

    12 은 **계열 단위**만 본다. 하네스 장치의 오염은 안 잡는다 — stream-json
       포착과 스캔 기준선은 전 케이스에 걸리므로, eval 꼬리표가 붙은 칸도 판정
       도구는 dev 계열 결과로 조정된 물건이다. 검사로 만들 수 없다.
       꼬리표가 **없는** 인용 자리도 못 잡는다. 꼬리표를 단 줄만 본다.
    14 은 `distribution.commercial` 값이 **맞는지**는 못 본다. 값이 있고 열거
       안이고 세 자리가 일치하는지만 본다 — 상류가 실제로 그 라이선스인지는
       사람이 근거를 짚어야 한다(`poisoned-skills.yaml` 이 지금 그 상태다).
    15 의 `ledger: true` 는 "회차를 태운 기록이 있다" 이지 "그 축의 값이 원시에
       묶인다" 가 아니다. 특히 `probe_path_naming` 은 두 팔이 케이스·모드·모델
       까지 같아서 장부만으로는 원리적으로 못 가른다.
    미분류(`role: 미분류`)는 검사로 못 푼다. 게시 문서가 프로브 이름을 안 적어서
       파일만으로 안 갈린다. 검사는 "미분류가 있다" 를 인쇄할 수 있을 뿐이다.

    python check_docs.py            직접 실행
    python check_docs.py selfcheck  훼손 시험만
    python runner.py selftest       selftest 안에서도 돈다
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

from classify_refusals import fisher, wilson

# Windows 기본 콘솔은 cp949 라 판정줄의 `—` 에서 UnicodeEncodeError 가 난다.
# 검사는 다 통과한 뒤에 죽으므로 **통과가 종료코드 1 로 읽힌다** — 검사기가
# 거짓말을 하는 것으로 보이고, 그러면 사람이 검사를 안 믿는다. 검사 내용을
# 무르게 하는 것이 아니라 **출력**만 고친다.
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

# 소수 둘째 자리 반올림만 허용한다. 0.02 로 잡았더니 실제로 게시됐던 오류
# (0/10 상한을 0.26 으로 인쇄, 윌슨은 0.278, 차이 0.0175)를 통과시켰다 —
# 잡으라고 만든 것을 못 잡는 값이었다. selfcheck() 가 이걸 잡았다.
TOL = 0.01
# HARDENING.md 는 **결과물**인데 여태 검사 밖에 있었다. 실무자가 실제로
# 설정을 복사해 가는 문서라 여기가 틀리면 가장 나쁘다.
DOCS = ["README.md", "README.en.md", "artifact/results.html", "HARDENING.md"]
# `README.en.md` 는 결과를 새로 내지 않는다 — 한국어 결과 문서의 압축 요약이다.
# 그래서 영어의 모든 분수는 아래 문서 어딘가에 대응 값이 있어야 한다(검사 9).
EN_DOC = "README.en.md"
EN_SOURCES = ["README.md", "HARDENING.md"]

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
# `6.8e-11` 도 읽는다. 여태 안 읽어서 `p = 6.8e-11` 이 `p = 6.8` 로 보였다 —
# 지수가 조용히 떨어지면 0.000000000068 이 6.8 로 대조된다. 봉인 문서(검사 17)가
# 그 표기를 쓰고 있어서, 그 문서를 4 에 넣는 순간 이 구멍이 먼저 드러났다.
PVAL = re.compile(r"(?<![A-Za-z])[Pp]\s*=\s*(\d+(?:\.\d+)?)"
                  r"(?:\s*[×x]\s*10\s*([" + SUPS + r"]+)|[eE]([+-]?\d+))?")
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
# **인접한 조각은 한 이름으로 잇는다.** 줄이 길어 둘로 쪼갠
#     Path(f"refusals-{stem}-{model}-"
#          f"{stamp}.json")
# 는 여태 이 검사에 아예 안 보였다 — 안 보이는 이름은 면제 목록에도 안 떠서
# 아무도 못 알아챈다. 검사 7 이 조용히 절반만 돌던 자리다.
OUTNAME = re.compile(r"""(?:Path|open)\(\s*((?:f?(["'])(?:(?!\2).)*\2\s*)+)""")
OUTPART = re.compile(r"""f?(["'])((?:(?!\1).)*)\1""")
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

# ── 검사 12 · 개발용 계열 표기 ────────────────────────────────────────
# 헤드라인으로 서 있는 칸이 **개발용 계열**(`split: dev`)에서 나왔다. 그 사실이
# 게시 문서에 없으면 독립 평가 수치로 읽힌다 — dev 계열은 증인·영수증·후속
# 스캔·스캔 기준선·판정 도구가 전부 그 계열의 결과를 보고 조정된 계열이다.
# 오라클은 `dataset/cases.yaml` 이고 계열을 검사기에 베끼지 않는다.
SPLITNOTE = re.compile(r"<!--\s*split:\s*(\w+)\s*-->")
# 기계용 꼬리표 말고 **사람이 보는 표기**도 같은 줄에 있어야 한다. 꼬리표는 HTML
# 주석이라 읽는 사람에게 안 보인다 — 철회를 주석으로 적는 것을 금지한 것과 같은
# 이유다(위 RETRACT 주석 참조).
SPLITMARK = re.compile(r"개발용 계열|dev-split|dev · 독립 평가 아님")
# 12 만 쓰는 문서 범위. `DOCS` 자체를 늘리면 다른 여덟 검사의 범위가 같이 늘고
# 거기서 오탐이 난다(실측으로 확인했다 — `check_registry` 를 docs/90 으로 넓히면
# 거기 `10/10 = 1.000` 은 fail-open 이 아니라 haiku·opus 실행률인데 문자열이
# 같아서 철회 위반으로 잡힌다).
SPLIT_DOCS = DOCS + ["docs/01-project-overview.md",
                     "writeup/2026-08-12-agentfence.md"]

# ── 검사 14 · 라이선스 ────────────────────────────────────────────────
LICENSE_DOC = "LICENSE"
NOTICE_DOC = "NOTICE"
EXTERNAL_DOC = "dataset/external.md"
# MIT 정본 본문의 sha256(CRLF 정규화 후). 브리핑이 "MIT 표준 문안을 변형하지
# 마라" 를 요구하는데 여태 기계로 집행되지 않았다. 2026-09-10 정본과 바이트
# 동일함을 확인하고 그 해시를 박아 잠근다.
MIT_SHA = "6137a2dde18bb6f471a05da9d10ddc187b6f866658099e1b3b8e1dba02374512"
# 정정 이력은 **지우는 게 아니라** 상한으로 잡는다. 오인용이 근거로 다시 서면
# 횟수가 늘고, 정정 문단을 지우면 규칙 2 위반이다 — 그래서 0 이 아니라 상한이다.
MISCITE = "3(a)(3)"
MISCITE_CAP = {NOTICE_DOC: 2, EXTERNAL_DOC: 1}
# licensor 가 **지정한** 가명이다. 오타째 두는 것이 곧 이행이므로(CC BY
# 3(a)(1)(A)(i) "including by pseudonym if designated") 누가 "오타 수정" 으로
# `anonymous` 로 고치면 지정 표기가 훼손된다.
PSEUDONYM = "annoymous"
URI = re.compile(r"https?://[^\s`|)]+")

# ── 검사 15 · 프로브 등록부 ───────────────────────────────────────────
PROBES = "probes.yaml"

# ── 검사 16 · p 인벤토리 ──────────────────────────────────────────────
PFAMILY = "p-family.yaml"
RECOMPUTE = ("원시", "표기", "없음")

# ── 검사 17 · 봉인 문서 ───────────────────────────────────────────────
# 봉인 표시가 그 문서 머리에 실제로 있는가, 그리고 그것을 가리키는 **현행 줄**이
# 같이 표시를 다는가. 봉인은 인용 금지이지 검사 면제가 아니다 — 봉인 문서의 p 도
# 검사 4 를 받는다(정정 상자 자체가 현행 주장이라서다. 실제로 그 상자가 중립 경로
# p 를 1.000 으로 적고 있었고 인쇄된 2x2 의 Fisher 는 0.412 였다).
SEALED = {
    "docs/90-model-behavior-analysis.md": "이 문서는 봉인입니다",
    "docs/91-superseded-results.md": "인용하지 마",
}
# 봉인 문서를 가리키는 줄이 달아야 하는 표시.
SEALMARK = re.compile(r"인용 금지|인용하지 마|현행 결론 아님|봉인")

# ── 프로토콜 혼합 집계 ────────────────────────────────────────────────
# 프록시 축 두 줄은 아직 **다른 프로브·다른 스킴**에서 온다(TLS 대 평문). 그
# 사실이 표에 붙어 있지 않으면 두 줄은 한 실험으로 읽힌다. `proxy-axis.json` 이
# 생겨 한 파일에서 네 팔이 나오면 이 요구는 사라진다.
PROTO_SECTION = "커스텀 프록시를 켜면 허용 목록도"
PROTO_CONFOUND = "아직 한 실험이 아니다"


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
            # 꼬리표(파일 이름)와 내용이 서로를 검증한다. 여태 버전은 **이름**
            # 에서만 읽혔고, 이름과 실제 바이너리가 어긋나도 아무도 못 잡았다.
            # 옛 원시에는 이 칸이 없다 — 소급하지 않고 건너뛴 사실을 인쇄한다.
            ver_tag, av = ver_of(f.name), d.get("agent_version")
            if av is None:
                skipped.append(f"{f.name} 에 agent_version 이 없다 — 이름표를 "
                               f"내용으로 검증 못 함(그 칸을 싣기 전 판)")
            elif ver_tag and av != ver_tag:
                bad.append(f"{f.name} 의 이름표는 v{ver_tag} 인데 파일 안 "
                           f"agent_version 은 {av} 다 — 꼬리표와 내용이 다르다")
            acc = pool.setdefault(
                (ver_tag, Path(d["case"]).stem, d["mode"]), [0, 0])
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
    sup, sci = m.group(2), m.group(3)
    if sup is None and sci is None:
        d = len(mant.partition(".")[2])
        return float(mant), 0.5 * 10.0 ** -d * (1 + 1e-9)
    e = int(sup.translate(SUPTRANS)) if sup is not None else int(sci)
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


def check_en_mirror(en=EN_DOC, sources=None, text=None):
    """영어 요약에만 사는 분수가 있는가.

    앞의 여덟 검사는 영어 문서의 값을 세 갈래로만 본다 — 구간·비율 재계산(1·2)과
    p 재계산(4)은 **문서 안의 정합**이고, 원시 대조(3·5)는 `README.md` 와
    `HARDENING.md` 만 읽으며, 문서 간 칸(6)과 등록부(8)는 **꼬리표나 등록이 붙은
    값**만 본다. 그래서 다음 셋을 동시에 만족하는 영어 분수는 아무 검사도 안 받는다.

        같은 줄에 `<!-- cell: -->` 가 없다 · 뒤에 구간이 없다 · `<!-- p: -->` 에도 없다

    이건 가상의 구멍이 아니다. 철회 사고 때 `README.en.md` 가 철회 전 수치를 그대로
    이고 있었는데 두 검사 다 OK 를 냈고, 사람이 눈으로 대조해서야 찾았다. 훼손
    시험에서도 `29/29` 를 `19/19` 로 바꿔 놓고 통과했다.

    영어는 **결과를 새로 내지 않는다** — 한국어 결과 문서의 압축 요약이다. 그러니
    대응 값이 없는 영어 분수는 출처가 영어뿐이라는 뜻이고, 그게 이 사고의 모양이다.
    값이 맞는지는 여기서 안 본다(그건 1~8 의 일이다). 여기서 보는 것은 **어느
    한국어 문서가 그 값을 지탱하는가** 하나다.

    `HARDENING.md` 를 대조 범위에 넣는다. 네트워크 표의 `29/29` 와 마스킹 표의
    `11/11`·`0/11` 은 `README.md` 가 아니라 거기서 온다 — 지어낸 값이 아니라
    **형제 결과 문서가 지탱하는** 값이다.

    **주석 안의 값은 지탱으로 안 센다.** 이 저장소는 철회에 이미 같은 규칙을 쓴다
    (`RETRACT` 는 주석을 안 본다 — 읽는 사람에게 안 보이는 철회는 표를 그대로 둔
    것이다). 근거도 같다: 영어의 수치를 한국어로 확인하러 온 사람은 본문을 읽지
    HTML 주석을 안 읽는다. 주석에만 있는 값은 그 사람에게 없는 것과 같다. 지금
    `0/11` 이 `README.md` 에서는 `<!-- p: 5/5 vs 0/11 -->` 주석뿐이지만
    `HARDENING.md` 본문에 있어서 이 규칙으로도 통과한다.

    **바닥이지 천장이 아니다.** 보는 것은 "이 값이 한국어 어딘가에 있는가" 이지
    "이 값이 그 칸에서 왔는가" 가 아니다. 훼손 시험에서 `29/29` 를 `19/19` 로
    바꾸면 **통과한다** — 복제 절 산문의 "원본은 19/19 거부" 가 대신 만족시킨다.
    칸까지 묶는 것은 꼬리표(`<!-- cell: -->`)를 다는 6 의 일이고, 여기서 그걸
    흉내내면 위치 추측이 된다(p 를 위치로 안 짝지은 것과 같은 이유다).

    반환: (오류 목록, 대조한 분수 수)
    """
    sources = list(sources or EN_SOURCES)
    pool = {d: COMMENT.sub("", Path(d).read_text(encoding="utf-8"))
            for d in sources if Path(d).exists()}
    if not pool:
        return [f"{en} 를 대조할 한국어 결과 문서가 하나도 없다 ({sources}) — "
                f"대조가 성립하지 않는다"], 0
    if text is None:
        if not Path(en).exists():
            return [], 0
        text = Path(en).read_text(encoding="utf-8")
    bad, checked = [], 0
    for ln, line in enumerate(text.splitlines(), 1):
        for a, b in FRAC.findall(COMMENT.sub("", line)):
            checked += 1
            # 경계까지 본다. `in` 이면 `0/11` 이 `10/110` 안에서도 맞다고 읽힌다.
            pat = re.compile(rf"(?<!\d){a}\s*/\s*{b}(?!\d)")
            if any(pat.search(t) for t in pool.values()):
                continue
            bad.append(f"{en}:{ln} 의 {a}/{b} 가 영어에만 있다 — "
                       f"{' · '.join(sorted(pool))} 의 **본문**(HTML 주석 제외)에서 "
                       f"같은 값을 못 찾았다. 영어는 한국어 결과 문서의 요약이므로 "
                       f"대응 값이 있어야 한다. 한국어가 그 값을 산문으로만 적고 "
                       f"있으면 분수로도 적고, 애초에 근거가 없으면 영어에서 지워라")
    return bad, checked


def _outnames(src):
    """소스에서 결과 파일 이름 표현식을 `(표현식, 시작위치)` 로 낸다.

    이어붙인 조각을 합친 뒤 `.json`/`.jsonl` 로 끝나는 것만 결과 파일로 본다.
    """
    for m in OUTNAME.finditer(src):
        expr = "".join(p.group(2) for p in OUTPART.finditer(m.group(1)))
        if expr.endswith(".json") or expr.endswith(".jsonl"):
            yield expr, m.start()


def check_names(entries=None):
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

    `entries` 를 주면 그 등록부로만 본다 — selfcheck 의 훼손 시험 통로다.

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
                                          # classify_refusals 는 결과를 쓰는데 이 집합 밖이라
                                          # 이름 검사에 **보이지 않았다**. 지금 이름은 구분자를
                                          # 달고 있어 덮어쓰기 위험은 없지만, 검사가 없으면
                                          # 다음 사람이 구분자를 떼도 아무도 안 잡는다.
                                          "classify_refusals.py",
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
        for expr, pos in _outnames(src):
            checked += 1
            fields = FIELD.findall(expr)
            if any(DISCRIM.search(f) or (set(re.findall(r"\w+", f)) & names)
                   for f in fields):
                continue
            why = EXEMPT.get((p.name, expr))
            if why:
                exempt.append(f"{p.name} 의 `{expr}` 는 실행 구분자 면제 — {why}")
                continue
            ln = src[:pos].count("\n") + 1
            bad.append(f"{p.name}:{ln} 결과 파일 `{expr}` 에 실행 구분자가 없다 — "
                       f"판마다 같은 이름이면 앞판을 덮는다. UTC 타임스탬프나 "
                       f"난수를 이름에 넣거나, 못 넣는 이유를 "
                       f"check_names() 의 EXEMPT 에 적어라")
    # 재측정 등록부가 부르는 프로브는 **결과 파일을 써야 한다.** 위 루프는 이미
    # 있는 쓰기 지점만 보므로 쓰기가 아예 없는 프로브는 통째로 검사 밖이었다 —
    # `fail-open-rate` 가 그랬다. 회차를 태우고 콘솔로만 읽은 값이 헤드라인이
    # 됐고, 지탱할 원시가 **존재할 수 없었다.** 등록부에 명령을 적는 것은 "이걸
    # 다시 재면 그 칸이 산다" 는 약속이므로 여기서 그 약속을 검사한다.
    for ent in (load_registry() if entries is None else entries):
        cmd = ent.get("command") or ""
        mods = sorted(set(re.findall(r"\b(\w+\.py)\b", cmd)))
        if not mods:
            exempt.append(f"{REGISTRY} 의 `{ent.get('id')}` 명령은 셸 스크립트라 "
                          f"프로브를 직접 못 짚는다 — 결과 쓰기 대조 안 됨")
            continue
        for mod in mods:
            mp = Path(mod)
            if not mp.exists():
                bad.append(f"{REGISTRY} 의 `{ent.get('id')}` 가 부르는 {mod} 이 없다")
                continue
            checked += 1
            if not any(_outnames(mp.read_text(encoding="utf-8"))):
                bad.append(f"{REGISTRY} 의 `{ent.get('id')}` 가 {mod} 을 부르는데 "
                           f"그 프로브는 결과 파일을 안 쓴다 — 콘솔에서 읽은 값은 "
                           f"원시에 못 묶는다")
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
    # **독립성 표기.** `independence` 가 붙은 항목은 원시가 지탱해도(backed 있음)
    # 독립 평가 수치가 아니다 — 다시 재도 회귀 재현이지 독립 평가가 아니다. 그
    # 값이 게시 문서에 서 있으면 같은 줄에 철회나 개발용 표기가 있어야 한다.
    indep = [(e["id"], _flat(e["published"])) for e in entries
             if e.get("independence") and e.get("published")]
    bad, ok = [], []
    for d in docs or SPLIT_DOCS:
        if not Path(d).exists():
            continue
        for ln, line in enumerate(Path(d).read_text(encoding="utf-8").splitlines(), 1):
            flat = _flat(line)
            # 철회 감시는 결과 문서(DOCS)만 본다 — 넓히면 오탐이 난다(docs/90 의
            # `10/10 = 1.000` 은 fail-open 이 아니라 haiku·opus 실행률이다).
            # 인자로 문서를 주면 그대로 따른다(selfcheck 의 훼손 시험 통로).
            for rid, val in (watch if docs is not None or d in DOCS else []):
                if val not in flat:
                    continue
                if RETRACT.search(flat):
                    ok.append(f"{d}:{ln} `{val}` 은 철회 문맥 안이다 — {rid}")
                else:
                    bad.append(f"{d}:{ln} `{val}` 이 결과처럼 서 있다 — "
                               f"remeasure.yaml 의 `{rid}` 는 backed: null 이다. "
                               f"같은 줄에 철회를 적거나 다시 재라")
            for rid, val in indep:
                if val not in flat:
                    continue
                if RETRACT.search(flat) or SPLITMARK.search(flat):
                    ok.append(f"{d}:{ln} `{val}` 은 독립성 표기 안이다 — {rid}")
                else:
                    bad.append(f"{d}:{ln} `{val}` 이 독립 평가 수치처럼 서 있다 — "
                               f"remeasure.yaml 의 `{rid}` 에 `independence` 가 "
                               f"적혀 있다. 같은 줄에 `개발용 계열` 표기나 철회를 "
                               f"적어라")
    return bad, len(watch) + len(indep), ok


# ── 검사 10 · 데이터셋 ────────────────────────────────────────────────
# `dataset/` 은 여태 아무 검사도 안 받았다. 색인·정제본·확보 표는 전부 손으로 쓴
# 값이고, 이 저장소가 반복해서 낸 실패가 정확히 그 모양이다 — 산문은 맞는데
# 인용되는 자리가 안 따라간다. 셋을 묶는다: 색인 <-> `cases/`,
# 색인 <-> `schema.md` 의 필수 칸, 확보 표 <-> `dataset/raw/` 의 실제 파일·바이트.
DATASET_INDEX = "dataset/cases.yaml"
SCHEMA_DOC = "dataset/schema.md"
NORMALIZED = "dataset/survey/normalized"
SURVEY_DOC = "dataset/survey/README.md"
RAW_DIR = "dataset/raw"
# 표의 값 칸이 통째로 백틱 대안들이면 그것이 열거형이다. 열거를 검사기에 베껴
# 두면 schema.md 와 갈라진다 — 문서를 오라클로 쓴다.
ENUMCELL = re.compile(r"^`[^`]+`(?:\s*\|\s*`[^`]+`)+$")
# 확보 표의 한 행: `| CIPR | `cipr` | 2,685 | 127,363,137 | …`
HAVEROW = re.compile(r"^\|[^|\n]+\|\s*`([\w.-]+)`\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|", re.M)
# 정제본에서 고정점으로 인정하는 칸. 자료마다 이름이 다르다(VCS 없는 것은 md5).
FIXPOINT = ("commit", "upstream_version", "file_md5")


def _md_table(text, header):
    """`header` 줄로 시작하는 마크다운 표의 데이터 행을 셀 리스트로 낸다.

    표를 헤더 문자열로 집는다. 같은 문서에 열 이름이 다른 표가 여럿 있어서
    (`| 채울 것 | 어디에 | 없으면 |`) 위치로 집으면 문서를 고칠 때 조용히 다른
    표를 읽는다. 셀 안의 이스케이프된 파이프는 구분자가 아니다.
    """
    rows, seen = [], False
    for line in text.splitlines():
        if not seen:
            seen = line.strip() == header
            continue
        if not line.strip().startswith("|"):
            break
        if set(line.replace("|", "").strip()) <= set("-: "):
            continue
        rows.append([c.strip().replace("\\|", "|")
                     for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))])
    return rows


def _enum(cell):
    return [t.strip("` ") for t in cell.split("|")]


def _migrate():
    """마이그레이션 스크립트를 import 한다. 개명표와 중복키 로더가 거기 있다.

    베끼지 않는 이유는 `_md_table` 로 `schema.md` 를 읽는 것과 같다 — 두 벌이
    되면 갈리고, 갈린 쪽이 조용히 이긴다.
    """
    import importlib.util
    if _migrate.mod is None:
        p = Path("dataset/survey/migrate_normalized.py")
        if not p.exists():
            return None
        spec = importlib.util.spec_from_file_location("_migrate_normalized", p)
        _migrate.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_migrate.mod)
    return _migrate.mod


_migrate.mod = None


def _rename_table():
    m = _migrate()
    return dict(m.RENAME) if m else {}


def _load_strict(text, name):
    """중복 키를 예외로 내는 로더. 없으면 `safe_load` 로 떨어진다.

    중복 키는 `safe_load` 가 **조용히 뒤엣것으로 덮는다.** 정제본은 손으로 쓴
    파일이라 그 사고가 실제로 일어날 수 있고, 덮인 값은 아무 데도 안 남는다.
    """
    m = _migrate()
    if m is None:
        return yaml.safe_load(text)
    return m.load_strict(text)


def _norm_block(d):
    """정제본의 출처 블록. **v1 은 최상위 `provenance` 한 갈래다**(2026-09-10 통일).

    예전에는 최상위 `provenance` · 최상위 `meta` · `meta.provenance` 세 갈래가
    공존했고(11 개 중 6/4/1) 이 함수가 **어느 갈래든 찾아** 주었다. 그 관용이
    통일을 강제하지 않았다 — 다음 자료가 옛 갈래로 들어와도 통과했다. 관용을
    지우는 것이 검사 13 이다.
    """
    b = d.get("provenance")
    return b if isinstance(b, dict) else {}


def _norm_bad(name, d):
    """정제본 하나가 스키마 v1 한 갈래이고 라이선스·고정점을 다는가. (검사 13)

    `schema.md` 「origin: external」이 승격에 요구하는 넷 중 둘이 라이선스와
    고정점이다. 나머지 둘(`upstream_id` · `what_it_does_not_test`)은 사례 단위라
    승격 시점에 본다.

    갈래 강제는 개명표를 **마이그레이션 스크립트에서 import** 한다. 두 벌로
    베끼면 반드시 갈리고, 갈린 쪽이 조용히 이긴다.
    """
    out = []
    if "meta" in d:
        out.append(f"{name} 에 최상위 `meta` 가 남아 있다 — 정제본 스키마 v1 은 "
                   f"최상위 `provenance` 한 갈래다 "
                   f"(`dataset/survey/README.md` 「정제본 스키마 v1」)")
    if "what_this_source_does_not_test" in d:
        out.append(f"{name} 의 `what_this_source_does_not_test` 는 v1 에서 "
                   f"`what_it_does_not_test` 다 — 이름이 갈렸다")
    if d.get("schema_version") != 1:
        out.append(f"{name} 에 `schema_version: 1` 이 없다 "
                   f"(지금 {d.get('schema_version')!r}) — 다음 자료가 따를 판이 "
                   f"파일 안에 없으면 갈래가 또 늘어난다")
    b = _norm_block(d)
    if not b:
        if "provenance" in d:
            out.append(f"{name} 의 `provenance` 가 매핑이 아니다")
        else:
            out.append(f"{name} 에 최상위 `provenance` 블록이 없다")
        return out
    if isinstance(b.get("provenance"), dict):
        out.append(f"{name} 의 `provenance` 가 한 겹 더 중첩됐다 — 한 겹 벗겨라")
    for old, new in sorted(_rename_table().items()):
        if old in b:
            out.append(f"{name} 의 출처 블록에 옛 칸 `{old}` 가 남아 있다 — "
                       f"v1 은 `{new}` 다")
    if not b.get("license"):
        out.append(f"{name} 의 출처 블록에 `license` 가 없다 — 확인 못 했으면 `unknown` 이라고 적는다")
    if not any(b.get(k) for k in FIXPOINT):
        out.append(f"{name} 의 출처 블록에 고정점이 없다 ({' · '.join(FIXPOINT)} 중 하나)")
    return out


def check_dataset(entries=None, schema=None, survey=None):
    """`dataset/` 의 색인·정제본·확보 표가 실제와 맞는가. (검사 10)

    인자를 주면 그 값으로만 본다 — selfcheck 가 훼손된 입력을 넣기 위한 통로다.
    저장소가 깨끗한 동안 진짜 파일을 오라클로 쓰면, 검사기가 고장나도 어서션이
    통과한다(이 파일의 다른 훼손 시험과 같은 이유).

    반환: (오류 목록, 검사 항목 수, 건너뜀 목록)
    """
    bad, checked, skipped = [], 0, []
    if entries is None:
        entries = yaml.safe_load(Path(DATASET_INDEX).read_text(encoding="utf-8"))
    if schema is None:
        schema = Path(SCHEMA_DOC).read_text(encoding="utf-8")
    if survey is None:
        survey = Path(SURVEY_DOC).read_text(encoding="utf-8")

    # ① 색인 <-> cases/*.yaml 1:1. 한쪽에만 있으면 "출처 없이 도는 케이스" 이거나
    #    "안 도는 출처" 다. 둘 다 데이터셋이 아니다.
    ids = [e.get("case_id") for e in entries]
    files = {p.stem for p in Path("cases").glob("*.yaml")}
    for cid in sorted(set(ids) - files):
        bad.append(f"{DATASET_INDEX} 의 `{cid}` 에 맞는 cases/{cid}.yaml 이 없다")
    for cid in sorted(files - set(ids)):
        bad.append(f"cases/{cid}.yaml 이 {DATASET_INDEX} 색인에 없다 — 출처 없는 케이스")
    for cid in sorted({c for c in ids if ids.count(c) > 1}):
        bad.append(f"{DATASET_INDEX} 에 `{cid}` 가 두 번 있다")
    checked += len(ids) + len(files)

    # ② schema.md 가 요구하는 칸과 열거값. 목록을 **문서에서 읽는다** —
    #    검사기에 베껴 두면 스키마를 고칠 때 갈라지고, 갈라진 쪽이 조용히 이긴다.
    top = [(c[0].strip("`"), c[2]) for c in _md_table(schema, "| 필드 | 필수 | 값 |")
           if len(c) >= 3 and "✓" in c[1]]
    sub = [(c[0].strip("`"), c[1]) for c in _md_table(schema, "| 하위 필드 | 값 |")
           if len(c) >= 2]
    # `outcome` 열거도 문서에서 읽는다. 표 머리가 다르므로 따로 집는다.
    outcomes = {r[0].strip("` ") for r in
                _md_table(schema, "| `outcome` | 뜻 |") if r}
    if not top or not sub:
        skipped.append(f"{SCHEMA_DOC} 의 필드 표를 못 찾았다 — 필수 칸 대조 안 됨")
    if not outcomes:
        skipped.append(f"{SCHEMA_DOC} 의 `outcome` 표를 못 찾았다 — 대조 안 됨")
    for e in entries:
        cid = e.get("case_id", "?")
        prov = e.get("provenance")
        for where, need, src in (("", top, e), ("provenance.", sub, prov)):
            if not isinstance(src, dict):
                bad.append(f"{cid} 의 `provenance` 가 매핑이 아니다")
                break
            for name, cell in need:
                checked += 1
                if name not in src:
                    bad.append(f"{cid} 에 필수 칸 `{where}{name}` 이 없다 ({SCHEMA_DOC})")
                elif ENUMCELL.match(cell) and str(src[name]) not in _enum(cell):
                    bad.append(f"{cid} 의 `{where}{name}` 이 {_enum(cell)} 밖이다: "
                               f"{src[name]!r}")

    # ③ 스키마가 적은 건수. 사례를 늘리고 문장을 안 고치는 것이 이 저장소의
    #    흔한 실패다(확보 전 추정치가 갱신되지 않는 것과 같은 부류).
    m = re.search(r"지금\s*(\d+)\s*건", schema)
    if m:
        checked += 1
        if int(m.group(1)) != len(entries):
            bad.append(f"{SCHEMA_DOC} 는 색인이 {m.group(1)} 건이라 적었는데 "
                       f"실제는 {len(entries)} 건")
    else:
        skipped.append(f"{SCHEMA_DOC} 에 「지금 N 건」 문장이 없다 — 건수 대조 안 됨")

    # ④ 정제본. `yaml.safe_load` 를 통과하는가(survey/README 가 그렇게 적었다)와
    #    라이선스·고정점이 있는가.
    norm = sorted(Path(NORMALIZED).glob("*.yaml"))
    for p in norm:
        checked += 1
        # **줄끝.** `.gitattributes` 가 `*.yaml` 을 안 덮으므로 이 검사만이 방벽이다.
        # 섞이면 체크아웃 한 번에 파일 전체가 diff 로 뜨고 마이그레이션 검증이
        # 줄 단위로 어긋난다.
        if p.read_bytes().count(b"\r\n"):
            bad.append(f"{p.as_posix()} 에 CRLF 가 섞였다 — 정제본은 LF 다")
        try:
            d = _load_strict(p.read_text(encoding="utf-8"), p.name)
        except (yaml.YAMLError, ValueError) as ex:
            # 중복 키는 `safe_load` 가 조용히 덮는다. 엄격 로더는 ValueError 다.
            bad.append(f"{p.as_posix()} 파싱 실패: {ex.__class__.__name__}: {ex}")
            continue
        d = d if isinstance(d, dict) else {}
        bad += _norm_bad(p.name, d)
        # 정제본의 `cases[]` 도 색인과 **같은 열거**를 받는다. 여태 검사 ② 는
        # `dataset/cases.yaml` 에만 걸려 있어서 여기가 사각지대였다 — 열거 밖
        # 값(`origin: agentcanary` 18 건 · `outcome: block` 16 건)이 거기 있었다.
        # `case_id` 가 있는 항목만 본다. 상류 요약(`case_candidates` 중 일부)은
        # 모양이 달라 전부 걸면 오탐이 쏟아진다. `not_ported`/`not_normalized` 는
        # **옮기지 않기로 한 레코드**라 애초에 대상이 아니다.
        for key in ("cases", "case_candidates"):
            for c in d.get(key) or []:
                if not isinstance(c, dict) or "case_id" not in c:
                    continue
                for where, need, src in (("", top, c),
                                         ("provenance.", sub, c.get("provenance"))):
                    if not isinstance(src, dict):
                        bad.append(f"{p.name} 의 `{c['case_id']}` 에 "
                                   f"`provenance` 매핑이 없다")
                        break
                    for name, cell in need:
                        checked += 1
                        if name not in src:
                            bad.append(f"{p.name} 의 `{c['case_id']}` 에 필수 칸 "
                                       f"`{where}{name}` 이 없다 ({SCHEMA_DOC})")
                        elif ENUMCELL.match(cell) and str(src[name]) not in _enum(cell):
                            bad.append(f"{p.name} 의 `{c['case_id']}` 의 "
                                       f"`{where}{name}` 이 {_enum(cell)} 밖이다: "
                                       f"{src[name]!r}")
                checked += 1
                o = (c.get("expected_policy") or {}).get("outcome")
                if outcomes and o not in outcomes:
                    bad.append(f"{p.name} 의 `{c['case_id']}` 의 "
                               f"`expected_policy.outcome` 이 {sorted(outcomes)} "
                               f"밖이다: {o!r}")

    # ⑤ 확보 표 <-> 디스크. 파일 수와 바이트를 문서에 적어 두고 아무도 다시 안
    #    세면, 그 표는 "감사가 쟀다" 는 서명만 남고 값은 굳는다.
    rows = HAVEROW.findall(survey)
    checked += 1
    if len(rows) != len(norm):
        bad.append(f"{SURVEY_DOC} 확보 표는 {len(rows)} 행인데 정제본은 {len(norm)} 개다")
    for label, count in re.findall(r"(실제 확보|정제본)\s*(\d+)\s*[건개]", survey):
        checked += 1
        if int(count) != len(rows):
            bad.append(f"{SURVEY_DOC} 의 「{label} {count}」 가 확보 표 {len(rows)} 행과 다르다")
    root = Path(RAW_DIR)
    if not root.is_dir():
        skipped.append(f"{RAW_DIR} 가 없다(.gitignore) — 확보 표의 파일 수·바이트 대조 안 됨")
    else:
        for name, nf, nb in rows:
            checked += 1
            d = root / name
            if not d.is_dir():
                bad.append(f"{SURVEY_DOC} 확보 표의 `{name}` 이 {RAW_DIR} 에 없다")
                continue
            # `.git` 은 빼고 센다 — 확보 표가 그렇게 잰 값이다(README 그 절).
            fs = [f for f in d.rglob("*") if f.is_file() and ".git" not in f.parts]
            got = (len(fs), sum(f.stat().st_size for f in fs))
            if got != (int(nf.replace(",", "")), int(nb.replace(",", ""))):
                bad.append(f"{SURVEY_DOC} 확보 표의 `{name}` 이 디스크와 다르다: "
                           f"표 {nf}파일 {nb}B · 실제 {got[0]}파일 {got[1]}B")
    for name, _, _ in rows:
        checked += 1
        if not (Path(NORMALIZED) / f"{name}.yaml").exists():
            bad.append(f"{SURVEY_DOC} 확보 표의 `{name}` 에 맞는 정제본 "
                       f"{NORMALIZED}/{name}.yaml 이 없다")
    return bad, checked, skipped


# ── 검사 12 · 개발용 계열 표기 ────────────────────────────────────────
def _split_index(index=None):
    """{case_id: 계열 split} 과 계열 안 불일치.

    split 은 사례에 붙지만 **판단 단위는 계열**이다. 한 계열의 대조군(`control`)
    은 그 계열의 팔이라 split 이 `control` 인 것이 정상이므로, 계열의 split 은
    `control` 을 뺀 나머지로 정한다. 여기를 안 빼면 지금 색인의 계열 셋이 전부
    "계열 안에서 split 이 갈린다" 로 잡힌다 — 조사 보고가 요구한 그대로 걸면
    첫 실행에서 오탐 셋이 나온다.
    """
    if index is None:
        index = yaml.safe_load(Path(DATASET_INDEX).read_text(encoding="utf-8"))
    fam, bad = {}, []
    for e in index:
        s = e.get("split")
        if s == "control":
            continue
        fam.setdefault(e.get("family_id"), set()).add(s)
    for f, ss in sorted(fam.items(), key=lambda x: str(x[0])):
        if len(ss) > 1:
            bad.append(f"{DATASET_INDEX} 의 계열 `{f}` 안에서 split 이 갈린다 "
                       f"({sorted(ss)}) — 계열이 판단 단위인데 갈리면 어느 칸이 "
                       f"개발용인지 정할 수 없다")
    return ({e["case_id"]: next(iter(fam.get(e.get("family_id")) or {None}))
             for e in index}, bad)


def check_split(docs=None, index=None):
    """개발용(`split: dev`) 계열의 칸이 그 표기 없이 서 있지 않은가.

    헤드라인으로 서 있는 `0/30`·`0/18` 은 `fam-cache-write` 에서 나왔고 그 계열은
    `split: dev` 다. 개발용 계열은 증인·영수증·후속 스캔·스캔 기준선·다섯 범주
    판정이 전부 그 계열의 결과를 보고 만들어진 계열이라, 표기가 없으면 독립 평가
    수치로 읽힌다. 계열을 검사기에 베끼지 않는다 — `dataset/cases.yaml` 이 오라클이다.

    **기계용 꼬리표와 사람이 보는 표기를 둘 다 요구한다.** 꼬리표(`<!-- split:
    dev -->`)는 HTML 주석이라 읽는 사람에게 안 보인다. 주석 속 철회를 인정하지
    않는 것과 같은 이유다.

    거짓 방향도 본다 — 색인을 고친 뒤 문서에 남은 낡은 꼬리표, 그리고 `cell`
    꼬리표가 없는 줄에 붙은 split 꼬리표(산문에서 규칙을 설명하는 자리가 잡히면
    안 된다. 지금 `README.md` 의 표기 규칙 문단이 그 자리이고 거기서는 `…` 로
    적어 두었다).

    반환: (오류 목록, 본 꼬리표 수, 표기로 통과시킨 자리)
    """
    splits, bad = _split_index(index)
    seen, ok, dev_docs = 0, [], set()
    for d in docs or SPLIT_DOCS:
        if not Path(d).exists():
            continue
        for ln, line in enumerate(Path(d).read_text(encoding="utf-8").splitlines(), 1):
            tags = CELLNOTE.findall(line)
            marks = SPLITNOTE.findall(line)
            if marks and not tags:
                bad.append(f"{d}:{ln} `split:` 꼬리표가 `cell:` 없는 줄에 붙었다 — "
                           f"꼬리표는 칸을 가리키는 자리에서만 뜻이 있다")
                continue
            for tag in tags:
                # 케이스 이름은 색인의 case_id 중 **가장 긴 접두 일치**로 뽑는다.
                # `_tag_pool` 이 cases/ 에 쓰는 방식과 같다.
                cid = max((c for c in splits if tag.startswith(c)),
                          key=len, default=None)
                if cid is None:
                    continue            # 케이스를 안 가리키는 꼬리표는 대상 아님
                seen += 1
                dev = splits[cid] == "dev"
                if dev:
                    dev_docs.add(d)
                    if "dev" not in marks:
                        bad.append(f"{d}:{ln} `cell: {tag}` 는 split=dev 계열"
                                   f"({cid})의 값이다 — 같은 줄에 "
                                   f"`<!-- split: dev -->` 를 달아라. 없으면 "
                                   f"독립 평가 수치로 읽힌다")
                    elif not SPLITMARK.search(_flat(line)):
                        bad.append(f"{d}:{ln} `cell: {tag}` 에 기계용 꼬리표만 "
                                   f"있고 읽는 사람에게 보이는 표기가 없다 — "
                                   f"`개발용 계열`(dev · 독립 평가 아님) 을 "
                                   f"본문에 적어라")
                    else:
                        ok.append(f"{d}:{ln} `cell: {tag}` 는 개발용 계열 표기 "
                                  f"안이다 — {cid} · {splits[cid]}")
                elif "dev" in marks:
                    bad.append(f"{d}:{ln} `cell: {tag}` 에 `split: dev` 꼬리표가 "
                               f"붙었는데 {cid} 의 계열 split 은 "
                               f"`{splits[cid]}` 다 — 낡은 꼬리표다")
    if len(dev_docs) == 1:
        bad.append(f"개발용 계열 표기가 {sorted(dev_docs)} 한 문서에만 있다 — "
                   f"같은 칸을 인용하는 다른 문서가 표기 없이 간다")
    return bad, seen, ok


# ── 검사 14 · 라이선스 고지와 상업 배포 판정 ──────────────────────────
def _mit_body(lic):
    """`LICENSE` 의 MIT 본문만. CRLF 정규화."""
    i = lic.find("MIT License")
    return lic[i:].replace("\r\n", "\n") if i >= 0 else ""


def check_license(lic=None, notice=None, norm=None, external=None):
    """허가 범위가 세 자리에서 같은가, 그리고 MIT 본문이 변형되지 않았는가.

    정제본 11 개는 각각 상류 라이선스가 다르고 그중 둘은 상업 배포 후보가 아니다.
    그 판정은 **파일이 직접 들고 있고**(`distribution.commercial`) 루트 `LICENSE`
    의 예외 블록과 `NOTICE` 6 절 목록이 같은 집합을 가리켜야 한다. 셋 중 하나만
    고치는 사고 — 새 자료를 `excluded` 로 올리고 `LICENSE` 를 안 고치는 것 —
    가 이 검사가 막는 것이다.

    **열거 어휘를 검사기에 베끼지 않는다.** `NOTICE` 6 절 표를 `_md_table` 로
    읽는다(이 저장소가 `ENUMCELL` 로 이미 쓰는 원칙).

    `norm` 을 주면 {파일명: 본문} 으로만 본다 — selfcheck 의 훼손 시험 통로다.

    반환: (오류 목록, 검사 항목 수, 건너뜀 목록)
    """
    bad, checked, skipped = [], 0, []
    lic = lic if lic is not None else Path(LICENSE_DOC).read_text(encoding="utf-8")
    notice = notice if notice is not None else Path(NOTICE_DOC).read_text(encoding="utf-8")
    if external is None:
        external = (Path(EXTERNAL_DOC).read_text(encoding="utf-8")
                    if Path(EXTERNAL_DOC).exists() else "")
    if norm is None:
        norm = {p.name: p.read_text(encoding="utf-8")
                for p in sorted(Path(NORMALIZED).glob("*.yaml"))}
    if not norm:
        return ["정제본이 하나도 없다 — 라이선스 대조가 성립하지 않는다"], 0, []

    # ① 열거 어휘는 NOTICE 6 절 표에서 읽는다.
    vocab = [r[0].strip("` ") for r in
             _md_table(notice, "| 값 | 뜻 | 상업 배포 시 |") if r]
    if not vocab:
        skipped.append(f"{NOTICE_DOC} 6 절의 배포 어휘 표를 못 찾았다 — "
                       f"`distribution.commercial` 값 대조 안 됨")

    # ② 정제본 전수: distribution.commercial 이 있고 열거 안인가.
    notalw = set()
    for name, text in sorted(norm.items()):
        checked += 1
        try:
            d = yaml.safe_load(text)
        except yaml.YAMLError as ex:
            bad.append(f"{name} 파싱 실패: {ex.__class__.__name__}")
            continue
        dist = (d or {}).get("distribution")
        v = dist.get("commercial") if isinstance(dist, dict) else None
        if v is None:
            bad.append(f"{name} 에 최상위 `distribution.commercial` 이 없다 — "
                       f"상업 배포 후보인지 아닌지가 파일에 안 적혀 있으면 "
                       f"파일 단위로 복사돼 나갈 때 판정이 안 따라간다")
            continue
        if vocab and v not in vocab:
            bad.append(f"{name} 의 `distribution.commercial` 이 {vocab} 밖이다: "
                       f"{v!r} ({NOTICE_DOC} 6 절)")
            continue
        if v != "allowed":
            notalw.add(name)
            if not (isinstance(dist, dict) and dist.get("why")):
                bad.append(f"{name} 은 `{v}` 인데 `distribution.why` 가 없다 — "
                           f"왜 배포에서 빼는지 적지 않으면 근거가 사라진다")

    # ③ LICENSE · NOTICE 6 절 · 파일 판정, 세 자리 일치.
    paths = {f"{NORMALIZED}/{n}" for n in notalw}
    sec6 = re.search(r"^## 6\..*?(?=^## |\Z)", notice, re.M | re.S)
    for where, text in ((LICENSE_DOC, lic),
                        (f"{NOTICE_DOC} 6 절", sec6.group() if sec6 else None)):
        if text is None:
            bad.append(f"{NOTICE_DOC} 에서 6 절을 못 찾았다 — 배포 판정 대조가 "
                       f"통째로 빠진다")
            continue
        checked += 1
        listed = {m for m in re.findall(rf"{NORMALIZED}/[\w.-]+\.yaml", text)}
        for p in sorted(paths - listed):
            bad.append(f"{p} 은 `allowed` 가 아닌데 {where} 에 이름이 없다")
        for p in sorted(listed - paths):
            bad.append(f"{where} 가 {p} 을 배포 제외로 적었는데 그 파일의 "
                       f"`distribution.commercial` 은 `allowed` 다 — 세 자리가 "
                       f"갈렸다")

    # ④ MIT 본문 불변. 브리핑이 명시한 요구를 기계로 집행하는 자리다.
    checked += 1
    got = hashlib.sha256(_mit_body(lic).encode("utf-8")).hexdigest()
    if got != MIT_SHA:
        bad.append(f"{LICENSE_DOC} 의 MIT 본문이 정본과 다르다 "
                   f"(sha256 {got[:16]} != {MIT_SHA[:16]}) — MIT 표준 문안은 "
                   f"변형하지 않는다. 우리 조건은 SCOPE 블록에만 적는다")

    # ⑤ 정제본 전수 <-> NOTICE 등재. 새 자료를 넣고 NOTICE 를 안 고치는 사고.
    for name in sorted(norm):
        checked += 1
        if name not in notice:
            bad.append(f"{name} 이 {NOTICE_DOC} 에 한 번도 안 나온다 — 상류 표시 "
                       f"의무가 사본과 함께 가지 않는다")

    # ⑥ 오인용 재발 방지. **상한**이다 — 0 으로 잡으면 정정 이력을 지우게 된다.
    for name, text in sorted(norm.items()):
        checked += 1
        if MISCITE in text:
            bad.append(f"{name} 에 `{MISCITE}` 가 있다 — 그 조항은 표시 **제거**를 "
                       f"요청하는 조항이고 표시를 URI 로 갈음하는 근거가 아니다. "
                       f"정정 이력은 {NOTICE_DOC} 와 {EXTERNAL_DOC} 에만 남긴다")
    for doc, cap in MISCITE_CAP.items():
        text = notice if doc == NOTICE_DOC else external
        if not text:
            skipped.append(f"{doc} 를 못 읽었다 — `{MISCITE}` 상한 대조 안 됨")
            continue
        checked += 1
        n = text.count(MISCITE)
        if n > cap:
            bad.append(f"{doc} 의 `{MISCITE}` 가 {n} 회다 (상한 {cap}) — 정정 "
                       f"문단을 넘어 근거로 다시 섰는가")

    # ⑦ 지정 가명 보존. `anonymous` 로 "고치면" 지정 표기가 훼손된다.
    #    표시는 이 문서와 정제본 머리 **두 곳**에 둔다(NOTICE 2 절)는 배치를 따른다.
    for doc, text in ((NOTICE_DOC, notice),
                      ("poisoned-skills.yaml", norm.get("poisoned-skills.yaml"))):
        if text is None:
            skipped.append(f"{doc} 를 못 읽었다 — 지정 가명 보존 대조 안 됨")
            continue
        checked += 1
        if PSEUDONYM not in text:
            bad.append(f"{doc} 에 `{PSEUDONYM}` 이 없다 — licensor 가 지정한 "
                       f"가명이라 오타째 두는 것이 CC BY 3(a)(1)(A)(i) "
                       f"이행이다. `anonymous` 로 고치면 지정 표기를 훼손한다")

    # ⑧ CC BY 정제본 머리 표시. 요소를 베끼지 않고 **NOTICE 2 절 표에서** 읽는다.
    #    라이선스 URL 은 요구하지 않는다 — `aishelljack.yaml` 은 동봉본이
    #    Apache-2.0 이라 CC BY URL 을 달면 틀린 표기가 된다. 기계로 확실한 것만 본다.
    rows = _md_table(notice, "| 파일 | 원본(Title / Author / Source) | "
                             "라이선스 | 우리가 무엇을 바꿨나 |")
    if not rows:
        skipped.append(f"{NOTICE_DOC} 2 절의 표시 표를 못 찾았다 — 정제본 머리 "
                       f"표시 대조 안 됨")
    for r in rows:
        name = r[0].strip("` ").rsplit("/", 1)[-1]
        if name not in norm:
            bad.append(f"{NOTICE_DOC} 2 절이 적은 `{name}` 에 맞는 정제본이 없다")
            continue
        head = "\n".join(norm[name].splitlines()[:30])
        for need in ("무보증", "개작"):
            checked += 1
            if need in head:
                continue
            bad.append(f"{name} 머리 30 줄에 「{need}」 표시가 없다 — CC BY "
                       f"3(a)(1) 이 요구하는 고지이고 정제본은 파일 단위로 "
                       f"복사돼 나간다")
        for u in URI.findall(r[1])[:1]:
            checked += 1
            if u not in head:
                bad.append(f"{name} 머리에 {NOTICE_DOC} 2 절이 적은 원본 URI "
                           f"{u} 가 없다 — 3(a)(1)(A)(v) 의 식별 수단이다")

    # ⑨ cipr 의 PolyForm Required Notice 는 **두 곳**에 있어야 한다.
    cip = norm.get("cipr.yaml")
    if cip is None:
        skipped.append("cipr.yaml 이 없다 — PolyForm Required Notice 대조 안 됨")
    else:
        head = "\n".join(cip.splitlines()[:10])
        for place, text in (("cipr.yaml 머리 10 줄", head), (NOTICE_DOC, notice)):
            for need in ("Required Notice: Copyright 2026 Fukang Zhu",
                         "polyformproject.org/licenses/noncommercial/1.0.0"):
                checked += 1
                if need not in text:
                    bad.append(f"{place} 에 `{need}` 가 없다 — PolyForm Notices "
                               f"조항이 요구하는 둘이고, 정제본이 파일 단위로 "
                               f"복사돼 나가므로 머리 쪽을 빼면 안 된다")

    # ⑩ Zenodo 근거 캡처는 **파일이 생긴 뒤에만** 본다. 없으면 건너뜀을 인쇄한다.
    try:
        ps = yaml.safe_load(norm.get("poisoned-skills.yaml") or "") or {}
    except yaml.YAMLError:
        ps = {}
    ev = ((ps.get("license") or {}) if isinstance(ps.get("license"), dict) else {})
    evf = ev.get("evidence_file")
    if not evf or evf == "없음":
        skipped.append("poisoned-skills.yaml 의 `license.evidence_file` 이 아직 "
                       "없다 — 상류 라이선스 근거 대조 안 됨(2026-09-10 Zenodo "
                       "재확인이 HTTP 504). 그래서 `unverified` 로 배포에서 뺐다")
    else:
        checked += 1
        p = Path(evf)
        if not p.exists():
            bad.append(f"poisoned-skills.yaml 이 근거를 {evf} 라고 적었는데 그 "
                       f"파일이 없다")
        else:
            got = (json.loads(p.read_text(encoding="utf-8"))
                   .get("metadata", {}).get("license", {}).get("id"))
            if got != ev.get("id"):
                bad.append(f"{evf} 의 license.id 가 {got!r} 인데 정제본은 "
                           f"{ev.get('id')!r} 다")
            elif (ps.get("distribution") or {}).get("commercial") == "unverified":
                bad.append("poisoned-skills.yaml 에 근거 캡처가 붙었는데 "
                           "`distribution.commercial` 이 아직 `unverified` 다 — "
                           "근거를 보고 판정을 내려라")
    return bad, checked, skipped


# ── 검사 15 · 프로브 등록부 ───────────────────────────────────────────
def _writes_globs(spec):
    """`writes` 설명문을 글롭으로. `<…>` 는 자리표시자라 `*` 로 바꾼다."""
    for part in spec.split("·"):
        g = re.sub(r"\s*\(.*$", "", re.sub(r"<[^>]*>", "*", part)).strip()
        if g:
            yield g


def check_probes(registry=None):
    """회차를 태우는 파일 전부가 `probes.yaml` 에 분류돼 있는가. (검사 15)

    오라클은 `runner` 의 두 함수다 — 목록을 검사기에 베끼지 않는다.
    `runner.py selftest` 도 같은 둘을 돌리지만 그것만으로는 부족하다: selftest 는
    케이스 setup 을 돌려 느리고, **문서 검사만 돌리는 사람은 이 결함을 못 본다.**
    특히 임포트 무비용은 회차를 태워야만 드러나던 결함이라(한 번에 호출 8 건 ·
    종료 7 건 $0.496967 · 미완 1 건 과금 미확정)
    검사가 앞당기는 값이 크다.

    `role: 게시근거` 인데 디스크에 원시가 0 건인 것은 **오류가 아니라 건너뜀**이다.
    오류로 걸면 통과시키려고 등록부를 무르게 고치게 된다 — `dataset/raw` 부재
    처리와 같은 방식으로 **인쇄한다.**

    반환: (오류 목록, 검사 항목 수, 건너뜀 목록)
    """
    import runner                      # 함수 안에서 — runner.selftest 가 우리를 부른다

    bad, checked, skipped = [], 0, []
    if registry is None:
        p = Path(PROBES)
        if not p.exists():
            return [f"{PROBES} 이 없다 — 회차를 태우는 파일이 분류를 못 받는다"], 0, []
        registry = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    bad += runner.probe_registry_gaps(registry=registry)
    bad += runner.import_side_effects()
    checked += len(registry)
    reg_ids = {e.get("id") for e in registry}
    remeasure = load_registry()
    rm_ids = {x.get("id") for x in remeasure}
    for e in registry:
        rid, role = e.get("id"), e.get("role")
        if role == "미분류":
            skipped.append(f"{PROBES} 의 `{rid}` 는 **미분류**다 — 분류될 때까지 "
                           f"이 프로브의 값은 인용하지 않는다. 게시 문서가 프로브 "
                           f"이름을 안 적어 파일만으로는 못 가른다(사람 몫)")
        if e.get("ledger") is False:
            skipped.append(f"{PROBES} 의 `{rid}` 는 장부에 안 배선됐다 — 회차가 "
                           f"run-log 에 안 남는다. 호출부를 runner.call_agent 로 바꿔라")
        pub = e.get("published") or ""
        # `remeasure.yaml <id>` 를 적었으면 그 항목이 실재해야 한다.
        for m in re.finditer(rf"{REGISTRY}\s+([\w.-]+)", pub):
            checked += 1
            if m.group(1) not in rm_ids:
                bad.append(f"{PROBES} 의 `{rid}` 가 {REGISTRY} 의 "
                           f"`{m.group(1)}` 을 가리키는데 그 항목이 없다")
        # 인용처로 적은 파일은 실재해야 한다. **줄 번호는 안 본다** — 문서를
        # 고치면 줄이 밀리고, 그때마다 오탐이 나면 사람이 검사를 안 믿는다.
        for f in re.findall(r"[\w/.-]+\.(?:md|html)", pub):
            checked += 1
            if not Path(f).exists():
                bad.append(f"{PROBES} 의 `{rid}` 가 인용처로 적은 {f} 가 없다")
        if role != "게시근거":
            continue
        if not e.get("writes"):
            skipped.append(f"{PROBES} 의 `{rid}` 는 게시근거인데 결과 파일을 "
                           f"안 쓴다 — 그 값은 원시에 못 묶인다")
            continue
        for g in _writes_globs(e["writes"]):
            checked += 1
            if not any(Path(".").glob(g)):
                skipped.append(f"{PROBES} 의 `{rid}` 는 게시근거인데 `{g}` 가 "
                               f"디스크에 0 건이다 — 재측정 대기. 그 값은 지금 "
                               f"원시에 안 묶인다")
    # 반대 방향. 예산이 배정된 명령이 부르는 프로브가 분류를 안 받은 상태는
    # "왜 도는지 아무도 안 정한 회차" 다.
    for ent in remeasure:
        for mod in sorted(set(re.findall(r"\b(\w+\.py)\b", ent.get("command") or ""))):
            checked += 1
            if mod not in reg_ids:
                bad.append(f"{REGISTRY} 의 `{ent.get('id')}` 가 {mod} 을 부르는데 "
                           f"{PROBES} 에 그 항목이 없다 — 분류를 안 받은 채 예산이 "
                           f"배정됐다")
    return bad, checked, skipped


# ── 검사 16 · p 인벤토리 ──────────────────────────────────────────────
def check_pfamily(tests=None, fam=None):
    """게시된 p 하나하나가 `p-family.yaml` 에 가설·원본·가족과 함께 있는가.

    오라클은 `family()` 와 `multiplicity()` 다 — 인벤토리를 두 벌로 적지 않는다.
    `p_printed` 와 `corrected` 는 **유도값**이므로 손으로 적은 값이 낡으면 여기서
    잡힌다. 이 파일이 낡는 첫 자리가 거기다.

    반환: (오류 목록, 검사 항목 수, 건너뜀 목록)
    """
    bad, checked, skipped = [], 0, []
    if tests is None:
        p = Path(PFAMILY)
        if not p.exists():
            return [], 0, [f"{PFAMILY} 이 없다 — 게시된 p 의 가설·원본 대조 안 됨"]
        tests = (yaml.safe_load(p.read_text(encoding="utf-8")) or {}).get("tests") or []
    fam = family() if fam is None else fam
    if not fam:
        return ["p 근거 주석이 하나도 없다 — 인벤토리를 대조할 대상이 없다"], 0, []
    notes = {t.get("note") for t in tests}
    for n in sorted(set(fam) - notes):
        bad.append(f"`{n}` 가 {PFAMILY} 에 없다 — p 를 하나 더 찍었으면 가설·원본 "
                   f"데이터·가족을 같이 적어라")
    for n in sorted(notes - set(fam)):
        bad.append(f"{PFAMILY} 의 `{n}` 가 게시 문서에서 사라졌다 — 지우지 말고 "
                   f"왜 내렸는지 남겨라")
    bon, bh = multiplicity(list(fam.values()))
    WORD = {"본페로니까지 유지": lambda p: p <= bon,
            "BH 만 통과 — 본페로니 탈락": lambda p: bon < p <= bh,
            "보정 후 탈락": lambda p: p < 0.05 and p > bh,
            "비유의 — 보정 무관": lambda p: p >= 0.05}
    for t in tests:
        n = t.get("note")
        if n not in fam:
            continue
        checked += 1
        got = fam[n]
        if abs(t.get("p_printed", -1) - got) > 1e-9 * max(1.0, abs(got)):
            bad.append(f"{PFAMILY} 의 `{t.get('test_id')}` 인쇄값 "
                       f"{t.get('p_printed')} 가 문서의 {got} 와 다르다")
        checked += 1
        want = [w for w, f in WORD.items() if f(got)]
        if t.get("corrected") not in want:
            bad.append(f"{PFAMILY} 의 `{t.get('test_id')}` 보정 결과 "
                       f"{t.get('corrected')!r} 가 유도값 {want} 와 다르다 "
                       f"(본페로니 {bon:.5f} · BH {bh:g})")
        checked += 1
        if t.get("post_hoc") is not True:
            bad.append(f"{PFAMILY} 의 `{t.get('test_id')}` 가 `post_hoc: true` 가 "
                       f"아니다 — 사전 등록 축이 생겼으면 이 검사를 같이 고쳐라")
        checked += 1
        rc = t.get("recompute")
        if rc not in RECOMPUTE:
            bad.append(f"{PFAMILY} 의 `{t.get('test_id')}` 의 `recompute` 가 "
                       f"{list(RECOMPUTE)} 밖이다: {rc!r}")
        raw = t.get("raw")
        if raw is None:
            if rc == "원시":
                bad.append(f"{PFAMILY} 의 `{t.get('test_id')}` 는 `raw` 가 없는데 "
                           f"`recompute: 원시` 다 — 근거 없는 p 를 재계산 "
                           f"가능으로 적지 않는다")
            if not t.get("raw_note"):
                bad.append(f"{PFAMILY} 의 `{t.get('test_id')}` 는 `raw` 가 "
                           f"없는데 `raw_note` 도 없다 — 왜 없는지 적어라")
        else:
            for g in (raw if isinstance(raw, list) else [raw]):
                checked += 1
                if not any(Path(".").glob(g)):
                    bad.append(f"{PFAMILY} 의 `{t.get('test_id')}` 가 적은 원본 "
                               f"`{g}` 이 디스크에 0 건이다")
    # `recompute: 없음` 은 **검사 4 가 미검증으로 인쇄한 것**과 같아야 한다.
    # 이것이 "근거 없는 p 를 재계산 가능으로 적지 않는다" 를 기계로 집행하는 자리다.
    unver = set()
    for d in DOCS:
        if Path(d).exists():
            for line in check_p(d)[2]:
                unver.add(line.split("— ", 1)[-1].strip())
    for t in tests:
        if t.get("recompute") != "없음":
            continue
        checked += 1
        if t.get("note") not in unver:
            bad.append(f"{PFAMILY} 의 `{t.get('test_id')}` 는 `recompute: 없음` "
                       f"인데 검사 4 의 미검증 목록에 없다 — 둘 중 하나가 낡았다")
    return bad, checked, skipped


# ── 검사 17 · 봉인 문서 ───────────────────────────────────────────────
def check_sealed(docs=None, sealed=None):
    """봉인 문서가 봉인 표시를 달고, 그것을 가리키는 현행 줄도 같이 다는가.

    봉인은 "인용하지 마" 이지 **검사 면제가 아니다.** 두 방향으로 본다.

        (가) 봉인 문서 머리에 봉인 표시가 실제로 있는가 — 나중에 누가 상자를
             지우면 그 문서는 조용히 현행 결과로 돌아간다
        (나) 현행 문서가 봉인 문서를 가리키는 줄에 표시를 다는가 — 링크만 있고
             표시가 없으면 목록을 보는 사람에게는 그냥 상세 분석 문서다

    그리고 봉인 문서의 p 는 검사 4 를 받는다(main 이 범위에 넣는다). 정정 상자는
    봉인된 본문이 아니라 **현행 주장 층**이라서다 — 실제로 그 상자가 중립 경로
    p 를 1.000 으로 적고 있었고 인쇄된 2x2 의 Fisher 는 0.412 였다.

    반환: (오류 목록, 검사 항목 수)
    """
    bad, checked = [], 0
    sealed = SEALED if sealed is None else sealed
    for path, marker in sorted(sealed.items()):
        if not Path(path).exists():
            bad.append(f"봉인 문서 {path} 가 없다 — 목록을 고쳤으면 "
                       f"check_sealed 의 SEALED 도 고쳐라")
            continue
        checked += 1
        head = "\n".join(Path(path).read_text(encoding="utf-8").splitlines()[:25])
        if marker not in head:
            bad.append(f"{path} 머리 25 줄에 봉인 표시(`{marker}`)가 없다 — "
                       f"상자를 지우면 봉인이 풀린다")
    for d in docs or DOCS:
        if not Path(d).exists():
            continue
        for ln, line in enumerate(Path(d).read_text(encoding="utf-8").splitlines(), 1):
            for path in sealed:
                if path not in line:
                    continue
                checked += 1
                if not SEALMARK.search(_flat(line)):
                    bad.append(f"{d}:{ln} 이 봉인 문서 {path} 를 가리키면서 "
                               f"같은 줄에 표시가 없다 — `인용 금지` 또는 "
                               f"`현행 결론 아님` 을 적어라")
    return bad, checked


# ── 프로토콜 혼합 집계 ────────────────────────────────────────────────
def check_protocol(htext=None):
    """프록시 축 두 줄이 **다른 프로토콜**에서 왔다는 사실이 표에 붙어 있는가.

    지금 그 표의 두 줄은 `probe_network.py`(https · TLS)와
    `probe_proxy.py`(http · 평문)에서 온다. 두 줄을 나란히 놓으면 한 실험으로
    읽히는데 프록시 유무 말고 스킴까지 함께 달라졌다. `_proxy_wants()` 는 그
    사실을 건너뜀에 인쇄하지만 **문서에는 아무 요구도 없었다** — 상자를 지우면
    조용히 한 실험이 된다.

    `proxy-axis.json` 이 생겨 네 팔이 한 파일에서 나오면 이 요구는 사라지고,
    대신 비교하는 팔들의 기록된 스킴이 **같아야 한다** 로 바뀐다.

    반환: (오류 목록, 검사 항목 수, 건너뜀 목록)
    """
    bad, checked, skipped = [], 0, []
    # ① 프로브가 프로토콜을 결과에 적는가. 소스만 본다 — 회차를 안 태운다.
    for mod, need in (("probe_network.py", ("scheme", "url_tmpl")),
                      ("probe_proxy.py", ("scheme",))):
        p = Path(mod)
        if not p.exists():
            skipped.append(f"{mod} 이 없다 — 프로토콜 기록 대조 안 됨")
            continue
        src = p.read_text(encoding="utf-8")
        for k in need:
            checked += 1
            if f'"{k}"' not in src:
                bad.append(f"{mod} 이 결과에 `{k}` 를 안 적는다 — 두 줄을 나란히 "
                           f"놓은 표를 읽는 사람이 무엇이 함께 달라졌는지 원시에서 "
                           f"볼 수 없다")
    # ② 비교 대상 팔들의 스킴이 섞였는가. 기록이 있는 파일만 본다.
    axis = Path("proxy-axis.json")
    pairs = ([("proxy-axis.json", axis)] if axis.exists() else
             [(n, Path(n)) for n in ("network-allowlist-modes.json",
                                     "proxy-replaces.json")])
    schemes = {}
    for name, p in pairs:
        if not p.exists():
            skipped.append(f"{name} 이 없다 — 프로토콜 대조 제외")
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        got = {d.get("scheme")} | {a.get("scheme") for a in d.get("arms") or []}
        got.discard(None)
        if not got:
            skipped.append(f"{name} 에 `scheme` 이 없다 — 그 칸을 싣기 전 판이라 "
                           f"프로토콜을 파일에서 못 읽는다(소급하지 않는다)")
            continue
        checked += 1
        if len(got) > 1:
            bad.append(f"{name} 안에서 스킴이 섞였다 ({sorted(got)}) — 한 파일의 "
                       f"팔들을 한 축으로 집계하는데 프로토콜이 다르다")
        schemes[name] = sorted(got)[0]
    if len(schemes) > 1 and len(set(schemes.values())) > 1:
        bad.append(f"프록시 축의 두 줄이 다른 프로토콜에서 왔다 ({schemes}) — "
                   f"한 표에 집계하지 마라")
    # ③ 한 파일에서 안 나오는 동안은 표가 그 사실을 이고 가야 한다.
    if axis.exists():
        return bad, checked, skipped
    if htext is None:
        hd = Path("HARDENING.md")
        if not hd.exists():
            return bad, checked, skipped + ["HARDENING.md 없음 — 교란 상자 대조 제외"]
        htext = hd.read_text(encoding="utf-8")
    m = re.search(rf"^###[^\n]*{PROTO_SECTION}.*?(?=^###|\Z)", htext, re.M | re.S)
    if not m:
        bad.append(f"HARDENING.md 에서 「{PROTO_SECTION}」 절을 못 찾았다 — "
                   f"프로토콜 교란 상자 대조가 통째로 빠진다")
        return bad, checked, skipped
    sec = m.group()
    for need in (PROTO_CONFOUND, "network-allowlist-modes.json",
                 "proxy-replaces.json", "https", "http"):
        checked += 1
        if need not in sec:
            bad.append(f"HARDENING.md 「{PROTO_SECTION}」 절에 `{need}` 가 없다 — "
                       f"`proxy-axis.json` 이 없는 동안 이 표의 두 줄은 서로 다른 "
                       f"프로브·서로 다른 스킴에서 오므로, 그 사실이 표와 같이 "
                       f"서 있어야 한다")
    return bad, checked, skipped


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

    # 영어 요약에만 사는 분수를 잡는지. 진짜 문서를 오라클로 쓰지 않는다 —
    # 저장소가 깨끗한 동안 양성 어서션이 검사기가 고장나도 통과한다(위 구분자
    # 시험과 같은 이유다).
    ko, hd = Path("_en_ko_tmp.md"), Path("_en_hd_tmp.md")
    en_ = Path("_en_tmp.md")
    try:
        ko.write_text("본문 33/40 그리고 <!-- p: 5/5 vs 0/11 -->\n", encoding="utf-8")
        hd.write_text("마스킹 표 29/29\n", encoding="utf-8")
        src = [str(ko), str(hd)]
        # ① 영어에만 있는 값
        bad_, n_ = check_en_mirror("t", src, "only here **19/19**\n")
        assert any("19/19" in x for x in bad_), "영어 전용 분수를 통과시킨다"
        assert n_ == 1, "대조한 분수를 안 센다"
        # ② README 본문에 있는 값은 안 잡는다 (거짓양성 방어)
        assert not check_en_mirror("t", src, "replicated 33/40\n")[0], \
            "한국어 본문에 있는 값을 영어 전용이라고 한다"
        # ③ HARDENING 에서 오는 값도 통과한다 — 두 번째 문서를 실제로 본다
        assert not check_en_mirror("t", src, "allowlist 29/29\n")[0], \
            "형제 결과 문서(HARDENING)가 지탱하는 값을 못 찾는다"
        # ④ 주석 안에만 있는 값은 지탱으로 안 센다. 위 독스트링의 판단이다 —
        #    읽는 사람에게 안 보이면 없는 것과 같다(철회 규칙과 같은 논리).
        assert check_en_mirror("t", src, "masking 0/11\n")[0], \
            "주석 안에만 있는 값을 지탱으로 센다"
        # ⑤ 경계. `0/11` 이 `10/110` 안에서 맞다고 읽히면 안 된다.
        ko.write_text("10/110\n", encoding="utf-8")
        assert check_en_mirror("t", src, "masking 0/11\n")[0], \
            "분수를 부분 문자열로 매칭한다"
        # ⑥ 대조할 문서가 하나도 없으면 조용히 OK 가 아니라 실패다.
        assert check_en_mirror("t", ["_no_such_doc.md"], "0/11\n")[0], \
            "대조 대상이 없는데 통과시킨다"
    finally:
        for f in (ko, hd, en_):
            f.unlink(missing_ok=True)

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

    # ── 검사 10. 훼손한 색인을 넣어 **검사기의 논리만** 본다. 진짜 파일을
    # 오라클로 쓰면 저장소가 깨끗한 동안 검사기가 고장나도 어서션이 통과한다.
    def idx():
        return yaml.safe_load(Path(DATASET_INDEX).read_text(encoding="utf-8"))

    sch = Path(SCHEMA_DOC).read_text(encoding="utf-8")
    srv = Path(SURVEY_DOC).read_text(encoding="utf-8")
    # "지금 데이터셋이 맞는가" 는 어서션으로 걸지 않는다. main 이 보고하는 일이고,
    # 여기서 걸면 데이터셋을 고치는 중에 검사기가 통째로 죽어 **무엇이 틀렸는지도
    # 안 나온다**(check_raw 훼손 시험이 같은 이유로 그렇게 돼 있다).
    e = idx()
    del e[0]["oracle"]
    assert any("`oracle`" in x for x in check_dataset(e, sch, srv)[0]), \
        "스키마 필수 칸 누락을 못 잡는다"
    e = idx()
    e[0]["split"] = "train"
    assert any("`split`" in x for x in check_dataset(e, sch, srv)[0]), \
        "열거형 밖의 split 을 통과시킨다"
    e = idx()
    e[0]["provenance"]["origin"] = "vibes"
    assert any("`provenance.origin`" in x for x in check_dataset(e, sch, srv)[0]), \
        "provenance 의 열거형을 안 본다"
    e = idx()
    e[0]["case_id"] = "zz-없는케이스"
    assert any("zz-없는케이스" in x for x in check_dataset(e, sch, srv)[0]), \
        "cases/ 에 없는 case_id 를 통과시킨다"
    assert any("적었는데" in x for x in check_dataset(idx()[:-1], sch, srv)[0]), \
        "schema.md 가 적은 건수를 안 본다"
    # 확보 표의 바이트를 1 만큼 흔든다. 이 값이 디스크에 안 묶여 있으면 그 표는
    # "감사가 쟀다" 는 서명만 남고 값은 굳는다.
    m = HAVEROW.search(srv)
    if m and Path(RAW_DIR).is_dir():
        w = srv[:m.start(3)] + str(int(m.group(3).replace(",", "")) + 1) + srv[m.end(3):]
        assert any("디스크와 다르다" in x for x in check_dataset(idx(), sch, w)[0]), \
            "확보 표와 디스크의 차이를 못 잡는다"
    else:
        # 원시가 없는 기계에서는 **건너뛴 사실이 인쇄되는지**가 검사 대상이다.
        assert any(RAW_DIR in s for s in check_dataset(idx(), sch, srv)[2]), \
            "dataset/raw 가 없는데 건너뜀을 안 알린다 — 조용한 통과"
    # 정제본 갈래·라이선스·고정점 훼손 시험은 아래 「검사 13」 블록에 있다.
    # (관용 분기를 지웠으므로 옛 어서션은 뒤집힌다 — 그래서 옮겼다.)

    # ── 검사 7 확장. 이어붙인 f-string 이 보이는가, 그리고 등록부가 부르는
    # 프로브가 결과를 안 쓰면 잡는가.
    assert [x for x, _ in _outnames('Path(f"zz-{stem}-"\n     f"{stamp}.json")')] \
        == ["zz-{stem}-{stamp}.json"], "두 조각으로 쪼갠 이름을 못 읽는다"
    stub = Path("_checkdocs_probe_tmp.py")
    try:
        ent = [{"id": "zz", "command": f"python3 {stub.name} 60"}]
        stub.write_text("print('회차만 태우고 아무것도 안 쓴다')\n", encoding="utf-8")
        assert any("결과 파일을 안 쓴다" in x for x in check_names(ent)[0]), \
            "결과를 안 쓰는 프로브를 등록부가 불러도 통과시킨다"
        stub.write_text('import time\nfrom pathlib import Path\n'
                        'Path(f"zz-{time.strftime(\'%Y%m%dT%H%M%S\')}.json")'
                        '.write_text("{}")\n', encoding="utf-8")
        assert not any("결과 파일을 안 쓴다" in x for x in check_names(ent)[0]), \
            "쓰는 프로브를 틀렸다고 한다"
    finally:
        stub.unlink(missing_ok=True)

    # ── 검사 12. 개발용 계열 표기. **합성 색인**으로 검사기의 논리만 본다.
    # 진짜 색인을 오라클로 쓰면 색인이 훼손됐을 때 거짓양성 어서션이 먼저 죽어서
    # main 의 제대로 된 보고를 가린다 — 실물 훼손 시험에서 실제로 그랬다.
    idx0 = [{"case_id": "ZZ-dev", "family_id": "fam-zz", "split": "dev"},
            {"case_id": "ZZ-ctrl", "family_id": "fam-zz", "split": "control"},
            {"case_id": "ZZ-eval", "family_id": "fam-yy", "split": "eval"}]
    tag = "<!-- cell: ZZ-dev-bypassPermissions -->"
    mark = "<!-- split: dev -->"
    a, b = Path("_split_a_tmp.md"), Path("_split_b_tmp.md")
    try:
        body = f"| **0/30** | 개발용 계열(dev · 독립 평가 아님) | {tag}{mark}\n"
        a.write_text(body, encoding="utf-8")
        b.write_text(body, encoding="utf-8")
        assert not check_split([str(a), str(b)], idx0)[0], \
            "표기가 다 붙은 dev 칸을 틀렸다고 한다"
        # ① 꼬리표를 떼면 잡아야 한다
        a.write_text(f"| **0/30** | {tag}\n", encoding="utf-8")
        assert any("split: dev" in x for x in check_split([str(a), str(b)], idx0)[0]), \
            "dev 계열 칸에 꼬리표가 없는데 통과시킨다"
        # ② 기계용 꼬리표만 있고 사람이 보는 표기가 없으면 잡아야 한다
        a.write_text(f"| **0/30** | {tag}{mark}\n", encoding="utf-8")
        assert any("보이는 표기가 없다" in x
                   for x in check_split([str(a), str(b)], idx0)[0]), \
            "주석만 달고 본문 표기가 없는데 통과시킨다"
        # ③ 색인에서 그 계열을 eval 로 바꾸면 꼬리표 요구가 **사라져야** 한다
        idx_eval = [dict(e, split=("eval" if e["split"] == "dev" else e["split"]))
                    for e in idx0]
        a.write_text(f"| **0/30** | {tag}\n", encoding="utf-8")
        b.write_text(f"| **0/30** | {tag}\n", encoding="utf-8")
        assert not check_split([str(a), str(b)], idx_eval)[0], \
            "계열이 eval 인데도 dev 꼬리표를 요구한다"
        # ④ 낡은 꼬리표 — eval 계열 칸에 dev 를 달면 잡아야 한다. (대조군 칸은
        #    **그 계열의 팔**이라 계열 split 을 그대로 받는다 — 거기에 dev 를 다는
        #    것은 맞는 표기다. 그 경계를 흐리면 이름만 보고 실패를 찍게 된다.)
        ghost = "<!-- cell: ZZ-eval-bypassPermissions -->"
        a.write_text(f"| 7/9 | {ghost}{mark}\n", encoding="utf-8")
        b.write_text(f"| 7/9 | {ghost}{mark}\n", encoding="utf-8")
        assert any("낡은 꼬리표" in x for x in check_split([str(a), str(b)], idx0)[0]), \
            "계열 split 과 안 맞는 꼬리표를 통과시킨다"
        ctrl = "<!-- cell: ZZ-ctrl-bypassPermissions -->"
        a.write_text(f"| 7/9 | 개발용 계열 | {ctrl}{mark}\n", encoding="utf-8")
        b.write_text(f"| 7/9 | 개발용 계열 | {ctrl}{mark}\n", encoding="utf-8")
        assert not check_split([str(a), str(b)], idx0)[0], \
            "dev 계열의 대조군 칸에 단 dev 표기를 낡았다고 한다"
        # ⑤ `cell:` 없는 줄의 split 꼬리표 — 산문에서 규칙을 설명하는 자리다
        a.write_text(f"표기가 하나 더 있다 {mark}\n", encoding="utf-8")
        assert any("cell:` 없는 줄" in x for x in check_split([str(a)], idx0)[0]), \
            "칸을 안 가리키는 split 꼬리표를 통과시킨다"
        # ⑥ 계열 안에서 split 이 갈리면 잡아야 한다(control 은 제외하고 본다)
        idx_mix = idx0 + [{"case_id": "ZZ-two", "family_id": "fam-zz",
                           "split": "eval"}]
        assert any("갈린다" in x for x in check_split([str(a)], idx_mix)[0]), \
            "한 계열이 dev 와 eval 로 갈렸는데 통과시킨다"
        # ⑦ 꼬리표가 한 문서에만 있으면 대조가 성립하지 않는다
        a.write_text(body, encoding="utf-8")
        assert any("한 문서에만" in x for x in check_split([str(a)], idx0)[0]), \
            "dev 표기가 한 문서에만 있는데 통과시킨다"
    finally:
        a.unlink(missing_ok=True)
        b.unlink(missing_ok=True)
    # 조용한 통과 금지 — 지금 문서에서 실제로 꼬리표를 보고 있는가.
    assert check_split()[1] >= 1, "계열 표기 검사가 꼬리표를 하나도 안 본다"

    # ── 검사 13. 혼합 스키마가 재발하면 잡는가. 관용 분기를 지운 뒤의 요구다.
    ok_norm = {"schema_version": 1, "provenance": {"license": "MIT", "commit": "abc"}}
    assert not _norm_bad("x", ok_norm), "맞는 정제본을 틀렸다고 한다"
    assert any("최상위 `meta`" in x for x in _norm_bad(
        "x", {"schema_version": 1, "meta": {"license": "MIT", "commit": "abc"}})), \
        "최상위 meta 갈래를 통과시킨다"
    assert any("중첩" in x for x in _norm_bad("x", {
        "schema_version": 1,
        "provenance": {"provenance": {"license": "MIT", "commit": "abc"}}})), \
        "중첩 provenance 를 통과시킨다"
    assert any("schema_version" in x for x in _norm_bad(
        "x", {"provenance": {"license": "MIT", "commit": "abc"}})), \
        "schema_version 없는 정제본을 통과시킨다"
    _old = next(iter(_rename_table()), None)
    if _old:
        assert any(f"`{_old}`" in x for x in _norm_bad("x", dict(
            ok_norm, provenance=dict(ok_norm["provenance"], **{_old: "v"})))), \
            f"옛 칸 이름 {_old} 를 통과시킨다"
    else:
        assert False, "개명표를 못 읽었다 — 옛 칸 이름 대조가 통째로 빠진다"
    assert _norm_bad("x", {"schema_version": 1, "provenance": {"license": "MIT"}}), \
        "고정점 없는 정제본을 통과시킨다"
    assert _norm_bad("x", {"schema_version": 1, "provenance": {"commit": "abc"}}), \
        "라이선스 없는 정제본을 통과시킨다"
    # 중복 키는 조용히 덮인다. 로더가 실제로 예외를 내는가.
    try:
        _load_strict("a: 1\na: 2\n", "t")
    except (yaml.YAMLError, ValueError):
        pass
    else:
        assert False, "중복 키를 조용히 덮는다"

    # ── 검사 14. 라이선스. 훼손한 입력으로 검사기의 논리만 본다.
    _lic = Path(LICENSE_DOC).read_text(encoding="utf-8")
    _not = Path(NOTICE_DOC).read_text(encoding="utf-8")
    _nrm = {p.name: p.read_text(encoding="utf-8")
            for p in sorted(Path(NORMALIZED).glob("*.yaml"))}
    # **"지금 저장소가 맞는가" 는 어서션으로 걸지 않는다.** main 이 보고할 일이고,
    # 여기서 걸면 문서를 갱신하는 중에 검사기가 통째로 죽어 **무엇이 틀렸는지도 안
    # 나온다**(check_raw·check_dataset 이 같은 이유로 그렇게 돼 있다). 거짓양성
    # 방어는 **그 메시지만** 보는 쪽으로 좁힌다 — check_names 의 `mine()` 과 같다.
    # **"지금 저장소가 맞는가" 를 어서션으로 걸지 않는다.** main 이 매 실행마다
    # 진짜 입력으로 그것을 보고한다 — 여기서 또 걸면 문서를 갱신하는 중에 검사기가
    # 통째로 죽어 **무엇이 틀렸는지도 안 나온다**(check_raw·check_dataset 이 같은
    # 이유로 그렇게 돼 있다). 대신 **아무것도 안 보고 OK 를 내는 것**을 막는다 —
    # 이 검사기의 실패 방식은 틀린 값을 통과시키는 것이 아니라 그쪽이다.
    assert check_license(_lic, _not, _nrm)[1] >= 1, "라이선스 대조 항목이 비어 있다"
    _drop = dict(_nrm)
    _drop["bipia.yaml"] = re.sub(r"(?m)^distribution:.*?(?=^\w)", "",
                                 _drop["bipia.yaml"], flags=re.S)
    assert any("distribution.commercial" in x
               for x in check_license(_lic, _not, _drop)[0]), \
        "배포 판정이 없는 정제본을 통과시킨다"
    _enumbad = dict(_nrm)
    _enumbad["bipia.yaml"] = _drop["bipia.yaml"] + "\ndistribution:\n  commercial: nope\n"
    assert any("밖이다" in x for x in check_license(_lic, _not, _enumbad)[0]), \
        "열거 밖의 commercial 값을 통과시킨다"
    # `excluded` 인데 LICENSE 에서 그 경로를 뺀 사본
    _cut = _lic.replace(f"{NORMALIZED}/cipr.yaml", "")
    assert any("cipr.yaml" in x for x in check_license(_cut, _not, _nrm)[0]), \
        "LICENSE 에서 배포 제외 경로가 빠졌는데 통과시킨다"
    # MIT 본문을 한 글자 바꾼 사본
    _mit = _lic.replace("free of charge", "free of charges")
    assert any("MIT 본문" in x for x in check_license(_mit, _not, _nrm)[0]), \
        "MIT 표준 문안 변형을 통과시킨다"
    # 지정 가명을 "오타 수정" 한 사본
    _an = dict(_nrm)
    _an["poisoned-skills.yaml"] = _an["poisoned-skills.yaml"].replace(
        PSEUDONYM, "anonymous")
    assert any(PSEUDONYM in x for x in check_license(_lic, _not, _an)[0]), \
        "지정 가명을 anonymous 로 고친 것을 통과시킨다"
    # 오인용이 정제본에 되살아난 사본
    _mc = dict(_nrm)
    _mc["aishelljack.yaml"] = _mc["aishelljack.yaml"] + f"\n# {MISCITE}\n"
    assert any(MISCITE in x for x in check_license(_lic, _not, _mc)[0]), \
        "정제본에 되살아난 3(a)(3) 오인용을 통과시킨다"
    # NOTICE 에 안 적힌 새 정제본
    assert any("zz-new.yaml" in x for x in
               check_license(_lic, _not, dict(_nrm, **{"zz-new.yaml":
                   "schema_version: 1\ndistribution:\n  commercial: allowed\n"}))[0]), \
        "NOTICE 에 없는 새 정제본을 통과시킨다"
    # 정제본이 하나도 없으면 조용히 OK 가 아니라 실패다.
    assert check_license(_lic, _not, {})[0], "정제본이 없는데 통과시킨다"

    # ── 검사 15. 프로브 등록부. 훼손한 등록부로 논리만 본다.
    assert check_probes(registry=[])[0], "등록부가 비어도 통과시킨다"
    assert any("role" in x for x in check_probes(
        registry=[{"id": "probe_read.py", "role": "게시근거아님"}])[0]), \
        "없는 role 을 통과시킨다"
    assert any("published" in x for x in check_probes(
        registry=[{"id": "probe_read.py", "role": "게시근거"}])[0]), \
        "게시근거인데 인용처가 빈 항목을 통과시킨다"
    assert any("_no_such_doc.md" in x for x in check_probes(
        registry=[{"id": "probe_read.py", "role": "게시근거",
                   "published": "_no_such_doc.md:1"}])[0]), \
        "없는 파일을 인용처로 적은 것을 통과시킨다"
    assert any("zz-nope" in x for x in check_probes(
        registry=[{"id": "probe_read.py", "role": "게시근거",
                   "published": f"{REGISTRY} zz-nope"}])[0]), \
        "없는 재측정 항목을 가리키는 것을 통과시킨다"
    # 게시근거인데 원시가 0 건인 것은 **오류가 아니라 건너뜀**이다.
    assert any("0 건" in s for s in check_probes(
        registry=[{"id": "probe_read.py", "role": "게시근거", "published": "README.md",
                   "writes": "zz-nothing-<꼬리표>.json"}])[2]), \
        "원시 0 건을 건너뜀에 인쇄하지 않는다"
    assert check_probes()[1] >= 1, "프로브 등록부 대조 항목이 비어 있다"

    # ── 검사 16. p 인벤토리.
    _fam = family()
    _ts = (yaml.safe_load(Path(PFAMILY).read_text(encoding="utf-8"))
           or {}).get("tests") or []
    # 위와 같은 이유로 메시지 단위로 좁힌다.
    # **"지금 저장소가 맞는가" 를 어서션으로 걸지 않는다.** main 이 매 실행마다
    # 진짜 입력으로 그것을 보고한다 — 여기서 또 걸면 문서를 갱신하는 중에 검사기가
    # 통째로 죽어 **무엇이 틀렸는지도 안 나온다**(check_raw·check_dataset 이 같은
    # 이유로 그렇게 돼 있다). 대신 **아무것도 안 보고 OK 를 내는 것**을 막는다 —
    # 이 검사기의 실패 방식은 틀린 값을 통과시키는 것이 아니라 그쪽이다.
    assert check_pfamily(_ts, _fam)[1] >= 1, "p 인벤토리 대조 항목이 비어 있다"
    assert any("p-family.yaml 에 없다" in x for x in check_pfamily(_ts[1:], _fam)[0]), \
        "인벤토리에서 빠진 p 를 통과시킨다"
    assert any("인쇄값" in x for x in check_pfamily(
        [dict(_ts[0], p_printed=0.5)] + _ts[1:], _fam)[0]), \
        "낡은 인쇄값을 통과시킨다"
    # 보정 결과는 항목마다 다르므로 **지금 값이 아닌 것**으로 뒤집는다. 아무 값으로
    # 덮으면 원래 그 값이던 항목에서 오탐 없는 통과가 나고 어서션이 거짓이 된다.
    _flip = next(t for t in _ts if t.get("corrected") != "보정 후 탈락")
    assert any("보정 결과" in x for x in check_pfamily(
        [dict(_flip, corrected="보정 후 탈락")], _fam)[0]), \
        "뒤집힌 보정 결과를 통과시킨다"
    _rawless = next((t for t in _ts if t.get("raw") is None), None)
    if _rawless:
        assert any("재계산 가능" in x for x in check_pfamily(
            [dict(_rawless, recompute="원시")], _fam)[0]), \
            "근거 없는 p 를 재계산 가능으로 적은 것을 통과시킨다"
    assert check_pfamily([], _fam)[0], "인벤토리가 비어도 통과시킨다"

    # ── 검사 17. 봉인 문서.
    # **전부 합성 입력이다.** 진짜 봉인 문서를 오라클로 쓰면 그 문서가 훼손됐을 때
    # 거짓양성 어서션이 먼저 죽어서 main 의 제대로 된 보고를 가린다(실물 훼손
    # 시험에서 실제로 그 엉뚱한 메시지가 나왔다 — check_names 가 같은 이유로
    # `mine()` 을 쓴다).
    tmp, sealed_tmp = Path("_checkdocs_tmp.md"), Path("_sealed_tmp.md")
    try:
        sealed_tmp.write_text("# 시험용\n\n> 인용하지 마\n", encoding="utf-8")
        fake_sealed = {str(sealed_tmp): "인용하지 마"}
        tmp.write_text(f"| [`{sealed_tmp}`](x) | 초기 결과 |\n", encoding="utf-8")
        assert any("표시가 없다" in x
                   for x in check_sealed([str(tmp)], fake_sealed)[0]), \
            "봉인 문서를 표시 없이 가리키는 줄을 통과시킨다"
        tmp.write_text(f"| [`{sealed_tmp}`](x) | **인용 금지** |\n", encoding="utf-8")
        assert not check_sealed([str(tmp)], fake_sealed)[0], \
            "같은 줄의 인용 금지를 못 읽는다"
        # 봉인 표시가 머리에서 사라지면 잡아야 한다 — 상자를 지우면 봉인이 풀린다
        sealed_tmp.write_text("# 시험용\n\n> 상세 분석\n", encoding="utf-8")
        assert any("봉인 표시" in x
                   for x in check_sealed([str(tmp)], fake_sealed)[0]), \
            "봉인 표시가 없는 문서를 봉인으로 통과시킨다"
        assert check_sealed([], {"_no_such_sealed.md": "x"})[0], \
            "없는 봉인 문서를 통과시킨다"
    finally:
        tmp.unlink(missing_ok=True)
        sealed_tmp.unlink(missing_ok=True)
    # 봉인 문서의 p 도 검사 4 를 받는다(main 이 범위에 넣는다). 여기서는 **범위에
    # 실제로 들어가는지**만 본다 — 값을 어서션으로 걸면 봉인 문서를 정정하는 중에
    # 검사기가 통째로 죽는다. 이 한 줄이 없으면 봉인 문서에서 p 가 사라져도
    # "검사 17 이 p 를 본다" 는 주장이 조용히 빈말이 된다.
    assert any(Path(_s).exists() and PVAL.search(
        COMMENT.sub("", Path(_s).read_text(encoding="utf-8"))) for _s in SEALED), \
        "봉인 문서에 p 가 하나도 없다 — 검사 4 가 거기서 아무것도 안 본다"

    # ── 프로토콜 혼합 집계. 교란 상자를 지우면 잡는가.
    _h = Path("HARDENING.md").read_text(encoding="utf-8")
    # **"지금 저장소가 맞는가" 를 어서션으로 걸지 않는다.** main 이 매 실행마다
    # 진짜 입력으로 그것을 보고한다 — 여기서 또 걸면 문서를 갱신하는 중에 검사기가
    # 통째로 죽어 **무엇이 틀렸는지도 안 나온다**(check_raw·check_dataset 이 같은
    # 이유로 그렇게 돼 있다). 대신 **아무것도 안 보고 OK 를 내는 것**을 막는다 —
    # 이 검사기의 실패 방식은 틀린 값을 통과시키는 것이 아니라 그쪽이다.
    assert check_protocol(_h)[1] >= 1, "프로토콜 대조 항목이 비어 있다"
    assert any(PROTO_CONFOUND in x
               for x in check_protocol(_h.replace(PROTO_CONFOUND, "한 실험이다"))[0]), \
        "교란 상자를 지운 것을 통과시킨다"
    assert any("proxy-replaces.json" in x for x in
               check_protocol(_h.replace("proxy-replaces.json", "어딘가"))[0]), \
        "원시 파일 이름이 빠진 교란 상자를 통과시킨다"

    # ── 검사 11. 이름표와 파일 안 버전이 어긋난 샤드를 잡는가. 진짜 원시는
    # 건드리지 않고 가짜 샤드를 잠깐 놓았다 지운다.
    fake = Path("wsl-v9.9.9-E-B1-write-outside-dontAsk-00000000T000000.json")
    try:
        fake.write_text(json.dumps({
            "case": "cases/E-B1-write-outside.yaml", "mode": "dontAsk",
            "attempts": 1, "valid": 1, "violations": 0, "verdict": "FIXED",
            "agent_version": "1.2.3"}), encoding="utf-8")
        assert any("꼬리표와 내용이 다르다" in x for x in check_raw()[0]), \
            "이름표와 agent_version 이 어긋난 샤드를 통과시킨다"
    finally:
        fake.unlink(missing_ok=True)


def main():
    selfcheck()
    bad, pairs, ps, unver = [], 0, 0, []
    # p 재계산(4)은 **봉인 문서까지** 본다. 봉인은 인용 금지이지 검사 면제가
    # 아니고, 정정 상자는 봉인된 본문이 아니라 현행 주장 층이다. 나머지 검사를
    # 같이 넓히지는 않는다 — `check_registry` 를 거기 넓히면 오탐이 난다(위 주석).
    for d in DOCS + sorted(SEALED):
        if Path(d).exists():
            if d in DOCS:
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
    en_bad, en_fracs = check_en_mirror()
    bad += en_bad
    name_bad, outs, exempt = check_names()
    bad += name_bad
    skipped += exempt
    reg_bad, watched, reg_ok = check_registry()
    bad += reg_bad
    skipped += reg_ok
    ds_bad, ds_checked, ds_skipped = check_dataset()
    bad += ds_bad
    skipped += ds_skipped
    sp_bad, sp_tags, sp_ok = check_split()
    bad += sp_bad
    skipped += sp_ok
    lic_bad, lic_checked, lic_skipped = check_license()
    bad += lic_bad
    skipped += lic_skipped
    pr_bad, pr_checked, pr_skipped = check_probes()
    bad += pr_bad
    skipped += pr_skipped
    pf_bad, pf_checked, pf_skipped = check_pfamily()
    bad += pf_bad
    skipped += pf_skipped
    se_bad, se_checked = check_sealed()
    bad += se_bad
    pt_bad, pt_checked, pt_skipped = check_protocol()
    bad += pt_bad
    skipped += pt_skipped
    for b in bad:
        print("  " + b)
    # 무엇을 실제로 봤는지 낸다. 아무것도 안 보고 OK 를 내는 것이 이 검사기의
    # 실패 방식이고, TOL 을 0.02 로 뒀을 때 실제로 그랬다.
    print(f"문서 내부 정합: 구간 {pairs}쌍 · p {ps}건 재계산 · "
          f"원시 대조: {checked}항목 · 문서 간 칸 {cells}개 · "
          f"영어 요약 분수 {en_fracs}개 · "
          f"결과 파일 이름 {outs}개 · 재측정 등록부 {watched}값 · "
          f"데이터셋 {ds_checked}항목")
    print(f"계열 표기 꼬리표 {sp_tags}개 · 라이선스 {lic_checked}항목 · "
          f"프로브 등록부 {pr_checked}항목 · p 인벤토리 {pf_checked}항목 · "
          f"봉인 {se_checked}자리 · 프로토콜 {pt_checked}항목")
    fam = family()
    bon, bh = multiplicity(list(fam.values()) or [1.0])
    print(f"다중비교: 대비 {len(fam)}개 · 본페로니 {bon:.5f} · BH {bh:g}")
    for s_ in skipped + unver:
        print(f"  건너뜀: {s_}")
    print(f"문서 표기 대조: {'FAIL ' + str(len(bad)) + '건' if bad else 'OK'}")
    return bad


if __name__ == "__main__":
    # `selfcheck` 인자는 훼손 시험만 돈다. 문서 대조 없이 **검사기가 실제로 무는지**
    # 만 보고 싶을 때 쓴다(비용 0). 인자 없이 부르면 main 이 selfcheck 를 먼저 돈다.
    if len(sys.argv) > 1 and sys.argv[1] == "selfcheck":
        selfcheck()
        print("check_docs selfcheck OK")
        sys.exit(0)
    sys.exit(1 if main() else 0)
