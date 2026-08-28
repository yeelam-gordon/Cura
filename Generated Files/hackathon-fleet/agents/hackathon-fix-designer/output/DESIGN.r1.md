# Windows Arm64 installer fix design — r1

## Decision

Implement two coordinated, upstreamable PRs: first make Cura's MSI builder and payload validator architecture-aware; then make `cura-workflows` select Arm64 CRTs, validate every packaged PE, package/sign on the existing X64 signing host, and smoke-test the signed payload on GitHub's real Arm64 hosted runner. Do not alter the already-working Conan dependency split or add broad fork-only workflow repoints.

## Current-state evidence

Repository baselines:

```text
Cura              5068661cd448b954328483a499fe4ff419b695b5 (main == origin/main)
cura-workflows    126f92d186e62a8c2f50ed1883c37a81e1d929de (main == origin/main)
```

Verified with `git status --short --branch` and `git log -8 --oneline --decorate` in both repositories.

### Confirmed working foundations

- Cura maps Windows Conan `armv8` to the Arm64 dependency/package path and already removes unsupported `pynavlib` from the Arm64 PyInstaller collection: `Cura/conanfile.py:607-609`; its Windows-X64-only hashes are isolated under `Windows_x64` in `Cura/conandata.yml:629-640`.
- The packaging directory is exported, packaged, and deployed, so a validator added there will be available as `cura_inst\packaging\...`: `Cura/conanfile.py:636-641,761-766,798-805`.
- The reusable installer fan-out already has a Windows Arm job on `self-hosted-Windows-ARM64`: `cura-workflows/.github/workflows/cura-installers.yml:89-98`.
- The dedicated Cura dispatcher already calls the Arm reusable workflow: `Cura/.github/workflows/windows-arm.yml:38-47`.
- History shows this is follow-up quality work, not a new port: `cura-workflows` PR #56 merged as `8dad60b` and created the Arm workflow; Cura tag `5.14.0-alpha.0` resolves to `17e7b05ddc5f047c6a0b601f3308785810a091ca`.
- GitHub's release API for `5.14.0-alpha.0` lists `UltiMaker-Cura-5.14.0-alpha.0-win64-ARM64.exe` (SHA-256 `3ecea607...`, published 2026-06-25). It lists no Windows Arm MSI asset.

### Confirmed defects

1. **Wrong CRT architecture.** The Arm workflow selects `x64/Microsoft.VC*.CRT` and copies six DLLs into the payload: `cura-workflows/.github/workflows/cura-installer-windows-arm.yml:104-115`. `git blame -L 104,115` attributes this unchanged copied block to the initial Arm workflow commit `643104c2`.
2. **MSI is marked X64.** `Cura/packaging/msi/create_windows_msi.py:107-114` hardcodes `candle -arch x64`, while the Arm workflow invokes it without an architecture argument at `cura-installer-windows-arm.yml:142-147`. The same hardcode exists at tag `5.14.0-alpha.0`.
3. **Signing parity is absent.** The X64 workflow signs `CuraEngine.exe`, `UltiMaker-Cura.exe`, the EXE installer, and MSI at `cura-installer-windows.yml:107-113,154-159,178-183`; the Arm workflow contains no `signtool` call.
4. **No payload architecture gate exists.** Both installer generators consume the full `dist/UltiMaker-Cura` tree (`create_windows_installer.py:22-35`; MSI `heat dir` at `create_windows_msi.py:92-105`), but neither workflow checks PE machine headers before packaging.
5. **The advertised hosted package-runner label is invalid.** `runner_scripts/make_runners_list.py:14-15` emits `windows-latest-arm64`; current GitHub documentation lists `windows-11-arm` and `windows-11-vs2026-arm`, not that label.
6. **The Arm CRT lookup cannot run on the hosted image.** The workflow hardcodes Visual Studio 2022 Community (`cura-installer-windows-arm.yml:106`); the current `windows-11-arm` image documents Visual Studio 2022 Enterprise at `C:\Program Files\Microsoft Visual Studio\2022\Enterprise`, plus `vswhere`, Bash, native Python, NSIS, and ARM64 VC tools.
7. **MSI/NSIS command failures are not reliably propagated.** MSI uses `subprocess.call` three times (`create_windows_msi.py:105,114,125`) and NSIS uses `subprocess.run` without `check=True` (`create_windows_installer.py:86-88`).
8. **Stable publication is not wired.** Release-candidate upload enumerates only Windows X64 artifacts at `Cura/.github/workflows/release-process_release-candidate.yml:179-180`; nightly uses a broad `UltiMaker-Cura-*` artifact pattern at `Cura/.github/workflows/nightly.yml:35-39`.

Microsoft requires an Arm64 MSI to have Template Summary platform `Arm64`, Page Count at least 500, and 64-bit component attributes. WiX 3.14.1 source includes `Platform.ARM64`; therefore `candle -arch arm64` is the appropriate existing-toolchain correction, not a WiX 4 migration.

## Root cause and duplication risks

The Arm workflow was cloned from the X64 workflow before architecture-sensitive concerns were factored out. It changed the package/profile/filename path but retained the X64 CRT lookup and inherited an MSI generator whose architecture had been fixed to X64 since 2023. Signing was omitted entirely, and no machine-header/MSI metadata assertion existed to catch either error.

Do **not** duplicate or redesign already-solved work:

- Do not change `pynavlib`, package hashes, PyInstaller target selection, G-code tests, or application runtime code.
- Do not introduce a new Arm Conan profile unless a real CI failure proves the current `installer.jinja` profile wrong.
- Do not repoint the inventory of unrelated `ultimaker/cura-workflows@main` references.
- Do not claim the NSIS bootstrap EXE itself is native Arm64; validate its packaged payload. NSIS may use an emulated launcher while carrying a fully Arm64 application.
- Do not place a demo certificate path or self-signed certificate creation in the upstream PR.

## Dependency graph and proposed architecture

```text
Cura PR (backward-compatible)
  MSI --architecture + fail-fast subprocesses
  payload PE validator + unit tests
          |
          v
Arm Conan package containing updated packaging tools
          |
          v
Arm payload-build job (self-hosted-Windows-ARM64 by default)
  PyInstaller -> Arm64 CRT discovery/copy -> blacklist cleanup
  -> all-PE architecture validation -> unsigned payload artifact
          |
          v
sign-and-package job (self-hosted-Windows-X64)
  sign internal EXEs with existing production eToken contract
  -> build NSIS EXE and Arm64 MSI
  -> sign final installers -> signtool verify -> final artifacts
          |
          v
hosted Arm smoke job (windows-11-arm)
  assert runner/Python Arm64 -> download signed payload/installers
  -> repeat PE validation -> verify signatures -> execute CuraEngine CLI smoke
          |
          v
nightly artifact collection; stable publication remains a separate gate
```

Packaging/signing on the known X64 signing runner is intentional: Authenticode can sign Arm binaries cross-architecture, the current X64 workflow proves that runner owns the eToken/CSP/tooling contract, and the Arm runner no longer needs physical access to that token or WiX. The internal EXEs are signed before installers are built, so their signatures are embedded in both installers.

## Exact change surface

### PR 1 — `Ultimaker/Cura`

1. **`packaging/msi/create_windows_msi.py`**
   - Change `build(dist_path, filename)` to `build(dist_path, filename, architecture)`.
   - Add required CLI argument `--architecture` with choices `x64` and `arm64`; retain default `x64` only if compatibility with unmodified callers is needed during staggered landing.
   - Replace hardcoded `"-arch", "x64"` with the validated argument.
   - Replace all three `subprocess.call(...)` uses with `subprocess.run(..., check=True)`.
2. **`packaging/NSIS/create_windows_installer.py`**
   - Change the `makensis` invocation to `subprocess.run(command, check=True)`.
3. **New `packaging/windows/validate_pe_architecture.py`**
   - CLI: `PATH --architecture arm64|x64`.
   - Recursively inspect every `.exe`, `.dll`, and `.pyd`.
   - Parse DOS `MZ`, `e_lfanew`, `PE\0\0`, and COFF Machine without external packages.
   - Accept only `0xAA64` for `arm64` and `0x8664` for `x64`; report relative path and actual code for every mismatch and exit nonzero. Malformed PE candidates are failures, not skips.
   - Require at least one PE and explicitly require the six copied CRT names for the Arm invocation.
4. **New tests**
   - `tests/Packaging/TestValidatePeArchitecture.py`: synthetic ARM64/X64/malformed PE fixtures; recursive enumeration; missing CRT; mixed-architecture failure.
   - `tests/Packaging/TestCreateWindowsMsi.py`: mock subprocess and assert `-arch arm64`/`-arch x64`, invalid CLI rejection, and `check=True`.
   - `tests/Packaging/TestCreateWindowsInstaller.py`: assert `makensis` failure propagates.

### PR 2 — `Ultimaker/cura-workflows`

1. **`.github/workflows/cura-installer-windows-arm.yml`**
   - Add optional `signing_operating_system` input defaulting to `self-hosted-Windows-X64`.
   - Split the current job into `build-arm-payload`, `sign-and-package`, and `smoke-test-on-hosted-arm`.
   - In `build-arm-payload`, replace the Community/X64 CRT block with `vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Redist.14.Latest -property installationPath`, select the newest non-`v*` `VC\Redist\MSVC` directory, then select `arm64\Microsoft.VC*.CRT`. Copy the same six named DLLs and fail if the installation, directory, or any file is missing.
   - Run `cura_inst\packaging\windows\validate_pe_architecture.py dist\UltiMaker-Cura --architecture arm64` after CRT copy, Python-DLL workaround, and blacklist cleanup.
   - Upload the complete unsigned payload plus `cura_inst\packaging` as a one-day intermediate artifact. Do not use the public `UltiMaker-Cura-*` naming pattern for this artifact.
   - In `sign-and-package`, download the intermediate artifact on the X64 signing runner; use the same four production signing calls and parameters as the X64 workflow: `C:\actions-runner\code_sign.cer`, `eToken Base Cryptographic Provider`, `${{ secrets.WIN_TOKEN_CONTAINER }}`, SHA-256, and Sectigo RFC3161 timestamping.
   - Build EXE from the signed payload and build MSI with `--architecture arm64`.
   - Verify each internal EXE and final installer with `signtool verify /pa /all /v`; upload only after verification.
   - Read MSI SummaryInformation properties through `WindowsInstaller.Installer`: property 7 must begin `Arm64;`, property 14 must be at least 500.
   - Upload a signed-payload artifact for the smoke job, plus the existing final EXE/MSI/application/engine artifact names.
   - In `smoke-test-on-hosted-arm`, use `windows-11-arm`, assert `$env:PROCESSOR_ARCHITECTURE -eq 'ARM64'` and native Python reports `ARM64`, rerun the PE validator, verify signatures, and run a deterministic CuraEngine help/version command with a timeout and required zero exit code. If the current engine CLI uses a different accepted help token, establish it in the first CI run and then freeze that exact command.
   - Restore the existing self-hosted Conan cache cleanup to the Arm build job.
2. **`.github/workflows/cura-installer-windows.yml`**
   - Pass `--architecture x64` explicitly to the MSI builder.
   - No signing semantic change.
3. **`.github/workflows/cura-installers.yml`**
   - Keep production Arm build on `self-hosted-Windows-ARM64`.
   - Pass `signing_operating_system: self-hosted-Windows-X64`.
4. **`runner_scripts/make_runners_list.py`**
   - Replace `windows-latest-arm64` with `windows-11-arm`.
5. **`.github/actions/setup-build-environment/action.yml`**
   - Rename the “Windows ARM64 self-hosted” step/comment to “Windows ARM64”; its native-Python PATH logic applies to hosted Arm too.
   - Remove the reference to nonexistent `runner_scripts/windows_arm_setup.ps1`; document self-hosted provisioning outside this code change if maintainers have a private runbook.

### Cura caller/reference handling

- Upstream merged callers remain `@main`; no mass reference change is part of either PR.
- To validate the workflow PR before merge, make a **temporary validation-only** change to `Cura/.github/workflows/windows-arm.yml:40`, pointing `uses:` to the exact workflow PR commit SHA, build the Cura PR's Arm Conan package, and dispatch with that package version. Revert this reference before merging.
- An external fork must also repoint the called workflow owner/ref. That is a demo-only patch, not upstream content. GitHub does not permit expressions in the `uses:` ref, so a dynamic repository/ref abstraction would not remove this requirement.

## Alternatives and tradeoffs

1. **Sign directly on the Arm runner.** Smaller YAML diff, but assumes the physical eToken, certificate file, CSP, and interactive token behavior exist on that machine. Rejected as the default because current evidence proves this contract only on the X64 signing runner.
2. **Make signing optional.** Easier fork CI, but risks silently publishing unsigned artifacts. Rejected upstream. A fork may substitute a clearly labeled self-signed PFX in its own branch solely to demonstrate workflow mechanics.
3. **Move all Arm building to `windows-11-arm`.** The label and native toolchain are real, but full Conan/PyInstaller disk/time/private-remote behavior is unverified and the image will migrate from VS2022 to VS2026 beginning 2026-09-21. Keep hosted execution as smoke evidence; allow a manual hosted build experiment only after a green targeted run.
4. **Migrate MSI to WiX 4.** Unnecessary scope: WiX 3.14.1 already includes ARM64, and the current scripts/templates are WiX 3 shaped.
5. **Ship only NSIS.** Matches the existing public alpha asset, but leaves the reusable workflow's MSI output falsely X64. Reject unless maintainers explicitly decide to remove Arm MSI generation.

## Ordered implementation and validation

1. Land/prepare Cura PR first; its X64 default keeps old workflow callers working.
2. Run:
   ```powershell
   python -m pytest tests\Packaging\TestValidatePeArchitecture.py tests\Packaging\TestCreateWindowsMsi.py tests\Packaging\TestCreateWindowsInstaller.py
   git diff --check
   ```
3. Build and publish the Cura PR's Arm Conan package through the existing package workflow.
4. Implement workflow PR and run:
   ```powershell
   python runner_scripts\make_runners_list.py --platform-windows-arm64
   # required JSON member: {"runner":"windows-11-arm","conan_extra_args":""}
   git diff --check
   ```
5. Apply the temporary exact-SHA caller reference and dispatch the Arm workflow with the PR package version.
6. Required CI evidence:
   - selected CRT path contains `\arm64\Microsoft.VC*.CRT`;
   - validator reports every PE and zero non-Arm64 entries;
   - `CuraEngine.exe` and `UltiMaker-Cura.exe` verify after production signing;
   - final EXE and MSI verify after signing;
   - MSI Template Summary starts `Arm64;` and Page Count is `>=500`;
   - hosted smoke logs `runner.arch/PROCESSOR_ARCHITECTURE/Python == ARM64` and a successful engine invocation;
   - X64 installer workflow remains green and MSI reports `x64;...`.
7. Revert the temporary workflow reference and merge workflow PR.
8. Do not add Arm artifacts to stable release upload until maintainer acceptance and physical/interactive Arm testing are recorded.

## Rollback

- If CI fails before release, revert the workflow PR first; the backward-compatible Cura MSI option can remain without behavioral change.
- If both must be reverted, revert `cura-workflows` before Cura so no caller passes an unsupported `--architecture`.
- A signing or hosted-smoke failure must fail the reusable workflow; never bypass it by publishing the intermediate unsigned artifact.
- If VS image migration breaks discovery, pin the smoke job temporarily to the last supported explicit GitHub image while fixing discovery; do not restore a Community/year hardcode.

## Ownership, assumptions, and gates

**Agent/contributor controlled:** source changes, unit tests, PE/MSI assertions, exact-SHA validation branch, hosted Arm smoke, and clearly isolated fork self-signing demonstrations.

**Ultimaker maintainer controlled:** Conan/private credentials, `WIN_TOKEN_CONTAINER`, `C:\actions-runner\code_sign.cer`, eToken/CSP availability on `self-hosted-Windows-X64`, self-hosted runner labels/provisioning, workflow-PR branch access, official signing, and release publication.

**Vendor controlled:** GitHub hosted labels/images and the announced VS2026 migration; Microsoft Visual Studio redistributable layout; Sectigo timestamp availability.

Open gates:

1. Confirm the X64 signing runner's WiX version accepts `candle -arch arm64`; the real compile and MSI SummaryInformation assertion are the acceptance test.
2. Confirm the eToken can sign Arm PE files non-interactively and the timestamp endpoint is reachable.
3. Confirm the deterministic CuraEngine smoke command and freeze it in the workflow.
4. No physical Windows Arm device is established here. A hosted Arm VM proves native build/runtime architecture, but it does **not** prove GUI rendering, driver integration, USB/printer behavior, sleep/resume, or end-user installation on physical hardware. Stable promotion requires a maintainer-owned physical Arm install/launch/slice/export test (or an explicitly accepted Windows-on-Arm VM substitute).
5. Stable release upload currently excludes Windows Arm; adding `win64-ARM64.exe/.msi` is a separate maintainer decision after gate 4.

confidence: high

Justification: Current source and history directly prove the CRT, signing, MSI metadata, runner-label, and reference behavior, while the design isolates the only unprovable elements—production credentials and physical Arm execution—as explicit maintainer gates.
