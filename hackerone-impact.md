An operator can believe filesystem and network enforcement is active while it is not, with no machine-readable way to detect the difference.

The settings file says `"sandbox": {"enabled": true}`, the process exits `0`, `result.is_error` is `false`, and no JSON event mentions the sandbox. Automation built on `--output-format stream-json` — the interface intended for exactly that purpose — has nothing to alert on.

The failure is measurable, not hypothetical. Using a build script that writes outside the workspace:

* sandbox active: **0/30** violations, 95% CI [0.00, 0.11]
* dependencies missing, `failIfUnavailable: false`: writes
  succeeded — **rate and interval withdrawn** (console observation, no per-run
  file survives; the silent-pass mechanism itself is backed by
  `verify-silent-fail.json`)

`sandbox.enabled` is `true` in both rows and the outcome is opposite, with no signal on stdout in either case. The two rows differ in more than one thing (the two packages, and `failIfUnavailable`), so this is a direction, not a one-factor contrast.

**This is not a sandbox escape.** With the dependencies present, the sandbox held in all 30 trials that left a per-run file (an earlier draw of 30 agreed but recorded none). The report concerns the observability of a control that is not running, not the defeat of one that is.

CVSS fits this issue poorly: the impact is conditional on how downstream automation consumes the structured output. It is submitted as Low deliberately.
