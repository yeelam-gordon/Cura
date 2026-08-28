# Executable shot list

Use a `1920 × 1080` canvas. This resolution is a production choice, not an evidence claim. Keep source paths visible when practical. Never replace a gate placeholder with a success card unless the corresponding guide procedure has actually run and its immutable evidence has been retained.

| Time | Classification | Capture instructions | Required label |
|---|---|---|---|
| `00:00–00:13` | STATIC ORIGINAL EVIDENCE | Open `[O3]` at “Observed workflow facts.” Frame the x64 CRT leakage and missing signing parity bullets. | `BEFORE — ORIGINAL AUDIT` |
| `00:13–00:27` | STATIC IMPLEMENTATION | Open `cura-workflows\.github\workflows\cura-installer-windows-arm.yml` around Arm CRT discovery and signing verification. Do not show it as executed output. | `AFTER — IMPLEMENTED, NOT EXTERNALLY EXECUTED` |
| `00:27–01:10` | STATIC PROCESS EVIDENCE | Show the fleet output folders for design, review, implementation, regression fix, and readiness. Animate arrows and hash icons. Sources: `[D] [DR] [I] [CR] [F] [R]`. | `MANAGER / WORKER EVIDENCE LOOP` |
| `01:10–01:40` | STATIC IMPLEMENTATION | Show `validate_pe_architecture.py`, MSI/NSIS `check=True`, `workflow_provenance.py`, `windows_arm_artifact_contract.py`, stable `matrix.platform`, and architecture-qualified artifact names. | `REUSABLE FAIL-CLOSED TOOLING` |
| `01:40–02:09` | EXTERNAL GATE — NOT EXECUTED | Show a three-stage diagram: native Arm payload → secure x64 sign/package → hosted Arm smoke. Dim every stage and add an “unexecuted” badge. Source: `[R] [G]`. | `PLACEHOLDER — EXTERNAL RUNS REQUIRED` |
| `02:09–02:27` | VERIFIED LOCAL OUTPUT | Open `[R]` at “Exact local validation evidence,” then show the matching readiness hash and both clean diff-check results from `DEMO.r1.md`. | `VERIFIED LOCAL OUTPUT / READ-ONLY REVERIFICATION` |
| `02:27–02:45` | STATIC PROCESS EVIDENCE | Show Cura and shared `cura-workflows` feeding the validator, provenance, contract, and runbook controls. Source: `[O1] [O4] [R] [G]`. | `ECOSYSTEM MULTIPLIER / UPSTREAM PATH` |
| `02:45–02:59` | EXTERNAL GATE — NOT EXECUTED | Full-screen limitations card. | `NO EXTERNAL SUCCESS CLAIM` |
| `02:59–03:22` | EXTERNAL GATE — NOT EXECUTED | Show the ordered next-step card and an empty frame for future CI, signing, and hardware footage. | `LOCAL PASS — PUBLICATION GATED` |

## External capture placeholders

Do not fabricate these shots. Replace a placeholder only with guide-compliant evidence:

- Exact immutable `C`, `V`, and `W` package and installer runs, URLs, summaries, artifact identifiers, and contract hashes `[G]`.
- Native self-hosted Windows Arm64 payload evidence and secure self-hosted x64 packaging evidence `[G]`.
- Production Authenticode and timestamp verification for internal and final files `[G]`.
- Hosted `windows-11-arm` smoke evidence `[G]`.
- Physical EXE and MSI clean install, lifecycle, launch, slice, export, restart, and uninstall evidence `[G]`.
- Performance, power, publication, and maintainer approval evidence only after separately approved execution `[R]`.
