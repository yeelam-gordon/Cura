# Windows Arm64 build, proof, and acceptance guide

## Status and scope

This runbook matches the current Cura and `cura-workflows` implementation. Local unit, Python, YAML, matrix, artifact-name, and diff checks are executable on Windows X64. Native Arm builds, production signing, hosted Arm smoke, installer lifecycle, GUI acceptance, physical-device behavior, performance, and power require the external environments identified below.

`HIR-REGRESSION-004` is locally closed: every matrix entry has a stable `platform` identifier, and immutable package-create provenance artifacts use `matrix.platform`. Linux and Wasm therefore remain distinct even though both use `ubuntu-latest`.

## Prerequisites

### Local source validation

- Windows PowerShell.
- Git.
- Python with the repository's existing `pytest` and `PyYAML` dependencies.
- Working trees:
  - `C:\s\Demo\Hack2026\Cura`
  - `C:\s\Demo\Hack2026\Cura-workflows`

### Exact-SHA CI proof

- A pushed Cura implementation commit `C`.
- A pushed `cura-workflows` implementation commit `W`.
- Permission to push a temporary Cura branch named `CURA-*`.
- `gh` authenticated to `Ultimaker/Cura`.
- Conan credentials available to the workflows.
- Native self-hosted labels:
  - `self-hosted-Windows-ARM64` for payload creation.
  - `self-hosted-Windows-X64` for secure signing and packaging.
- GitHub hosted `windows-11-arm` availability for smoke testing.

### Secure X64 signing runner

- Native Windows Python.
- NSIS `makensis.exe`.
- WiX `heat.exe`, `candle.exe`, and `light.exe` with Arm64 support.
- Windows SDK `signtool.exe`.
- `C:\actions-runner\code_sign.cer`.
- `eToken Base Cryptographic Provider`.
- Non-empty `WIN_TOKEN_CONTAINER`.
- Network access to `http://timestamp.sectigo.com`.
- Windows Installer COM.

## 1. Local validation

Run from PowerShell.

```powershell
Set-Location 'C:\s\Demo\Hack2026\Cura'
$env:PYTEST_ADDOPTS='--confcutdir="tests\Packaging"'
python -m pytest tests\Packaging\TestValidatePeArchitecture.py tests\Packaging\TestCreateWindowsMsi.py tests\Packaging\TestCreateWindowsInstaller.py
if ($LASTEXITCODE -ne 0) { throw "Cura packaging tests failed: $LASTEXITCODE" }

python -m pytest tests\Packaging
if ($LASTEXITCODE -ne 0) { throw "Cura packaging suite failed: $LASTEXITCODE" }

git diff --check
if ($LASTEXITCODE -ne 0) { throw "Cura diff check failed: $LASTEXITCODE" }
```

```powershell
Set-Location 'C:\s\Demo\Hack2026\Cura-workflows'
python -m pytest runner_scripts\tests\test_windows_arm_artifact_contract.py runner_scripts\tests\test_workflow_provenance.py
if ($LASTEXITCODE -ne 0) { throw "Workflow contract tests failed: $LASTEXITCODE" }

python -m pytest runner_scripts\tests
if ($LASTEXITCODE -ne 0) { throw "Workflow script suite failed: $LASTEXITCODE" }

python runner_scripts\make_runners_list.py --platform-windows-arm64
if ($LASTEXITCODE -ne 0) { throw "Arm runner matrix failed: $LASTEXITCODE" }

git diff --check
if ($LASTEXITCODE -ne 0) { throw "Workflow diff check failed: $LASTEXITCODE" }
```

Expected Arm matrix:

```json
{"include": [{"platform": "windows-arm64", "runner": "windows-11-arm", "conan_extra_args": ""}]}
```

Parse all changed YAML:

```powershell
Set-Location 'C:\s\Demo\Hack2026\Cura-workflows'
@'
from pathlib import Path
import yaml

files = [
    Path(".github/actions/setup-build-environment/action.yml"),
    Path(".github/workflows/conan-package.yml"),
    Path(".github/workflows/conan-recipe-export.yml"),
    Path(".github/workflows/conan-recipe-version.yml"),
    Path(".github/workflows/cura-installer-windows-arm.yml"),
    Path(".github/workflows/cura-installer-windows.yml"),
    Path(".github/workflows/cura-installers.yml"),
    Path(".github/workflows/make-runners-list.yml"),
]
for path in files:
    if not isinstance(yaml.safe_load(path.read_text(encoding="utf-8")), dict):
        raise SystemExit(f"not a YAML mapping: {path}")
print(f"parsed {len(files)} YAML files")
'@ | python -
if ($LASTEXITCODE -ne 0) { throw "YAML parsing failed: $LASTEXITCODE" }
```

### Required matrix and uniqueness checks

```powershell
Set-Location 'C:\s\Demo\Hack2026\Cura-workflows'
$cases = [ordered]@{
    '--platform-linux'         = @('linux', 'ubuntu-latest', '')
    '--platform-windows'       = @('windows', 'windows-latest', '')
    '--platform-mac'           = @('macos', 'macos-13', '')
    '--platform-windows-arm64' = @('windows-arm64', 'windows-11-arm', '')
    '--platform-wasm'          = @('wasm', 'ubuntu-latest', '-pr:h cura_wasm.jinja')
}
foreach ($flag in $cases.Keys) {
    $matrix = python runner_scripts\make_runners_list.py $flag | ConvertFrom-Json
    if ($LASTEXITCODE -ne 0 -or $matrix.include.Count -ne 1) {
        throw "matrix failed: $flag"
    }
    $entry = $matrix.include[0]
    $expected = $cases[$flag]
    if ($entry.platform -ne $expected[0] -or
        $entry.runner -ne $expected[1] -or
        $entry.conan_extra_args -ne $expected[2]) {
        throw "matrix mismatch: $flag"
    }
}

$linuxWasm = python runner_scripts\make_runners_list.py --platform-linux --platform-wasm | ConvertFrom-Json
$linuxWasmNames = @($linuxWasm.include | ForEach-Object {
    "package-provenance-create-12345-1-$($_.platform)"
})
if ($linuxWasmNames.Count -ne 2 -or @($linuxWasmNames | Sort-Object -Unique).Count -ne 2) {
    throw 'Linux and Wasm provenance artifact names collide'
}

$allJson = python runner_scripts\make_runners_list.py `
    --platform-linux --platform-windows --platform-mac --platform-windows-arm64 --platform-wasm
$all = $allJson | ConvertFrom-Json
$allNames = @($all.include | ForEach-Object {
    "package-provenance-create-12345-1-$($_.platform)"
})
if ($allNames.Count -ne 5 -or @($allNames | Sort-Object -Unique).Count -ne 5) {
    throw 'All-platform provenance artifact names are not unique'
}
$linuxWasmNames
$allNames
```

Expected Linux+Wasm names:

```text
package-provenance-create-12345-1-linux
package-provenance-create-12345-1-wasm
```

Expected all-platform suffixes: `linux`, `windows`, `macos`, `windows-arm64`, and `wasm`.

## 2. Create immutable `C`, `W`, and `V`

`V` must be one commit directly on `C`, and it must contain both caller changes before either workflow runs.

```powershell
$CuraRepo = 'C:\s\Demo\Hack2026\Cura'
$WorkflowRepo = 'C:\s\Demo\Hack2026\Cura-workflows'

$C = (git -C $CuraRepo rev-parse HEAD).Trim()
$W = (git -C $WorkflowRepo rev-parse HEAD).Trim()
if ($C -notmatch '^[0-9a-f]{40}$' -or $W -notmatch '^[0-9a-f]{40}$') {
    throw 'C and W must be exact commits'
}

$Branch = "CURA-arm64-proof-$($C.Substring(0,8))"
git -C $CuraRepo switch -c $Branch $C
```

In `Cura\.github\workflows\conan-package.yml`, keep the existing trigger and replace the reusable job with:

```yaml
jobs:
  conan-package:
    uses: ultimaker/cura-workflows/.github/workflows/conan-package.yml@<W>
    with:
      cura_workflows_ref: <W>
      allow_non_default_branch_package_create: true
      platform_linux: false
      platform_windows: false
      platform_mac: false
      platform_windows_arm64: true
      platform_wasm: false
    secrets: inherit
```

In `Cura\.github\workflows\windows-arm.yml`, add these `workflow_dispatch.inputs`:

```yaml
      package_workflow_run_id:
        description: 'Validated package workflow run ID'
        required: true
        type: string
      package_workflow_run_attempt:
        description: 'Validated package workflow run attempt'
        required: true
        type: string
```

Use this reusable job, substituting the same literal `W` twice:

```yaml
jobs:
  windows-installer:
    uses: ultimaker/cura-workflows/.github/workflows/cura-installer-windows-arm.yml@<W>
    with:
      cura_conan_version: ${{ inputs.cura_conan_version }}
      package_overrides: ${{ inputs.package_overrides }}
      conan_args: ${{ inputs.conan_args }}
      enterprise: ${{ inputs.enterprise }}
      staging: ${{ inputs.staging }}
      operating_system: ${{ inputs.operating_system }}
      signing_operating_system: self-hosted-Windows-X64
      cura_workflows_ref: <W>
      package_workflow_run_id: ${{ inputs.package_workflow_run_id }}
      package_workflow_run_attempt: ${{ inputs.package_workflow_run_attempt }}
    secrets: inherit
```

Commit both files together:

```powershell
git -C $CuraRepo add .github/workflows/conan-package.yml .github/workflows/windows-arm.yml
git -C $CuraRepo commit -m 'Add temporary immutable Arm64 validation callers'
$V = (git -C $CuraRepo rev-parse HEAD).Trim()

$parents = (git -C $CuraRepo rev-list --parents -n 1 $V).Trim().Split(' ')
if ($parents.Count -ne 2 -or $parents[1] -ne $C) {
    throw 'V must have exactly C as its parent'
}
$changed = @(git -C $CuraRepo diff --name-only "$C..$V")
$expected = @('.github/workflows/conan-package.yml', '.github/workflows/windows-arm.yml')
if (@(Compare-Object $changed $expected).Count) {
    throw "C..V contains unexpected files: $($changed -join ', ')"
}

python "$WorkflowRepo\runner_scripts\workflow_provenance.py" validate-callers `
  --repository $CuraRepo --validation-sha $V --workflow-sha $W `
  --output "$CuraRepo\source-chain.json"
if ($LASTEXITCODE -ne 0) { throw "Local C/V/W validation failed: $LASTEXITCODE" }
Remove-Item "$CuraRepo\source-chain.json"

git -C $CuraRepo push -u origin $Branch
```

The push must start the package workflow at exactly `V`.

## 3. Validate the Arm Conan package run

```powershell
$runs = gh run list --repo Ultimaker/Cura --workflow conan-package.yml `
  --branch $Branch --commit $V --event push --limit 20 `
  --json databaseId,headSha,createdAt,status,conclusion,url | ConvertFrom-Json
$packageRun = $runs | Where-Object headSha -eq $V |
  Sort-Object createdAt -Descending | Select-Object -First 1
if (-not $packageRun) { throw 'Package run for V was not found' }

$PackageRunId = [string]$packageRun.databaseId
gh run watch $PackageRunId --repo Ultimaker/Cura --exit-status
if ($LASTEXITCODE -ne 0) { throw "Package run failed: $PackageRunId" }

$PackageAttempt = [string](gh api "repos/Ultimaker/Cura/actions/runs/$PackageRunId" --jq .run_attempt)
$PackageEvidence = Join-Path $CuraRepo 'package-proof'
Remove-Item $PackageEvidence -Recurse -Force -ErrorAction SilentlyContinue
gh run download $PackageRunId --repo Ultimaker/Cura `
  --name "validated-package-provenance-$PackageRunId-$PackageAttempt" `
  --dir $PackageEvidence
if ($LASTEXITCODE -ne 0) { throw 'Validated package provenance download failed' }

$packageChainPath = Get-ChildItem $PackageEvidence -Recurse -Filter package-chain.json |
  Select-Object -First 1 -ExpandProperty FullName
$packageChain = Get-Content -Raw $packageChainPath | ConvertFrom-Json
$PackageReference = [string]$packageChain.package_reference
if ($packageChain.C -ne $C -or $packageChain.V -ne $V -or $packageChain.W -ne $W) {
    throw 'Downloaded package chain does not match C/V/W'
}
```

Required package evidence:

- Package job ran on `windows-11-arm`.
- Runner, `PROCESSOR_ARCHITECTURE`, and Python report `ARM64`.
- All sixteen provenance instances are present exactly once and resolve to `W`.
- The package reference, run ID, run attempt, `C`, `V`, and `W` match `package-chain.json`.
- Required provenance and validation-chain artifact uploads succeeded.

## 4. Dispatch the installer at unchanged `V`

```powershell
gh workflow run windows-arm.yml --repo Ultimaker/Cura --ref $Branch `
  -f "cura_conan_version=$PackageReference" `
  -f "package_workflow_run_id=$PackageRunId" `
  -f "package_workflow_run_attempt=$PackageAttempt" `
  -f 'enterprise=false' `
  -f 'staging=false' `
  -f 'operating_system=self-hosted-Windows-ARM64'
if ($LASTEXITCODE -ne 0) { throw 'Installer dispatch failed' }

Start-Sleep -Seconds 5
$installerRuns = gh run list --repo Ultimaker/Cura --workflow windows-arm.yml `
  --branch $Branch --commit $V --event workflow_dispatch --limit 20 `
  --json databaseId,headSha,createdAt,status,conclusion,url | ConvertFrom-Json
$installerRun = $installerRuns | Where-Object headSha -eq $V |
  Sort-Object createdAt -Descending | Select-Object -First 1
if (-not $installerRun) { throw 'Installer run for V was not found' }

$InstallerRunId = [string]$installerRun.databaseId
gh run watch $InstallerRunId --repo Ultimaker/Cura --exit-status
if ($LASTEXITCODE -ne 0) { throw "Installer run failed: $InstallerRunId" }
$InstallerAttempt = [string](gh api "repos/Ultimaker/Cura/actions/runs/$InstallerRunId" --jq .run_attempt)
```

Expected job order:

1. `build-arm-payload` on native self-hosted Arm64.
2. `sign-and-package` on secure self-hosted X64.
3. `smoke-test-on-hosted-arm` on `windows-11-arm`.

## 5. Download and independently verify signed outputs

```powershell
$EvidenceRoot = Join-Path $CuraRepo 'arm64-evidence'
Remove-Item $EvidenceRoot -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $EvidenceRoot | Out-Null

gh run download $InstallerRunId --repo Ultimaker/Cura `
  --name "windows-arm64-signed-payload-$InstallerRunId-$InstallerAttempt" `
  --dir "$EvidenceRoot\signed"
if ($LASTEXITCODE -ne 0) { throw 'Signed payload download failed' }

$release = Get-Content -Raw "$EvidenceRoot\signed\metadata\release-evidence.json" | ConvertFrom-Json
$exeName = Split-Path ($release.files | Where-Object path -Like '*.exe').path -Leaf
$msiName = Split-Path ($release.files | Where-Object path -Like '*.msi').path -Leaf
$installerBase = [IO.Path]::GetFileNameWithoutExtension($exeName)

gh run download $InstallerRunId --repo Ultimaker/Cura --name "$installerBase-exe" --dir "$EvidenceRoot\installers"
if ($LASTEXITCODE -ne 0) { throw 'EXE download failed' }
gh run download $InstallerRunId --repo Ultimaker/Cura --name "$installerBase-msi" --dir "$EvidenceRoot\installers"
if ($LASTEXITCODE -ne 0) { throw 'MSI download failed' }

python "$WorkflowRepo\runner_scripts\windows_arm_artifact_contract.py" verify `
  --root "$EvidenceRoot\signed" `
  --contract "$EvidenceRoot\signed\metadata\signed-contract.json"
if ($LASTEXITCODE -ne 0) { throw 'Signed contract verification failed' }

python "$WorkflowRepo\runner_scripts\windows_arm_artifact_contract.py" verify-release `
  --root "$EvidenceRoot\installers" `
  --evidence "$EvidenceRoot\signed\metadata\release-evidence.json"
if ($LASTEXITCODE -ne 0) { throw 'Installer release evidence verification failed' }

python "$EvidenceRoot\signed\packaging\windows\validate_pe_architecture.py" `
  "$EvidenceRoot\signed\payload\UltiMaker-Cura" --architecture arm64 `
  --require python3.dll --require concrt140.dll --require msvcp140.dll `
  --require msvcp140_1.dll --require msvcp140_2.dll `
  --require vcruntime140.dll --require vcruntime140_1.dll `
  --require UltiMaker-Cura.exe --require CuraEngine.exe
if ($LASTEXITCODE -ne 0) { throw 'Downloaded payload is not wholly Arm64' }
```

Verify Authenticode:

```powershell
$signedFiles = @(
  "$EvidenceRoot\signed\payload\UltiMaker-Cura\CuraEngine.exe",
  "$EvidenceRoot\signed\payload\UltiMaker-Cura\UltiMaker-Cura.exe",
  "$EvidenceRoot\installers\$exeName",
  "$EvidenceRoot\installers\$msiName"
)
foreach ($file in $signedFiles) {
    & signtool verify /pa /all /v $file
    if ($LASTEXITCODE -ne 0) { throw "Signature verification failed: $file" }
}
```

Verify MSI architecture and components:

```powershell
$installer = New-Object -ComObject WindowsInstaller.Installer
$msiPath = (Resolve-Path "$EvidenceRoot\installers\$msiName").Path
$database = $installer.GetType().InvokeMember('OpenDatabase','InvokeMethod',$null,$installer,@($msiPath,0))
$summary = $database.GetType().InvokeMember('SummaryInformation','GetProperty',$null,$database,@(0))
$template = [string]$summary.GetType().InvokeMember('Property','GetProperty',$null,$summary,@(7))
$pageCount = [int]$summary.GetType().InvokeMember('Property','GetProperty',$null,$summary,@(14))
if (-not $template.StartsWith('Arm64;')) { throw "MSI template is $template" }
if ($pageCount -lt 500) { throw "MSI page count is $pageCount" }

$view = $database.GetType().InvokeMember('OpenView','InvokeMethod',$null,$database,@('SELECT `Attributes` FROM `Component`'))
$view.GetType().InvokeMember('Execute','InvokeMethod',$null,$view,$null)
$componentCount = 0
while ($record = $view.GetType().InvokeMember('Fetch','InvokeMethod',$null,$view,$null)) {
    $attributes = [int]$record.GetType().InvokeMember('IntegerData','GetProperty',$null,$record,@(1))
    if (($attributes -band 256) -eq 0) { throw 'MSI contains a 32-bit component' }
    $componentCount++
}
if ($componentCount -eq 0) { throw 'MSI contains no components' }
```

## 6. Physical Windows Arm acceptance

Use a maintainer-owned native Windows Arm64 device or a restorable native Arm64 test image. Record device model, CPU, Windows edition/build, test account, installer SHA-256, timestamps, logs, and pass/fail. Do not substitute emulation evidence.

### Clean EXE install

```powershell
$exe = Resolve-Path "$EvidenceRoot\installers\$exeName"
Get-FileHash $exe -Algorithm SHA256
$process = Start-Process $exe -ArgumentList '/S' -Wait -PassThru
if ($process.ExitCode -ne 0) { throw "EXE install failed: $($process.ExitCode)" }

$entry = Get-ChildItem 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall' |
  Get-ItemProperty | Where-Object DisplayName -Like 'UltiMaker Cura *' |
  Sort-Object DisplayVersion -Descending | Select-Object -First 1
if (-not $entry) { throw 'EXE install registration not found' }
$uninstaller = $entry.UninstallString.Trim('"')
$curaExe = Join-Path (Split-Path $uninstaller) 'UltiMaker-Cura.exe'
if (!(Test-Path $curaExe)) { throw 'Installed Cura executable not found' }
```

Launch Cura interactively, load a representative STL, slice through CuraEngine, export G-code, close Cura, and restart it. Preserve application/engine logs.

### EXE upgrade/lifecycle

Install the approved older signed Arm64 EXE, complete the smoke steps, then install the new EXE with `/S`. Record whether the product intentionally replaces or coexists with the older version; verify the actual registry entries, install directories, launch, slice, restart, and uninstall behavior. The current NSIS template includes the version in its product name and install directory, so replacement must not be assumed without observed evidence.

### EXE uninstall

```powershell
$process = Start-Process $uninstaller -ArgumentList '/S' -Wait -PassThru
if ($process.ExitCode -ne 0) { throw "EXE uninstall failed: $($process.ExitCode)" }
if (Test-Path (Split-Path $uninstaller)) { throw 'EXE install directory remains' }
```

### Clean MSI install

Start from a restored clean image.

```powershell
$msi = Resolve-Path "$EvidenceRoot\installers\$msiName"
$installLog = Join-Path $EvidenceRoot 'msi-install.log'
Get-FileHash $msi -Algorithm SHA256
$process = Start-Process msiexec.exe `
  -ArgumentList @('/i', "`"$msi`"", '/qn', '/norestart', '/L*v', "`"$installLog`"") `
  -Wait -PassThru
if ($process.ExitCode -notin 0,3010) { throw "MSI install failed: $($process.ExitCode)" }
```

Launch Cura interactively and repeat load, slice, G-code export, close, and restart acceptance.

### MSI upgrade and uninstall

Install the approved older signed Arm64 MSI, then install the newer MSI with a separate verbose log. Verify the intended replace/coexist behavior rather than assuming it. Obtain the installed uninstall command from the matching ARP entry:

```powershell
$entry = Get-ChildItem 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall' |
  Get-ItemProperty | Where-Object DisplayName -Like 'UltiMaker Cura*' |
  Sort-Object DisplayVersion -Descending | Select-Object -First 1
if (-not $entry) { throw 'MSI install registration not found' }

$uninstallLog = Join-Path $EvidenceRoot 'msi-uninstall.log'
$productCode = [regex]::Match($entry.UninstallString, '\{[0-9A-Fa-f-]{36}\}').Value
if (-not $productCode) { throw 'MSI product code not found' }
$process = Start-Process msiexec.exe `
  -ArgumentList @('/x', $productCode, '/qn', '/norestart', '/L*v', "`"$uninstallLog`"") `
  -Wait -PassThru
if ($process.ExitCode -notin 0,3010) { throw "MSI uninstall failed: $($process.ExitCode)" }
```

### Physical acceptance checklist

- Native OS and CPU identity recorded.
- EXE and MSI hashes match release evidence.
- All four signatures verify.
- Clean EXE install, launch, slice, export, restart, and uninstall pass.
- Clean MSI install, launch, slice, export, restart, and uninstall pass.
- Older-to-newer lifecycle behavior is recorded for both formats.
- No unexpected X64/Win32 process or payload file is observed.
- No performance or power claim is made unless a separately approved measurement plan is executed.

## 7. Diagnostics

| Failure | Required action |
|---|---|
| Runner/Python is not `ARM64` | Stop; correct the native runner image/PATH. Do not use emulated Python. |
| Native `<sys.base_prefix>\python3.dll` is missing, wrong version, or not `0xAA64` | Stop; repair native Python. Never restore the AMD64 workaround DLL. |
| VS/CRT discovery returns zero or multiple directories | Record `vswhere` output and installed redist layout; repair the runner image. |
| Any PE is malformed or not `0xAA64` | Use the validator's complete error list; replace/rebuild the offending dependency. |
| Contract has missing/extra files or hash/size mismatch | Discard the transferred artifact and rerun from a clean workspace. |
| Signing preflight or verification fails | Do not package/upload a release; retain only restricted diagnostics. |
| MSI template, page count, or component attributes fail | Block the MSI and correct WiX authoring/toolchain support. |
| Hosted engine smoke times out, exits nonzero, or lacks `usage` | Block publication and retain the job logs. |
| Matrix provenance artifact uniqueness assertion fails | Stop; preserve stable unique `platform` values and keep package-create upload names bound to `matrix.platform`. |

## 8. External gates and cleanup

Stable publication remains blocked until exact-SHA CI, secure production signing, hosted Arm smoke, X64 regression, and both physical installer acceptance paths pass and maintainers explicitly approve publication.

After recording immutable run URLs, summaries, artifact IDs/digests, contract hashes, and `C/V/W`, remove local downloads and revert the temporary validation commit/branch. Never merge `V`.
