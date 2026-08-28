# ARM-FIX r1

## Input integrity

- Readiness record: `ARM-READY.r1.md`
- Verified SHA-256: `726BAD62C81D658A1774305D774EE56ADF32B1D3FD5E63C549B51CDB9E430F03`
- Stable finding accepted unchanged: `HIR-REGRESSION-004`.

## Root-cause fix mapping

- Root cause: Linux and Wasm both use `ubuntu-latest`, while the immutable package-create provenance artifact name used `matrix.runner`; both jobs therefore generated the same name.
- Fix: `make_runners_list.py` now emits stable platform identifiers: `linux`, `windows`, `macos`, `windows-arm64`, and `wasm`.
- Upload binding: `conan-package.yml` now names each matrix provenance artifact with `${{ matrix.platform }}` and records that platform in the job summary.
- Download binding: the existing run-scoped pattern `package-provenance-create-${{ github.run_id }}-${{ github.run_attempt }}-*` continues to select every newly platform-qualified artifact.
- Contract preservation: exact-SHA workflow/action/helper verification, provenance JSON schema and instances, component paths, package-chain validation, and immutable run/attempt scoping are unchanged.

## Changed implementation/test files

1. `cura-workflows/runner_scripts/make_runners_list.py`
2. `cura-workflows/.github/workflows/conan-package.yml`
3. `cura-workflows/runner_scripts/tests/test_workflow_provenance.py`

Regression coverage includes an explicit Linux+Wasm duplicate-name assertion and an all-five-platform stable identifier/name assertion.

## Exact validation evidence

| Check | Exact result |
|---|---|
| Readiness hash | `ARM_READY_SHA256=726BAD62C81D658A1774305D774EE56ADF32B1D3FD5E63C549B51CDB9E430F03` |
| Complete workflow tests: `python -m pytest runner_scripts\tests` | Exit `0`; `22 passed in 2.77s` |
| Targeted Cura packaging tests | Exit `0`; `17 passed in 0.34s` |
| Complete Cura packaging tests | Exit `0`; `17 passed in 0.46s` |
| Changed implementation/test Python compilation | Exit `0`; `COMPILED_COUNT=11` |
| Changed YAML parsing | Exit `0`; `PARSED_COUNT=8` |
| Linux+Wasm immutable names | Exit `0`; `UNIQUE_COUNT=2 NAMES=package-provenance-create-12345-1-linux,package-provenance-create-12345-1-wasm` |
| All-platform immutable names | Exit `0`; `UNIQUE_COUNT=5 NAMES=package-provenance-create-12345-1-linux,package-provenance-create-12345-1-windows,package-provenance-create-12345-1-macos,package-provenance-create-12345-1-windows-arm64,package-provenance-create-12345-1-wasm` |
| Single-platform runner loop | Exit `0`; Linux=`linux/ubuntu-latest`, Windows=`windows/windows-latest`, macOS=`macos/macos-13`, Windows Arm64=`windows-arm64/windows-11-arm`, Wasm=`wasm/ubuntu-latest` |
| X64/Arm installer artifact uniqueness | Exit `0`; `UNIQUE_COUNT=4` |
| Forbidden-pattern scan | Exit `0`; `FORBIDDEN_MATCHES=0` |
| Cura diff check | Exit `0`; `CURA_DIFF_CHECK=CLEAN` |
| Cura-workflows diff check | Exit `0`; `WORKFLOW_DIFF_CHECK=CLEAN` |

## Limitations

- No hosted GitHub Actions matrix run was available locally; workflow behavior was validated through YAML parsing, CLI matrix generation, regression tests, and exact artifact-name assertions.
- Existing unrelated implementation changes were preserved; no workboard was edited, no subagent was launched, and no commit was created.

## Verdict

**HIR-REGRESSION-004: FIXED**

**Confidence: high**

**Justification:** Stable platform identities make Linux, Wasm, and every supported matrix job produce distinct immutable provenance artifact names without changing exact-SHA or provenance validation semantics.
