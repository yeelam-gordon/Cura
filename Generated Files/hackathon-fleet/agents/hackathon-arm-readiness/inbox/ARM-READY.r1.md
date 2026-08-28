# ARM-READY r1 Assignment

objective: Prove all locally executable build/test/architecture behavior for the complete implementation and produce the authoritative Windows Arm64 build/test guide.

inputs:
- Approved design composite.
- Complete current implementation in both repositories.
- Final implementation review: `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-implementation-reviewer\output\CODE-REVIEW.r2.md`
  - SHA-256: `4F54268E12D94AD1A4492A93B73085DA19DEE11EEE55A1A686FAE4FC926EE46F`
- Known medium finding `HIR-REGRESSION-004` must be explicitly reproduced and classified.

constraints:
- Discover/use existing tools only; do not install new tools unless a chosen command fails solely due to a missing declared dependency.
- Do not edit product/workflow code or the workboard; do not launch subagents.
- You may write only:
  - `C:\s\Demo\Hack2026\Cura\Generated Files\windows-arm-build-test-guide.md`
  - `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-arm-readiness\output\ARM-READY.r1.md`
- Never claim hosted Arm, secure signing, installer lifecycle, GUI, physical hardware, performance, or power evidence that was not actually executed.
- Return stable findings for every locally reproducible failure.

expected_output:
- Verdict and exact commands/exit codes for targeted tests, relevant broader checks, Python/YAML validation, runner matrices, artifact uniqueness, and diff hygiene.
- Architecture-closure assessment for PE/CRT/python/MSI/signature contracts.
- Explicit tested/not-tested table and external gates.
- Executable Windows Arm runbook at the required guide path, including prerequisites, exact C/V/W workflow sequence, expected outputs, diagnostics, clean install/upgrade/uninstall, payload architecture/signature/MSI checks, and physical Arm acceptance.
- `confidence: high|medium|low` with one-sentence justification.

acceptance_evidence:
- All locally controllable tests pass or stable findings are returned.
- Guide commands are internally consistent with the implementation.
- `HIR-REGRESSION-004` is either disproved with evidence or returned for correction.
