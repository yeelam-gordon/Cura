# PR plan and stable handoff

Two coordinated PRs:
1. **Cura PR** — keep package-architecture fixes, `pynavlib` gating, and any Cura-side workflow repointing together.
2. **cura-workflows PR** — fix ARM installer parity, CRT selection, signing parity, and the runner matrix in one pass.

Validation notes:
- There is no dedicated G-code golden-test harness in this clone.
- Use the current anchors (`tests/TestGCodeListDecorator.py`, `tests/TestPrintInformation.py`, `scripts/check_gcode_buffer.py`) plus any new golden fixtures before promotion.
- Verify both Windows X64 and Windows ARM64 installer paths separately.

Stable-promotion handoff:
- `nightly-stable.yml` is the stable-release entry point.
- It forwards to `nightly.yml` with `release_tag: "nightly-stable"` and `caller_workflow: "nightly-stable.yml"`.
- `nightly.yml` then calls `ultimaker/cura-workflows/.github/workflows/cura-installers.yml@main` and uploads the release artifacts.
- Promotion should wait until both PRs are green and the ARM64 installer artifacts match the intended signing/CRT behavior.

Combined file inventory:

**Cura**
- `conandata.yml`
- `resources/conandata.yml`
- `conanfile.py`
- `plugins/3DConnexion/NavlibClient.py`
- `plugins/3DConnexion/plugin.json`
- `plugins/3DConnexion/__init__.py`
- `tests/TestGCodeListDecorator.py`
- `tests/TestPrintInformation.py`
- `scripts/check_gcode_buffer.py`
- `.github/workflows/conan-package-resources.yml`
- `.github/workflows/conan-package.yml`
- `.github/workflows/find-packages.yml`
- `.github/workflows/installers.yml`
- `.github/workflows/linux.yml`
- `.github/workflows/macos.yml`
- `.github/workflows/nightly.yml`
- `.github/workflows/nightly-stable.yml`
- `.github/workflows/nightly-testing.yml`
- `.github/workflows/printer-linter-format.yml`
- `.github/workflows/printer-linter-pr-diagnose.yml`
- `.github/workflows/process-pull-request.yml`
- `.github/workflows/release-process_release-candidate.yml`
- `.github/workflows/unit-test-post.yml`
- `.github/workflows/unit-test.yml`
- `.github/workflows/update-translation.yml`
- `.github/workflows/windows-arm.yml`
- `.github/workflows/windows.yml`
- `packaging/NSIS/create_windows_installer.py`
- `packaging/msi/create_windows_msi.py`

**cura-workflows**
- `.github/workflows/benchmark.yml`
- `.github/workflows/conan-package.yml`
- `.github/workflows/conan-recipe-version.yml`
- `.github/workflows/conan-recipe-export.yml`
- `.github/workflows/cura-installer-linux.yml`
- `.github/workflows/cura-installer-macos.yml`
- `.github/workflows/cura-installer-windows-arm.yml`
- `.github/workflows/cura-installer-windows.yml`
- `.github/workflows/cura-installers.yml`
- `.github/workflows/extract-ticket-and-find-packages.yml`
- `.github/workflows/find-package-by-ticket.yml`
- `.github/workflows/lint-formatter.yml`
- `.github/workflows/lint-tidier.yml`
- `.github/workflows/make-runners-list.yml`
- `.github/workflows/npm-package.yml`
- `.github/workflows/unit-test.yml`
- `.github/workflows/update-translation.yml`
- `runner_scripts/cleanup_distribution.py`
- `runner_scripts/make_runners_list.py`
- `runner_scripts/prepare_installer.py`
