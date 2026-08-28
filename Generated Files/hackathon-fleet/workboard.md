# Hackathon Fleet Workboard

## Project

- Objective: Promote Cura's existing Windows Arm64 installer path toward stable quality by removing x64 CRT leakage, restoring workflow parity, validating the complete payload, and producing an executable Arm runbook and honest demo package.
- Authority: manager (this root session)
- Binding: parallel only for independent work
- Transport: native; `graph-routing` and `graph-manager` were requested but are unavailable in this CLI installation
- Maximum active workers: 2
- Repositories:
  - `C:\s\Demo\Hack2026\Cura` at `5068661cd4`
  - `C:\s\Demo\Hack2026\cura-workflows` at `126f92d`

## Role Assignments

| Role | Agent | Responsibility |
|---|---|---|
| Delivery owner | manager | Scope, dependency graph, evidence acceptance, integration, PR/demo verdict |
| Fix designer | hackathon-fix-designer | Root cause and immutable change design |
| Design risk reviewer | hackathon-design-risk-reviewer | Independent investigation and adversarial design review |
| Implementer | hackathon-implementer | Implement only the accepted design |
| Implementation reviewer | hackathon-implementation-reviewer | Review design compliance and actual behavior |
| Arm readiness owner | hackathon-arm-readiness | Build/test/architecture evidence and Windows Arm guide |
| Demo producer | hackathon-demo-producer | Demo script, shots, narration, subtitles, and impact evidence |

## Tasks

| ID | Owner | Depends on | State | Revision | Acceptance criteria | Output |
|---|---|---|---|---|---|---|
| DESIGN | hackathon-fix-designer | none | accepted-input | r1 | Current-state evidence, root cause, exact change surface, alternatives, tests, rollback, gates, confidence | `agents/hackathon-fix-designer/output/DESIGN.r1.md` |
| RISK | hackathon-design-risk-reviewer | none | accepted-input | r1 | Independent evidence, stable findings, corrections, verdict, confidence | `agents/hackathon-design-risk-reviewer/output/RISK.r1.md` |
| DESIGN-REVIEW | hackathon-design-risk-reviewer | DESIGN,RISK | revise | r1 | Review current design; zero open critical/high findings for GO | `agents/hackathon-design-risk-reviewer/output/DESIGN-REVIEW.r1.md` |
| DESIGN-REVISION | hackathon-fix-designer | DESIGN-REVIEW | candidate | r2 | Address every accepted finding with verified assumptions and high confidence | `agents/hackathon-fix-designer/output/DESIGN.r2.md` |
| DESIGN-REVIEW-2 | hackathon-design-risk-reviewer | DESIGN-REVISION | revise | r2 | Final convergence review; zero open critical/high findings and high confidence | `agents/hackathon-design-risk-reviewer/output/DESIGN-REVIEW.r2.md` |
| DESIGN-REVISION-3 | hackathon-fix-designer | DESIGN-REVIEW-2 | candidate | r3 | Close DR-PROVENANCE-006 while preserving all accepted r2 requirements | `agents/hackathon-fix-designer/output/DESIGN.r3.md` |
| DESIGN-REVIEW-3 | hackathon-design-risk-reviewer | DESIGN-REVISION-3 | accepted-with-binding-correction | r3 | Third and final design verdict | `agents/hackathon-design-risk-reviewer/output/DESIGN-REVIEW.r3.md` |
| IMPLEMENT | hackathon-implementer | accepted-design | review | r1 | Surgical implementation, mapped requirements, targeted tests, confidence | `agents/hackathon-implementer/output/IMPLEMENT.r1.md` |
| CODE-REVIEW | hackathon-implementation-reviewer | IMPLEMENT | revise | r1 | Complete diff review; zero open critical/high findings and PASS | `agents/hackathon-implementation-reviewer/output/CODE-REVIEW.r1.md` |
| IMPLEMENT-FIX | hackathon-implementer | CODE-REVIEW | review | r2 | Fix accepted HIR-PROV-001, HIR-WORKFLOW-002, and HIR-BOUNDARY-003 | `agents/hackathon-implementer/output/IMPLEMENT.r2.md` |
| CODE-REVIEW-2 | hackathon-implementation-reviewer | IMPLEMENT-FIX | accepted-medium-open | r2 | Zero critical/high findings; high confidence; HIR-REGRESSION-004 carried to Arm readiness | `agents/hackathon-implementation-reviewer/output/CODE-REVIEW.r2.md` |
| ARM-READY | hackathon-arm-readiness | accepted-implementation | revise | r1 | Build/test exit codes, payload architecture closure, executable guide, limitations | `agents/hackathon-arm-readiness/output/ARM-READY.r1.md` |
| ARM-FIX | hackathon-implementer | ARM-READY | done | r1 | Fix ARM-BUILD-001/HIR-REGRESSION-004 matrix artifact collision | `agents/hackathon-implementer/output/ARM-FIX.r1.md` |
| ARM-READY-2 | hackathon-arm-readiness | ARM-FIX | local-pass-external-gates | r2 | Revalidate complete implementation and update authoritative guide | `agents/hackathon-arm-readiness/output/ARM-READY.r2.md` |
| DEMO | hackathon-demo-producer | ARM-READY | done | r1 | 2-4 minute evidence-backed package with narration/subtitle identity | `agents/hackathon-demo-producer/output/DEMO.r1.md` |
| INTEGRATE | manager | DESIGN,CODE-REVIEW,ARM-READY,DEMO | done-local-external-gates | r1 | Required artifacts exist; PR-ready/demo-ready or blocked with quoted evidence | this workboard |

## Acceptance Gates

1. One immutable approved design with no open critical/high findings and high-confidence designer/reviewer evidence.
2. Implementation matches that design and has no open critical/high review findings.
3. Required build/tests pass, or limitations are explicitly accepted with evidence.
4. `Generated Files/windows-arm-build-test-guide.md` is executable.
5. All five files under `Generated Files/demo/` exist and all claims are sourced.

## Risk Register

| ID | Risk | State | Required evidence/mitigation |
|---|---|---|---|
| R1 | Production signing requires Ultimaker's physical token and secrets | open-external | Keep production signing semantics; document that credential-backed execution is maintainer-controlled |
| R2 | No physical Windows Arm hardware is established in this workspace | open-external | Separate static/local validation from physical install/run claims; never imply hardware proof |
| R3 | Full Conan/PyInstaller installer build may require private credentials and self-hosted infrastructure | open-external | Prove all locally controllable behavior; record exact CI command and external gate |
| R4 | Fork-specific workflow repointing could make an upstream PR unsuitable | open | Prefer upstreamable workflow changes; isolate any fork-only proof mechanism |
| R5 | Committed `python_dll_workaround\python3.dll` is AMD64 and copied into Arm payload | confirmed-critical | Accepted finding RISK-ARCH-002; design must specify an Arm-safe source/removal and regression evidence |
| R6 | Arm MSI is currently authored with x64 metadata | confirmed-high | Accepted finding RISK-PACKAGE-003; architecture-aware authoring and metadata assertion required |
| R7 | Packaging subprocess failures and missing artifacts can false-green | confirmed-high | Accepted finding RISK-VALIDATION-004; fail-fast subprocesses and required artifact errors |
| R8 | Proof runs can execute upstream helper actions/scripts instead of changed fork code | confirmed-high | Accepted finding RISK-PROVENANCE-008; immutable SHA provenance map required |
| R9 | Linux+Wasm package matrix jobs share the same provenance artifact name | closed | Stable platform IDs; all-platform uniqueness 5/5 in ARM-READY r2 |

## Final Output Paths

- Accepted design: immutable composite of `agents/hackathon-fix-designer/output/DESIGN.r3.md` (`8F6EB544288CC1A18523184F583494D24F7232C58DD9B73984C8D4C3089225AC`) and binding correction `DR-PROVENANCE-007` from `agents/hackathon-design-risk-reviewer/output/DESIGN-REVIEW.r3.md` (`C43ADD6BA9899DE1AFD99BB62DA7AC282462E608FB840C7E3065FA33F3DAB8C0`)
- Windows Arm guide: `Generated Files/windows-arm-build-test-guide.md`
- Demo package: `Generated Files/demo/`
- Worker records: `Generated Files/hackathon-fleet/agents/<agent>/{inbox,output}/<task>.r<revision>.md`

## Accepted Evidence

- Design: immutable r3 composite listed above; all critical findings closed, with the reviewer's single-`V` ordering correction binding implementation.
- Implementation: complete two-repository diff; final review has zero open critical/high findings and high confidence.
- Arm readiness: `agents/hackathon-arm-readiness/output/ARM-READY.r2.md`, SHA-256 `9A2CC85400BF7C84F64F1CEEDD08C7224403F585F511B8B1CCCD2E6DAE514381`.
- Guide: `Generated Files/windows-arm-build-test-guide.md`, SHA-256 `A49CDBE323D767B6D5B568CDC27855BD72DC9C4FEB784264E3A132475463D21E`.
- Demo report: `agents/hackathon-demo-producer/output/DEMO.r1.md`, SHA-256 `0EC86178E5DBE376E9B61B0F6C5DEE07C5696DF1A75E385A126753537352BADC`.
- Manager final local run:
  - Cura packaging: 17 passed.
  - cura-workflows helpers/contracts: 22 passed.
  - Eight changed YAML files parsed.
  - All five platform identities emitted; Windows Arm uses `windows-11-arm`.
  - Both repository diff checks clean.
- Demo package: five required files, 356-word narration, 202-second subtitle timeline, exact normalized narration/subtitle identity, and zero unsupported completion claims.

## Final Status

**PR-ready locally; demo package ready; final Windows Arm validation and stable publication blocked on external evidence.**

The implementation, tests, guide, and evidence-honest demo assets are complete in the workspace. No critical/high code-review finding remains. The following gates were not available and are not claimed:

1. Commit/push immutable `C` and `W`, then create one direct-child `V` containing both caller changes before either run.
2. Run native Arm package/payload CI and secure X64 production signing with maintainer credentials.
3. Complete hosted `windows-11-arm` smoke and X64 regression workflows.
4. Test signed EXE and MSI install, launch, slice, export, restart, upgrade/coexistence, and uninstall on physical Windows Arm hardware.
5. Obtain maintainer approval for stable release publication and replace demo placeholders only with retained evidence.
