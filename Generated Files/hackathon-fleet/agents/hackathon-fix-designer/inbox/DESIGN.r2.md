# DESIGN r2 Assignment

objective: Revise the exact r1 design to address every accepted reviewer finding and produce one implementation-complete candidate design.

inputs:
- Original design: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-fix-designer\output\DESIGN.r1.md`
  - SHA-256: `A3E7FAAEF6AB8F58A5FD52668C8E9CECCB6ACC01E26968EAA59806D5FE9A20A8`
- Exact design review: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-design-risk-reviewer\output\DESIGN-REVIEW.r1.md`
  - SHA-256: `81299A1C2AAE618C28A427CD706A0FFA7C4EF1EAF49081765698E671097A473F`
- Independent risk record: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-design-risk-reviewer\output\RISK.r1.md`
  - SHA-256: `F17BE2EB662C80E089B529F002AEE70C77A6F5CE3F161002F4593CD89E4BA5EB`
- Current unchanged source baselines in both repositories.

constraints:
- Read all three records verbatim. The reviewer record is relayed unchanged and every critical/high correction is manager-accepted.
- Do not edit product code, prior records, or the workboard.
- You may write only `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-fix-designer\output\DESIGN.r2.md`.
- Do not launch subagents.
- Preserve production-signing, physical Windows Arm, and stable-publication gates.
- Resolve `python3.dll` with a specific source and validation contract, not merely detection or allowlisting.

expected_output:
- A self-contained replacement design, not a patch note.
- Explicit disposition of `DR-ARCH-001`, `DR-PROVENANCE-002`, `DR-BOUNDARY-003`, `DR-VALIDATION-004`, and `DR-ARCH-005`.
- Exact files/symbols/workflows and ordered implementation/test/rollback plan.
- Exact cross-job artifact/metadata/tool contract and exact-SHA validation provenance.
- `confidence: high|medium|low` and one-sentence justification.

acceptance_evidence:
- No open critical/high reviewer finding.
- All locally controllable assumptions converted to tests or commands.
- External secrets/hardware/release decisions remain explicit gates.
