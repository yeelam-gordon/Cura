# Cura Windows Arm64 demo script

## Evidence rules

- Primary video target: `03:22`, derived from the subtitle timeline and paced below; this is a production estimate, not a product metric.
- `VERIFIED OUTPUT` means captured from the final readiness record or a read-only command against the current workspace.
- `STATIC IMPLEMENTATION` means code or documentation inspection only; it does not imply workflow execution.
- `EXTERNAL GATE — NOT EXECUTED` must remain visible wherever CI, signing, payload, installer, GUI, hardware, performance, power, or publication is discussed.
- Sources are listed in `impact-evidence.md`. The final readiness source is `[R]`; the authoritative runbook is `[G]`.

## Storyboard and narration

### Opening — problem and before state

**Visual:** Title card, then the original workflow audit beside the Arm workflow CRT line. Label the audit `STATIC ORIGINAL EVIDENCE` and the code `STATIC IMPLEMENTATION`.

**Narration:** Windows Arm64 support in Cura was not just a build flag. The original audit found that the Arm installer selected the x64 Visual C++ runtime path and lacked the signing parity present in the mature x64 workflow.

**Claim basis:** The original audit identifies the x64 CRT path and missing signing parity `[O3]`. The current implementation replaces that path with Arm CRT discovery and adds signing/verification logic `[R]`.

### Manager-and-worker workflow

**Visual:** Animate the fleet handoff: audit → design → risk review → implementation → code review → regression repair → readiness → demo. Show record hashes between stages. Label `STATIC PROCESS EVIDENCE`.

**Narration:** Our manager-and-worker process turned that finding into an evidence chain. Audit, design, risk review, implementation, code review, regression repair, readiness, and demo production each produced a bounded handoff. Hashes protected the handoffs, and reviewers forced defects in provenance, artifact identity, and matrix naming back through the loop.

**Claim basis:** The design, reviews, implementation reports, regression fix, and readiness records document the iterative handoffs and hash checks `[D] [DR] [I] [CR] [F] [R]`.

### Implemented after state

**Visual:** Fast code montage of the PE validator, MSI/NSIS checked subprocesses, provenance checker, stable platform identity, artifact contract, Arm CRT and native Python checks. Label every pane `STATIC IMPLEMENTATION — BEHAVIOR NOT EXECUTED IN THIS DEMO`.

**Narration:** The implemented after state is fail closed. Cura now has a dependency-free PE architecture validator, architecture-aware MSI generation, checked packaging subprocesses, and tests for malformed, mixed, missing, and empty outputs. The reusable workflows now carry exact workflow identity, stable platform names, architecture-qualified artifacts, and canonical file contracts with sizes and hashes.

**Claim basis:** The complete implementation and closure map are recorded in `[I]` and `[R]`; the required behavior is specified in `[G]`.

### Arm build, signing, and smoke design

**Visual:** Use the trust-boundary diagram from the design as a static graphic. Highlight build, secure packaging, and hosted smoke in sequence. Keep a persistent lower-third: `EXTERNAL GATES — NOT EXECUTED`.

**Narration:** The Arm path now requires native Arm host and Python identity before build work, discovers the Arm runtime instead of the x64 path, requires the native Python runtime DLL, validates the complete PE payload, transfers only a verified unsigned contract, and prepares internal and final signature verification. A hosted Arm smoke stage verifies the signed contract and engine command, but that stage has not been executed here.

**Claim basis:** These are implemented/static contracts and unexecuted gates, not completed external results `[R] [G]`.

### Measured local proof

**Visual:** Full-screen final readiness validation table, then terminal cards for the readiness hash and both clean diff checks. Label `VERIFIED LOCAL OUTPUT`.

**Narration:** Local proof is strong and specific. The final readiness record shows every local packaging and workflow suite passed, compilation and YAML parsing passed, each supported matrix case matched, Linux and Wasm names remained distinct, installer artifact names stayed architecture-qualified, forbidden patterns were absent, and both repository diffs were clean.

**Claim basis:** Exact commands, exits, and results are in `[R]`. The readiness hash and diff checks are independently reverified in the worker report.

### Ecosystem multiplier and upstream path

**Visual:** Diagram Cura → shared `cura-workflows` → package/build/sign/smoke evidence → maintainer gates. Label `REUSABLE TOOLING` and `UPSTREAM PATH`.

**Narration:** The multiplier is the method, not one patch. The validator, provenance checker, artifact contract, matrix identity, and acceptance runbook form reusable release-engineering controls for other architecture ports and upstream review across Cura and its shared workflow repository.

**Claim basis:** The coordinated repository scope comes from `[O1]` and `[O4]`; reusable tools and the exact-SHA upstream validation path are documented in `[R]` and `[G]`.

### Limitations and next external step

**Visual:** Red gate card listing all unexecuted areas, followed by an empty capture frame labeled `PLACEHOLDER — INSERT EXTERNAL EVIDENCE ONLY AFTER EXECUTION`.

**Narration:** The boundary is equally important. We do not claim hosted CI, production signing, a real Arm payload, installer lifecycle, GUI execution, physical Arm behavior, performance, power, or stable publication. The next step is an exact-commit package and installer proof, followed by secure production signing, hosted Arm smoke, x64 regression, physical EXE and MSI acceptance, and explicit maintainer approval. Locally, this is ready for external validation; publication remains gated.

**Claim basis:** The external-gate list and verdict are quoted from `[R]`; the ordered external procedure is `[G]`.
