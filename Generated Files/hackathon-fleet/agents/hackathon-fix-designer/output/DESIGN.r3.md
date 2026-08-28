# Windows Arm64 installer fix design — r3

## Decision

Implement two coordinated, upstreamable PRs. The Cura PR makes Windows packaging architecture-aware, fail-fast, and independently verifiable. The `cura-workflows` PR builds only on a proven native Arm64 host, sources `python3.dll` from that host's native CPython installation, transfers a hash-locked payload/metadata contract to the existing secure X64 signing runner, signs internal binaries before packaging, authors and validates an Arm64 MSI, and smoke-tests the signed result on `windows-11-arm`. Production signing, physical Windows Arm acceptance, and stable publication remain mandatory external gates.

## Immutable inputs and source baseline

The r3 assignment inputs were read verbatim and their SHA-256 values verified:

| Record | SHA-256 |
|---|---|
| `hackathon-fix-designer\output\DESIGN.r2.md` | `ADD584856B897BAB3220F44250C3ECCA29F16EA902D5B946CD39E8DEC8344652` |
| `hackathon-design-risk-reviewer\output\DESIGN-REVIEW.r2.md` | `88F44626AD605653607AF13A02AE28421DCC61C7EA6DEE294D13D825F758C43D` |

The accepted r2 input lineage remains part of this design:

| Record | SHA-256 |
|---|---|
| `hackathon-fix-designer\output\DESIGN.r1.md` | `A3E7FAAEF6AB8F58A5FD52668C8E9CECCB6ACC01E26968EAA59806D5FE9A20A8` |
| `hackathon-design-risk-reviewer\output\DESIGN-REVIEW.r1.md` | `81299A1C2AAE618C28A427CD706A0FFA7C4EF1EAF49081765698E671097A473F` |
| `hackathon-design-risk-reviewer\output\RISK.r1.md` | `F17BE2EB662C80E089B529F002AEE70C77A6F5CE3F161002F4593CD89E4BA5EB` |

Current product baselines remain:

```text
Cura              5068661cd448b954328483a499fe4ff419b695b5
cura-workflows    126f92d186e62a8c2f50ed1883c37a81e1d929de
```

The only Cura working-tree addition is the generated fleet-record directory; tracked product source is unchanged.

## Reviewer-finding dispositions

| Finding | Disposition | Design closure |
|---|---|---|
| `DR-ARCH-001` | **Accepted; closed in design.** | The Arm workflow must copy only `<sys.base_prefix>\python3.dll` from the native Arm64 Python selected by the setup action, verify source and destination as `0xAA64`, compare their SHA-256 values, and never copy or allowlist the committed AMD64 workaround DLL. |
| `DR-PROVENANCE-002` | **Accepted; closed in design.** | One literal workflow PR SHA is passed through the validation callers, package workflow, recipe-version workflow, both recipe-export invocations, runner-list workflow, package-create job, installer workflow, every locally checked-out setup/upload/override action, every setup helper checkout, and the runner-list script checkout; the package caller explicitly sets `platform_windows_arm64: true`. |
| `DR-PROVENANCE-006` | **Accepted; closed in design.** | `cura_workflows_ref` is threaded through both nested recipe workflows; each nested job checks out action definitions at that ref, invokes setup/upload locally, pins setup's helper checkout to the same ref, asserts literal-SHA equality, and records every workflow/action/helper invocation separately in proof evidence. |
| `DR-BOUNDARY-003` | **Accepted; closed in design.** | A canonical, hash-locked build contract carries filename/version/app metadata and every transferred file hash; the clean X64 job verifies it, creates a fresh venv, installs packaged installer requirements, and preflights every tool, certificate, provider, and runtime before signing or packaging. |
| `DR-VALIDATION-004` | **Accepted; closed in design.** | Packaging scripts use `check=True` and assert non-empty outputs; every required upload uses `if-no-files-found: error`, success artifacts do not use `always()`, and missing/empty files fail before upload. |
| `DR-ARCH-005` | **Accepted; closed in design.** | The first build-job step asserts Windows, `runner.arch == ARM64`, `PROCESSOR_ARCHITECTURE == ARM64`, and native Python `platform.machine() == ARM64`, and records the values before Conan or PyInstaller executes. |

No critical or high review finding remains open in this design.

### Explicit disposition of `DR-PROVENANCE-006`

**Accepted; closed in design.** The r2 package proof was not immutable because `conan-recipe-version.yml` and both invocations of `conan-recipe-export.yml` still loaded setup/upload actions from mutable `main`. r3 requires the exact ref `W` at every nested boundary, local action execution from a checkout whose HEAD is asserted as `W`, the same `W` for each setup helper checkout, and invocation-by-invocation evidence; no package-proof step may reference `ultimaker/cura-workflows/...@main`.

## Architecture and trust boundaries

```text
Cura PR exact SHA C plus validation-only caller SHA V
  packaging scripts + validators + tests
          |
          v
Arm Conan package produced from V, whose product tree equals C,
using cura-workflows exact SHA W
          |
          v
build-arm-payload (self-hosted-Windows-ARM64)
  early host/Python gate
  -> Conan/PyInstaller
  -> Arm64 CRT discovery
  -> native CPython python3.dll copy
  -> blacklist cleanup
  -> strict all-PE validation
  -> canonical unsigned artifact contract
          |
          v
sign-and-package (self-hosted-Windows-X64)
  clean workspace + contract verification
  -> fresh packaging venv + tool/provider preflight
  -> sign and verify CuraEngine.exe/UltiMaker-Cura.exe
  -> build NSIS EXE and Arm64 MSI
  -> validate MSI database
  -> sign and verify final installers
  -> canonical signed contract and hard-failing uploads
          |
          v
smoke-test-on-hosted-arm (windows-11-arm)
  native host/Python gate
  -> signed-contract verification
  -> repeat PE/signature/MSI checks
  -> timed `CuraEngine.exe help` smoke
          |
          v
nightly artifacts only
  -> physical Arm acceptance gate
  -> separate maintainer stable-publication decision
```

The secure X64 job may sign Arm64 PE files cross-architecture; it must not execute them. The hosted Arm job executes the signed engine. No unsigned intermediate artifact is a publishable release artifact.

## PR 1 — exact Cura changes

### `packaging\windows\validate_pe_architecture.py` — new

Provide a dependency-free CLI:

```text
python validate_pe_architecture.py PATH --architecture arm64|x64
    [--require RELATIVE_PATH ...] [--manifest-out FILE]
```

Required behavior:

1. Accept a file or recursively enumerate a directory's `.exe`, `.dll`, and `.pyd` files in case-insensitive, relative-path sort order.
2. Parse `MZ`, `e_lfanew`, `PE\0\0`, and COFF Machine directly. Accept only `0xAA64` for `arm64` and `0x8664` for `x64`.
3. Treat malformed/truncated candidates, zero candidates, missing required paths, and every machine mismatch as failures; print all failures before returning nonzero.
4. Do not support an architecture allowlist for the Arm application payload.
5. When `--manifest-out` is supplied, write deterministic JSON containing schema version, requested architecture, expected machine code, and for every PE: relative path, byte length, SHA-256, and machine code.
6. The Arm workflow supplies these required paths:

```text
python3.dll
concrt140.dll
msvcp140.dll
msvcp140_1.dll
msvcp140_2.dll
vcruntime140.dll
vcruntime140_1.dll
UltiMaker-Cura.exe
CuraEngine.exe
```

### `packaging\msi\create_windows_msi.py`

- Change `build(dist_path, filename)` to `build(dist_path, filename, architecture)`.
- Add `--architecture` with choices `x64` and `arm64`, defaulting to `x64` only for staggered landing compatibility.
- Pass the validated value to `candle -arch`.
- Replace the three `subprocess.call` invocations with `subprocess.run(..., check=True)`.
- After `heat`, require non-empty `HeatFile.wxs`; after `candle`, require both expected non-empty `.wixobj` files; after `light`, require the requested MSI to exist and be non-empty.

### `packaging\NSIS\create_windows_installer.py`

- Invoke `makensis` with `subprocess.run(command, check=True)`.
- Require the requested EXE path to exist and have nonzero length after `makensis` returns.

### Tests

Add:

- `tests\Packaging\__init__.py`
- `tests\Packaging\TestValidatePeArchitecture.py`
- `tests\Packaging\TestCreateWindowsMsi.py`
- `tests\Packaging\TestCreateWindowsInstaller.py`

Tests must cover ARM64/X64/malformed synthetic PEs, recursive ordering, mixed-machine aggregation, zero candidates, required-file failures including `python3.dll`, deterministic manifest hashes, both MSI architecture values, invalid architecture rejection, `check=True`, nonzero tool failure, and zero-success-with-missing/empty-output failure.

## PR 2 — exact `cura-workflows` changes

### Provenance plumbing

#### `.github\actions\setup-build-environment\action.yml`

- Add boolean input `cleanup_workspace`, default `true`; guard the current cleanup step with it.
- Keep `cura_workflows_branch`, and use it for the existing `Cura-workflows` checkout.
- Rename the Arm setup step to `Setup Python (Windows ARM64)` and remove the nonexistent `windows_arm_setup.ps1` instruction.
- Emit `python-path`, `python-base-prefix`, `python-version`, and `python-machine`; fail unless the Arm path reports `ARM64`.
- After checkout, print `git -C Cura-workflows rev-parse HEAD`; if `cura_workflows_branch` is a 40-hex SHA, require equality.

#### `.github\workflows\cura-installer-windows-arm.yml`

Add input `cura_workflows_ref`, default `main`, and input `signing_operating_system`, default `self-hosted-Windows-X64`.

Every job starts by cleaning only `${{ github.workspace }}`, then checks out `Ultimaker/cura-workflows` at `${{ inputs.cura_workflows_ref }}` into `_cura_workflows_action`. Invoke both composite actions by local path:

```yaml
uses: ./_cura_workflows_action/.github/actions/setup-build-environment
```

and:

```yaml
uses: ./_cura_workflows_action/.github/actions/set-package-overrides
```

Pass `cleanup_workspace: false` and `cura_workflows_branch: ${{ inputs.cura_workflows_ref }}` to setup. This makes the action definitions and the `Cura-workflows` helper checkout resolve to the same supplied SHA without a self-referential SHA literal inside commit `W`.

#### `.github\workflows\conan-package.yml`

- Add input `cura_workflows_ref`, default `main`.
- Add boolean input `allow_non_default_branch_package_create`, default `false`; permit `make-runners-list` and `conan-package-create` on a non-default push only when this input is true, so the exact-SHA validation caller can build without weakening normal branch behavior.
- Pass `cura_workflows_ref` to `conan-recipe-version.yml`, both `conan-recipe-export.yml` invocations, and `make-runners-list.yml`; no nested call may omit it.
- In `conan-package-create`, clean the workspace, check out `Ultimaker/cura-workflows` into `_cura_workflows_action` at that ref, invoke `./_cura_workflows_action/.github/actions/setup-build-environment`, pass `cleanup_workspace: false`, and pass the same ref as `cura_workflows_branch`.
- In every job that resolves `cura_workflows_ref`, print the requested ref and resolved checkout SHA; when the input matches `^[0-9a-fA-F]{40}$`, compare case-insensitively and fail on inequality before Conan or upload work.

#### `.github\workflows\conan-recipe-version.yml`

- Add string input `cura_workflows_ref`, default `main`.
- In `make-versions`, clean only `${{ github.workspace }}`, check out `Ultimaker/cura-workflows` at `${{ inputs.cura_workflows_ref }}` into `_cura_workflows_action`, and capture `git -C _cura_workflows_action rev-parse HEAD`.
- Replace `ultimaker/cura-workflows/.github/actions/setup-build-environment@main` with `./_cura_workflows_action/.github/actions/setup-build-environment`; pass `cleanup_workspace: false` and `cura_workflows_branch: ${{ inputs.cura_workflows_ref }}` in addition to the existing repository/branch inputs.
- After setup, capture `git -C Cura-workflows rev-parse HEAD`; if the requested ref is a 40-hex SHA, require both the action checkout and helper checkout to equal it before `conan inspect` or broadcast-data generation.
- Record separate proof rows for the `conan-recipe-version` workflow invocation, its setup-action invocation, and its setup helper checkout.

#### `.github\workflows\conan-recipe-export.yml`

- Add string input `cura_workflows_ref`, default `main`; both `conan-recipe-export-specific` and `conan-recipe-export-latest` in `conan-package.yml` must pass it.
- In each `package-export` invocation, clean only `${{ github.workspace }}`, check out `Ultimaker/cura-workflows` at `${{ inputs.cura_workflows_ref }}` into `_cura_workflows_action`, and capture its resolved HEAD.
- Replace setup `@main` with `./_cura_workflows_action/.github/actions/setup-build-environment`; pass `cleanup_workspace: false` and `cura_workflows_branch: ${{ inputs.cura_workflows_ref }}` in addition to all existing inputs.
- Replace upload `@main` with `./_cura_workflows_action/.github/actions/upload-conan-package`; retain the existing package name and private-data inputs.
- After setup and again immediately before local upload, require `_cura_workflows_action` to exist at the originally captured HEAD; capture the `Cura-workflows` helper HEAD; when the requested ref is a 40-hex SHA, require action and helper HEADs to equal it before export or upload.
- Record distinct proof rows for each of the two workflow invocations and, within each, its setup-action, setup helper checkout, and upload-action invocation. The `specific` and `latest` rows may not be collapsed.

#### `.github\workflows\make-runners-list.yml`

Add required/defaulted input `cura_workflows_ref`, use it instead of hardcoded `main` for the `Cura-workflows` checkout, print the requested and resolved checkout SHAs before running the script, and fail on inequality when the input is a literal 40-hex SHA.

#### Package provenance evidence contract

Every package job writes one Markdown table row per executed workflow/action/helper invocation to `$GITHUB_STEP_SUMMARY`, with columns `instance`, `component_path`, `requested_ref`, `resolved_sha`, and `status`. `instance` is stable and job-specific; at minimum the proof contains:

```text
conan-package/workflow
conan-recipe-version/workflow
conan-recipe-version/setup-action
conan-recipe-version/setup-helper-checkout
conan-recipe-export-specific/workflow
conan-recipe-export-specific/setup-action
conan-recipe-export-specific/setup-helper-checkout
conan-recipe-export-specific/upload-action
conan-recipe-export-latest/workflow
conan-recipe-export-latest/setup-action
conan-recipe-export-latest/setup-helper-checkout
conan-recipe-export-latest/upload-action
make-runners-list/workflow
make-runners-list/script-checkout
conan-package-create/setup-action
conan-package-create/setup-helper-checkout
```

For a literal proof SHA, every row above has `requested_ref = W`, `resolved_sha = W`, and `status = PASS`. Workflow rows are tied to the immutable reusable-workflow call graph (`@W` for the entry workflow and local nested workflow paths within that revision); action/helper/script rows use their asserted checkout HEAD. The package run summary also records `C`, `V`, the produced Conan reference, runner label, runner/Python identity, and the SHA-256 of each invoked workflow/action file from the asserted `_cura_workflows_action` checkout. Any missing, duplicate, non-PASS, or non-`W` required row fails the proof.

Add `runner_scripts\tests\test_workflow_provenance.py`, using only the Python standard library, to assert input declarations and propagation, local setup/upload paths, `cleanup_workspace: false`, helper-ref forwarding, literal-SHA assertions, all required evidence instance IDs, and absence of `ultimaker/cura-workflows/.github/actions/*@main` from `conan-package.yml`, `conan-recipe-version.yml`, and `conan-recipe-export.yml`.

#### `runner_scripts\make_runners_list.py`

Replace `windows-latest-arm64` with `windows-11-arm`.

### Canonical artifact contract

Add `runner_scripts\windows_arm_artifact_contract.py` with:

```text
create --root ROOT --metadata METADATA_JSON --output CONTRACT_JSON
       --include payload --include packaging --include metadata\unsigned-pe.json

verify --root ROOT --contract CONTRACT_JSON
```

`create` writes canonical UTF-8 JSON with sorted keys and compact separators. It records schema version `1`, the supplied metadata, and the sorted relative path, size, and SHA-256 of every included file. `verify` rejects an unsupported schema, unsafe/duplicate paths, a missing or extra included file, size/hash mismatch, or malformed required metadata. Add `runner_scripts\tests\test_windows_arm_artifact_contract.py` for round-trip, mutation, deletion, addition, traversal, duplicate, and canonical-output cases.

The unsigned intermediate artifact name is:

```text
windows-arm64-unsigned-${{ github.run_id }}-${{ github.run_attempt }}
```

Its exact layout is:

```text
payload\UltiMaker-Cura\**
packaging\**
metadata\unsigned-pe.json
metadata\build-contract.json
```

`build-contract.json` metadata must contain:

```text
architecture = ARM64
expected_machine = 0xAA64
installer_filename
cura_version_full
cura_app_name
cura_conan_reference
caller_repository
caller_sha
cura_source_sha
cura_implementation_sha
cura_workflows_ref
cura_workflows_sha
workflow_ref
run_id
run_attempt
runner.os
runner.arch
PROCESSOR_ARCHITECTURE
python.executable
python.base_prefix
python.version
python.machine
python3_dll.source_path
python3_dll.size
python3_dll.sha256
python3_dll.machine
vs.installation_path
vs.redist_version
vs.crt_directory
each copied CRT source path, size, SHA-256, and machine
```

The build job exposes only the artifact name, upload-artifact `artifact-id`, `artifact-digest`, and SHA-256 of `build-contract.json` as job outputs. Packaging metadata is read from the verified contract, never from residual workspace state.

### `build-arm-payload`

Run on `${{ inputs.operating_system }}`. Its first functional step, before setup, Conan, or PyInstaller, must require:

```text
runner.os == Windows
runner.arch == ARM64
$env:PROCESSOR_ARCHITECTURE == ARM64
platform.machine() == ARM64
```

After setup, assert that `_cura_workflows_action`, `Cura-workflows`, and the requested literal `cura_workflows_ref` all resolve to the same SHA.

Retain the current Conan install and PyInstaller flow, then:

1. Resolve Visual Studio with:
   ```powershell
   $vswhere = (Get-Command vswhere.exe -ErrorAction Stop).Source
   $vs = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Redist.14.Latest -property installationPath
   ```
2. Require exactly one returned installation path. Under `VC\Redist\MSVC`, select the highest semantic/version-sortable non-`v*` directory, then require exactly one `arm64\Microsoft.VC*.CRT` directory.
3. Copy the six named CRT files, requiring each source to exist and be non-empty. Validate each source as Arm64 before copying and require source/destination SHA-256 equality.
4. Resolve the native Python source with:
   ```powershell
   $pythonExe = (Get-Command python.exe -ErrorAction Stop).Source
   $pythonBase = & $pythonExe -c "import sys; print(sys.base_prefix)"
   $python3Dll = Join-Path $pythonBase "python3.dll"
   ```
5. Require `$python3Dll` to exist and be non-empty; require `platform.machine()` to equal `ARM64`; require the DLL's file version major/minor to match the interpreter major/minor; validate the source DLL as `0xAA64`; copy it to `dist\UltiMaker-Cura\python3.dll`; require source/destination SHA-256 equality; record source path/version/hash.
6. Never read `python_dll_workaround\python3.dll` in the Arm workflow. If the native runtime lacks a valid `python3.dll`, fail the job with no fallback.
7. Run blacklist cleanup, then run the full payload validator with all nine required paths and emit `metadata\unsigned-pe.json`.
8. Stage only the exact artifact layout above, create `build-contract.json`, verify it immediately, assert it and every staged file are non-empty, then upload with retention one day and `if-no-files-found: error`.
9. Restore Conan cache cleanup under `if: ${{ always() && startsWith(inputs.operating_system, 'self-hosted') }}`; cleanup is not a success artifact.

### `sign-and-package`

Run on `${{ inputs.signing_operating_system }}` with `needs: build-arm-payload`.

1. Clean the workspace, check out workflow tools at the supplied ref, download the unsigned artifact by exact name, compare `build-contract.json` to the job-output SHA-256, run contract `verify`, and rerun strict Arm64 PE validation before signing.
2. Parse `installer_filename`, `cura_version_full`, and `cura_app_name` from the verified contract and expose them as step/job outputs. Reject empty values, path separators, an architecture other than `ARM64`, or a filename not ending `-win64-ARM64`.
3. Create a fresh venv under the current workspace and install only `packaging\pip_requirements_installer_basic.txt`; require `python -c "import jinja2, semver"` to succeed.
4. Preflight and print absolute paths/file versions for `python.exe`, `makensis.exe`, `signtool.exe`, `heat.exe`, `candle.exe`, and `light.exe`. Require `C:\actions-runner\code_sign.cer` to exist and be non-empty, require `certutil -csplist` to contain `eToken Base Cryptographic Provider`, require `WIN_TOKEN_CONTAINER` to be non-empty, and instantiate `WindowsInstaller.Installer`.
5. Sign `payload\UltiMaker-Cura\CuraEngine.exe` and `UltiMaker-Cura.exe` with the existing production contract:
   ```text
   /fd sha256
   /tr http://timestamp.sectigo.com
   /td sha256
   /f C:\actions-runner\code_sign.cer
   /csp "eToken Base Cryptographic Provider"
   /kc ${{ secrets.WIN_TOKEN_CONTAINER }}
   ```
   Each command has a two-minute timeout and is followed immediately by `signtool verify /pa /all /v`.
6. Rerun Arm64 PE validation after signing.
7. Build the EXE from the signed payload. Build the MSI with `--architecture arm64`. Require both exact files to exist and have nonzero length.
8. Validate the MSI with `WindowsInstaller.Installer`:
   - SummaryInformation property 7 begins `Arm64;`.
   - SummaryInformation property 14 is an integer at least `500`.
   - Every `Component` table row has `Attributes & 256 != 0`; any 32-bit component fails the job.
9. Sign the final EXE and MSI with the same production parameters, then run `signtool verify /pa /all /v` on both.
10. Create `metadata\signed-pe.json`, `metadata\signing-evidence.json`, and `metadata\release-evidence.json`. The evidence records tool paths/versions, certificate SHA-256, signature-verification results, MSI properties/component count, and final file sizes/SHA-256 values.
11. Create and immediately verify a canonical `metadata\signed-contract.json` covering the signed payload and evidence.
12. Upload only after all checks pass:

| Artifact | Contents | Retention |
|---|---|---|
| `windows-arm64-signed-payload-${run_id}-${run_attempt}` | signed payload plus all metadata/contracts | 5 days |
| `${installer_filename}-exe` | exact final EXE | 5 days |
| `${installer_filename}-msi` | exact final MSI | 5 days |
| `UltiMaker-Cura.exe` | exact signed application EXE | 5 days |
| `CuraEngine.exe` | exact signed engine EXE | 5 days |

Every upload uses `if-no-files-found: error`; none uses `always()`. A separate `if: failure()` diagnostic artifact may contain logs only and must use a non-public `windows-arm64-diagnostics-*` name.

### `smoke-test-on-hosted-arm`

Run on `windows-11-arm` with `needs: sign-and-package`.

1. First assert Windows, `runner.arch`, `PROCESSOR_ARCHITECTURE`, and native Python all report `ARM64`.
2. Check out workflow tools at the exact supplied ref, download the signed-payload, EXE, and MSI artifacts by exact names, compare the signed-contract SHA to the signing-job output, and verify the contract.
3. Rerun strict all-PE Arm64 validation.
4. Run `signtool verify /pa /all /v` for both internal EXEs and both final installers.
5. Repeat all MSI SummaryInformation and 64-bit Component-table assertions.
6. Execute exactly:
   ```text
   payload\UltiMaker-Cura\CuraEngine.exe help
   ```
   Capture stdout/stderr, enforce a 60-second timeout, require exit code zero, and require the combined output to contain case-insensitive `usage`; timeout termination must target only the captured process ID.
7. Upload no release artifact from this job; its log and summary are acceptance evidence.

### Other workflow files

- `.github\workflows\cura-installer-windows.yml`: pass `--architecture x64` explicitly and adopt the same packaging-output existence assertions and hard-failing required uploads without changing signing semantics.
- `.github\workflows\cura-installers.yml`: pass `operating_system: self-hosted-Windows-ARM64` and `signing_operating_system: self-hosted-Windows-X64`.
- `.github\actions\setup-build-environment\action.yml`: the Arm-native Python logic applies to hosted and self-hosted Arm.

## Exact-SHA pre-merge proof

Let:

```text
C = exact 40-hex commit SHA of the Cura PR
W = exact 40-hex commit SHA of the cura-workflows PR
V = temporary Cura validation-only commit
```

Create `V` on a branch matching Cura's existing `CURA-*` package-workflow trigger. `V` must be based directly on `C`, and `git diff --name-only C..V` must list only the two validation caller workflows below.

In `V`:

1. Change `Cura\.github\workflows\conan-package.yml` to:
   - call `ultimaker/cura-workflows/.github/workflows/conan-package.yml@W`;
   - pass `cura_workflows_ref: W`;
   - pass `allow_non_default_branch_package_create: true`;
   - pass `platform_windows_arm64: true`;
   - pass `platform_linux/windows/mac/wasm: false`.
2. Push `V` and run the package workflow. The checked-out/package source revision is `V`; the proof must record `C`, `V`, and `W`, prove that `C..V` changes only the two caller workflows, and include every required package provenance row from the contract above, `windows-11-arm`, runner/Python Arm64 identity, invoked-file hashes, and the uploaded Conan reference. All sixteen required package rows must resolve to literal `W`; a missing, duplicate, mutable, or mismatched row fails the run.
3. Change `Cura\.github\workflows\windows-arm.yml` to call `ultimaker/cura-workflows/.github/workflows/cura-installer-windows-arm.yml@W`, pass `cura_workflows_ref: W`, and dispatch with the exact Conan reference produced in step 2.
4. Across the package and installer runs, proof evidence must record each invocation separately:

| Invocation evidence | Required resolved revision |
|---|---|
| reusable package workflow | `W` |
| nested recipe-version workflow | `W` |
| recipe-version setup action checkout | `W` |
| recipe-version setup helper checkout | `W` |
| recipe-export-specific workflow | `W` |
| recipe-export-specific setup action checkout | `W` |
| recipe-export-specific setup helper checkout | `W` |
| recipe-export-specific upload action checkout | `W` |
| recipe-export-latest workflow | `W` |
| recipe-export-latest setup action checkout | `W` |
| recipe-export-latest setup helper checkout | `W` |
| recipe-export-latest upload action checkout | `W` |
| make-runners-list workflow and script checkout | `W` |
| package-create setup action and helper checkout | `W` |
| reusable installer workflow | `W` |
| every installer-job setup action checkout and helper checkout | `W` |
| every installer-job set-package-overrides action checkout | `W` |
| Cura product implementation | `C` |
| Cura package checkout and validation callers | `V`, with only the two declared workflow files differing from `C` |

For installer jobs, use the same `instance`, `component_path`, `requested_ref`, `resolved_sha`, and `status` columns and emit one row for every actual local action invocation; generic or deduplicated action rows are insufficient. Each job asserts `_cura_workflows_action` and any `Cura-workflows` helper checkout against literal `W` before consuming scripts, building, signing, packaging, or smoke testing.

5. Attach the package-run URL, installer-run URL, complete job summaries, artifact IDs/digests, unsigned/signed contract hashes, invoked workflow/action file hashes, and the `C`/`V`/`W` map to the PR validation record.
6. Revert all changes in `V` before merge. No fork owner, temporary branch, certificate, runner label, or validation SHA may remain in the upstreamable diff.

This path uses one workflow implementation SHA, `W`, for every changed workflow/action/script and every nested recipe invocation, records the exact package checkout `V` and underlying product implementation `C`, and explicitly exercises the corrected Arm package runner.

## Ordered implementation and validation plan

1. Implement the Cura PR and run:
   ```powershell
   python -m pytest tests\Packaging\TestValidatePeArchitecture.py tests\Packaging\TestCreateWindowsMsi.py tests\Packaging\TestCreateWindowsInstaller.py
   git diff --check
   ```
2. Implement the workflow PR and run:
   ```powershell
   python -m pytest runner_scripts\tests\test_windows_arm_artifact_contract.py runner_scripts\tests\test_workflow_provenance.py
   python runner_scripts\make_runners_list.py --platform-windows-arm64
   git diff --check
   ```
   Required runner JSON:
   ```json
   {"include":[{"runner":"windows-11-arm","conan_extra_args":""}]}
   ```
3. Produce exact SHAs `C` and `W`; apply validation-only commit `V`.
4. Run the exact-SHA Arm Conan package proof and retain its immutable package reference and provenance summary.
5. Dispatch the exact-SHA installer proof.
6. Require CI evidence for:
   - native Arm build host and Python before Conan;
   - native `<sys.base_prefix>\python3.dll`, `0xAA64`, with source/destination matching hashes;
   - Arm CRT source directory and all six DLL hashes/machines;
   - zero non-Arm64 payload PEs;
   - verified internal and final production signatures;
   - non-empty EXE/MSI/application/engine artifacts with hard-failing uploads;
   - MSI `Arm64;`, page count `>=500`, and all components 64-bit;
   - hosted Arm `CuraEngine.exe help` success;
   - exact `C`/`V`/`W` provenance, all required package and installer invocation rows resolving to `W`, invoked-file hashes, and artifact contract digests.
7. Run the X64 installer workflow and require an X64 PE manifest, verified signatures, non-empty outputs, and MSI Template Summary beginning `x64;`.
8. Revert `V`, merge in dependency order, and keep stable Arm publication disabled.
9. On maintainer-owned physical Windows Arm hardware, test both signed installer formats: install, launch Cura, load a representative STL, slice through CuraEngine, export G-code, close/restart, and uninstall. Record device/CPU, Windows edition/build, installer SHA-256, logs, and outcome.
10. Only after step 9 passes may maintainers separately add the validated Arm EXE/MSI names to `Cura\.github\workflows\release-process_release-candidate.yml` and test a draft release.

## Rollback

1. Before release, revert the `cura-workflows` PR first. The Cura architecture option and validators are backward-compatible and may remain.
2. If both PRs must be reverted, revert `cura-workflows` before Cura so no caller passes an unsupported MSI option.
3. If the native Python installation lacks a valid Arm64 `python3.dll`, stop the Arm build; do not restore the committed AMD64 DLL or add an allowlist.
4. If the secure runner lacks WiX Arm64 support, the signing provider/token, or timestamp access, fail with no final uploads; do not publish only NSIS or unsigned artifacts under the normal names.
5. If hosted smoke fails, retain diagnostics only and block publication.
6. If physical acceptance or release approval is absent, leave Arm artifacts out of the stable release workflow.

## Explicit gates and ownership

**Contributor-controlled and required before merge:** source changes, unit tests, exact-SHA package/installer runs, early architecture assertions, native `python3.dll` sourcing, PE/contracts/MSI/output validation, X64 regression, and hosted Arm engine smoke.

**Ultimaker-maintainer controlled:** private Conan credentials, secure-runner access, `WIN_TOKEN_CONTAINER`, certificate file, eToken provider/token operation, production Authenticode signing, physical Windows Arm testing, and stable release publication.

**Vendor-controlled:** GitHub Arm image availability/migration, Visual Studio redistributable layout, WiX behavior on the secure runner, and Sectigo timestamp availability.

Stable promotion is **NO-GO** until production signing succeeds, both signed installers pass physical Windows Arm acceptance, and maintainers explicitly approve and test release-draft publication.

confidence: high

Justification: r3 preserves every accepted r2 architecture, validation, signing, hardware, and release gate while closing `DR-PROVENANCE-006` with literal-SHA propagation, local pinned actions, asserted helper checkouts, and complete invocation-level proof.
