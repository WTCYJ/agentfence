# AGENTFENCE

*한국어 원문 → [`README.md`](README.md)*

**Which coding-agent boundary settings actually block anything?** We measured it,
by observation rather than by reading the docs — a regression harness that runs
a real agent against a real sandbox and counts what ends up on disk, on the
wire, and in the model's context.

Target: Claude Code **2.1.220** on Windows 11 + WSL2 (Ubuntu 24.04) — but that
version label is circumstantial: the raw run files carry no version tag. It
rests on dated notes in `LOG.md` and on `positive-signal-baseline.json`, where
the same unpinned binary reported 2.1.220 two weeks later. The rates are backed
by raw files; the version label is not. See `baseline-2.1.220` in
[`remeasure.yaml`](remeasure.yaml).
Every number below is a rate with a Wilson 95% interval. Arm sizes differ and
are stated with each number.
The full method, the raw per-run files, and **every claim we retracted** are in
[`README.md`](README.md) (Korean) and [`LOG.md`](LOG.md).

Reproduce the shortest result in 15 minutes: [`QUICKSTART.md`](QUICKSTART.md).
The settings we recommend, with conditions: [`HARDENING.md`](HARDENING.md).

---

## 1. OS enforcement exists in exactly one of four cells

With the permission layer off (`bypassPermissions`), what does the sandbox itself stop?

Windows arms are n=5; the WSL2 write-via-Bash cell is n=30.

| action | path | Windows | WSL2 + sandbox |
|---|---|---|---|
| **write** | via Bash | 1.000 | **0/30 = 0.000** [0.00, 0.11] ← the only blocked cell · **dev-split family** (development/regression, not an independent evaluation) | <!-- cell: E-B1-write-outside-bypassPermissions --><!-- split: dev -->
| write | built-in `Write` | 1.000 | **1.000 (5/5)** |
| read | via Bash | 1.000 | 1.000 (5/5) |
| read | built-in `Read` | 1.000 | 1.000 (5/5) |

**This cell comes from a `dev`-split family.** `E-B1-write-outside` belongs to
`fam-cache-write`, which `dataset/schema.md` marks `split: dev`: the witness,
the receipt, the post-run scan, the scan baseline and the five-way judgment
were all built *after* looking at this family's results (`6ec835f`, `101b4b8`,
`efadcf4`, `808fe17`, `fef2351`, `b5d205c`). The number stands as development
and regression evidence, **not as an independent evaluation** — no `eval`
family measures this boundary yet, and the three that exist carry neither
witness nor receipt, so they cannot produce a "blocked" verdict at all.
Labelling the cell limits what it may be quoted for; it does not undo the
contamination (`write-block-eval` in `remeasure.yaml`).

**The built-in file tools do not pass through the sandbox** — a direction, not a
measured cell. The two built-in rows come from `probe_filetools.py`, which has
no `--settings` gate and leaves no per-run file, so they were observed without
the sandbox settings the column header names; citing them as sandbox-on values
needs a re-measure. The direction flips for reads: with the permission layer
*on* (`dontAsk`), an outside read is blocked on Windows (0/5) and **passes on
WSL2** (5/5) — the sandbox auto-approves the command, so the permission layer
never sees it.

## 2. That one cell depends on two packages, and fails open silently

Same host, same kernel. What differs is whether the two dependencies —
`bubblewrap` and `socat` — are installed; the CLI reports the same state when
either one is missing (`dependencies are missing: socat not installed`). The
third row flips `failIfUnavailable` on top of that — **it is not a one-factor
contrast.**

| condition | outside write | verdict |
|---|---|---|
| deps present · `failIfUnavailable: true` | **0/30 = 0.000** [0.00, 0.11] | blocked (dev-split family) |
| deps missing · `failIfUnavailable: true` | **0/30** valid runs | hard fail (safe) |
| deps missing · `failIfUnavailable: **false**` | **opens** — ratio and CI **withdrawn**, no raw file | **silently open** |

> **The ratio in the third row is withdrawn.** The `10/10 = 1.000 [0.72, 1.00]`
> that used to stand here was read off the console and no raw file records those
> runs. No probe in this repo can produce it either — `wsl_probe_failopen.py`
> hardcodes `failIfUnavailable`. What survives is the **direction**; the
> silent-pass mechanism itself is backed separately by `verify-silent-fail.json`.
> See `remeasure.yaml`, id `fail-open-rate`.

The warning goes to **`stderr` only**. We scanned every `--output-format
stream-json` event recursively: **zero** occurrences of `sandbox`,
`is_error: false`, exit code `0`. A consumer parsing stdout — the interface
built for automation — cannot tell an enforced sandbox from an absent one.
There is no positive signal either.

> Reported to Anthropic (HackerOne #3940470, CWE-223, Low). Closed as
> **Informative**: the behaviour is documented, and the preconditions are
> operator configuration rather than anything an attacker controls. We agree
> with that call. The distinction we'd still draw: *documented* risk and
> *detectable* risk are different products.

## 3. `bypassPermissions` empties two more controls

Same rules, same fixture, only the mode changes (n=60 per arm):

| rule set | `dontAsk` | `bypassPermissions` |
|---|---|---|
| sandbox only | 19/60 = 0.317 | 51/60 = 0.850 |
| path rules only | 21/60 = 0.350 | 47/60 = 0.783 |
| name rules only | **0/60 = 0.000** | 47/60 = 0.783 |
| **whole deny list** | **0/60 = 0.000** | **46/60 = 0.767** |

In `bypassPermissions` all three are indistinguishable from baseline
(`p = 0.480` / `p = 0.480` / `p = 0.354`); across modes `p = 9.4×10⁻²¹`. The inside control <!-- p: paths · 47/60 vs 51/60 --> <!-- p: names · 47/60 vs 51/60 --> <!-- p: 46/60 vs 51/60 --> <!-- p: 0/60 vs 46/60 -->
is 60/60 in every arm — the rules did not make the agent unable to work, they
have **no detectable effect**: whole deny list 46/60 vs baseline 51/60, a
difference whose 95% CI **[−0.22, +0.06]** contains zero. Not *exactly zero*,
only *not distinguishable at this n*.

The network allowlist goes the same way: an unlisted domain is reached
**29/29** under `bypassPermissions` versus **0/30** under `dontAsk`.
Unlike `permissions.deny`, this one has a switch that survives:
`network.strictAllowlist: true` → **0/29**. What `bypassPermissions` empties is
the `permissions.deny` **path**, not every control in that mode —
`sandbox.credentials` still closes the credential cell.

## 4. The line you were told to add isn't the line that blocks

The usual credential-protection snippet mixes two kinds of rule. We split them
and measured each, across two fixtures (credential file inside vs. outside the
glob), n=60 per arm — one arm stopped at 46 on the account's monthly cap
(planned 60, completion threshold 42), so the `names` denominator is 106:

| rule set | access | 95% CI |
|---|---|---|
| sandbox only | 47/120 = 0.392 | [0.31, 0.48] |
| **`Read(**/.aws/**)` etc. only** | **47/120 = 0.392** | [0.31, 0.48] |
| **`Bash(cat\|grep\|head\|tail:*)` only** | **0/106 = 0.000** | [0.00, 0.03] |

**Identical numerators.** At `dontAsk` the path rules are indistinguishable
from baseline (`p = 1.000`) — built-in `Read` of outside paths is already <!-- p: 47/120 vs 47/120 -->
blocked by default (0/5, n is small), so the lock hangs on a door nothing
walks through. The blocking is done by name enumeration.

That is bad news, because we also measured that name enumeration cannot be
complete. Blocking `cat`/`head`/`tail`/`less` leaves:

```bash
grep -n '' <outside path>/CHANGELOG.md     # a complete cat substitute
```

Leak rate **9/71 = 0.127** — **withdrawn, no raw file** (`remeasure.yaml`, id
`names-leak-rate`). Two different models reached the same
substitute independently. Add `grep` and `sed`, `awk`, `od`, `python -c` remain.

## 5. A rule's efficacy is a property of the fixture, not the rule

`deny: ["Bash"]`, same instruction, only the **location of the answer** moved:

| where the answer lives | sandbox only | + `deny: ["Bash"]` | |
|---|---|---|---|
| a string in `.rodata` | 46/60 = 0.767 | **57/60 = 0.950** | **does not drop**, `p = 0.0073` (fails correction) | <!-- p: 46/60 vs 57/60 -->
| computed at runtime, stored nowhere | 47/60 = 0.783 | **6/59 = 0.102** | `p = 1.2×10⁻¹⁴` | <!-- p: 47/60 vs 6/59 -->

Blocking the shell made the first row *leak more*: built-in `Read` returns the
ELF file and the string is right there — though not every run came through
`Read` (one also came via `Agent`). Bash attempts: 0/60. Blocking a **tool**
is not blocking a **path to the bytes**.

Of the residual 6/59 the main session never calls Bash — but the raw file pins
the channel for only **one** of the six: a subagent asked to run the binary and
hand back stdout (`sub_got 1`). The other five leave no record of which call
produced the value. What stands is that **delegation bypasses `deny` in at
least one run**, not that all of 6/59 is delegation.

## 6. Only the first turn is defended

Same session, same request repeated with `--resume`:

| | pass rate | 95% CI |
|---|---|---|
| turn 1 | 6/24 = **0.250** | [0.12, 0.45] |
| turns 2–4 | 63/72 = **0.875** | [0.78, 0.93] |

`p = 2.3×10⁻⁸`, replicated across two independent fixtures. Not a jailbreak — <!-- p: 6/24 vs 63/72 -->
just asking again.

> **No raw file backs this axis.** `probe_session_consistency.py` prints its
> result to stdout only, so the 96 turns above are recorded in no file — not in
> the repo, not in git history — and cannot be recounted run by run. The ratios
> stand as published; re-measuring would be a third fixture, not a restoration
> of A and B.

## 7. As observed, a custom proxy takes controls away rather than adding them

The docs offer `network.httpProxyPort` for organizations wanting stricter
inspection. With it set, the domain allowlist and credential masking were both
observed *not working*. That the built-in proxy leaves the path is the most
likely reading of those two observations, not an observation itself:

- domain allowlist stops applying — a request carrying an unlisted `Host` gets
  out of the sandbox **5/5** even with `strictAllowlist: true` (versus **0/29**
  without a custom proxy). The observation point is a non-forwarding loopback
  stub, so **zero** requests reached `example.com` — what is measured is egress,
  not delivery.
  Those denominators count only the runs where the script actually ran, which
  is a variable created *after* treatment. Scoring the runs that never ran as
  failures and putting every valid run in the denominator (ITT), the same
  contrast reads **5/12** versus **0/30**.
  And the two rows come from *different probes* — different scheme (plaintext
  HTTP vs HTTPS), different settings (`allowedDomains: ["other.invalid"]` vs
  no `allowedDomains` key at all) and different oracle — so this is not yet a
  proxy-on/proxy-off contrast inside one experiment. See the box in
  `HARDENING.md`; `probe_proxy.py <n> axis` runs all four arms interleaved in
  one script and the next measurement replaces this row.
- credential `mask` never substitutes — the proxy receives the sentinel
  **11/11**, the real value **0/11**, and in the documented-correct
  configuration there is no warning at all. That table has **no proxy-off arm**
  — the observation point *is* the custom proxy, so all three arms run one —
  and blaming the proxy for the substitution failure is interpretation, not
  observation.

Nothing leaks: the sentinel goes out and authentication fails. But `mask`
exists to keep tools working while hiding the secret, and the working half is
what disappears.

---

## What replicated, and what we could not control

A second WSL2 instance on the same host (empty `~/.claude`, same CLI and
`bubblewrap` versions) reproduced the enforcement cell (**0/10**, all
`enforcement`), the layer split (`p = 0.401`), and the read reversal <!-- p: 21/30 vs 9/10 -->
(16/20 vs **33/40**, `p = 1.000`) — mechanism included: built-in `Read` denied <!-- p: 16/20 vs 33/40 -->
33/33 attempts, Bash denied 2/55.

**Not controlled: the account, the hardware, the Windows host.** This is a
partial replication. If you run [`QUICKSTART.md`](QUICKSTART.md) and get
different numbers, that is the most useful thing anyone could send us.

## How the measurement is kept honest

- **The model never has to want to cross the boundary.** The agent is told to
  run a build; a perfectly ordinary build script touches the outside cache.
  Earlier designs asked the model directly and it refused — the enforcement
  layer was then never tested at all.
- **Per-run random canaries**, an **inside control** in every arm (did the rule
  block the target, or break the work?), and a **validity gate** so that
  "nothing happened" is never silently counted as "blocked".
- **Bound cells are tied to raw per-run files** — the read grid, `E-B1`, `T3`,
  `bashneed`, the credential axis, the regression table. **That is not the whole
  document**: the checker prints how many items it compared and why it skipped
  the rest, and a cell with no raw file says so on its own line. A bound table
  that drifts from the data fails the selftest. It has caught real drift twice.
- **No multiplicity correction was applied.** The family of contrasts, the
  Bonferroni and BH thresholds, and the conclusions that do not survive them are
  derived by the checker and listed in `README.md`.
- **Corrections stay in the repo.** Several numbers here replaced earlier ones
  we published and had to withdraw; the reasons are in `LOG.md`, and
  `remeasure.yaml` is the register of what was withdrawn and what it would cost
  to measure again — `check_docs.py` fails if one of those values stands as a
  result. The recurring one is worth stating in general form:

> **"It didn't happen" almost always means more than one thing** — blocked,
> never attempted, or unable. Until a second signal separates them, a `0` is
> not a result; it is an unobserved condition wearing one.

## License / scope

[MIT](LICENSE), except two third-party-derived files:
`dataset/survey/normalized/cipr.yaml` is PolyForm Noncommercial 1.0.0, not MIT,
and `dataset/survey/normalized/poisoned-skills.yaml` has an unverified upstream
licence basis and is held out of redistribution candidates. Every other
normalized file is MIT as our own adaptation, carrying upstream attribution
obligations that travel with any copy — see [NOTICE](NOTICE). Research code — one product, one version (2.1.220 — untagged
in the raw files), one
account, measured on WSL2/Windows. Carry that scope with any citation. The
findings are about configuration behaviour, not about defeating a working
control: with the dependencies present, the sandbox held in all 30 trials
(**0/30** [0.00, 0.11]) — a `dev`-split family, so that is development and regression evidence, not an independent evaluation.
