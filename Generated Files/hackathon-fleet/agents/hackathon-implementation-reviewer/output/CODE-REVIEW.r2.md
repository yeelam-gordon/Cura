# CODE-REVIEW r2

## Integrity and scope

- Verified and read `CODE-REVIEW.r1.md`: `7E6090957FC9684CC04A2853877504712D803FEB83760F48BA1C4C70FBA3BC35`.
- Verified and read `IMPLEMENT.r2.md`: `D3F774353A121893DF9EEB0CEC699D7EC724A754C6663F6C6AF0D2AAE6DC042C`.
- Re-read the approved composite: `DESIGN.r3.md` = `8F6EB544288CC1A18523184F583494D24F7232C58DD9B73984C8D4C3089225AC`; `DESIGN-REVIEW.r3.md` = `C43ADD6BA9899DE1AFD99BB62DA7AC282462E608FB840C7E3065FA33F3DAB8C0`.
- Baselines remain Cura `5068661cd448b954328483a499fe4ff419b695b5` and cura-workflows `126f92d186e62a8c2f50ed1883c37a81e1d929de`.
- Inspected every tracked and untracked implementation/test file in the current two-repository diff.

## Finding

### HIR-REGRESSION-004 — Linux and Wasm matrix jobs collide on the new provenance artifact

- **Severity:** medium
- **Location:** `cura-workflows/runner_scripts/make_runners_list.py:8-17`; `cura-workflows/.github/workflows/conan-package.yml:253-259`
- **Observed behavior:** Enabling Linux and Wasm creates two distinct matrix jobs whose `matrix.runner` is `ubuntu-latest`, but both upload `package-provenance-create-${run_id}-${run_attempt}-ubuntu-latest`. `actions/upload-artifact@v7` rejects the second upload because artifact names are run-scoped and immutable.
- **Expected behavior:** Every supported matrix combination must use a unique provenance artifact name.
- **Reproduction:** `python runner_scripts\make_runners_list.py --platform-linux --platform-wasm` returned two `ubuntu-latest` entries with different Conan arguments; the upload name includes only `matrix.runner`.
- **Required correction:** Add a stable unique matrix/platform identifier to the artifact name, or limit this provenance upload to the single-platform proof path.

## Prior-finding disposition

| Finding | Disposition | Reproduction/evidence |
|---|---|---|
| `HIR-PROV-001` | **CLOSED in implementation; exact-SHA CI remains an external gate.** | The runtime uses `job.workflow_ref`/`job.workflow_sha`, validates exact component paths and literal `W`, enforces one-parent `V` with exactly both callers, and binds package reference/run identity to `C/V/W`. Tests reject arbitrary paths, mutable callers, wrong invocation refs, and package-chain mismatches. |
| `HIR-WORKFLOW-002` | **CLOSED.** | X64 and Arm64 application/engine artifact names are architecture-qualified; the literal upload-name intersection is empty. |
| `HIR-BOUNDARY-003` | **CLOSED.** | Signed installers are included in `signed-contract.json`; hosted smoke verifies downloaded filenames, sizes, and SHA-256 values against contract-bound release evidence. Exact-file and substituted-file tests pass. |

## Approved-design compliance map

| Area | Status |
|---|---|
| Input hashes and source baselines | COMPLIES |
| Strict PE validation and required Arm/X64 paths | COMPLIES |
| MSI/NSIS checked subprocesses and non-empty outputs | COMPLIES |
| Cura packaging tests | COMPLIES |
| Literal-SHA workflow/action/helper plumbing | COMPLIES statically |
| Single immutable `C/V/W` caller and package binding | COMPLIES statically; exact-SHA CI gate pending |
| Native Arm host/Python, CRT, and `python3.dll` gates | COMPLIES statically; native runner gate pending |
| Canonical unsigned artifact boundary | COMPLIES |
| Secure signing preflight, signatures, and Arm64 MSI validation | COMPLIES statically; secure-runner gate pending |
| Signed artifact/smoke identity | COMPLIES — `HIR-BOUNDARY-003` closed |
| X64/Arm64 installer artifact uniqueness | COMPLIES — `HIR-WORKFLOW-002` closed |
| General package matrix regression safety | REVISE — `HIR-REGRESSION-004` |
| Hosted Arm smoke, physical acceptance, and stable publication | EXTERNAL NO-GO gates retained |

## Local validation

- Cura packaging tests: `17 passed`.
- Workflow provenance/contract tests: `20 passed`.
- All eight changed YAML files parsed.
- Arm runner output: `windows-11-arm`.
- Both repository diffs passed `git diff --check`.
- Linux+Wasm duplicate-runner artifact collision reproduced statically.

## Verdict

**REVISE**

**confidence: high**

**Justification:** Complete diff inspection and passing targeted tests close all three prior findings, but a deterministic supported matrix combination still fails because two jobs upload the same immutable provenance artifact name.
