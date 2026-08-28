# IMPLEMENT r1 worker report

## Record integrity and decision

- Read `DESIGN.r3.md` and `DESIGN-REVIEW.r3.md` verbatim.
- Verified SHA-256:
  - design: `8F6EB544288CC1A18523184F583494D24F7232C58DD9B73984C8D4C3089225AC`
  - binding review: `C43ADD6BA9899DE1AFD99BB62DA7AC282462E608FB840C7E3065FA33F3DAB8C0`
- The source baselines match the design (`Cura` `5068661cd448b954328483a499fe4ff419b695b5`; `cura-workflows` `126f92d186e62a8c2f50ed1883c37a81e1d929de`).
- Source reality did not invalidate the approved design. No validation-only caller commit was created because exact PR SHAs `C` and `W` do not yet exist.

## Exact changed files

### Cura

- `packaging\windows\validate_pe_architecture.py`
- `packaging\msi\create_windows_msi.py`
- `packaging\NSIS\create_windows_installer.py`
- `tests\Packaging\__init__.py`
- `tests\Packaging\TestValidatePeArchitecture.py`
- `tests\Packaging\TestCreateWindowsMsi.py`
- `tests\Packaging\TestCreateWindowsInstaller.py`

### cura-workflows

- `.github\actions\setup-build-environment\action.yml`
- `.github\workflows\conan-package.yml`
- `.github\workflows\conan-recipe-export.yml`
- `.github\workflows\conan-recipe-version.yml`
- `.github\workflows\cura-installer-windows-arm.yml`
- `.github\workflows\cura-installer-windows.yml`
- `.github\workflows\cura-installers.yml`
- `.github\workflows\make-runners-list.yml`
- `runner_scripts\make_runners_list.py`
- `runner_scripts\windows_arm_artifact_contract.py`
- `runner_scripts\workflow_provenance.py`
- `runner_scripts\tests\test_windows_arm_artifact_contract.py`
- `runner_scripts\tests\test_workflow_provenance.py`

The workboard was not edited. No commit was created.

## Requirement mapping

| Requirement | Implementation |
|---|---|
| Strict dependency-free PE architecture validation | New Cura validator recursively validates all `.exe`, `.dll`, and `.pyd` files, aggregates failures, enforces required paths, and emits deterministic SHA-256 manifests. |
| Fail-closed MSI/NSIS packaging | MSI supports validated `x64`/`arm64`, passes `-arch`, uses `check=True`, and validates all intermediate/final outputs; NSIS uses `check=True` and validates its exact output. |
| Required Cura tests | Added synthetic PE, deterministic manifest, architecture, malformed/mixed/empty/required-file, subprocess failure, and missing/empty output tests. |
| Pinned setup/action/helper provenance | Added `cura_workflows_ref`, local action checkouts, literal-SHA assertions, helper checkout forwarding, workspace-preserving setup, and invocation-level evidence. |
| Complete package proof | Added canonical provenance row generation plus aggregate validation that rejects missing, duplicate, non-PASS, or wrong-SHA rows; records `C`, `V`, `W`, caller/source revisions, runner/Python identity, Conan reference, and invoked-file hashes. |
| Binding `V` correction | Validation mode requires one source revision whose parent diff is exactly both Cura caller workflows before accepting proof; no caller changes were created locally. |
| Native Arm runner selection/gates | Runner list now emits `windows-11-arm`; package/build/smoke gates require Windows, ARM64 runner/environment, and native ARM64 Python before build work. |
| Native CRT and `python3.dll` | Arm build discovers VS via `vswhere`, selects the newest Arm64 CRT, validates/copies/hashes six CRTs, and sources only native `<sys.base_prefix>\python3.dll` with version, PE, and hash checks. |
| Canonical artifact boundary | Added canonical create/verify contract CLI with required metadata and rejection of unsafe/duplicate/missing/extra/mutated files. |
| Split Arm build/sign/package/smoke | Reworked Arm workflow into native build, clean secure X64 signing/packaging, and hosted `windows-11-arm` smoke jobs with strict contracts, PE/signature/MSI checks, hard-failing uploads, and timed engine execution. |
| Arm64 MSI and signing evidence | MSI uses `--architecture arm64`; summary/template/page/component assertions, internal/final signature verification, tool/certificate/provider preflight, and signed/release evidence are recorded. |
| X64 regression safety | X64 explicitly passes `--architecture x64`, emits an X64 PE manifest, validates MSI template, verifies signatures, enforces non-empty outputs, and uses hard-failing uploads. |
| Installer orchestration | All-installers passes distinct Arm build/sign runner labels and forwards the workflow ref. |

## Commands and results

- Hash verification: exit `0`; both hashes matched.
- Raw specified Cura pytest command: exit `4` because pre-existing `tests\conftest.py` imports unavailable `UM`.
- `$env:PYTEST_ADDOPTS='--confcutdir="tests\Packaging"'; python -m pytest tests\Packaging\TestValidatePeArchitecture.py tests\Packaging\TestCreateWindowsMsi.py tests\Packaging\TestCreateWindowsInstaller.py`: exit `0`, `17 passed`.
- `python -m pytest runner_scripts\tests\test_windows_arm_artifact_contract.py runner_scripts\tests\test_workflow_provenance.py`: exit `0`, `12 passed`.
- `python runner_scripts\make_runners_list.py --platform-windows-arm64`: exit `0`; emitted `{"include": [{"runner": "windows-11-arm", "conan_extra_args": ""}]}`.
- PyYAML `safe_load` over every changed workflow/action YAML: exit `0`; all eight files parsed.
- `python -m py_compile` over all changed production Python scripts: exit `0`.
- Forbidden mutable/legacy pattern scan (`python_dll_workaround`, `windows-latest-arm64`, nested setup/upload `@main`): no matches.
- `git diff --check` in `Cura`: exit `0`.
- `git diff --check` in `cura-workflows`: exit `0`.

## Limitations and external gates

- Exact `C`/`W` SHAs, single validation commit `V`, hosted package/installer runs, and immutable run URLs/artifact evidence require committed PR revisions and were intentionally not fabricated.
- Native/self-hosted Arm build, secure X64 production signing, hosted Arm smoke, X64 workflow execution, and physical Windows Arm installer acceptance were not available locally.
- Certificate, token container, eToken provider, Conan credentials, WiX/NSIS secure-runner installations, timestamp service, and publication remain maintainer/vendor-controlled gates.
- YAML was parsed locally, but GitHub-hosted workflow execution is still required to validate runner/tool-specific behavior.
- The unmodified Cura pytest invocation is blocked by the local absence of Uranium (`UM`); the requested packaging tests themselves pass when isolated from the unrelated root fixture import.

## Diff/commit readiness

The two product diffs are locally validated and ready for review, but must not be committed or used for exact-SHA proof until maintainers create `C` and `W`, then create one unchanged `V` containing both caller changes before either run.

confidence: medium

Justification: all locally controllable code, tests, contract checks, YAML parsing, runner output, and diff checks pass, while hosted Arm, secure signing, exact-SHA CI, and physical-hardware gates remain externally unverified.
