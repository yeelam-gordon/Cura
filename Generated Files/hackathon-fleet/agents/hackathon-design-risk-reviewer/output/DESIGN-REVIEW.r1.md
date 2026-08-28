# DESIGN-REVIEW r1

## Record integrity and bounded verdict

- `DESIGN.r1.md` SHA-256 verified: `A3E7FAAEF6AB8F58A5FD52668C8E9CECCB6ACC01E26968EAA59806D5FE9A20A8`.
- `RISK.r1.md` SHA-256 verified: `F17BE2EB662C80E089B529F002AEE70C77A6F5CE3F161002F4593CD89E4BA5EB`.
- Source baselines verified unchanged at Cura `5068661cd448b954328483a499fe4ff419b695b5` and cura-workflows `126f92d186e62a8c2f50ed1883c37a81e1d929de`.

**verdict: REVISE**

The proposed build-on-Arm/sign-and-package-on-X64 architecture is viable, but r1 is not implementable as written because one accepted critical architecture defect remains unchanged and the validation provenance, cross-job contract, early architecture gate, and false-green artifact rules are incomplete. Stable promotion remains **NO-GO** until the design's production-signing and physical Windows Arm gates pass and release publication is separately approved.

## Findings

### DR-ARCH-001 — Arm workflow still injects the committed x64 `python3.dll`

- **Maps to:** `RISK-ARCH-002`
- **Design location:** “Exact change surface / PR 2 / cura-installer-windows-arm.yml,” which says to run validation after the “Python-DLL workaround,” but specifies no replacement or removal of that workaround.
- **Source evidence:** `cura-installer-windows-arm.yml:118-120` copies `Cura-workflows/python_dll_workaround/*`; the committed `python3.dll` is 56,320 bytes and its COFF Machine is `0x8664`, not Arm64 `0xAA64`.
- **Observed gap:** the proposed strict all-PE validator will correctly fail every Arm build after the unchanged x64 DLL is copied; detection is not correction.
- **Severity:** **critical**
- **Required correction:** explicitly replace the Arm step with the deployed native Arm64 Python runtime's `python3.dll`, add an Arm64-built forwarding DLL, or prove the workaround unnecessary and omit it for Arm; then assert that the resulting `python3.dll` exists and is `0xAA64`. Do not copy or allowlist the committed x64 DLL.

### DR-PROVENANCE-002 — the proof run does not pin every changed workflow/action/script

- **Maps to:** `RISK-PROVENANCE-008`, `RISK-RUNNER-005`
- **Design location:** “Cura caller/reference handling” pins only `Cura/.github/workflows/windows-arm.yml` to the workflow PR SHA; “Ordered implementation and validation” says to build the Arm Conan package through the existing package workflow.
- **Source evidence:** the called Arm workflow itself uses `ultimaker/cura-workflows/.github/actions/setup-build-environment@main` and `set-package-overrides@main` at lines 65 and 76. The setup action checks out `Ultimaker/Cura-workflows` at default `main` at `action.yml:87-89`. Cura's package caller uses `cura-workflows/.../conan-package.yml@main`, does not pass `platform_windows_arm64`, and the reusable workflow defaults that input to `false`; its runner-list job also checks out `main`.
- **Observed gap:** the proposed proof can execute the PR reusable workflow while silently using upstream composite actions and helper scripts; moreover, the stated pre-merge Arm package build will neither select Arm nor exercise the PR's corrected runner label.
- **Severity:** **high**
- **Required correction:** define a validation provenance map and temporary caller changes that pin the installer workflow, package workflow, both composite actions, and the setup action's Cura-workflows checkout to one exact PR SHA. For the package proof, pass `platform_windows_arm64: true` explicitly. Record all resolved SHAs in the run and revert every validation-only reference before merge. GitHub permits SHA refs but does not permit contexts or expressions in `jobs.<job_id>.uses`.

### DR-BOUNDARY-003 — the new X64 job lacks an explicit metadata and tool/runtime contract

- **Maps to:** `RISK-RUNNER-006`, `RISK-SIGN-007`
- **Design location:** “Dependency graph and proposed architecture” and “Exact change surface / PR 2,” where `sign-and-package` only downloads “the complete unsigned payload plus `cura_inst\packaging`.”
- **Source evidence:** the current single job consumes step outputs `INSTALLER_FILENAME`, `CURA_VERSION_FULL`, and `CURA_APP_NAME` directly and creates a venv/install set before running packaging. The NSIS/MSI scripts import `jinja2` and `semver`; a fresh downstream job cannot access another job's step outputs without declared `jobs.<id>.outputs` and `needs.<id>.outputs`.
- **Observed gap:** r1 does not specify how filename/version/app-name cross the artifact/job boundary or how the clean signing job obtains Python dependencies and resolves `python`, `makensis`, `signtool`, `heat`, `candle`, and `light`.
- **Severity:** **high**
- **Required correction:** declare immutable build-job outputs (or a checked manifest artifact) for all packaging metadata; make `sign-and-package` depend on and validate them; install the packaged installer requirements into a fresh venv; preflight every required executable and certificate path; print resolved versions/paths; then package and sign. Never depend on residual state in a self-hosted workspace.

### DR-VALIDATION-004 — required outputs can still degrade to upload warnings

- **Maps to:** `RISK-VALIDATION-004`
- **Design location:** “Exact change surface / PR 1” adds `check=True`; PR 2 says “upload only after verification” but does not require output assertions or `if-no-files-found: error`.
- **Source evidence:** current Arm uploads omit `if-no-files-found`; `actions/upload-artifact@v7` defaults it to `warn`. The accepted risk correction also requires expected outputs to exist and be non-empty.
- **Observed gap:** fail-fast subprocesses cover nonzero tool exits, but not a zero exit with missing/empty output, nor any required upload whose path is absent.
- **Severity:** **high**
- **Required correction:** after NSIS/MSI creation, assert each expected file exists and has nonzero length; set `if-no-files-found: error` on the intermediate payload, signed payload, EXE, MSI, application, and engine uploads; remove `always()` from success artifacts and retain diagnostics separately if desired.

### DR-ARCH-005 — build-host architecture is checked only in the later smoke job

- **Maps to:** `RISK-ARCH-009`
- **Design location:** PR 2 requires `$env:PROCESSOR_ARCHITECTURE` and native-Python assertions in `smoke-test-on-hosted-arm`, but gives no equivalent first step in `build-arm-payload`.
- **Source evidence:** the reusable workflow accepts an arbitrary string `operating_system`; current setup validates Python architecture only inside the composite action and has no explicit Windows/runner architecture gate in the Arm workflow.
- **Observed gap:** a mislabelled or misrouted build host is detected only indirectly and late by payload scanning, contrary to the accepted fail-early invariant.
- **Severity:** **high**
- **Required correction:** make the first build-job step assert `runner.os == Windows`, `runner.arch == ARM64`, `$env:PROCESSOR_ARCHITECTURE == ARM64`, and `platform.machine() == ARM64`, and emit those values in the evidence manifest before Conan or PyInstaller runs.

## Complete critical/high risk disposition

| Risk ID | Disposition in r1 |
|---|---|
| `RISK-ARCH-001` | **Accepted; design-corrected with gate.** `vswhere`, Arm64 CRT selection, named-file checks, and all-PE validation are specified. |
| `RISK-ARCH-002` | **Accepted; OPEN critical.** See `DR-ARCH-001`. |
| `RISK-PACKAGE-003` | **Accepted; design-corrected with gate.** Architecture parameter, `arm64`, Template Summary, Page Count, and WiX acceptance gate are specified. |
| `RISK-VALIDATION-004` | **Accepted; PARTIAL/OPEN high.** `check=True` is covered; missing/non-empty output assertions and upload hard-failure semantics are not. See `DR-VALIDATION-004`. |
| `RISK-RUNNER-005` | **Accepted; PARTIAL/OPEN high.** `windows-11-arm` is an official current label and a completed run is gated, but the pre-merge package caller/provenance path is not wired. See `DR-PROVENANCE-002`. |
| `RISK-RUNNER-006` | **Accepted; PARTIAL/OPEN high.** Version-independent `vswhere` discovery and X64 packaging are sound, but the fresh packaging job's tool/runtime preflight is unspecified. See `DR-BOUNDARY-003`. |
| `RISK-SIGN-007` | **Accepted; design-corrected with external gate.** X64 secure-runner signing, internal-before-container signing, verification, and credential gates are explicit. |
| `RISK-PROVENANCE-008` | **Accepted; OPEN high.** See `DR-PROVENANCE-002`. |
| `RISK-ARCH-009` | **Accepted; PARTIAL/OPEN high.** Strict payload/MSI/smoke validation is specified, but the build job lacks the required early host/Python assertion. See `DR-ARCH-005`. |
| `RISK-RELEASE-010` | **Accepted; bounded closed for this scope.** Arm remains intentionally excluded from stable publication until physical acceptance and a separate maintainer decision; r1 makes no stable-promotion claim. |

## Revision acceptance boundary

A revised immutable design may receive `GO` only after it incorporates the five corrections above, retains every production-signing/physical-hardware/release gate, and defines one exact-SHA proof path whose logs show native Arm build identity, zero unapproved non-Arm64 payload PEs, verified signatures, valid Arm64 MSI metadata, hard-failing artifacts, and successful hosted Arm engine execution.

**confidence: high**

**Justification:** the immutable records, current source, binary header, official runner/image documentation, GitHub reusable-workflow/output rules, and artifact-action defaults directly establish both the architecture's viability and the remaining critical/high gaps.
