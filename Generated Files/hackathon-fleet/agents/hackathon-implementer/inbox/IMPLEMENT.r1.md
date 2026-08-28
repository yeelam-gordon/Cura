# IMPLEMENT r1 Assignment

objective: Implement the manager-approved Windows Arm64 design across Cura and cura-workflows without redesign.

inputs:
- Approved design: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-fix-designer\output\DESIGN.r3.md`
  - SHA-256: `8F6EB544288CC1A18523184F583494D24F7232C58DD9B73984C8D4C3089225AC`
- Binding final review/correction: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-design-risk-reviewer\output\DESIGN-REVIEW.r3.md`
  - SHA-256: `C43ADD6BA9899DE1AFD99BB62DA7AC282462E608FB840C7E3065FA33F3DAB8C0`
- Repositories:
  - `C:\s\Demo\Hack2026\Cura`
  - `C:\s\Demo\Hack2026\cura-workflows`

constraints:
- Implement every locally controllable design requirement, including tests.
- Binding correction: any validation commit `V` must contain both caller changes before either package or installer run; do not create validation-only caller changes now unless exact PR SHAs exist.
- Do not redesign silently. If source reality invalidates the design, stop with a design-change request.
- Preserve unrelated changes; `Generated Files` is manager-owned.
- Do not launch subagents.
- You may edit product/workflow/test files in both repositories and write only your worker result to `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-implementer\output\IMPLEMENT.r1.md`; do not edit the workboard.
- Do not commit.

expected_output:
- Implemented files in both repositories.
- Design requirement mapped to each change.
- Exact commands, exit codes/results, and unresolved limitations.
- Diff/commit readiness and `confidence: high|medium|low` with one-sentence justification.

acceptance_evidence:
- Cura targeted packaging tests pass.
- cura-workflows artifact-contract tests pass.
- Arm runner-list command emits `windows-11-arm`.
- YAML parses for every changed workflow/action file.
- `git diff --check` passes in both repositories.
- No production-signing, hosted-CI, or physical-hardware result is claimed without actual evidence.
