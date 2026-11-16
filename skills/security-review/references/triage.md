# Stages 3 to 5: Verify, fix, and accept

## Stage 3: Verify and triage

Scanners over-report. An unverified list of five hundred findings is not a review; it is the raw material for one.

**De-duplicate first.** The same problem often appears from several layers (a hard-coded key from Semgrep and TruffleHog; an open port from Checkov, Prowler, and Nmap). Merge them into one finding that cites each source.

**Verify each finding** by dispatching verifier agents (`prompts/verifier.md`): Reasoning tier for anything a scanner rated critical or high, Standard for the rest, batched by area so no agent gets more than about twenty. A verifier reads the code or configuration the finding cites and decides:

- **Confirmed**: the weakness is real and reachable.
- **Not reachable**: the pattern is present but cannot be triggered (a vulnerable function in a dependency that is never called, a rule on a resource that has no route to the internet). Keep it, at low severity.
- **False positive**: the scanner is wrong. Record why.
- **By design**: real, intended, and consistent with the architecture (a public website bucket). Record why.

Verification means reading and reasoning, plus at most a single harmless request that shows the condition exists. It never means exploiting the weakness. If a finding can only be confirmed by exploiting it, record it as "likely, not confirmed" and rate it as if it were real.

**Rate each confirmed finding yourself** from two things: what an attacker gains, and how easily.

| Severity | Meaning |
|---|---|
| **Critical** | Anyone on the internet can read or change data, take over an account or the system, or use a live credential, with no special access. Fix now. |
| **High** | Serious impact but needs something first (a logged-in account, a specific condition), or moderate impact that is trivially reachable. |
| **Medium** | Limited impact, or needs unlikely conditions. Weakens defence in depth. |
| **Low** | Hardening and hygiene. |

Scanner severities are an input, not the answer; adjust for this system and say why when you differ.

Write everything to `docs/security/<slug>/findings.md`: one entry per finding with an ID, severity, status, where it is, what an attacker could do in one plain sentence, the evidence, and the sources. No secret values.

**Tell the user immediately**, without waiting for the rest of the review, about any verified live credential, any data store open to the public, and anything suggesting the system has already been compromised.

## Stage 4: Fix

Attempt every critical and high finding. Fix medium and low findings only where the change is small and safe; otherwise report them.

How a fix is made depends on where the problem lives:

- **Code and infrastructure code.** If this review follows a build, write a gap plan and use the build's fix loop and reviews (`build-from-prfaq`, `references/review.md`). Otherwise use the same pattern directly: a fresh implementer writes a test that demonstrates the weakness, fixes it, and shows the test passing; a fresh reviewer confirms the fix closes the finding and does not just hide the symptom; same implementer for three rounds, then a stronger model or higher effort for two more.
- **Dependencies.** Upgrade to the fixed version and run the full test suite. If no fixed version exists, or the upgrade breaks the product, that is "cannot fix now": record the mitigation, if any.
- **Committed secrets.** Removing the secret from the code does not fix it. The fix is the user rotating the credential; say so directly and treat the finding as open until they confirm they have. Then remove it from the code and move it to a secrets manager. Rewriting git history is the user's decision, and optional once the credential is dead.
- **Live cloud configuration.** Propose the change; the user applies it (`cloud.md`).
- **A fix that would change what the product does** (remove a feature, change who can see what) is a PR/FAQ deviation when this follows a build. Ask the user.

**Re-scan after fixing.** Re-run the scanners that reported each fixed finding, on the affected target only, and mark the finding fixed only when the scanner no longer reports it and the verifier agrees. Then run the project's full test suite: a security fix that breaks the product is not finished.

Never mark something fixed by suppressing the rule, excluding the file from scanning, or lowering its severity.

## Stage 5: Risk acceptance

Some critical and high findings will not be fixable now: no patched version exists, the fix needs a redesign, it depends on a third party, the fix loop ran out of rounds. These do not block completion. They do require the owner's informed, explicit decision.

For each such finding, present to the user:

1. What it is, in plain words, and where.
2. What an attacker could do with it, and how likely that is for this system.
3. What was tried, and why it could not be fixed.
4. Any mitigation that reduces the risk in the meantime, and whether it has been applied.
5. What fixing it properly would take.

Then ask them to confirm, finding by finding, that they understand the risk and accept it for now. Do not bundle them into one yes; do not accept "fine, whatever" for a critical finding without restating what is being accepted and getting a clear answer.

Record each acceptance in `docs/security/<slug>/risk-acceptance.md`: the finding, the date, what the user said, any mitigation, and a date to revisit it.

- A finding the user **accepts** is reported as "open, risk accepted".
- A finding the user **declines to accept** stays "open, not accepted". Offer to keep working on it. The review, and any build it belongs to, is then reported as complete with open security findings.
- **You never accept a risk on the user's behalf**, and silence is not acceptance. In an unattended run, leave these as "open, awaiting decision" and put them at the top of the report.

## Stage 6: Report

Write `docs/security/<slug>/report.md` from `templates/report.md`, and give the user its summary: what was tested, what was not, what was found, what was fixed, what remains and on what terms.
