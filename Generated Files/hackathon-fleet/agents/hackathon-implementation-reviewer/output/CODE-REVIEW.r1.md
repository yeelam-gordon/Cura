# CODE-REVIEW r1

## Integrity and scope

- All three assigned SHA-256 values matched.
- Baselines matched: Cura `5068661cd448b954328483a499fe4ff419b695b5`; cura-workflows `126f92d186e62a8c2f50ed1883c37a81e1d929de`.
- Reviewed every tracked implementation diff and every untracked implementation addition listed in `IMPLEMENT.r1.md`, plus the unchanged Cura caller workflows needed to evaluate runtime integration.

## Findings

### HIR-PROV-001 — exact-SHA proof can report `W` without executing workflows from `W`

- **Severity:** high
- **Location:** `cura-workflows/.github/workflows/conan-package.yml:178,192-217`; `cura-workflows/.github/workflows/cura-installer-windows-arm.yml:107-130,218-242`; `cura-workflows/runner_scripts/workflow_provenance.py:29-85`
- **Observed behavior:** Workflow evidence assigns the SHA of `_cura_workflows_action` to reusable-workflow rows; the aggregate validator trusts that self-reported SHA and does not validate `component_path`. The package-side `V` check validates only the two changed filenames, while the installer merely treats a nonconforming caller as `C == V` instead of failing. Consequently, callers may execute `@main`, pass literal `W`, and still produce all-PASS rows claiming the workflows ran from `W`.
- **Expected behavior:** Proof must attest the actual reusable/nested workflow revision and enforce one unchanged `V`, based directly on `C`, containing the two corrected callers for both runs.
- **Evidence/reproduction:** No workflow compares its executed call target to `W`; `github.workflow_ref` is only recorded as metadata. The validator test intentionally accepts arbitrary `component_path` values.
- **Required correction:** Validate both caller files' exact `@W` targets and inputs, fail the installer unless `C..V` is exactly the two approved callers, bind the installer to the package run/reference and same `C/V/W`, and derive workflow rows from verifiable invocation provenance rather than an unrelated action checkout.

### HIR-WORKFLOW-002 — X64 and Arm jobs publish duplicate artifact names in one run

- **Severity:** high
- **Location:** `cura-workflows/.github/workflows/cura-installers.yml:38-40,92-94`; `cura-workflows/.github/workflows/cura-installer-windows.yml:228-242`; `cura-workflows/.github/workflows/cura-installer-windows-arm.yml:589-605`
- **Observed behavior:** The orchestrator runs both Windows workflows, and both upload artifacts named `UltiMaker-Cura.exe` and `CuraEngine.exe`. Artifact names are run-scoped and immutable for the used upload-artifact generation, so the later uploads conflict.
- **Expected behavior:** All required artifacts from the combined installer workflow must upload successfully and remain architecture-unambiguous.
- **Evidence/reproduction:** Static intersection of the two workflows' literal artifact names returns both `UltiMaker-Cura.exe` and `CuraEngine.exe`.
- **Required correction:** Use architecture-qualified artifact names and update all consumers/evidence, or otherwise ensure only one producer owns each run-scoped name.

### HIR-BOUNDARY-003 — downloaded installers are not checked against signed-contract evidence

- **Severity:** medium
- **Location:** `cura-workflows/.github/workflows/cura-installer-windows-arm.yml:533-547,573-587,671-692`
- **Observed behavior:** Final EXE/MSI hashes are placed in contract-covered `release-evidence.json`, but the installers are uploaded separately and the smoke job never compares their size/hash to that evidence; it checks only signatures and MSI structure.
- **Expected behavior:** The smoke-tested installers must be cryptographically identified as the exact outputs recorded by the signing job.
- **Evidence/reproduction:** The signed contract includes evidence but not the installer files, and the smoke path never reads `release-evidence.json` or hashes `installers\*.exe`/`*.msi`.
- **Required correction:** Include the final installers in the signed contract artifact, or verify each downloaded installer's filename, size, and SHA-256 against contract-bound release evidence before signature/MSI checks.

## Approved-design compliance map

| Area | Status |
|---|---|
| Input hashes and source baselines | COMPLIES |
| Strict PE validator and required paths | COMPLIES |
| MSI/NSIS checked subprocesses and non-empty outputs | COMPLIES |
| Cura packaging tests | COMPLIES |
| Literal-SHA action/helper plumbing | PARTIAL — HIR-PROV-001 |
| Binding single-`V` correction and workflow invocation proof | REVISE — HIR-PROV-001 |
| Native Arm host/Python, CRT, and `python3.dll` gates | COMPLIES statically; native CI gate remains |
| Unsigned canonical artifact boundary | COMPLIES |
| Secure signing preflight, signatures, and Arm64 MSI checks | COMPLIES statically; secure-runner gate remains |
| Signed artifact/smoke identity | PARTIAL — HIR-BOUNDARY-003 |
| X64 regression safeguards | COMPLIES statically |
| Combined installer orchestration | REVISE — HIR-WORKFLOW-002 |
| Physical Arm acceptance and stable publication | EXTERNAL NO-GO gate retained |

## Local validation

- Cura packaging tests: `17 passed`.
- Workflow contract/provenance tests: `12 passed`.
- Changed YAML files: all 8 parsed.
- Arm runner output: `windows-11-arm`.
- Both repository diffs passed `git diff --check`.
- Hosted Arm, secure signing, exact-SHA GitHub Actions, and physical hardware remain external gates.

## Verdict

**REVISE**

**confidence: high**

**Justification:** Complete file inspection and passing local tests establish the implemented mechanics, while two deterministic high-severity workflow/provenance defects prevent trustworthy successful acceptance.
