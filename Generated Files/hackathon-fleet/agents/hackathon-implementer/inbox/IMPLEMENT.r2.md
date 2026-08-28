# IMPLEMENT r2 Assignment

objective: Correct every accepted implementation-review finding and revalidate the complete current diff.

inputs:
- Exact review: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-implementation-reviewer\output\CODE-REVIEW.r1.md`
  - SHA-256: `7E6090957FC9684CC04A2853877504712D803FEB83760F48BA1C4C70FBA3BC35`
- Approved immutable design composite from the r1 assignment.
- Current implementation in both repositories.

constraints:
- The manager accepts all three findings unchanged: `HIR-PROV-001` (high), `HIR-WORKFLOW-002` (high), and `HIR-BOUNDARY-003` (medium).
- Fix root causes; add or update tests that reproduce each finding.
- Preserve all prior design requirements and unrelated changes.
- Do not launch subagents, edit the workboard, commit, or create validation-only caller commits.
- You may edit implementation/test files and write only `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-implementer\output\IMPLEMENT.r2.md`.

expected_output:
- Exact fix mapping for all three stable findings.
- Updated changed-file list and commands/results.
- Remaining external gates and `confidence: high|medium|low` with one-sentence justification.

acceptance_evidence:
- Caller/provenance validation cannot claim `W` while executing mutable refs and enforces one `C/V/W` chain.
- Combined jobs use unique architecture-qualified artifact names.
- Smoke inputs are hash/size bound to signed release evidence.
- All targeted tests, YAML parse, runner output, Python compile, forbidden-pattern checks, and both diff checks pass.
