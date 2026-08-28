# Arm quality fix workspace summary

Clones captured in this workspace:
- `Cura` @ `5068661cd448b954328483a499fe4ff419b695b5`
- `cura-workflows` @ `126f92d186e62a8c2f50ed1883c37a81e1d929de`

Baseline:
- `conandata.yml` and `resources/conandata.yml` already carry `5.14.0-alpha.0`.
- No repository-local instruction file was present in either clone.
- This workspace is documentation-only; no product code was changed.

What the fix spans:
- Cura-side package architecture, `pynavlib`, and G-code validation.
- cura-workflows-side ARM installer parity, CRT selection, signing parity, and runner design.
- Two coordinated PRs, then stable-promotion handoff.

See the companion docs:
- `02-cura-package-audit.md`
- `03-cura-workflows-audit.md`
- `04-prs-validation-handoff.md`
