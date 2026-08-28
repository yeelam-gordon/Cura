# Impact and evidence

## Source key

- `[R]` `Generated Files\hackathon-fleet\agents\hackathon-arm-readiness\output\ARM-READY.r2.md` — final readiness, exact local commands/results, implementation scope, gates, and verdict.
- `[G]` `Generated Files\windows-arm-build-test-guide.md` — authoritative local, exact-SHA CI, signing, hosted smoke, physical acceptance, diagnostics, and publication procedure.
- `[O1]` `Generated Files\01-arm-quality-fix-summary.md` — original workspace baseline and coordinated repository scope.
- `[O2]` `Generated Files\02-cura-package-audit.md` — original Cura package audit.
- `[O3]` `Generated Files\03-cura-workflows-audit.md` — original workflow audit and before state.
- `[O4]` `Generated Files\04-prs-validation-handoff.md` — original coordinated PR and stable-handoff plan.
- `[D]` `Generated Files\hackathon-fleet\agents\hackathon-fix-designer\output\DESIGN.r3.md` — architecture and trust-boundary design.
- `[DR]` `Generated Files\hackathon-fleet\agents\hackathon-design-risk-reviewer\output\DESIGN-REVIEW.r3.md` — design risk review.
- `[I]` `Generated Files\hackathon-fleet\agents\hackathon-implementer\output\IMPLEMENT.r2.md` — complete implementation and prior-finding fix map.
- `[CR]` `Generated Files\hackathon-fleet\agents\hackathon-implementation-reviewer\output\CODE-REVIEW.r2.md` — regression finding and review disposition.
- `[F]` `Generated Files\hackathon-fleet\agents\hackathon-implementer\output\ARM-FIX.r1.md` — matrix-collision root cause, correction, and regression evidence.

## Quantified local evidence

Every quantitative claim below has an explicit source.

| Evidence | Exact value | Source |
|---|---:|---|
| Readiness record integrity | SHA-256 `9A2CC85400BF7C84F64F1CEEDD08C7224403F585F511B8B1CCCD2E6DAE514381` | Assignment hash, independently reverified; `[R]` |
| Current implementation inspected by readiness | `3,856` lines across `7` Cura files and `13` cura-workflows files | `[R]`, “Integrity and scope” |
| Cura targeted packaging result | `17 passed in 0.39s`, exit `0` | `[R]`, “Exact local validation evidence” |
| Cura complete packaging result | `17 passed in 0.27s`, exit `0` | `[R]`, “Exact local validation evidence” |
| Workflow targeted result | `22 passed in 2.88s`, exit `0` | `[R]`, “Exact local validation evidence” |
| Workflow complete result | `22 passed in 2.93s`, exit `0` | `[R]`, “Exact local validation evidence” |
| Python syntax validation | `COMPILED_COUNT=11`, exit `0` | `[R]`, “Exact local validation evidence” |
| YAML syntax validation | `PARSED_COUNT=8`, exit `0` | `[R]`, “Exact local validation evidence” |
| Supported single-platform cases checked | `SINGLE_PLATFORM_COUNT=5`, exit `0` | `[R]`, “Exact local validation evidence” |
| Linux and Wasm immutable provenance names | `LINUX_WASM_UNIQUE_COUNT=2`, exit `0` | `[R]`, “Exact local validation evidence” |
| All-platform immutable provenance names | `ALL_PLATFORM_UNIQUE_COUNT=5`, exit `0` | `[R]`, “Exact local validation evidence” |
| Architecture-qualified installer workflow artifacts | `INSTALLER_ARTIFACT_UNIQUE_COUNT=4`, exit `0` | `[R]`, “Exact local validation evidence” |
| Forbidden-pattern result | `FORBIDDEN_MATCHES=0`, exit `0` | `[R]`, “Exact local validation evidence” |
| Repository diff hygiene | Both checks exit `0` and report clean | `[R]`, “Exact local validation evidence”; independently reverified in `DEMO.r1.md` |
| Required package provenance instances | `16` distinct required instances | `[R]`, “Architecture closure”; `[D]`, “Package provenance evidence contract” |
| Required CRT files in the Arm build contract | `6` named non-empty DLLs | `[R]`, “Architecture closure”; `[G]`, secure runner and validation requirements |
| Required Arm payload paths in strict PE validation | `9` paths | `[D]`, “PR 1 — exact Cura changes”; `[G]`, downloaded-payload validation command |
| Final readiness verdict | `LOCAL PASS — READY FOR EXTERNAL VALIDATION; STABLE PUBLICATION REMAINS GATED.` | `[R]`, “Verdict” |

## Before, after, and multiplier

| Claim | Evidence |
|---|---|
| Before: the Arm installer selected an x64 CRT path and lacked signing parity. | `[O3]`, “Observed workflow facts.” |
| After: Arm CRT discovery, native `python3.dll`, strict all-file PE checks, architecture-aware MSI/NSIS behavior, canonical unsigned/signed contracts, exact workflow provenance, architecture-qualified artifacts, and stable matrix identities are implemented and locally tested or statically checked. | `[I] [F] [R]` |
| Reusable multiplier: the PE validator, provenance checker, artifact-contract tool, stable matrix identity, and acceptance guide can be reused at workflow and architecture boundaries rather than only for one installer patch. | `[D] [I] [R] [G]` |
| Upstream path: coordinated Cura and `cura-workflows` changes use immutable `C`, `V`, and `W` validation, then maintainer-controlled signing, physical acceptance, and publication. | `[O1] [O4] [G]` |

## Claim audit and exclusions

The original `hackathon-submission.md` contains prospective statements about a green hosted build, demo signing, and a live run. Those statements are not used as completed-result evidence because the final readiness record explicitly says hosted CI, production signing, real payload architecture, installer lifecycle, GUI execution, physical Arm behavior, performance, power, publication, and maintainer approval remain unexecuted or gated `[R]`.

The demo therefore claims only:

- verified local tests and static checks exactly reported in `[R]`;
- read-only inspection of the current implementation;
- implemented fail-closed behavior described by `[I]`, `[F]`, and `[R]`;
- a guide-defined external validation path `[G]`.

It does not claim completion of any external gate.
