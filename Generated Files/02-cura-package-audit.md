# Cura package audit

Observed package facts:
- `conandata.yml:1` and `resources/conandata.yml:1` ship `5.14.0-alpha.0`.
- `conandata.yml:126` marks `pynavlib` as a collect-all dependency.
- `conandata.yml:630-640` documents `pynavlib` as Windows x64 only, not ARM64.
- `conanfile.py:114` maps Windows ARM64 PyInstaller output to `arm64`.
- `conanfile.py:607-609` removes `pynavlib` on ARM64 Windows because no ARM64 wheels exist.
- `plugins/3DConnexion/NavlibClient.py:16,19,22` imports and subclasses `pynavlib`, so the package gate matters.
- Current G-code validation surfaces are `tests/TestGCodeListDecorator.py`, `tests/TestPrintInformation.py`, and `scripts/check_gcode_buffer.py`; no dedicated golden-test harness was found.

Package-architecture takeaway:
- Cura already has the right shape for an ARM64 package split; the remaining work is to keep architecture-sensitive dependencies and validation aligned with that split.

Cura files in scope:
- `conandata.yml`
- `resources/conandata.yml`
- `conanfile.py`
- `plugins/3DConnexion/NavlibClient.py`
- `plugins/3DConnexion/plugin.json`
- `plugins/3DConnexion/__init__.py`
- `tests/TestGCodeListDecorator.py`
- `tests/TestPrintInformation.py`
- `scripts/check_gcode_buffer.py`
- `packaging/NSIS/create_windows_installer.py`
- `packaging/msi/create_windows_msi.py`
