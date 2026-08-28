# IMPLEMENT r2 worker report

## Integrity

- Read `CODE-REVIEW.r1.md` verbatim.
- Verified SHA-256: `7E6090957FC9684CC04A2853877504712D803FEB83760F48BA1C4C70FBA3BC35`.
- Repository HEADs remain unchanged: Cura `5068661cd448b954328483a499fe4ff419b695b5`; cura-workflows `126f92d186e62a8c2f50ed1883c37a81e1d929de`.
- No subagent was launched, no workboard/caller-validation commit was created, and no commit was made.

## Accepted-finding fix map

### `HIR-PROV-001` — fixed

- Package and nested workflow rows now use and validate `job.workflow_ref` plus `job.workflow_sha`, rather than assigning an unrelated action-checkout SHA.
- The validator now enforces the exact expected `component_path` for every required instance and rejects mutable/nonmatching workflow invocation refs.
- Exact-SHA proof validates that `V` is checked out, has exactly one parent `C`, and `C..V` changes exactly `.github/workflows/conan-package.yml` and `.github/workflows/windows-arm.yml`.
- Both validation callers must target literal `@W` and pass the required literal `W`/platform inputs.
- Package evidence now binds `C/V/W`, the produced Conan reference, package run ID, and run attempt into a validated artifact.
- Installer proof downloads that exact package-run artifact, revalidates the same callers, and rejects any package reference, run identity, or `C/V/W` mismatch. Non-proof mutable-ref runs emit `validation_proof=NOT_REQUESTED` and cannot claim `C/V/W`.
- Reproducing tests reject arbitrary component paths, mutable caller targets, mismatched invocation refs, non-single caller chains, and package-chain mismatches.

### `HIR-WORKFLOW-002` — fixed

- X64 application/engine artifacts are `windows-x64-UltiMaker-Cura.exe` and `windows-x64-CuraEngine.exe`.
- Arm64 equivalents are `windows-arm64-UltiMaker-Cura.exe` and `windows-arm64-CuraEngine.exe`; Arm evidence records those names.
- A regression test and literal upload-name intersection check prove the combined workflows have no duplicate literal artifact names.

### `HIR-BOUNDARY-003` — fixed

- Final signed EXE/MSI files are copied into `signed\installers` and included in `signed-contract.json`.
- `release-evidence.json` records contract-relative installer names, nonzero sizes, and SHA-256 values.
- Hosted Arm smoke verifies separately downloaded installer filenames, sizes, and SHA-256 values against that signed-contract-bound evidence before signature/MSI checks.
- Reproducing tests pass for exact files and reject a substituted installer.

## r2-touched files

- `cura-workflows\.github\workflows\conan-package.yml`
- `cura-workflows\.github\workflows\conan-recipe-export.yml`
- `cura-workflows\.github\workflows\conan-recipe-version.yml`
- `cura-workflows\.github\workflows\make-runners-list.yml`
- `cura-workflows\.github\workflows\cura-installer-windows.yml`
- `cura-workflows\.github\workflows\cura-installer-windows-arm.yml`
- `cura-workflows\runner_scripts\workflow_provenance.py`
- `cura-workflows\runner_scripts\windows_arm_artifact_contract.py`
- `cura-workflows\runner_scripts\tests\test_workflow_provenance.py`
- `cura-workflows\runner_scripts\tests\test_windows_arm_artifact_contract.py`

## Complete current implementation file list

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

No Cura caller file was left modified because the approved design requires the literal-`W` caller changes to exist only together in future validation commit `V`.

## Validation evidence

- Review hash verification: exit `0`; exact hash above.
- Cura packaging tests with `PYTEST_ADDOPTS=--confcutdir="tests\Packaging"`: exit `0`; `17 passed in 0.49s`.
- `python -m pytest runner_scripts\tests\test_windows_arm_artifact_contract.py runner_scripts\tests\test_workflow_provenance.py`: exit `0`; `20 passed in 2.72s`.
- PyYAML `safe_load` over all eight changed workflow/action YAML files: exit `0`; `parsed 8 YAML files`.
- `python runner_scripts\make_runners_list.py --platform-windows-arm64`: exit `0`; `{"include": [{"runner": "windows-11-arm", "conan_extra_args": ""}]}`.
- `python -m py_compile` for `workflow_provenance.py`, `windows_arm_artifact_contract.py`, and `make_runners_list.py`: exit `0`.
- Forbidden-pattern scan over proof/Arm paths (`python_dll_workaround`, `windows-latest-arm64`, nested setup/upload `@main`, obsolete `github.job_workflow_*`): exit `0`; no matches.
- X64/Arm64 literal upload-artifact name intersection: exit `0`; names are unique.
- `git diff --check` in Cura and cura-workflows: both exit `0`.

## Remaining external gates

- Exact committed `C`, `V`, and `W`, package/installer run URLs, and immutable hosted artifacts require maintainers to create one unchanged `V` containing both approved caller changes.
- Native/self-hosted Arm build, secure X64 production signing, hosted `windows-11-arm` smoke, X64 workflow execution, and physical Windows Arm acceptance remain unexecuted external gates.
- Certificate/token/provider, Conan credentials, WiX/NSIS secure-runner installations, timestamping, publication, and stable-channel release remain maintainer/vendor controlled.

confidence: high

Justification: All three deterministic root causes now have fail-closed implementations and reproducing tests with every required local validation passing, while only explicitly external CI, signing, and hardware gates remain.
