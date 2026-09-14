#!/usr/bin/env python3
"""정제본 스키마 v1 마이그레이션 — `dataset/survey/normalized/*.yaml`.

**왜 덤프하지 않는가.** 이 파일들은 40~70%가 주석이고 그 안에 CC BY 3(a)(1)
표시와 PolyForm Required Notice 가 들어 있다(cipr.yaml 머리, livepi.yaml:16-20,
redcode.yaml:16-22, poisoned-skills.yaml:10-18, aishelljack.yaml:12-21).
PyYAML 에는 주석 보존 덤프가 없고 ruamel 은 새 의존성이라 금지다. 그래서
`yaml.compose()` 가 주는 **노드 좌표**(start_mark.line/column)로 바꿀 줄의
바꿀 열만 집는다. 정규식이 아니라 파서가 준 위치이고, 주석·들여쓰기·블록
스칼라는 한 글자도 안 건드린다.

돌리는 법:  python dataset/survey/migrate_normalized.py          (적용)
            python dataset/survey/migrate_normalized.py --check  (계획만 인쇄)
비용 0. 모델을 부르지 않는다.
"""
import collections
import pathlib
import sys

import yaml

NORM = pathlib.Path(__file__).resolve().parent / "normalized"

SCHEMA_VERSION = 1

# 파일 층 provenance 블록 안에서만 적용한다. 사례 층(cases[].provenance)은
# 이미 dataset/schema.md 7칸을 따르므로 건드리지 않는다.
RENAME = {
    "repo": "source_url",
    "source": "source_name",
    "collected": "obtained",
    "raw_path": "local_path",
    "raw_size": "checkout",
    "arxiv": "paper",
}

# aishelljack 만 `obtained` 가 날짜가 아니라 "경로 — n files, m B" 문자열이고
# 날짜는 옆 칸 `collected` 에 있다. 먼저 checkout 으로 비켜 준 뒤 collected 를
# obtained 로 올린다. 값은 한 글자도 안 바꾼다 — 쪼개면 지어내기가 된다.
PER_FILE_RENAME = {"aishelljack.yaml": {"obtained": "checkout"}}

# 최상위 키 개명.
TOP_RENAME = {"meta": "provenance", "what_this_source_does_not_test": "what_it_does_not_test"}

# dataset/schema.md 열거값에 맞춘다. 검사를 무르게 하지 않고 표기를 고친다.
ORIGIN_ENUM = {"changelog", "docs", "cve", "design", "measurement", "external"}
OUTCOME_FIX = {"block": "deny"}
# cipr X-cipr-control-clean-repo — 자극이 없는 정상 빌드라 schema.md 의 benign.
# `control` 은 cases/*.yaml 의 kind 축 값이고 schema.md 가 다른 축이라고 못박았다.
DTYPE_FIX = {"X-cipr-control-clean-repo": ("control", "benign")}

# cases[] 에서 빼고 not_ported 로 옮기는 레코드. 스스로 "옮기지 않는다"고 적어
# 놓고 cases 에 앉아 있었고, 필수 칸 input_artifacts·preconditions 가 없다.
MOVE_OUT = {"agentcanary.yaml": "X-canary-chain-revshell-bashrc"}


class StrictLoader(yaml.SafeLoader):
    """중복 키를 조용히 덮지 않는다. safe_load 의 기본은 나중 값으로 덮어쓴다."""


def _no_dup(loader, node, deep=False):
    seen = set()
    for k, _ in node.value:
        key = loader.construct_object(k, deep=deep)
        if key in seen:
            raise ValueError(f"중복 키: {key!r} ({node.start_mark})")
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_dup)


def load_strict(text):
    return yaml.load(text, Loader=StrictLoader)


# ---------------------------------------------------------------------------
# 계획
# ---------------------------------------------------------------------------
def _items(node):
    return node.value if isinstance(node, yaml.MappingNode) else []


def _get(node, name):
    for k, v in _items(node):
        if k.value == name:
            return k, v
    return None, None


def _rename(keynode, new, edits):
    m = keynode.start_mark
    edits.append((m.line, m.column, keynode.value, new))


def _setval(valnode, old, new, edits):
    m = valnode.start_mark
    assert valnode.value == old, (valnode.value, old)
    edits.append((m.line, m.column, old, new))


def _case_records(root):
    """case_id 를 가진 레코드만. 상류 요약(case_id 없음)은 스키마가 다르다."""
    for key in ("cases", "case_candidates", "not_ported", "not_normalized"):
        _, seq = _get(root, key)
        if not isinstance(seq, yaml.SequenceNode):
            continue
        for item in seq.value:
            if isinstance(item, yaml.MappingNode) and _get(item, "case_id")[0] is not None:
                yield key, item


def plan(path, text):
    """(줄 편집 목록, 구조 편집 dict) — 둘 다 비면 이미 v1 이다."""
    root = yaml.compose(text)
    edits = []
    struct = {}
    name = path.name

    if _get(root, "schema_version")[0] is None:
        first = min(k.start_mark.line for k, _ in _items(root))
        struct["insert_version"] = first

    # 최상위 키 개명 + aishelljack 의 meta 풀기
    unwrap = None
    keys = [k for k, _ in _items(root)]
    for i, (k, v) in enumerate(_items(root)):
        if k.value == "meta" and _get(v, "provenance")[0] is not None:
            # meta 아래에 provenance 가 또 있다 — 개명이 아니라 한 겹 벗기기다.
            nxt = keys[i + 1].start_mark.line if i + 1 < len(keys) else len(text.splitlines())
            unwrap = (k.start_mark.line, nxt)
            nk, _ = _get(v, "name")
            if nk is not None:
                _rename(nk, "source_name", edits)
        elif k.value in TOP_RENAME:
            _rename(k, TOP_RENAME[k.value], edits)

    if unwrap:
        struct["unwrap"] = unwrap

    # 파일 층 provenance 안의 칸 이름
    prov = _get(root, "provenance")[1] or _get(root, "meta")[1]
    if unwrap:
        prov = _get(prov, "provenance")[1]
    if isinstance(prov, yaml.MappingNode):
        # aishelljack 만 파일 층에 origin 이 있고 값이 `design` 이었다. 외부
        # 코퍼스에 붙을 수 없는 값이라 열거값으로 고친다(schema.md origin).
        ok, ov = _get(prov, "origin")
        if ok is not None and ov.value != "external":
            _setval(ov, ov.value, "external", edits)
        once = PER_FILE_RENAME.get(name, {})
        table = dict(RENAME)
        table.update(once)
        present = {k.value for k, _ in _items(prov)}
        for k, _ in _items(prov):
            new = table.get(k.value)
            if not new:
                continue
            if new in present:
                # 일회성 자리 비키기는 이미 끝난 것이다(멱등). 그 외는 충돌이다.
                if k.value in once:
                    continue
                # 비켜 주는 쪽이 먼저 개명되면 충돌이 아니다.
                if table.get(new) is None:
                    raise ValueError(f"{name}: `{k.value}` -> `{new}` 가 기존 칸을 덮는다. 손으로 갈라라")
            _rename(k, new, edits)

    # 사례 층 열거값
    for _, rec in _case_records(root):
        cid = _get(rec, "case_id")[1].value
        _, p = _get(rec, "provenance")
        if isinstance(p, yaml.MappingNode):
            ok, ov = _get(p, "origin")
            if ok is not None and ov.value not in ORIGIN_ENUM:
                # 자료 이름은 ref 와 파일 이름이 이미 지목한다. 정보 손실 없음.
                _setval(ov, ov.value, "external", edits)
        _, ep = _get(rec, "expected_policy")
        if isinstance(ep, yaml.MappingNode):
            ok, ov = _get(ep, "outcome")
            if ok is not None and ov.value in OUTCOME_FIX:
                _setval(ov, ov.value, OUTCOME_FIX[ov.value], edits)
        if cid in DTYPE_FIX:
            old, new = DTYPE_FIX[cid]
            dk, dv = _get(rec, "dataset_type")
            if dk is not None and dv.value == old:
                _setval(dv, old, new, edits)

    # cases 에서 not_ported 로 빼기
    target = MOVE_OUT.get(name)
    if target:
        _, seq = _get(root, "cases")
        if isinstance(seq, yaml.SequenceNode):
            for item in seq.value:
                ck, cv = _get(item, "case_id")
                if cv is not None and cv.value == target:
                    assert item is seq.value[-1], "마지막 항목만 옮길 수 있다"
                    struct["move_out"] = item.start_mark.line
    return edits, struct


# ---------------------------------------------------------------------------
# 적용
# ---------------------------------------------------------------------------
def apply(text, edits, struct):
    lines = text.split("\n")
    for line, col, old, new in sorted(edits, key=lambda e: (-e[0], -e[1])):
        s = lines[line]
        assert s[col:col + len(old)] == old, (line, col, old, s)
        lines[line] = s[:col] + new + s[col + len(old):]

    if "move_out" in struct:
        i = struct["move_out"]
        head = ["# cases 가 아니다 — 아래 what_it_does_not_test 가 옮기지 않는 이유를 적는다.", "not_ported:"]
        lines[i:i] = head if not lines[i - 1].strip() else [""] + head

    if "unwrap" in struct:
        a, b = struct["unwrap"]
        for i in range(a + 1, min(b, len(lines))):
            if lines[i].startswith("  "):
                lines[i] = lines[i][2:]
        del lines[a]

    if "insert_version" in struct:
        i = struct["insert_version"]
        if "unwrap" in struct and i > struct["unwrap"][0]:
            i -= 1
        lines[i:i] = [f"schema_version: {SCHEMA_VERSION}", ""]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 대조 — 스크립트가 스스로 확인한다
# ---------------------------------------------------------------------------
def comments(text):
    return [l.strip() for l in text.split("\n") if l.strip().startswith("#")]


def scalars(obj, out=None):
    """모든 잎 값. 키는 안 센다 — 개명이 값에 영향을 주면 안 된다."""
    out = collections.Counter() if out is None else out
    if isinstance(obj, dict):
        for v in obj.values():
            scalars(v, out)
    elif isinstance(obj, list):
        for v in obj:
            scalars(v, out)
    else:
        out[repr(obj)] += 1
    return out


def census(obj, key, out=None):
    out = [] if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                out.append(repr(v))
            census(v, key, out)
    elif isinstance(obj, list):
        for v in obj:
            census(v, key, out)
    return sorted(out)


def verify(before, after, edits, struct, name):
    b, a = load_strict(before), load_strict(after)

    got, want = comments(after), comments(before)
    if "move_out" in struct:
        want = want + ["# cases 가 아니다 — 아래 what_it_does_not_test 가 옮기지 않는 이유를 적는다."]
        want.sort(), got.sort()
    assert got == want, f"{name}: 주석이 바뀌었다 (라이선스 표시가 여기 있다)"

    for k in ("case_id", "license", "commit", "upstream_version", "file_md5", "split"):
        assert census(b, k) == census(a, k), f"{name}: {k} 가 바뀌었다"

    sb, sa = scalars(b), scalars(a)
    for _, _, old, new in edits:
        if old in RENAME or old in TOP_RENAME or old in PER_FILE_RENAME.get(name, {}) or old == "name":
            continue  # 키 개명은 값에 안 잡힌다
        sb[repr(old)] -= 1
        sb[repr(new)] += 1
    if "insert_version" in struct:
        sb[repr(SCHEMA_VERSION)] += 1
    assert +sb == +sa, f"{name}: 값이 사라지거나 생겼다 {(+sb) - (+sa)} / {(+sa) - (+sb)}"

    assert "meta" not in a, f"{name}: meta 가 남았다"
    assert isinstance(a.get("provenance"), dict), f"{name}: 최상위 provenance 가 없다"
    assert a.get("schema_version") == SCHEMA_VERSION, f"{name}: schema_version 이 없다"
    assert after.count("\r\n") == 0, f"{name}: CRLF 가 섞였다"


def main(argv):
    check = "--check" in argv
    touched = 0
    for p in sorted(NORM.glob("*.yaml")):
        before = p.read_text(encoding="utf-8")
        load_strict(before)  # 중복 키는 여기서 죽는다
        edits, struct = plan(p, before)
        if not edits and not struct:
            print(f"  = {p.name}")
            continue
        touched += 1
        after = apply(before, edits, struct)
        verify(before, after, edits, struct, p.name)
        print(f"  * {p.name}: 개명 {len(edits)} · 구조 {sorted(struct)}")
        if not check:
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(after)
            # 멱등 — 쓴 것을 다시 계획해 보면 비어야 한다.
            e2, s2 = plan(p, p.read_text(encoding="utf-8"))
            assert not e2 and not s2, f"{p.name}: 두 번째 실행이 또 고치려 든다"
    print(f"{touched} 개 파일" if touched else "이미 v1 이다")
    return 0


def selfcheck():
    """가드가 실제로 무는지. 비용 0."""
    try:
        load_strict("a: 1\na: 2\n")
        raise AssertionError("중복 키를 통과시킨다")
    except ValueError:
        pass

    class P:
        name = "x.yaml"
    try:
        plan(P, "provenance:\n  repo: a\n  source_url: b\n")
        raise AssertionError("덮어쓰는 개명을 통과시킨다")
    except ValueError:
        pass

    t = "# 표시 줄\nmeta:\n  source: s\n  repo: r\n  collected: \"2026-01-01\"\n"
    e, s = plan(P, t)
    out = apply(t, e, s)
    assert comments(out) == ["# 표시 줄"], out
    d = load_strict(out)
    assert d["schema_version"] == 1 and set(d["provenance"]) == {"source_name", "source_url", "obtained"}, d
    assert plan(P, out) == ([], {}), "멱등이 아니다"
    print("selfcheck OK")
    return 0


if __name__ == "__main__":
    sys.exit(selfcheck() if "selfcheck" in sys.argv else main(sys.argv))
