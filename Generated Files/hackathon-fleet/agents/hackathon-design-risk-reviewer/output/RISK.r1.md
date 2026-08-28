# RISK r1 — Independent Windows Arm64 Installer Assessment

## Baseline and verdict

- Inspected every file under `Cura\Generated Files`, Cura `main` at `5068661cd448b954328483a499fe4ff419b695b5`, and cura-workflows `main` at `126f92d186e62a8c2f50ed1883c37a81e1d929de`.
- Repository history shows the Arm workflow was copied from the x64 workflow in `cura-workflows` commit `643104c` (2026-01-05); later work corrected the displayed architecture/profile but left several x64-coupled packaging assumptions.
- GitHub's API confirms that release `5.14.0-alpha.0` published an Arm64-named EXE on 2026-06-25. That proves artifact production, not payload architecture, signature, installability, or native execution.

**Initial verdict: NO-GO** for implementation or stable-promotion under the current “one-line CRT plus signing parity” framing. The effort remains viable, but two additional architecture defects, false-green packaging, hosted-runner incompatibilities, signing provenance, and end-to-end Arm validation must be designed and gated first.

## Current-state/root-cause assessment

The primary root cause is an incomplete x64-to-Arm workflow clone, not a single bad glob. Architecture is passed as a filename label to `prepare_installer.py`, while the workflow independently selects CRTs, copies a committed ABI DLL, invokes an x64-hardcoded MSI builder, and never checks the final payload's PE machine types. The existing package-side `pynavlib` exclusion is already correct and is not evidence that the rest of the native dependency graph is clean.

## Findings

### RISK-ARCH-001 — x64 CRT DLLs are forced into the Arm payload

- **Status/severity:** confirmed defect — **critical**
- **Location/evidence:** `cura-workflows\.github\workflows\cura-installer-windows-arm.yml:106-115`; line 109 selects `x64/Microsoft.VC*.CRT` before copying six DLLs into `dist\UltiMaker-Cura`.
- **Observed:** an Arm64 process is placed beside x64 CRT DLLs with loader-preferred names.
- **Expected:** the bundled CRT files must be Arm64 and selected from the actual installed VS instance/toolset.
- **Required correction:** locate VS with `vswhere`, select an explicit/latest supported MSVC redist directory, use `arm64\Microsoft.VC*.CRT`, fail on missing/ambiguous files, and verify every copied DLL has PE machine `0xAA64`.
- **Reproduction:** `rg -n "MSDIR=|MSDIR_DLLS=" cura-workflows\.github\workflows\cura-installer-windows-arm.yml`.

### RISK-ARCH-002 — a committed x64 `python3.dll` is also copied into every Arm payload

- **Status/severity:** confirmed defect — **critical**
- **Location/evidence:** `cura-installer-windows-arm.yml:119` copies `cura-workflows\python_dll_workaround\python3.dll`; its PE machine is `0x8664` (AMD64), size 56,320 bytes.
- **Observed:** the workflow fixes libraries linked to `python3.dll` by injecting an ABI-incompatible x64 forwarding DLL.
- **Expected:** use the Arm64 Python runtime's `python3.dll`, an Arm64-built equivalent, or prove the workaround is unnecessary and remove it for Arm.
- **Required correction:** make the workaround architecture-aware and add a regression assertion for `python3.dll` machine type. Do not merely allowlist it: it is an in-process DLL.
- **Reproduction:**
  `python -c "import struct,pathlib; p=pathlib.Path(r'cura-workflows\python_dll_workaround\python3.dll'); b=p.read_bytes(); o=struct.unpack_from('<I',b,0x3c)[0]; print(hex(struct.unpack_from('<H',b,o+4)[0]))"`
  currently prints `0x8664`; Arm64 is `0xaa64`.

### RISK-PACKAGE-003 — the Arm workflow creates an MSI explicitly marked x64

- **Status/severity:** confirmed defect — **high**
- **Location/evidence:** the Arm workflow calls `Cura\packaging\msi\create_windows_msi.py` at `cura-installer-windows-arm.yml:146`; `create_windows_msi.py:108` hardcodes `"-arch", "x64"`.
- **Observed:** an ARM64-named MSI is authored as an x64 Windows Installer database.
- **Expected:** an Arm package must carry `Arm64` platform metadata; Microsoft documents the MSI Template Summary as the compatibility gate and requires `Arm64` for 64-bit Arm packages.
- **Required correction:** add an architecture argument to the MSI builder, preserve x64 as the x64 caller's explicit/default value, pass Arm64 from the Arm workflow, and inspect the produced MSI Template Summary. If the installed WiX version cannot author Arm64, disable the Arm MSI rather than publish a mislabeled one.
- **Evidence:** `rg -n 'create_windows_msi|"-arch", "x64"' cura-workflows\.github\workflows\cura-installer-windows-arm.yml Cura\packaging\msi\create_windows_msi.py`; reference: <https://learn.microsoft.com/windows/win32/msi/template-summary>.

### RISK-VALIDATION-004 — installer-tool failures can produce a green job

- **Status/severity:** confirmed defect — **high**
- **Location/evidence:** `create_windows_installer.py:88` runs `makensis` without `check=True`; `create_windows_msi.py:105,114,125` ignores `heat`, `candle`, and `light` return codes. Arm artifact uploads at workflow lines `136,151,159,167` omit `if-no-files-found`, whose `upload-artifact@v7` default is `warn`.
- **Observed:** a tool that starts but exits nonzero does not fail the Python script; a missing output can then yield only an upload warning.
- **Expected:** any packaging failure or missing expected file must fail the job.
- **Required correction:** use `subprocess.run(..., check=True)` for every packaging command, assert outputs exist and are non-empty, and set `if-no-files-found: error` on required artifacts. Apply this without regressing x64 callers.
- **Evidence:** `rg -n "subprocess\\.(run|call)|upload-artifact" Cura\packaging cura-workflows\.github\workflows\cura-installer-windows-arm.yml`; action default: <https://github.com/actions/upload-artifact/blob/v7/README.md#inputs>.

### RISK-RUNNER-005 — current hosted-Arm runner assumptions are not executable as written

- **Status/severity:** confirmed mismatch plus CI-gated claim — **high**
- **Location/evidence:** `runner_scripts\make_runners_list.py:15` emits `windows-latest-arm64`, which is not an official GitHub-hosted label. The Arm dispatcher only offers `self-hosted-Windows-ARM64` (`Cura\.github\workflows\windows-arm.yml:33-36`), and the aggregate workflow hardcodes that self-hosted label (`cura-installers.yml:97`).
- **Observed:** package and installer runner paths are inconsistent, and generated prose treats retargeting as a one-line proven substitution.
- **Expected:** use a currently supported label and make package/installer dispatch explicit and testable.
- **Required correction:** replace the package label with an official current label (`windows-11-arm` for the current VS2022 image or `windows-11-vs2026-arm` for explicit VS2026 testing), expose the selected label deliberately, and prove one queued/completed run. Do not claim CI availability until that run exists.
- **External evidence (2026-08-27):** <https://github.blog/changelog/2026-08-20-windows-11-arm64-vs2026-image-generally-available/> and the official image manifests in `actions/runner-images`.

### RISK-RUNNER-006 — the Arm workflow is tied to one self-hosted VS layout and likely lacks hosted MSI tools

- **Status/severity:** confirmed path defect; WiX availability is **unverified** — **high**
- **Location/evidence:** `cura-installer-windows-arm.yml:106` hardcodes `C:\Program Files\Microsoft Visual Studio\2022\Community`. The current official `windows-11-arm` manifest reports VS 2022 **Enterprise** at `...\2022\Enterprise`; the new VS2026 image uses `C:\Program Files\Microsoft Visual Studio\18\Enterprise`. Both list NSIS, but the manifests have no WiX/`heat`/`candle`/`light` entry.
- **Observed:** simply switching `runs-on` will fail CRT discovery; MSI tool availability has not been established.
- **Expected:** discover tools by capability, not edition/version path.
- **Required correction:** use `vswhere`, print resolved tool/redist versions, and add a preflight for `python`, `conan`, `pyinstaller`, `makensis`, `signtool`, `heat`, `candle`, and `light`. Install an already-approved WiX dependency only if absent, or move sign/package work to a prepared secure runner.
- **CI gate:** on the chosen hosted label, capture `runner.arch`, `platform.machine()`, `vswhere`, and `Get-Command` results before accepting hosted-runner feasibility.

### RISK-SIGN-007 — x64 signing cannot be copied to Arm without a credential/topology decision

- **Status/severity:** confirmed external dependency — **high**
- **Location/evidence:** x64 signing at `cura-installer-windows.yml:113-114,156,177` requires local `C:\actions-runner\code_sign.cer`, the `eToken Base Cryptographic Provider`, and secret `WIN_TOKEN_CONTAINER`. No evidence establishes those on the Arm runner. The Arm workflow's `WIN_CERT_INSTALLER_CER*` environment values are unused.
- **Observed:** there is no Arm signing; a hosted runner cannot access Ultimaker's physical token. A self-signed PFX exercises different `/f /p` semantics and trust, so it is demo signing, not production parity.
- **Expected:** internal `CuraEngine.exe` and `UltiMaker-Cura.exe`, then final EXE/MSI, must be signed and verified under an explicitly defined production or demo trust model.
- **Required correction:** choose and document either (a) provision/attest the token/provider on the Arm self-hosted runner, or (b) transfer the unsigned Arm payload to the existing secure x64 signing runner, sign the Arm binaries there, package, then sign installers. Keep demo self-signing isolated and clearly non-production.
- **Secrets gate:** production parity requires maintainer evidence that the certificate path, CSP, token container, timestamp endpoint, and secret are available; verify with `signtool verify /pa /all /v` after packaging.

### RISK-PROVENANCE-008 — a fork proof can silently execute upstream helpers instead of changed code

- **Status/severity:** confirmed design trap — **high**
- **Location/evidence:** the Arm workflow invokes both composite actions from `ultimaker/cura-workflows@main` (`:65,:76`). `setup-build-environment/action.yml:87-89` then checks out `Ultimaker/Cura-workflows` at its input ref, default `main`, and later steps run scripts from that checkout.
- **Observed:** repointing Cura to a forked reusable workflow tests inline workflow edits, but fork changes to setup actions, helper scripts, or the committed DLL are ignored unless every reference/checkout is aligned.
- **Expected:** a proof run must identify one immutable repository+SHA for every changed workflow/action/script.
- **Required correction:** produce a provenance map from the Actions run, pin proof references to SHAs, and explicitly repoint all changed cross-repository action/checkouts for the fork test. Revert/isolate fork-only references before an upstream PR.
- **Evidence:** `rg -n "uses: ultimaker/cura-workflows|repository: Ultimaker/Cura-workflows|cura_workflows_branch" cura-workflows\.github`.

### RISK-ARCH-009 — architecture is a label, not an enforced invariant

- **Status/severity:** confirmed validation gap — **high**
- **Location/evidence:** `prepare_installer.py` uses `--architecture ARM64` only to construct filenames; the reusable workflow accepts any string for `operating_system` and has no early `runner.arch == ARM64` assertion. No payload PE scan exists.
- **Observed:** a misrouted x64 runner can create ARM64-named artifacts, and checking only the CRT source folder would miss the x64 `python3.dll`, x64 `.pyd`/Qt DLLs, or x64 subprocesses.
- **Expected:** build host, Python, main binaries, in-process DLL/PYD closure, subprocesses, CRT, and MSI metadata must be verified.
- **Required correction:** fail early unless Windows/ARM64/Python ARM64; after cleanup and before signing, scan every `.exe`, `.dll`, and `.pyd` PE COFF machine value. Default to ARM64-only for in-process modules; maintain a narrowly justified allowlist for emulated standalone tools/installer stubs. Validate `UltiMaker-Cura.exe`, `CuraEngine.exe`, Qt/Python extensions, CRT, `python3.dll`, MSI Template Summary, and Authenticode explicitly.
- **Hardware gate:** only a physical/VM Windows Arm run can close install, launch, model load, slice, CuraEngine subprocess, and uninstall behavior.

### RISK-RELEASE-010 — the release-candidate publisher omits Windows Arm artifacts

- **Status/severity:** confirmed scope defect — **high** for stable promotion
- **Location/evidence:** `Cura\.github\workflows\release-process_release-candidate.yml:181-182` uploads only `win64-X64.exe` and `.msi`; no Windows Arm asset is selected, although `cura-installers.yml` builds an Arm job. Nightly upload is wildcard-based, so this defect is specific to the formal release-draft path.
- **Observed:** fixing/building Arm does not make it part of an official release candidate.
- **Expected:** stable-promotion design must state whether Arm is alpha-only or publish it intentionally.
- **Required correction:** after architecture/signing/run gates pass, add the validated Arm artifact names to release upload and test the draft path; otherwise explicitly keep Arm excluded and do not claim stable promotion.
- **Evidence:** `rg -n "gh release upload|win64" Cura\.github\workflows\release-process_release-candidate.yml`.

### RISK-SCOPE-011 — generated Cura-side package/G-code work is partly duplicate or unrelated

- **Status/severity:** confirmed scope hazard — **medium**
- **Evidence:** `Cura\conanfile.py:607-609` already excludes `pynavlib` on Windows Arm64; `plugins\3DConnexion\__init__.py` catches load failure. No evidence connects G-code golden tests to CRT, signing, PE architecture, or installer authoring.
- **Required correction:** do not modify `pynavlib` gating or G-code behavior without a failing Arm-specific test. Cura-side changes should be limited to necessary architecture-aware packaging (notably MSI/error propagation) and test dispatch/provenance.

## Required acceptance gates

1. **Static/local:** PE scan catches the current `0x8664` `python3.dll`; MSI builder is architecture-parameterized; packaging commands propagate failure; required uploads fail when absent.
2. **Hosted CI:** one run on an official Arm label proves tool discovery, ARM64 Python, Conan/PyInstaller completion, EXE and (if supported) MSI creation, and publishes digests plus the architecture manifest.
3. **Dependency/ABI:** zero unapproved x64 in-process PE files; each intentionally emulated standalone binary is documented and exercised.
4. **Demo signing:** ephemeral self-signed cert only, verified under an explicitly temporary trust setup; no claim of vendor trust.
5. **Production signing:** maintainer-controlled token/CSP/secret execution signs and verifies both internal binaries and final installers; otherwise production signing remains open.
6. **Windows Arm execution:** install EXE and MSI (if retained), launch Cura, load a representative model, slice through CuraEngine, restart, and uninstall on real Windows Arm hardware/VM. Record OS/build/device and logs.
7. **Upstream/fork:** run metadata proves all changed workflow/action/script SHAs; fork-only runner/certificate references are absent from the upstreamable diff.
8. **Release:** release-draft behavior explicitly includes validated Arm assets or declares them non-stable/out of scope.

## Confidence

**confidence: high** — direct current-source and history inspection confirms multiple independent x64 leaks and packaging/provenance defects, while secrets-backed signing, hosted CI completion, and physical Windows Arm execution are correctly retained as external gates.
