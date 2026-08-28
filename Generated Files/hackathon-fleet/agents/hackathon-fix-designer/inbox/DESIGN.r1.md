# DESIGN r1 Assignment

objective: Independently verify the current Windows Arm64 installer problem across both repositories and produce an upstreamable fix design with an exact implementation and validation surface.

inputs:
- Every file in `C:\s\Demo\Hack2026\Cura\Generated Files`
- `C:\s\Demo\Hack2026\Cura` at current `main`
- `C:\s\Demo\Hack2026\cura-workflows` at current `main`
- Focus on CRT architecture selection, signing parity, installer payload architecture validation, reusable-workflow references, and hosted versus self-hosted runner reality.

constraints:
- Do not edit product code or the manager workboard.
- You may write only `C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-fix-designer\output\DESIGN.r1.md`.
- Do not launch subagents.
- Verify claims from current source and available repository history; separate agent-controlled work from vendor/maintainer-controlled work.
- Avoid fork-only changes unless explicitly isolated as a demo option.

expected_output:
- Current-state evidence with paths/lines/commands.
- Root cause and already-solved work/duplication risks.
- Dependency graph, proposed architecture, alternatives and tradeoffs.
- Exact files, symbols, and workflows to change.
- Ordered implementation, test, rollback design, and open assumptions/gates.
- `confidence: high|medium|low` and one-sentence justification.

acceptance_evidence:
- Source lines or command output for each material claim.
- A design that can be implemented without silent redesign.
- Explicit handling of production signing secrets and unavailable physical Arm validation.

