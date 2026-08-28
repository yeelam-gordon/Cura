# Windows Arm64 test and video execution prompt

Run this prompt in GitHub Copilot CLI on a native Windows Arm64 machine. Start
Copilot from an empty parent directory with permissions to clone repositories,
run GitHub Actions commands, launch Cura, capture the desktop, and write
evidence.

```text
You are the Windows Arm64 validation and demo owner for the Cura hackathon.
Work autonomously, but never claim a test, signature, GUI action, performance
result, or publication unless you retain direct evidence for it.

Authoritative revisions:
- Cura implementation C:
  936c23370ec0142356c494dd9c7f29373995171f
- Cura immutable validation V:
  22382e42f0a2cd9127d9257c47abd8beb81d079d
- cura-workflows upstreamable implementation W:
  e6b5333134b94c2d97e6d6705f1d2f2f920ad75a
- cura-workflows fork-only validation WF:
  cae8fdfedf63b48f0bb94647948f167c67d69b1a
- Cura validation branch:
  CURA-arm64-proof-936c2337
- Cura demo/evidence branch:
  hackathon/windows-arm64-demo
- cura-workflows validation branch:
  hackathon/windows-arm64-validation
- Fork owner:
  yeelam-gordon

FIRST — establish exact source identity:
1. Verify this is native Windows Arm64:
   - `$env:PROCESSOR_ARCHITECTURE` must be `ARM64`.
   - Record `Get-CimInstance Win32_OperatingSystem`.
   - Record Python executable, version, and
     `[System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture`.
2. Clone:
   - `https://github.com/yeelam-gordon/Cura.git`
   - `https://github.com/yeelam-gordon/cura-workflows.git`
3. In Cura, fetch and checkout `hackathon/windows-arm64-demo`. Verify commit
   ancestry contains V and C exactly.
4. In cura-workflows, checkout `hackathon/windows-arm64-validation` and verify
   HEAD equals WF exactly and has W as its parent.
5. Abort on any SHA mismatch. Write all identity evidence under:
   `Cura\Generated Files\demo\evidence\source-identity.txt`.

LOCAL VALIDATION:
1. Read and follow
   `Cura\Generated Files\windows-arm-build-test-guide.md`.
2. Run the complete Cura packaging suite and cura-workflows test suite.
3. Parse every changed YAML file and run all matrix uniqueness checks.
4. Run `workflow_provenance.py validate-callers` against V and WF. The checked
   out demo branch is later than V, so perform this check in a detached worktree
   at V; do not rewrite or amend V.
5. Capture commands, exit codes, stdout, and stderr under
   `Generated Files\demo\evidence\local-validation\`.

GITHUB CI PROOF:
1. Inspect the push-triggered `conan-package.yml` run for repository
   `yeelam-gordon/Cura`, branch `CURA-arm64-proof-936c2337`, and exact commit V.
2. If it is still running, watch it. If it failed, retain logs and diagnose the
   first root-cause failure. Do not hide missing Conan credentials, unavailable
   packages, runner limits, or fork permission failures.
3. If package CI succeeds, download and verify its provenance chain. Confirm
   C/V/WF identities and record the package reference, run ID, and attempt.
4. The installer workflow requires a native Arm payload runner plus a secure
   X64 signing runner. Dispatch it only if those exact runner labels and required
   secrets are configured in the fork. Never substitute production-signing
   claims with a self-signed certificate.
5. If production infrastructure is unavailable, keep it as an explicit external
   gate. You may perform a separately labeled `DEMO SELF-SIGNED` local signing
   exercise, but it must never be described as trusted or production signed.
6. Save run URLs, downloaded contracts, logs, and hashes under
   `Generated Files\demo\evidence\ci\`.

NATIVE APPLICATION ACCEPTANCE:
1. Use a verified Arm64 installer or unpacked payload from the exact proof chain.
   Do not use an unrelated public build as evidence for this change.
2. Verify PE machine type for Cura, CuraEngine, Python DLLs, PYDs, Qt DLLs, and
   bundled CRT files before launch.
3. Exercise and record:
   - clean install;
   - Cura launch and About/version evidence;
   - load a small known model;
   - slice it;
   - preview layers;
   - export G-code;
   - close and restart;
   - upgrade/coexistence behavior if a prior Cura version is available;
   - uninstall for both EXE and MSI where artifacts exist.
4. Compare correctness with x64-emulated Cura only if the same model/profile and
   version can be used. Do not invent performance or power comparisons.
5. Save logs, screenshots, exported G-code hashes, and architecture reports under
   `Generated Files\demo\evidence\native-arm64\`.

SCREEN CAPTURE:
1. Prefer an existing trusted screen recorder on the machine. If none exists and
   `ffmpeg` supports `gdigrab`, capture the desktop while launching Cura and
   completing the short slice/export path.
2. Produce
   `Generated Files\demo\evidence\native-arm64\cura-arm64-demo.mp4`.
3. Keep the clip concise and readable. Remove unrelated windows and notifications.
4. Do not record credentials, tokens, private package URLs, or signing secrets.

SLIDECAST VIDEO:
1. Invoke the `slidecast` skill. If it is not registered, read:
   `C:\Users\yeelam\OneDrive - Microsoft\Documents\.copilot\skills\slidecast\SKILL.md`
   and follow it literally.
2. Treat these checked-in files as the validated story/evidence plan:
   - `Generated Files\demo\demo-script.md`
   - `Generated Files\demo\shot-list.md`
   - `Generated Files\demo\narration.txt`
   - `Generated Files\demo\subtitles.srt`
   - `Generated Files\demo\impact-evidence.md`
3. Copy the complete Slidecast `templates` package into
   `Generated Files\demo\slidecast\`; do not copy only `deck.html`.
4. Author an engineering-focused animated HTML deck. Preserve the planned
   sequence: problem, manager/worker evidence chain, implemented controls,
   native proof, ecosystem leverage, honest limitations.
5. Replace every `EXTERNAL GATE — NOT EXECUTED` placeholder only when the
   corresponding retained evidence exists. Otherwise leave it visible.
6. Create a storyboard whose narration matches the final spoken script. Embed
   `cura-arm64-demo.mp4` when available; use `pauseDeck:true` while it plays.
7. Build through the installed Slidecast `scripts\build.py` pipeline. Produce:
   - `Generated Files\demo\slidecast\deck.html`
   - `Generated Files\demo\slidecast\storyboard.json`
   - `Generated Files\demo\slidecast\build\final.mp4`
   - soft subtitles and a burned-subtitle MP4 variant.
8. Sample rendered frames at slide midpoints. Verify no clipping, no subtitle
   collision, readable evidence labels, deterministic capture resources, and
   exact narration/subtitle identity.

FINAL EVIDENCE COMMIT:
1. Update `impact-evidence.md`, `demo-script.md`, narration, and subtitles only
   from retained proof.
2. Write `Generated Files\demo\evidence\RESULT.md` containing:
   - exact C, V, W, and WF;
   - machine identity;
   - every command and exit code;
   - CI run URLs and conclusions;
   - artifact hashes;
   - native acceptance results;
   - what was not tested and why;
   - final video paths and duration.
3. Commit only evidence/demo changes to a new branch based on
   `hackathon/windows-arm64-demo`, then push it to the fork. Do not amend C, V,
   W, or WF.
4. End with one verdict:
   - `DEMO READY`;
   - `LOCAL PROOF ONLY — EXTERNAL CI/HARDWARE GATE`;
   - `BLOCKED`, with the first reproducible blocker.
```

## Expected starting command

```powershell
New-Item -ItemType Directory -Force C:\s\Demo\Hack2026-Arm64 | Out-Null
Set-Location C:\s\Demo\Hack2026-Arm64
copilot --yolo --experimental --autopilot -i "Read and execute the complete prompt from https://raw.githubusercontent.com/yeelam-gordon/Cura/hackathon/windows-arm64-demo/Generated%20Files/ARM64-TEST-AND-VIDEO-PROMPT.md"
```

The ARM64 machine must have GitHub CLI authentication for the fork. Production
signing credentials must not be copied to an untrusted machine.
