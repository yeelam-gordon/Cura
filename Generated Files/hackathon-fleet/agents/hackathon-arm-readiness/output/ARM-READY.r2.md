# ARM-READY r2

## Integrity and scope

- `ARM-READY.r1.md` SHA-256 verified: `726BAD62C81D658A1774305D774EE56ADF32B1D3FD5E63C549B51CDB9E430F03`.
- `ARM-FIX.r1.md` SHA-256 verified: `ED8060F0357F59A30CF9A6716CCC74987E14DB4342823923B37A65C83B324ABE`.
- Repository baselines remain Cura `5068661cd448b954328483a499fe4ff419b695b5` and cura-workflows `126f92d186e62a8c2f50ed1883c37a81e1d929de`.
- Inspected the complete 3,856-line current implementation: all 7 Cura and 13 cura-workflows product, workflow, helper, and test files listed by `IMPLEMENT.r2.md`, including all 796 lines of `cura-installer-windows-arm.yml`.
- Inspected the actual matrix fix and its regression tests. Current fix-file SHA-256 values:
  - `make_runners_list.py`: `D951A4EB6B30D0E0A4BE3914E3A8F9FA4E556148736674C794D2EB796409A981`
  - `conan-package.yml`: `0DF5F8530C0BBC9BD4C0D8044D71A7F8FDF859AA51BC62DE886F8A7DD50433FB`
  - `test_workflow_provenance.py`: `235CF217A1047AAFC66BA217A07B55B11F759B4B2044E7D47E3FDEF1D84B298B`
- Updated only this record and `Generated Files\windows-arm-build-test-guide.md`; no product/workflow/workboard file was edited and no subagent was launched.

## Actual fix and `HIR-REGRESSION-004`

- `make_runners_list.py` emits stable platform identities: `linux`, `windows`, `macos`, `windows-arm64`, and `wasm`.
- `conan-package.yml` binds immutable package-create provenance upload names to `${{ matrix.platform }}` while retaining the run/attempt-scoped wildcard download.
- The regression suite explicitly checks Linux+Wasm and all-five-platform uniqueness and rejects use of `${{ matrix.runner }}` for this upload.
- Reproduction now yields two unique Linux+Wasm names and five unique all-platform names.

**`HIR-REGRESSION-004`: CLOSED locally.**

## Exact local validation evidence

| Validation | Exact command | Exit | Exact result |
|---|---|---:|---|
| Cura targeted packaging | `python -m pytest tests\Packaging\TestValidatePeArchitecture.py tests\Packaging\TestCreateWindowsMsi.py tests\Packaging\TestCreateWindowsInstaller.py` from Cura with `PYTEST_ADDOPTS=--confcutdir="tests\Packaging"` | 0 | `17 passed in 0.39s` |
| Cura complete packaging | `python -m pytest tests\Packaging` with the same setting | 0 | `17 passed in 0.27s` |
| Workflow targeted | `python -m pytest runner_scripts\tests\test_windows_arm_artifact_contract.py runner_scripts\tests\test_workflow_provenance.py` | 0 | `22 passed in 2.88s` |
| Workflow complete | `python -m pytest runner_scripts\tests` | 0 | `22 passed in 2.93s` |
| Changed Python syntax | `python -m py_compile` over the 11 implementation/test modules used in r1 | 0 | `COMPILED_COUNT=11` |
| Changed YAML syntax | PyYAML `safe_load` over the changed action and seven workflows | 0 | `PARSED_COUNT=8` |
| Every single-platform matrix | Loop over `--platform-linux`, `--platform-windows`, `--platform-mac`, `--platform-windows-arm64`, `--platform-wasm` with exact platform/runner/argument assertions | 0 | `SINGLE_PLATFORM_COUNT=5`; expected values all matched |
| Linux+Wasm uniqueness | Generate both entries and render `package-provenance-create-12345-1-$($_.platform)` | 0 | `LINUX_WASM_UNIQUE_COUNT=2`; names end in `linux`,`wasm` |
| All-platform uniqueness | Generate all five entries and render the same immutable names | 0 | `ALL_PLATFORM_UNIQUE_COUNT=5`; suffixes `linux`,`windows`,`macos`,`windows-arm64`,`wasm` |
| X64/Arm application-engine artifacts | Extract/assert architecture-qualified upload names from both installer workflows | 0 | `INSTALLER_ARTIFACT_UNIQUE_COUNT=4` |
| Forbidden patterns | `Select-String` over proof/Arm paths for AMD64 workaround, obsolete Arm label, nested setup/upload `@main`, and obsolete workflow claims | 0 | `FORBIDDEN_MATCHES=0` |
| Cura hygiene | `git -C 'C:\s\Demo\Hack2026\Cura' diff --check` | 0 | `CURA_DIFF_CHECK=CLEAN` |
| Workflow hygiene | `git -C 'C:\s\Demo\Hack2026\Cura-workflows' diff --check` | 0 | `WORKFLOW_DIFF_CHECK=CLEAN` |

Exact uniqueness results:

```text
LINUX_WASM_NAMES=package-provenance-create-12345-1-linux,package-provenance-create-12345-1-wasm
ALL_PLATFORM_NAMES=package-provenance-create-12345-1-linux,package-provenance-create-12345-1-windows,package-provenance-create-12345-1-macos,package-provenance-create-12345-1-windows-arm64,package-provenance-create-12345-1-wasm
INSTALLER_ARTIFACT_NAMES=windows-x64-UltiMaker-Cura.exe,windows-x64-CuraEngine.exe,windows-arm64-UltiMaker-Cura.exe,windows-arm64-CuraEngine.exe
```

Local host evidence: Python `3.12.10`, `platform.machine()=AMD64`, `PROCESSOR_ARCHITECTURE=AMD64`; `actionlint` was not installed.

## Architecture closure

| Contract | Closure |
|---|---|
| Matrix/provenance uniqueness | **Locally closed.** Stable platform identity separates Linux and Wasm despite their shared runner; all supported entries and immutable names are unique. |
| Exact-SHA provenance | **Code/test closed; CI gated.** Invocation ref/SHA, component paths, 16 instances, single-parent C/V/W callers, and package-chain identity are fail-closed and tested. |
| PE | **Code/test closed; payload gated.** Dependency-free parsing, all-file aggregation, required files, deterministic manifests, ARM64/X64/malformed cases pass; no real Arm payload was available. |
| CRT | **Statically closed; execution gated.** One discovered Arm64 CRT directory, six non-empty DLLs, PE machine checks, and copy hashes are required. |
| Python | **Statically closed; execution gated.** Native Arm Python and matching `<sys.base_prefix>\python3.dll` are mandatory; the AMD64 workaround is absent from Arm/proof paths. |
| MSI/NSIS | **Generator behavior locally closed; real tools gated.** Architecture selection, checked subprocesses, and non-empty outputs pass; real Arm64 WiX/NSIS outputs were not produced locally. |
| Artifact boundary | **Code/test closed; hosted transfer gated.** Unsigned/signed contracts and installer release evidence bind exact file sets, sizes, and SHA-256 values. |
| Signing | **Statically closed; externally gated.** Tool/certificate/provider/token preflight and immediate internal/final verification exist; no production signing was executed. |

## Tested / not tested / external gates

### Tested locally

- All r1 unit, broader suite, Python compilation, YAML parsing, matrix, application/engine artifact uniqueness, forbidden-pattern, and diff-hygiene checks.
- Linux+Wasm and all-five-platform immutable provenance uniqueness.
- Complete implementation and guide consistency.

### Not tested; must remain gated

- Exact committed/pushed `C`, direct-child `V`, and `W`; GitHub Actions package/installer runs and retained hosted artifacts.
- Native self-hosted Windows Arm64 package/payload build and secure self-hosted X64 packaging.
- Real Arm64 CRT, native `python3.dll`, Conan credentials, WiX/NSIS execution, MSI database output, and X64 workflow regression.
- Production certificate/provider/token use, Authenticode, timestamping, and signed-file verification.
- Hosted `windows-11-arm` smoke.
- Physical Arm EXE/MSI clean install, upgrade/coexistence, launch, slicing, G-code export, restart, and uninstall.
- Physical-device compatibility, performance, power, publication, and maintainer approval.

No external CI, signing, hosted-runner, or physical-hardware success is claimed.

## Verdict

**LOCAL PASS — READY FOR EXTERNAL VALIDATION; STABLE PUBLICATION REMAINS GATED.**

**Confidence: high.**

**Justification:** Every locally reproducible validation passes and stable platform-qualified provenance names close the Linux+Wasm collision, while all unexecuted CI, signing, and hardware requirements remain explicit external gates.
