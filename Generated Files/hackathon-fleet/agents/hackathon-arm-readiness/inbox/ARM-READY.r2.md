# ARM-READY r2 Assignment

objective: Revalidate the complete final two-repository implementation after the matrix fix and update the authoritative Windows Arm guide and final readiness verdict.

inputs:
- Prior readiness: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-arm-readiness\output\ARM-READY.r1.md`
  - SHA-256: `726BAD62C81D658A1774305D774EE56ADF32B1D3FD5E63C549B51CDB9E430F03`
- Fix report: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-implementer\output\ARM-FIX.r1.md`
  - SHA-256: `ED8060F0357F59A30CF9A6716CCC74987E14DB4342823923B37A65C83B324ABE`
- Complete current implementation.

constraints:
- Re-run the full r1 local validation set plus Linux+Wasm and all-platform uniqueness checks.
- Inspect the actual fix and guide consistency.
- Do not edit product/workflow code or workboard; do not launch subagents.
- You may update only:
  - `C:\s\Demo\Hack2026\Cura\Generated Files\windows-arm-build-test-guide.md`
  - `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-arm-readiness\output\ARM-READY.r2.md`
- Keep every unexecuted CI/signing/hardware claim explicitly gated.

expected_output:
- Final local verdict, exact commands/results, architecture closure, tested/not-tested, external gates, confidence.
- Updated executable guide.

acceptance_evidence:
- Zero locally reproducible build/test failures.
- `HIR-REGRESSION-004` closed with reproducing evidence.
- High confidence based on commands/artifacts, not prose.
