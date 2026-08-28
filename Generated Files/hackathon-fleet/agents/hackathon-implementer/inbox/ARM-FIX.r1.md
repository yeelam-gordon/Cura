# ARM-FIX r1 Assignment

objective: Fix the Arm-readiness finding `HIR-REGRESSION-004` so every supported package matrix job uses a unique immutable provenance artifact name.

inputs:
- Exact readiness record: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-arm-readiness\output\ARM-READY.r1.md`
  - SHA-256: `726BAD62C81D658A1774305D774EE56ADF32B1D3FD5E63C549B51CDB9E430F03`
- Current complete implementation in `C:\s\Demo\Hack2026\cura-workflows`.

constraints:
- Accept the stable finding unchanged.
- Add a stable matrix/platform identifier to upload/download/provenance naming as needed.
- Add a Linux+Wasm regression test that fails on duplicate names.
- Preserve exact-SHA proof semantics and all approved design requirements.
- Do not launch subagents, edit the workboard, commit, or change unrelated files.
- Write only `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-implementer\output\ARM-FIX.r1.md` besides implementation/test edits.

expected_output:
- Root-cause fix mapping, changed files, exact test/check results, limitations, and confidence.

acceptance_evidence:
- Linux+Wasm and all-platform matrices yield unique provenance artifact names.
- Existing workflow tests, YAML parsing, runner output, Python compile, and diff checks pass.
