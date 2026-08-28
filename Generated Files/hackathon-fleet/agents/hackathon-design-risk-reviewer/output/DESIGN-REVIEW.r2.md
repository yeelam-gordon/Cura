# DESIGN-REVIEW r2

## Record integrity and verdict

- `DESIGN.r2.md` SHA-256 verified: `ADD584856B897BAB3220F44250C3ECCA29F16EA902D5B946CD39E8DEC8344652`.
- `DESIGN-REVIEW.r1.md` SHA-256 verified: `81299A1C2AAE618C28A427CD706A0FFA7C4EF1EAF49081765698E671097A473F`.
- `RISK.r1.md` SHA-256 verified: `F17BE2EB662C80E089B529F002AEE70C77A6F5CE3F161002F4593CD89E4BA5EB`.
- Tracked source is unchanged at Cura `5068661cd448b954328483a499fe4ff419b695b5` and cura-workflows `126f92d186e62a8c2f50ed1883c37a81e1d929de`.

**verdict: REVISE**

r2 closes the critical architecture defect and four of the five prior review findings, but its exact-SHA package proof still executes mutable `main` copies of an action changed by the design. Stable promotion remains **NO-GO** until production signing, both physical Windows Arm installer tests, and separate maintainer release approval pass.

## Remaining critical/high finding

### DR-PROVENANCE-006 — nested package jobs still execute the changed setup action from `main`

- **Maps to:** `DR-PROVENANCE-002`, `RISK-PROVENANCE-008`
- **Design location:** “PR 2 / Provenance plumbing / `.github\workflows\conan-package.yml`” localizes setup only in `conan-package-create`, while “Exact-SHA pre-merge proof” claims the setup composite action resolves to `W`.
- **Source evidence:** `conan-package.yml:63-85` invokes `conan-recipe-version.yml` and `conan-recipe-export.yml`; those workflows invoke `setup-build-environment@main` at `conan-recipe-version.yml:81` and `conan-recipe-export.yml:55`, and recipe export invokes `upload-conan-package@main` at line 71.
- **Observed gap:** a package proof called at immutable `W` still runs mutable action definitions during versioning/export, so its asserted one-SHA provenance map is false and a concurrent `main` change can alter the produced/uploaded reference.
- **Severity:** **high**
- **Exact correction:** add and pass `cura_workflows_ref` through both nested workflows; in each job check out `_cura_workflows_action` at that ref, invoke setup and upload actions by local path, pass the same ref to setup's helper checkout, assert every resolved checkout equals literal `W`, and record every invocation in the proof summary.

No critical finding remains open.

## Five `DESIGN-REVIEW.r1` finding dispositions

| Finding | Final disposition |
|---|---|
| `DR-ARCH-001` | **Accepted; closed in design.** Native `<sys.base_prefix>\python3.dll` is required, machine/hash checked, and the committed AMD64 DLL is prohibited. |
| `DR-PROVENANCE-002` | **Accepted; PARTIAL/OPEN high.** Installer and Arm package-create paths are pinned, but nested package version/export jobs remain on mutable `main`; see `DR-PROVENANCE-006`. |
| `DR-BOUNDARY-003` | **Accepted; closed in design.** Canonical metadata/file contracts, clean-workspace verification, fresh venv setup, and complete tool/provider preflight are explicit. |
| `DR-VALIDATION-004` | **Accepted; closed in design.** Tool failures, missing/empty outputs, and required uploads all hard-fail; success artifacts no longer use `always()`. |
| `DR-ARCH-005` | **Accepted; closed in design.** Windows/ARM64 runner, environment, and Python checks occur before setup, Conan, or PyInstaller and are recorded. |

## Original critical/high risk dispositions

| Risk ID | Final disposition |
|---|---|
| `RISK-ARCH-001` | **Accepted; closed in design.** Arm64 CRT discovery, named-file checks, hashes, and PE validation are specified. |
| `RISK-ARCH-002` | **Accepted; closed in design.** The AMD64 workaround DLL is forbidden and native Arm64 `python3.dll` is mandatory. |
| `RISK-PACKAGE-003` | **Accepted; closed in design.** MSI architecture is parameterized and Arm64 summary/component metadata is gated. |
| `RISK-VALIDATION-004` | **Accepted; closed in design.** Subprocess, output, and artifact-upload false-green paths are eliminated. |
| `RISK-RUNNER-005` | **Accepted; design-corrected with CI gate.** `windows-11-arm`, explicit Arm selection, and a completed exact-SHA package run are required. |
| `RISK-RUNNER-006` | **Accepted; design-corrected with external gate.** VS discovery is version-independent and X64 packaging preflights WiX/NSIS/signing capabilities. |
| `RISK-SIGN-007` | **Accepted; design-corrected with external gate.** Secure X64 cross-signing, internal-before-container signing, verification, and credential ownership are explicit. |
| `RISK-PROVENANCE-008` | **Accepted; OPEN high.** Nested package jobs remain mutable; see `DR-PROVENANCE-006`. |
| `RISK-ARCH-009` | **Accepted; closed in design.** Early host checks, strict all-PE manifests, MSI checks, and hosted Arm execution enforce architecture. |
| `RISK-RELEASE-010` | **Accepted; bounded closed for this scope.** Arm stays outside stable publication pending physical acceptance and a separate maintainer decision. |

## Convergence boundary

After `DR-PROVENANCE-006` is corrected, the design is specific enough for implementation without redesign and retains explicit production-signing, hosted/physical Arm, X64-regression, and stable-publication gates.

**confidence: high**

**Justification:** verified immutable records and unchanged source directly show that all critical defects are designed closed while the two nested `@main` action calls leave one reproducible high-severity provenance gap.
