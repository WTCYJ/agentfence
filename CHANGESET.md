# AGENTFENCE 변경본 해시 명세

기준 커밋: 79cf54d532fe7a3e7b5558d3d68e010642013faf

대상은 이 커밋 위에 올린 정비 변경 전량이다. 둘은 뺐다 —
`.gitignore` 된 `dataset/raw/`(외부 저작물, 재배포하지 않는다)와
**작성 시점에 진행 중이던 2026-09-14 회귀 실행 기록**(`run-log/*20260914*`).
쓰이는 중인 파일을 해시로 고정하면 다음 줄이 붙는 순간 값이 틀린다.
그 기록은 실행이 끝난 뒤 따로 커밋한다.

다시 만들려면 같은 방식으로 센다. 값이 다르면 그 사이에 파일이 바뀐 것이다.

```bash
git diff --cached --name-only
```

파일 64개

| sha256 | 바이트 | 경로 |
|---|---|---|
| `4771bef2c04a34b548b77ea7581cf821152d9dea9c2c85151a07856fe3639314` | 3 | `.lock-E-B1-write-outside-bypassPermissions` |
| `336bb644c8ed076831b11802aefafc8fbe744ae9687322c0710ef718d13f0670` | 43398 | `HARDENING.md` |
| `23a978c75bf53e618f64fa4fcd74140bb6cd7366ad126ef06d8ad387ce0926d4` | 2432 | `LICENSE` |
| `e903468a5ee076b4d6ef36047275df7821800bd93cdd0c26c795e742aeffa48f` | 136470 | `LOG.md` |
| `d85bc3025e58df060929ab73f7b4f1a4907d5c20c79119965463438324680316` | 20548 | `NOTICE` |
| `39703f5063cb2a84e1fe1edfb71a54c9dc1670201a7a4bbedd56cb0c2a3a1d6d` | 3511 | `QUICKSTART.md` |
| `42e11b0a3e50a9afd5e7ff63c7668c70b92a7f78bbba9b399c6056166da64828` | 15120 | `README.en.md` |
| `cb3fab55a980f1d66e7d48aae3e80440bcd3718e9a95d8f9dbca4e87e1f514c3` | 104415 | `README.md` |
| `cfa896dc50890d66cebafd156431b87110c5396b67bc1d0d3333244e6628d879` | 75614 | `artifact/results.html` |
| `658815ef9496792662e07324f8780aa947c66f2d4fc45d4b03cf0e0f772a4ae9` | 164857 | `check_docs.py` |
| `710abfacae93985b6e9ee264f30f02c1bb2706fddf43ff14513e657c789c35c4` | 3634 | `check_mask_warn.py` |
| `cf00f36245e25a66e823a254898a323a998afdfc8dc1cb7ff7329438d7af4e9e` | 4996 | `check_positive_signal.py` |
| `979815fbd919f6035ea741da1b0e8e05a7c03ae8cbd6c34824931027f0bddc23` | 3856 | `classify_executed.py` |
| `e5ec4418ef27ee9a9aa0520f7bad29ea4d7baaeb3991cafb33da5c492797d005` | 20771 | `dataset/external.md` |
| `307271188e841ed634f9769448c2e27557a3a70bd6bb4598092cd0b95fdb2c3c` | 17126 | `dataset/survey/README.md` |
| `668745132e613194a4b0b77053e2b47cf600d7ae8a77d2bb53a4b1bb9b6e0455` | 4128 | `dataset/survey/evidence/datacite-10.5281-zenodo.19281322.json` |
| `fb78c8aeb3cf6648c0be867b406bd7859ec6380ec92f56865b5a95ceab6aec73` | 4330 | `dataset/survey/evidence/datacite-10.6084-m9.figshare.30111988.json` |
| `259298323ada9e62ac4b3cc3a2c4a8f629d001dd51292ca24cdab6c3ff86aa7b` | 13675 | `dataset/survey/migrate_normalized.py` |
| `727a8c8c625223ef1e5165aec3311ce1b845df91716da39bf0c321cca1ea06e2` | 26893 | `dataset/survey/normalized/agentcanary.yaml` |
| `73294b7aae926747bfe121b8a249c482332f2e3ca665cda0cf9708b3664fa860` | 76283 | `dataset/survey/normalized/aishelljack.yaml` |
| `aa35ef2ea5418bd88f377a50372e2d5d55ec422b468f7bcf4245418b08b8c89d` | 16542 | `dataset/survey/normalized/bipia.yaml` |
| `a327de75166b4ee4082b36c46d193e693c87779b4353d0842f90f515a85ac531` | 33528 | `dataset/survey/normalized/cipr.yaml` |
| `cf22d80b00202ddd9f390f02a3567525733c1c6d3b740664a83665368144e095` | 17068 | `dataset/survey/normalized/deeptrap.yaml` |
| `40381e45e059235cce104b2b92aacece373ff523d441f519ae4ef28b58757916` | 14001 | `dataset/survey/normalized/inspect-evals-agentdojo.yaml` |
| `56599a581378dbd5ff6a7d9b1567eea81c993a4db2e010522912d654589c8b33` | 14220 | `dataset/survey/normalized/livepi.yaml` |
| `3862152c7ca58630f7dda73e642e6dc692b7ca82078b339520a6c5ba9f086cb0` | 10978 | `dataset/survey/normalized/malicious-agent-skills-bench.yaml` |
| `84db7d32de07a182be68b32b2650619370903c3013deb2c27938cacd608d4a6f` | 16235 | `dataset/survey/normalized/poisoned-skills.yaml` |
| `8877a66ac2f74850bfa5e871955d8a74f72c73c2f5bb28f931b8f5b0801398cb` | 23932 | `dataset/survey/normalized/redcode.yaml` |
| `8a17e9d9a6cffce26effd5a9f52bf8b87c477ba0e41a7d6a98189b34b6548794` | 22695 | `dataset/survey/normalized/redteamcua.yaml` |
| `9cc371b6b3b5c2d595926dc33738c9c8b54932cba5a4e06d799a76282ee77512` | 2598 | `diag_sandbox.py` |
| `7f94d741268adf6656130544beb4ec3087a85447678fec6d29d2b851a8baa9ef` | 9019 | `docs/01-project-overview.md` |
| `ec9a75c7dd79ef57a0b1ac276391027d7730cbc93eddfe982f5d486a976b05dc` | 22723 | `docs/90-model-behavior-analysis.md` |
| `496a83ee46034ac2386b52ee45d91a5ffedccc3b931fc0cb8ee0cc8181e552ea` | 44788 | `p-family.yaml` |
| `9b10624ad780fbac34392b27369d00146ea8dd82a4b03e70cbfab393cec5ebc5` | 40483 | `plan/independence.yaml` |
| `27a8a59ce0b8e3be7f3c14ce46d5eb0b6e6913383b00ae21a5c1357bcbbaeb8d` | 3131 | `preflight.py` |
| `96126829609588bfad13e35f9cf38d4796d17ccb32c1ad6f48c4d907f0b5b5cb` | 17148 | `probe_bash_needed.py` |
| `6f71f5d74f37159de38d87c5c9d77dd76b1d4db146267dc5f437e289e5fdfeb5` | 24377 | `probe_credentials.py` |
| `3fd155ed367adce6272afe142acadcec59bcf62da1f4a42665c77e746acf1467` | 11657 | `probe_credguard.py` |
| `900f7b1e83d0ac45e32864bcf4bcfde23bbc8fadfbe06d747d9547a7a5b35483` | 4903 | `probe_filetools.py` |
| `65146b6f621cfe7f5b8ab8d99b56fcae377afed0905c60f3ae7bde04095b49dd` | 3561 | `probe_model_axis.py` |
| `b8915adfd8ea760acd3fc77bde2773efb6990affcb8557a2258cfbce62facb69` | 14146 | `probe_network.py` |
| `95541cb44a6188dd2a103d923389dc64a41a3c760a503449af5fcff424df3163` | 4906 | `probe_path_naming.py` |
| `41e43de25efd6ce552fe92fd39cb89d80fafccf8e8d2ed171384a434657f193c` | 4761 | `probe_persistence_flag.py` |
| `cadacf396a834f10e80c820eea5cef87fdd22cd76824b1d0a8cdea4306b96cf2` | 35238 | `probe_proxy.py` |
| `a9af28fbbd8e8865069ef79dc782b79307857c25fcbbe97e3689bc0ce92e1bcd` | 14107 | `probe_read.py` |
| `5130b3a97dda0718b42d1962e5d9298656e7ac0854c353234c50e7a14769b4e7` | 3613 | `probe_readout.py` |
| `1737418ab3fab30e86c8aec0024fcc0418c6eaca7a81c6874f61f675a7ceb6b5` | 14772 | `probe_session_consistency.py` |
| `c50c34ded00efa49211b09d378aa0c21791951d673c0e06d7ae03d0541d7be73` | 4060 | `probe_session_split.py` |
| `31a0550a8b6d1db10f6e5bc7be701a23d7f5e3a4c821363fd29685c09d49b18e` | 16251 | `probes.yaml` |
| `b1f084a62919fc7a8f92f7562e141df9f2ba6095f0f70af1fc0270cffeb30f97` | 24479 | `remeasure.yaml` |
| `a3163f0b1e69f2861381aee49eb060ecc6798251eed49c45aa4791ff5681224e` | 2057 | `repro_exec_rate.py` |
| `f62f18d7265a0ebcf4304c0a6a5d014e23e88c10b69a0d23c7412e2b671638a9` | 38690 | `run-log/20260909T223838-38672-ledger.jsonl` |
| `6bd9c733dea9fda42d79a3041bc10a4f2766255d53f4c067b91206666599d120` | 247 | `run-log/20260910T015359-50772-ledger.jsonl` |
| `57ae040535a6f6c2196f1d9fbc3f90758556d455cb613c25dcf2b748dafb6186` | 9672 | `run-log/README.md` |
| `f9c8797ca24153cb140e45f55cf6dcb1e284ab4dddf7775a6fdeb1a09e5f7231` | 11970 | `run-log/WHY-20260910-import-runs.md` |
| `18301968fef0b0a4a9556f2d99a5653f3ce3c5e8d3dd0d23c8f41040a0fcffbc` | 10662 | `run_regression.sh` |
| `b33dda00be4c572245e6c4326c1d87d743af049e6cd21daf7835daf693880256` | 105551 | `runner.py` |
| `be10753fdb1563f8ad0bb9d48a70127741f927a2ee92a6ae71d7d8f22f971811` | 3355 | `verify_audit.py` |
| `6dc157407d066703a54fac8db5b25b9b79c076e3bac7dfa2b21ade08b5d1ec33` | 7465 | `verify_silent_fail.py` |
| `c3c116abb4d1720f67b7167a1dc92dce0e5ccc9aec7e133f5f6a5ef19c50d73c` | 11294 | `writeup/2026-08-12-agentfence.md` |
| `63dde2128a64dee48ce3d8cb8b9904bdeb9b4f86df3bd4a7f40cc66f7c95a68d` | 15013 | `wsl_probe_failopen.py` |
| `a62da815477776a9b62be966cac9b381eaf27964776da433d07ec98889559493` | 5809 | `wsl_probe_lockdown.py` |
| `7fcbf3e1ef1b4a069041966af69b2beaff4a3f28003a9212b7cf405cd1ab65db` | 4033 | `wsl_symlink_probe.py` |
| `20d57e410a56f900614754187d1f2555bd040d0c1092dec8190a43c3b35c3e1f` | 4129 | `wsl_symlink_probe2.py` |
