# ARM-READY r1

## Integrity and inspected scope

- `CODE-REVIEW.r2.md` SHA-256 verified as `4F54268E12D94AD1A4492A93B73085DA19DEE11EEE55A1A686FAE4FC926EE46F`.
- Repository baselines verified:
  - Cura: `5068661cd448b954328483a499fe4ff419b695b5`
  - cura-workflows: `126f92d186e62a8c2f50ed1883c37a81e1d929de`
- Inspected the complete current implementation: all modified and untracked product/test files listed by `IMPLEMENT.r2.md`, including all 796 lines of the Arm workflow and every changed reusable workflow/action/script/test.
- No product/workflow/workboard file was edited and no subagent was launched.
- Authoritative guide written to `C:\s\Demo\Hack2026\Cura\Generated Files\windows-arm-build-test-guide.md`.

## Validation results

| Validation | Exact command | Exit | Result |
|---|---|---:|---|
| Cura targeted packaging tests | `Set-Location 'C:\s\Demo\Hack2026\Cura'; $env:PYTEST_ADDOPTS='--confcutdir="tests\Packaging"'; python -m pytest tests\Packaging\TestValidatePeArchitecture.py tests\Packaging\TestCreateWindowsMsi.py tests\Packaging\TestCreateWindowsInstaller.py` | 0 | `17 passed in 0.54s` |
| Cura broader packaging suite | `Set-Location 'C:\s\Demo\Hack2026\Cura'; $env:PYTEST_ADDOPTS='--confcutdir="tests\Packaging"'; python -m pytest tests\Packaging` | 0 | `17 passed in 0.36s` |
| Workflow targeted tests | `Set-Location 'C:\s\Demo\Hack2026\Cura-workflows'; python -m pytest runner_scripts\tests\test_windows_arm_artifact_contract.py runner_scripts\tests\test_workflow_provenance.py` | 0 | `20 passed in 3.04s` |
| Workflow broader script suite | `Set-Location 'C:\s\Demo\Hack2026\Cura-workflows'; python -m pytest runner_scripts\tests` | 0 | `20 passed in 2.44s` |
| Changed Python compilation | `python -m py_compile` over the 11 changed/new implementation and test modules in both repositories | 0 | 11 modules compiled |
| Changed YAML parsing | PyYAML `safe_load` over the changed action plus seven workflows | 0 | 8 mappings parsed |
| Arm runner matrix | `python runner_scripts\make_runners_list.py --platform-windows-arm64` | 0 | `windows-11-arm` |
| Every single-platform matrix | Loop over Linux, Windows, macOS, Windows Arm64, and Wasm flags | 0 | Expected runner/profile emitted for all five |
| X64/Arm installer artifact uniqueness | Static extraction/assertion of the four architecture-qualified application/engine upload names | 0 | Four distinct names |
| Forbidden-pattern scan | `Select-String` over proof/Arm paths for AMD64 workaround, obsolete Arm label, nested setup/upload `@main`, and obsolete workflow claims | 0 | Zero matches |
| Cura diff hygiene | `git -C 'C:\s\Demo\Hack2026\Cura' diff --check` | 0 | Clean |
| Workflow diff hygiene | `git -C 'C:\s\Demo\Hack2026\Cura-workflows' diff --check` | 0 | Clean |

Exact supplemental commands:

```powershell
Get-FileHash -Algorithm SHA256 'C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-implementation-reviewer\output\CODE-REVIEW.r2.md'
```

Exit `0`; hash matched.

```powershell
Set-Location 'C:\s\Demo\Hack2026'
python -m py_compile Cura\packaging\windows\validate_pe_architecture.py Cura\packaging\msi\create_windows_msi.py Cura\packaging\NSIS\create_windows_installer.py Cura\tests\Packaging\TestValidatePeArchitecture.py Cura\tests\Packaging\TestCreateWindowsMsi.py Cura\tests\Packaging\TestCreateWindowsInstaller.py Cura-workflows\runner_scripts\make_runners_list.py Cura-workflows\runner_scripts\workflow_provenance.py Cura-workflows\runner_scripts\windows_arm_artifact_contract.py Cura-workflows\runner_scripts\tests\test_workflow_provenance.py Cura-workflows\runner_scripts\tests\test_windows_arm_artifact_contract.py
```

Exit `0`.

```powershell
Set-Location 'C:\s\Demo\Hack2026\Cura-workflows'
@'
from pathlib import Path
import yaml
files = [
Path('.github/actions/setup-build-environment/action.yml'),
Path('.github/workflows/conan-package.yml'),
Path('.github/workflows/conan-recipe-export.yml'),
Path('.github/workflows/conan-recipe-version.yml'),
Path('.github/workflows/cura-installer-windows-arm.yml'),
Path('.github/workflows/cura-installer-windows.yml'),
Path('.github/workflows/cura-installers.yml'),
Path('.github/workflows/make-runners-list.yml'),
]
for path in files:
    assert isinstance(yaml.safe_load(path.read_text(encoding='utf-8')), dict)
print(f'PARSED_COUNT={len(files)}')
'@ | python -
```

Exit `0`; `PARSED_COUNT=8`.

```powershell
Set-Location 'C:\s\Demo\Hack2026\Cura-workflows'
foreach ($flag in @('--platform-linux','--platform-windows','--platform-mac','--platform-windows-arm64','--platform-wasm')) {
    python runner_scripts\make_runners_list.py $flag
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
```

Exit `0`.

```powershell
Set-Location 'C:\s\Demo\Hack2026\Cura-workflows'
@'
import re
from pathlib import Path
text = '\n'.join(p.read_text(encoding='utf-8') for p in [
    Path('.github/workflows/cura-installer-windows.yml'),
    Path('.github/workflows/cura-installer-windows-arm.yml'),
])
names = re.findall(r'^\s+name:\s+(windows-(?:x64|arm64)-(?:UltiMaker-Cura|CuraEngine)\.exe)\s*$', text, re.M)
if len(names) != 4 or len(set(names)) != 4:
    raise SystemExit('artifact names are not unique')
print('UNIQUE_COUNT=4')
'@ | python -
```

Exit `0`; `UNIQUE_COUNT=4`.

```powershell
Set-Location 'C:\s\Demo\Hack2026\Cura-workflows'
$files=@('.github\workflows\conan-package.yml','.github\workflows\conan-recipe-version.yml','.github\workflows\conan-recipe-export.yml','.github\workflows\make-runners-list.yml','.github\workflows\cura-installer-windows-arm.yml','.github\actions\setup-build-environment\action.yml','runner_scripts\workflow_provenance.py')
$patterns=@('python_dll_workaround','windows-latest-arm64','ultimaker/cura-workflows/.github/actions/setup-build-environment@main','ultimaker/cura-workflows/.github/actions/upload-conan-package@main','github.job_workflow_')
$matches=@(Select-String -Path $files -Pattern $patterns -SimpleMatch)
if ($matches.Count) { exit 1 }
```

Exit `0`; zero matches.

Two preliminary pytest invocations from `C:\s\Demo\Hack2026` exited `4` because `tests\Packaging` was resolved outside the Cura repository; changing to the documented repository directory produced the passing results above. This was an invocation correction, not a product failure.

## Stable finding

### HIR-REGRESSION-004 — Linux and Wasm package jobs still collide

- **Severity:** medium
- **Status:** reproduced; open.
- **Command:** `Set-Location 'C:\s\Demo\Hack2026\Cura-workflows'; python runner_scripts\make_runners_list.py --platform-linux --platform-wasm`
- **Exit:** `0`
- **Output:** two entries use `runner: ubuntu-latest`, with Conan arguments `""` and `"-pr:h cura_wasm.jinja"`.
- **Failing uniqueness assertion:**
  ```powershell
  Set-Location 'C:\s\Demo\Hack2026\Cura-workflows'
  $matrix = python runner_scripts\make_runners_list.py --platform-linux --platform-wasm | ConvertFrom-Json
  $names = @($matrix.include | ForEach-Object { "package-provenance-create-12345-1-$($_.runner)" })
  $duplicates = @($names | Group-Object | Where-Object Count -gt 1)
  if ($duplicates.Count -gt 0) {
      Write-Error "duplicate immutable artifact name: $($duplicates[0].Name) ($($duplicates[0].Count)x)"
      exit 1
  }
  ```
- **Exit:** `1`
- **Failure:** `duplicate immutable artifact name: package-provenance-create-12345-1-ubuntu-latest (2x)`.
- **Impact:** the second `actions/upload-artifact@v7` upload is deterministically rejected because artifact names are immutable within a run.
- **Correction:** add a stable unique platform/matrix identifier to both the upload name and matching download pattern, then add a Linux+Wasm regression test.

No other locally reproducible implementation failure was found.

## Architecture closure

| Contract | Assessment |
|---|---|
| PE | **Code-level closed.** Dependency-free parsing, all-candidate aggregation, required-file enforcement, deterministic manifests, and ARM64/X64/malformed tests pass. No real Arm payload was available locally. |
| CRT | **Statically closed; execution gated.** Workflow requires `vswhere`, one selected Arm64 CRT directory, all six named non-empty DLLs, `0xAA64`, and source/destination hash equality. Local AMD64 host could not execute this path. |
| Python | **Statically closed; execution gated.** Native Arm Python and `<sys.base_prefix>\python3.dll` are mandatory, version/machine/hash checked, and the AMD64 workaround is absent from Arm/proof paths. Native Arm Python was not available locally. |
| MSI | **Locally closed for generator behavior; runtime gated.** `-arch arm64|x64`, checked subprocesses, and non-empty outputs are tested. Actual WiX Arm64 authoring, SummaryInformation, and Component-table checks require the secure runner and produced MSI. |
| Signature | **Statically closed; externally gated.** Tool/certificate/provider/token preflight, internal/final signing, immediate verification, signed contract, and installer hash/size binding are present. No certificate, token, timestamp, or signed files were used locally. |

## Tested / not tested

| Area | Status | Evidence/limit |
|---|---|---|
| Packaging Python behavior | Tested | 17 passing targeted/broader tests |
| Provenance and artifact contracts | Tested | 20 passing targeted/broader tests |
| Python syntax | Tested | 11 modules compiled |
| YAML syntax | Tested | 8 changed YAML mappings parsed; no `actionlint` executable was installed |
| Runner matrix generation | Tested | All single platforms pass; Linux+Wasm collision reproduced |
| Application/engine artifact-name uniqueness | Tested | Four architecture-qualified names are distinct |
| Real native Arm build | Not tested | Local machine/Python report AMD64 |
| Native Arm CRT and `python3.dll` | Not tested | Requires native Arm runner/toolchain |
| Conan/package workflow execution | Not tested | Requires pushed exact `C/V/W`, credentials, and CI |
| X64 installer workflow execution | Not tested | Requires secure self-hosted runner |
| NSIS/WiX installer creation | Not tested | No produced payload and required runner tools |
| Production Authenticode/timestamping | Not tested | No certificate, provider token, or signing run |
| Hosted `windows-11-arm` smoke | Not tested | No hosted workflow run |
| Clean install/upgrade/uninstall | Not tested | No signed installers or disposable physical Arm environment |
| GUI, slicing, and G-code export | Not tested | Requires physical Windows Arm acceptance |
| Physical hardware, performance, power | Not tested | No evidence generated or claimed |

## External gates

1. Correct `HIR-REGRESSION-004`.
2. Produce immutable commits `C` and `W`, then one direct-child validation commit `V` containing both caller changes.
3. Run and retain exact-SHA Arm package proof and installer proof with complete provenance/contracts.
4. Run X64 regression.
5. Complete secure production signing and hosted Arm smoke.
6. Complete clean install, older-to-newer lifecycle, launch, representative STL slice, G-code export, restart, and uninstall for both signed formats on physical Windows Arm.
7. Obtain explicit maintainer stable-publication approval.

## Verdict

**REVISE**

**confidence: high**

**Justification:** Complete local inspection and all controllable validations passed, but the deterministic Linux+Wasm immutable-artifact collision remains an open supported-matrix regression.
