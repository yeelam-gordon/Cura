# DEMO r1 worker report

## Integrity and scope

- Verified final readiness with:
  `Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\s\Demo\Hack2026\Cura\Generated Files\hackathon-fleet\agents\hackathon-arm-readiness\output\ARM-READY.r2.md'`
- Exact result: `9A2CC85400BF7C84F64F1CEEDD08C7224403F585F511B8B1CCCD2E6DAE514381`, matching the assignment.
- Read the authoritative `windows-arm-build-test-guide.md`, every original generated evidence file outside fleet/demo records, the design/review/implementation lineage, and the relevant current implementation.
- Launched no subagents and edited no product code, workflow code, workboard, guide, or prior record.

## Outputs

The assignment-required `5` demo files exist:

1. `Generated Files\demo\demo-script.md` — SHA-256 `E251DFA5F5CE276F17C2135529B682B6C04DC41345C165E8CA8E41EE76F5D858`
2. `Generated Files\demo\shot-list.md` — SHA-256 `99103B60409C5393EF6FC9A12CABEBFA23A3DE284D2DD16ACD19DF4A2DC76D67`
3. `Generated Files\demo\narration.txt` — SHA-256 `EAD30A1AAC139667A7C5FBCD70598D0A7411008365D0FF0B5E59E75642BFC0EF`
4. `Generated Files\demo\subtitles.srt` — SHA-256 `2177E2CE6821E7DDB63FF15AF0228696DF7BA210C0916CBC8DD45CA9B5CB5B62`
5. `Generated Files\demo\impact-evidence.md` — SHA-256 `6C5AE119B3B09CA59355E5FED0C1412D8FFFCCDCF2588501A8D14330209891E7`

The count and hashes above are exact output from the final package-validation command.

## Narration and timing

- Exact word count: `356`.
- Subtitle timeline: `00:00:00,000` through `00:03:22,000`, exactly `202` seconds.
- Read-speed estimates from the same validation command: `164` seconds at `130` words per minute and `142` seconds at `150` words per minute.
- The timed primary video is therefore `03:22`, inside the assignment's required `2–4` minute range.

## Exact narration/subtitle identity

Documented normalization:

1. Convert CRLF/CR to LF.
2. For SRT, remove blank lines, cue-index lines matching `^\d+$`, and timestamp lines matching `^\d{2}:\d{2}:\d{2},\d{3}\s+-->\s+\d{2}:\d{2}:\d{2},\d{3}$`.
3. Join remaining subtitle text lines with one space.
4. For both texts, collapse all whitespace to one space and trim.
5. Compare ordinally and case-sensitively.

Exact result: `NARRATION_SUBTITLE_IDENTICAL=True`.

## Claim audit

- The narration explicitly says hosted Arm smoke was not executed, lists the prohibited result areas as non-claims, and says publication remains gated.
- Unsupported-completion regex:
  `hosted CI (passed|succeeded|completed)|production signing (passed|succeeded|completed)|physical Arm (passed|succeeded|completed)|GUI (passed|succeeded|completed)|stable publication (passed|succeeded|completed)`
- Exact result: `UNSUPPORTED_COMPLETION_MATCHES=0`.
- Exact narration gate-phrase count for `not claim|not been executed|remains gated`: `3`.
- `impact-evidence.md` cites every quantitative evidence value to original generated evidence or the final readiness record and explicitly excludes stale prospective success language from `hackathon-submission.md`.
- `shot-list.md` labels every shot as verified output, static evidence/implementation, or an unexecuted external-gate placeholder.

## Exact validation evidence

Final validation command checked file existence, normalized narration/SRT identity, word count, subtitle duration, unsupported-completion language, output hashes, readiness hash, and both repository diff checks.

```text
REQUIRED_FILE_COUNT=5
MISSING_FILE_COUNT=0
NARRATION_SUBTITLE_IDENTICAL=True
NARRATION_WORD_COUNT=356
SRT_START=00:00:00,000
SRT_END=00:03:22,000
SRT_DURATION_SECONDS=202
ESTIMATED_SECONDS_AT_130_WPM=164
ESTIMATED_SECONDS_AT_150_WPM=142
UNSUPPORTED_COMPLETION_MATCHES=0
NARRATION_GATE_PHRASE_COUNT=3
READINESS_SHA256=9A2CC85400BF7C84F64F1CEEDD08C7224403F585F511B8B1CCCD2E6DAE514381
CURA_DIFF_CHECK=CLEAN
WORKFLOW_DIFF_CHECK=CLEAN
```

No external CI, production signing, real Arm payload, installer lifecycle, GUI, physical Arm, performance, power, or publication gate was executed or claimed.

confidence: high

Justification: The package is source-traceable, exactly normalized, timed within the required range, independently hash-checked, and explicit about every unexecuted external gate.
