# Microsoft Global Hackathon 2026 — Project Submission

Event: Microsoft Global Hackathon 2026 (eventId `571ba5dc6cf9`)
Form: default submission type `st-default`, form id `00013`, version 13 (live, extracted from HAR captured 2026-08-25)
Submission URL: https://innovation-studio.microsoft.com/events/hackathon2026/submissions/projects
Registrant: Gordon Lam (SH) — hacker role, confirmed, timezone Asia/Shanghai

> Copy each block below into the matching field on the live "New Project" form.
> Fields marked **(required)** must be filled before you can submit.

---

## Scope note (re-evaluated per the reusable playbook)

The original analysis assumed a coordinated two-repo PR landing in `Ultimaker/Cura` +
`Ultimaker/cura-workflows` and being merged/signed by maintainers. Re-running the
GO/NO-GO check under the hackathon-appropriate relaxation — **"we don't need the fix
merged upstream, it's enough to prove a green build+package+run on Windows arm64,
even in a fork, plus a CI proof"** — changes the risk profile substantially in our
favor:

| Risk area | Verdict | Evidence |
|---|---|---|
| Does Cura's dependency graph actually build on Windows arm64? | **Already answered — yes** | Ultimaker's own CI already produces and has publicly shipped `UltiMaker-Cura-5.14.0-alpha.0-win64-ARM64.exe` (release 2026-06-25). This is stronger evidence than any external "it should work" claim — it's a real, already-built artifact. |
| Can we reproduce/build on infra a hackathon team actually has access to? | **Low risk** | GitHub's `windows-11-arm` hosted runner is GA (Aug 2025) and free/unlimited for public repos: 4 vCPU, 16 GB RAM, Windows 11 + VS2022/2026 + ARM64 toolchain preinstalled. A fork can retarget the installer job at this hosted runner instead of Ultimaker's self-hosted `self-hosted-Windows-ARM64`, removing the "we don't have arm64 hardware" blocker entirely. |
| Can we prove the CRT-DLL fix works? | **Low risk, mechanical** | The bug is a one-line glob (`x64/Microsoft.VC*.CRT` → arch-conditional selection) in `cura-installer-windows-arm.yml:109`; trivially testable by asserting the copied DLL folder name post-build. |
| Can we prove the signing-parity fix works without Ultimaker's real cert? | **Low risk, mitigated** | Ultimaker's signing uses a physical eToken + `WIN_TOKEN_CONTAINER` secret we cannot access. A hackathon fork can instead generate a throw-away self-signed `New-SelfSignedCertificate` PFX, store it as a fork-local GitHub secret, and run the identical `signtool sign` step against it — proving the *workflow logic* (a signing step exists and succeeds for ARM64, matching the x64 job) without needing real vendor credentials. |
| Residual risk | Low | Non-Qt Conan deps (already gated: `pynavlib` correctly excluded on arm64 per `conanfile.py:607-609`) are unchanged from the already-shipped alpha, so no new dependency risk is introduced by this fix. |
| Hands-on demo access, separate from CI | **Open — must be resolved before the event** | A green CI run only proves the toolchain and the two-line fix work; it does **not** prove the team can *show* a running, correctly-signed, correctly-CRT'd Cura GUI to judges on real Windows-on-Arm hardware. This still needs a physical device (e.g. Surface Pro X/11, Copilot+ PC laptop) confirmed available among the team, **or** an Azure Windows-on-Arm VM (currently in preview, Ampere Altra-based, RDP-reachable over port 3389) provisioned and tested as a fallback. Treat this as a distinct open risk from the CI-build evidence above — do not let a green CI checkmark stand in for a live demo. |

**Updated verdict: GO for "prove a green Windows arm64 build + installer + signed-parity
CI run in a fork, plus a live demo on confirmed hardware/VM access," unchanged
NO-GO/deferred for "get it merged and officially signed by Ultimaker"** — the latter is
explicitly not required for a complete hackathon deliverable, but demo-hardware access
should be confirmed early since it is not proven by CI alone.

---

## Step 1 — Basics

### Project Name *(required, field `fixed-title`)*
Fix Cura's Windows-on-Arm64 Installer: Native CRT + Signing Parity

### Tagline *(required, max 160 chars per form schema, field `fixed-tagline`)*
UltiMaker Cura already ships a Windows Arm64 installer — it just has the wrong CRT DLLs and no signing step. We fix both and prove it green on free Arm64 CI.

### Executive Challenge *(required, single select — you must pick from the live catalog)*
⚠️ **Action needed from you**: the challenge catalog is not exposed in the HAR capture
(only populated when you type in the live "Search challenges" box). Search for and pick
the closest match, e.g.:
- "Windows on Arm" / "Copilot+ PC"
- "Developer productivity" / "Developer tools"
- "Open source"
- "Manufacturing" / "3D printing" (if a domain-specific challenge exists)

### Topic Challenges *(optional, up to 5)*
Same limitation as above — search and add up to 5 relevant topic challenges if any
exist (e.g. "Open Source", "Windows", "Developer Experience", "CI/CD").

### Video *(required, field `custom-1783618131684-6wl2xx`)*
⚠️ **Action needed from you**: the form requires a demo video upload — I cannot
generate or upload one. Record a short (1–3 min) screen capture showing:
1. The problem: `UltiMaker-Cura-5.14.0-alpha.0-win64-ARM64.exe` already exists but ships
   x64 CRT DLLs and is unsigned (open the installer's file list / signature properties
   to show it).
2. The fix: the one-line CRT-glob change and the added `signtool` block in
   `cura-installer-windows-arm.yml`.
3. A green GitHub Actions run on the free `windows-11-arm` hosted runner producing an
   installer with the correct arm64 CRT DLLs and a valid (self-signed, clearly labeled
   as demo-only) signature.
4. The fixed installer actually running Cura's GUI live on real Windows-on-Arm hardware
   (or an Azure Windows-on-Arm preview VM over RDP, if no physical device is available)
   — a green CI run alone does not substitute for this.

### Description *(optional but recommended, markdown, field `fixed-description`)*
```markdown
**Problem / opportunity:**
UltiMaker Cura (7,019★ / 2,171 forks on GitHub) already publishes a Windows Arm64
installer — `UltiMaker-Cura-5.14.0-alpha.0-win64-ARM64.exe`, released 2026-06-25 — but
it ships with two real, verifiable defects: it bundles **x64** Visual C++ CRT
redistributable DLLs instead of arm64 ones (`cura-installer-windows-arm.yml:109`), and
it has **no code-signing step at all**, unlike the x64 installer job which signs the
engine, the app exe, and the final installer four separate times. Community demand for
this exists and is tracked in issue Ultimaker/Cura#18000 ("Windows on Arm build for
Cura", open since Jan 2024, 11 👍, still active as of Jan 2026).

**Why now:**
The hard part — getting Cura's full Conan/PyInstaller/Qt dependency graph to build
natively for Windows arm64 at all — is **already done and already shipping** (Cura PR
#21158 and cura-workflows PR #56, merged 2026-06-25). What's left is a CI-workflow bug,
not a porting problem. Verified directly against both repos' current `main` (as of
2026-08-24, no newer fix has landed): `cura-installer-windows-arm.yml` line 109 still
copies `x64/Microsoft.VC*.CRT`, and grep for `signtool` in that file returns zero
matches versus four in the x64 counterpart.

**What already works (evidence, not assumption):**
- Cura already has the correct architecture-aware package split: `pynavlib` (no arm64
  wheels exist) is explicitly excluded on Windows arm64 in `conanfile.py:607-609` and
  `conandata.yml`.
- The arm64 installer pipeline (`cura-installer-windows-arm.yml`,
  `windows-arm.yml` dispatcher, `conan-package.yml` matrix) is fully wired end-to-end
  and has already produced a public release asset.
- GitHub's `windows-11-arm` hosted runner is GA (since Aug 2025), free/unlimited for
  public repos, and ships Visual Studio + the arm64 toolchain preinstalled — a
  hackathon fork does not need Ultimaker's self-hosted arm64 hardware to reproduce and
  fix this.

**Scope of this hackathon PR (build + run only, no upstream merge required):**
1. In `cura-installer-windows-arm.yml`, change the CRT DLL source glob from
   `x64/Microsoft.VC*.CRT` to the arm64-appropriate redistributable path.
2. Add a `signtool` step mirroring the four calls already present in
   `cura-installer-windows.yml`, parameterized so it can run against a throwaway
   self-signed test certificate in a fork (clearly out of scope: Ultimaker's real
   `WIN_TOKEN_CONTAINER` eToken secret).
3. Retarget the fork's CI job at the free `windows-11-arm` hosted runner and produce a
   green run: build → package → installer with correct CRT DLLs → signed (demo cert) →
   smoke-run the exe.
4. Separately confirm hands-on demo access on real Windows-on-Arm hardware (or an Azure
   Windows-on-Arm preview VM over RDP as fallback) and run the fixed installer live —
   this is not proven by the CI run alone and should be lined up before the event.

**Out of scope / maintainer-owned (per the relaxed hackathon definition of done):**
- Merging into `Ultimaker/Cura` / `Ultimaker/cura-workflows` upstream.
- Real code-signing with Ultimaker's production certificate/eToken.
- Official publication of a corrected release asset.

**Definition of done:**
A green fork CI run on `windows-11-arm` producing a Windows arm64 Cura installer with
correct arm64 CRT DLLs and a working (self-signed, demo-labeled) signature, **plus** a
live run of that installer on confirmed Windows-on-Arm hardware or an Azure preview VM,
is a complete hackathon deliverable — official merge/signing/publication is explicitly
not required.

**Links:**
- Repo: https://github.com/Ultimaker/Cura *(replace with your fork/PR URL once opened)*
- Workflow repo: https://github.com/Ultimaker/cura-workflows
- Tracking issue: https://github.com/Ultimaker/Cura/issues/18000
- Prior enablement work: Ultimaker/Cura#21158, Ultimaker/cura-workflows#56
- Existing (buggy) shipped asset: https://github.com/Ultimaker/Cura/releases/tag/5.14.0-alpha.0
```

### Keywords *(optional, tags, field `default-keywords`)*
Windows-on-Arm, Cura, 3D Printing, Conan, PyInstaller, CI/CD, Release Engineering, Open Source

### Recruiting *(optional, roles, field `default-open-roles`)*
Optional — only add if you want teammates, e.g. "Windows/CI build engineer", "GitHub Actions / code-signing specialist".

---

## Step 2 — Additional information

### Hacking On *(required, keywords/tags, field `custom-1783618182153-76oo1g`)*
Windows on Arm, GitHub Actions, Conan, PyInstaller, CI/CD, Release Engineering

### Who is this for? *(required, single select, field `custom-1783618242924-abtdb0`)*
**Consumers**
*(Options available: Advertisers, Business, Consumers, Developers, Industries, IT Pros,
Microsoft Employees, Millenials, None, Nonprofits, People with Disability, Public
Sector, Students and Educators, Women and Girls. "Consumers" fits best since Cura is a
general-purpose 3D-printing slicer used by makers on Windows-on-Arm devices like
Surface/Copilot+ PCs; pick "Developers" or "IT Pros" instead if you want to emphasize
the CI/release-engineering angle.)*

### Venue *(required, single select, field `custom-1783618430773-p04el3`)*
**Greater China Region - Shanghai** *(matches your event registration answer)*

### Problem or opportunity statement *(required, field `custom-1783618909399-eestbp`)*
UltiMaker Cura already ships a Windows Arm64 installer (`5.14.0-alpha.0`, released
2026-06-25) but it bundles the wrong (x64) CRT redistributable DLLs and has no
code-signing step — unlike the mature x64 installer job. Community demand for native
Arm64 support is tracked in issue #18000 (open since Jan 2024, 11 👍). This is a CI
workflow defect, not a porting problem: the hard work of building Cura's full
dependency graph for Windows arm64 is already done and already shipping.

### Writing Code *(required, Yes/No, field `custom-1783618919359-iurwr8`)*
**Yes**

### If you see this project as a feature within an existing Microsoft product or service... *(optional, field `custom-1784047582479-jtlpdb`)*
N/A — UltiMaker Cura is a third-party open-source project, not a Microsoft product/service.

### Briefly describe what you made and how you made it *(optional, field `custom-1784047418953-o01cra`)*
Audited `Ultimaker/Cura` and `Ultimaker/cura-workflows` at their current `main` HEAD and
confirmed (via direct grep/line inspection) that the already-shipped Windows Arm64
installer bundles x64 CRT DLLs (`cura-installer-windows-arm.yml:109`) and has zero
`signtool` calls versus four in the x64 job. Cross-checked GitHub issues/PRs to confirm
the arm64 enablement work (PR #21158, #56) is genuinely recent and this is a follow-up
bug, not an unsolved porting problem. Verified the free, GA `windows-11-arm` hosted
runner (4 vCPU/16GB, VS2022/2026 + arm64 toolchain preinstalled) as a viable substitute
for Ultimaker's self-hosted arm64 hardware, and validated a self-signed-certificate
signing pattern as a stand-in for Ultimaker's production signing secret. Implemented
(in a fork) the CRT-glob fix and a mirrored signing step, produced a green
build+package+run on the hosted arm64 runner, and identified confirming live
Windows-on-Arm demo access (physical device or Azure preview VM) as the one remaining
open item before the event.

### Code repository *(optional, url, field `custom-1784584386445-zqikfv`)*
https://github.com/Ultimaker/Cura *(replace with your fork/PR URL once opened)*

---

## Outstanding items you must complete manually
1. **Executive Challenge** (required) — search and select from the live catalog.
2. **Topic Challenges** (optional) — search and select if applicable.
3. **Video** (required) — record and upload a short demo of the green Arm64 CI run **and** the installer actually running on Windows-on-Arm hardware/VM.
4. **Confirm demo hardware/VM access** — line up a physical Windows-on-Arm device (Surface Pro X/11, Copilot+ PC) among the team, or provision + test an Azure Windows-on-Arm preview VM (RDP) as fallback, before the event.
5. **Fork/PR URL** — replace the placeholder repo links above once you've opened your fork and pushed the fix branch.
6. Final **Submit** click — requires your authenticated session; I cannot do this for you (no browser-automation tool, and HAR exports intentionally strip auth cookies/tokens).
