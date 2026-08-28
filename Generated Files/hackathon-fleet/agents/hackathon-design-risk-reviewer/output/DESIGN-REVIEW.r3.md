# DESIGN-REVIEW r3

## Record integrity

- `DESIGN.r3.md` SHA-256 verified: `8F6EB544288CC1A18523184F583494D24F7232C58DD9B73984C8D4C3089225AC`.
- `DESIGN-REVIEW.r2.md` SHA-256 verified: `88F44626AD605653607AF13A02AE28421DCC61C7EA6DEE294D13D825F758C43D`.
- Both immutable records were read verbatim.

## Verdict

**verdict: REVISE**

r3 closes `DR-PROVENANCE-006` and retains every accepted r2 architecture, boundary, validation, signing, hardware, regression, and publication gate, but its ordered exact-SHA proof cannot produce the single immutable validation commit `V` that the evidence contract requires.

## Critical/high disposition

### r2 review findings

| Finding | Final disposition |
|---|---|
| `DR-ARCH-001` | **Accepted; closed in design.** Native `<sys.base_prefix>\python3.dll` remains mandatory, with source/destination Arm64 machine and hash checks and no workaround fallback. |
| `DR-PROVENANCE-002` | **Accepted; closed in design except for the new `V` identity defect below.** Literal `W` is propagated through package, installer, nested workflow, action, helper, override, and script boundaries with invocation-level proof. |
| `DR-BOUNDARY-003` | **Accepted; closed in design.** Canonical contracts, clean transfer verification, fresh packaging environment, and complete signing/tool preflight remain required. |
| `DR-VALIDATION-004` | **Accepted; closed in design.** Tool errors, absent or empty outputs, contract failures, and required upload failures remain hard failures. |
| `DR-ARCH-005` | **Accepted; closed in design.** Native Windows Arm64 host, environment, and Python checks remain first functional gates. |
| `DR-PROVENANCE-006` | **Accepted; closed in design.** Both recipe workflows receive `cura_workflows_ref`, execute setup/upload actions from the asserted local checkout at `W`, pin helper checkouts to `W`, prohibit nested `@main`, and emit distinct workflow/action/helper proof rows. |

### Original critical/high risks

| Risk ID | Final disposition |
|---|---|
| `RISK-ARCH-001` | **Closed in design.** Arm64 CRT discovery, named-file validation, hashes, and PE checks remain explicit. |
| `RISK-ARCH-002` | **Closed in design.** Native Arm64 `python3.dll` is required and the AMD64 workaround is prohibited. |
| `RISK-PACKAGE-003` | **Closed in design.** Arm64 MSI authoring and SummaryInformation/component-table validation remain mandatory. |
| `RISK-VALIDATION-004` | **Closed in design.** Packaging subprocesses, outputs, contracts, and uploads fail closed. |
| `RISK-RUNNER-005` | **Closed in design with CI gate.** Native build identity and hosted `windows-11-arm` smoke execution remain required. |
| `RISK-RUNNER-006` | **Closed in design with external gate.** Version-independent VS discovery and secure-runner packaging preflight remain required. |
| `RISK-SIGN-007` | **Closed in design with external gate.** Production internal/final signing and immediate verification remain maintainer-controlled gates. |
| `RISK-PROVENANCE-008` | **`DR-PROVENANCE-006` closed; OPEN high through `DR-PROVENANCE-007`.** Workflow implementation provenance is pinned, but the claimed single Cura validation revision is not achievable in the specified order. |
| `RISK-ARCH-009` | **Closed in design.** Early identity checks, strict all-PE validation, MSI checks, and native execution remain required. |
| `RISK-RELEASE-010` | **Bounded closed for design scope.** Stable publication remains blocked on production signing, physical Arm acceptance of both installers, and explicit maintainer approval. |

## New high finding

### DR-PROVENANCE-007 — the ordered proof mutates singular commit `V` between package and installer runs

- **Maps to:** `RISK-PROVENANCE-008`
- **Severity:** **high**
- **Design location:** “Exact-SHA pre-merge proof,” steps 1–3.
- **Observed gap:** r3 defines `V` as one exact 40-hex commit based directly on `C`, then instructs the team to push and run the package workflow after changing only `conan-package.yml`, and only afterward change `windows-arm.yml`; committing the second change creates another SHA, while amending or force-pushing makes the package run reference the superseded SHA, so the two runs cannot truthfully share the asserted single `V`.
- **Impact:** the required `C`/`V`/`W` map and statement that `C..V` contains both validation callers become false or ambiguous, weakening the immutable evidence chain used to accept the package consumed by the installer.
- **Exact correction:** create and push one commit `V`, based directly on `C`, containing both validation-caller workflow changes before either run; invoke both package and installer workflows at that unchanged SHA and record that same `V` in both summaries and validation evidence.

No critical finding is open; one high finding remains open.

## External gates

The design correctly retains exact-SHA CI proof, X64 regression, production Authenticode signing, hosted Arm smoke testing, physical Windows Arm testing of both installers, and separate maintainer stable-publication approval.

**confidence: high**

**Justification:** the verified records show complete closure of the nested mutable-action defect, but steps 1–3 necessarily create two validation revisions while the acceptance evidence claims one immutable `V`.
