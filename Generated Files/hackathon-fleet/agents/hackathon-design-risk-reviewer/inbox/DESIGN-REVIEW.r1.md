# DESIGN-REVIEW r1 Assignment

objective: Review the designer's exact r1 proposal against the independent r1 risk assessment and current source, producing a bounded design-convergence verdict.

inputs:
- Exact designer record: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-fix-designer\output\DESIGN.r1.md`
  - SHA-256: `A3E7FAAEF6AB8F58A5FD52668C8E9CECCB6ACC01E26968EAA59806D5FE9A20A8`
- Exact independent risk record: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-design-risk-reviewer\output\RISK.r1.md`
  - SHA-256: `F17BE2EB662C80E089B529F002AEE70C77A6F5CE3F161002F4593CD89E4BA5EB`
- Both repositories at their current unchanged baselines.
- Manager accepts all confirmed critical/high findings in `RISK.r1.md`; none may be dropped without contrary source evidence.

constraints:
- Read and review both immutable records verbatim; this path-and-hash relay is the manager's exact relay of design and findings.
- Do not edit product code, either source record, or the workboard.
- You may write only `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-design-risk-reviewer\output\DESIGN-REVIEW.r1.md`.
- Do not launch subagents.
- Check whether the proposed architecture is implementable with existing workflow artifact boundaries, credential topology, GitHub reusable-workflow rules, and repository packaging scripts.

expected_output:
- Stable finding IDs, mapped where possible to `RISK.r1.md`.
- For each finding: exact design section/location, source evidence, observed gap, severity, and required correction.
- Explicit disposition of every critical/high finding from `RISK.r1.md`.
- `GO`, `REVISE`, or `NO-GO` verdict.
- `confidence: high|medium|low` and one-sentence justification.

acceptance_evidence:
- `GO` is permitted only with zero open critical/high findings, all assumptions verified or explicit gates, and high confidence.
- Corrections must be precise enough for the designer to produce an immutable implementable revision.
