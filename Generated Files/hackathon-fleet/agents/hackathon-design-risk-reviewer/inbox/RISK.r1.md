# RISK r1 Assignment

objective: Independently investigate and adversarially assess the Windows Arm64 installer problem before seeing the designer's proposal, identifying root-cause errors, regressions, dependency/ABI risks, signing traps, runner assumptions, and scope hazards.

inputs:
- Every file in `C:\s\Demo\Hack2026\Cura\Generated Files`
- `C:\s\Demo\Hack2026\Cura` at current `main`
- `C:\s\Demo\Hack2026\cura-workflows` at current `main`
- Current x64 and Arm installer workflows, dispatchers, package scripts, and contribution expectations.

constraints:
- Do not edit product code or the manager workboard.
- You may write only `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-design-risk-reviewer\output\RISK.r1.md`.
- Do not launch subagents.
- Investigate current upstream reality rather than trusting generated prose.
- Findings must use stable IDs and distinguish confirmed defects from unverified claims.

expected_output:
- Independent current-state/root-cause assessment.
- Stable finding IDs with location/evidence, observed versus expected, severity, and required correction.
- Explicit upstream/fork, signing, architecture-validation, and Windows Arm execution risks.
- Initial `GO`, `REVISE`, or `NO-GO` verdict.
- `confidence: high|medium|low` and one-sentence justification.

acceptance_evidence:
- Source lines or reproducible commands for every critical/high finding.
- Clear gates for claims that require secrets, CI, or physical Arm hardware.
