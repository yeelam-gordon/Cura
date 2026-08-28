# CODE-REVIEW r1 Assignment

objective: Independently review the complete current two-repository implementation against the approved design and actual runtime/workflow behavior.

inputs:
- Approved design: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-fix-designer\output\DESIGN.r3.md`
  - SHA-256: `8F6EB544288CC1A18523184F583494D24F7232C58DD9B73984C8D4C3089225AC`
- Binding correction/review: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-design-risk-reviewer\output\DESIGN-REVIEW.r3.md`
  - SHA-256: `C43ADD6BA9899DE1AFD99BB62DA7AC282462E608FB840C7E3065FA33F3DAB8C0`
- Implementation report: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-implementer\output\IMPLEMENT.r1.md`
  - SHA-256: `8B5C9477FCDE94F43E8B53DC40DA9AD2F9AA8D20DB7FD2D66922DF90D85966B2`
- Complete tracked and untracked diffs in:
  - `C:\s\Demo\Hack2026\Cura`
  - `C:\s\Demo\Hack2026\cura-workflows`

constraints:
- Review actual files and all untracked additions, not only the worker report.
- Do not edit product code, prior records, or the workboard.
- You may write only `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-implementation-reviewer\output\CODE-REVIEW.r1.md`.
- Do not launch subagents.
- Ignore style/nits; report correctness, security/trust, architecture/ABI, workflow semantics, artifact boundaries, provenance, regression, error-handling, and upstreamability defects.

expected_output:
- Stable findings with file/location, observed behavior, expected behavior, reproduction/evidence, severity, and required correction.
- Explicit approved-design compliance map.
- `PASS` or `REVISE`.
- `confidence: high|medium|low` and one-sentence justification.

acceptance_evidence:
- `PASS` only with zero open critical/high findings and high confidence.
- Distinguish locally reproducible defects from external CI/secrets/hardware gates.
