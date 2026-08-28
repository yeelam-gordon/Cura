# DESIGN r3 Assignment

objective: Produce the final self-contained design revision, preserving every r2 requirement and closing the sole remaining high finding `DR-PROVENANCE-006`.

inputs:
- Candidate r2 design: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-fix-designer\output\DESIGN.r2.md`
  - SHA-256: `ADD584856B897BAB3220F44250C3ECCA29F16EA902D5B946CD39E8DEC8344652`
- Exact r2 review: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-design-risk-reviewer\output\DESIGN-REVIEW.r2.md`
  - SHA-256: `88F44626AD605653607AF13A02AE28421DCC61C7EA6DEE294D13D825F758C43D`

constraints:
- Read both exact records verbatim and preserve every accepted r2 contract and external gate.
- Correct `DR-PROVENANCE-006` exactly: thread `cura_workflows_ref` through nested recipe version/export workflows, use local SHA-pinned setup/upload actions, pin helper checkouts, assert resolved revisions, and include every invocation in proof evidence.
- Do not edit product code, prior records, or the workboard.
- You may write only `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-fix-designer\output\DESIGN.r3.md`.
- Do not launch subagents.

expected_output:
- A self-contained replacement design.
- Explicit disposition of `DR-PROVENANCE-006`.
- Exact implementation/test/provenance requirements.
- `confidence: high|medium|low` and one-sentence justification.

acceptance_evidence:
- Zero open critical/high findings.
- Implementer can execute without redesign.
