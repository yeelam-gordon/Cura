# DESIGN-REVIEW r2 Assignment

objective: Perform the final convergence review of the designer's self-contained r2 design against every previously accepted critical/high finding and current source.

inputs:
- Candidate immutable design: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-fix-designer\output\DESIGN.r2.md`
  - SHA-256: `ADD584856B897BAB3220F44250C3ECCA29F16EA902D5B946CD39E8DEC8344652`
- Prior exact review: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-design-risk-reviewer\output\DESIGN-REVIEW.r1.md`
  - SHA-256: `81299A1C2AAE618C28A427CD706A0FFA7C4EF1EAF49081765698E671097A473F`
- Independent risk record: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-design-risk-reviewer\output\RISK.r1.md`
  - SHA-256: `F17BE2EB662C80E089B529F002AEE70C77A6F5CE3F161002F4593CD89E4BA5EB`
- Current unchanged source baselines in both repositories.

constraints:
- Read the relayed records verbatim and verify their hashes.
- Do not edit product code, prior records, or the workboard.
- You may write only `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-design-risk-reviewer\output\DESIGN-REVIEW.r2.md`.
- Do not launch subagents.
- Do not reopen medium/nit scope unless it creates a critical/high correctness defect.

expected_output:
- Explicit disposition of all five `DESIGN-REVIEW.r1` findings and all original critical/high risks.
- Any remaining stable finding with location, evidence, severity, and exact correction.
- `GO`, `REVISE`, or `NO-GO`.
- `confidence: high|medium|low` and one-sentence justification.

acceptance_evidence:
- `GO` only with zero open critical/high findings, explicit external gates, and high confidence.
- Confirm the design is specific enough for an implementer to execute without redesign.
