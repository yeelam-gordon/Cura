# cura-workflows audit

Observed workflow facts:
- `cura-installer-windows.yml:2,33-37` defaults to `self-hosted-Windows-X64`.
- `cura-installer-windows.yml:113-177` signs the internal EXE plus the final EXE/MSI installers.
- `cura-installer-windows.yml:126` copies CRT DLLs from `x64/Microsoft.VC*.CRT`.
- `cura-installer-windows-arm.yml:2,40,59,100` targets `self-hosted-Windows-ARM64` and builds ARM64 installers.
- `cura-installer-windows-arm.yml:109` still copies CRT DLLs from `x64/Microsoft.VC*.CRT`, which is the x64 CRT leakage.
- `cura-installer-windows-arm.yml` has no `signtool` step, so signing parity is missing versus x64.
- `cura-installers.yml:43,97` explicitly splits self-hosted Windows X64 and ARM64 installer jobs.
- `conan-package.yml:41,102,108` threads `platform_windows_arm64` through a matrix and then runs on `matrix.runner`.
- `make-runners-list.yml:18,52-53` and `runner_scripts/make_runners_list.py` add a hosted `windows-latest-arm64` runner option, so package build can stay hosted while installers stay self-hosted.

Fork-repointing inventory (`ultimaker/cura-workflows` references):
- `benchmark.yml`
- `conan-package.yml`
- `conan-recipe-version.yml`
- `conan-recipe-export.yml`
- `cura-installer-linux.yml`
- `cura-installer-macos.yml`
- `cura-installer-windows-arm.yml`
- `cura-installer-windows.yml`
- `extract-ticket-and-find-packages.yml`
- `find-package-by-ticket.yml`
- `lint-formatter.yml`
- `lint-tidier.yml`
- `npm-package.yml`
- `unit-test.yml`
- `update-translation.yml`

cura-workflows files in scope:
- `.github/workflows/cura-installer-windows.yml`
- `.github/workflows/cura-installer-windows-arm.yml`
- `.github/workflows/cura-installers.yml`
- `.github/workflows/conan-package.yml`
- `.github/workflows/make-runners-list.yml`
- `runner_scripts/make_runners_list.py`
- `runner_scripts/prepare_installer.py`
- `runner_scripts/cleanup_distribution.py`
