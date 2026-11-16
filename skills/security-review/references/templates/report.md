# Security review: <product>

<date>. Authorization: `authorization.md`, confirmed <date>.

## Summary

<Three or four sentences: what was reviewed, the most serious thing found, what was fixed, what remains open and on what terms.>

| Severity | Found | Fixed | Open, risk accepted | Open, not accepted |
|---|---|---|---|---|
| Critical | | | | |
| High | | | | |
| Medium | | | | |
| Low | | | | |

**Status:** <no open critical or high findings | complete, with accepted risks | complete, with open security findings>

## Coverage

| Layer | Tool and version | Target | Result | Notes |
|---|---|---|---|---|
| Code | | | run / partly run / not run | |
| Secrets | | | | |
| Dependencies and images | | | | |
| Infrastructure code | | | | |
| Cloud configuration | | | | |
| Network exposure | | | | |
| Running application | | | | |
| Overload resilience | configuration review | | | not load tested |

### Not tested

<Everything out of scope, declined, unavailable, or not run, and what that leaves unknown.>

## Security claims in the PR/FAQ

| Truth | Claim | Verified? | Evidence |
|---|---|---|---|

## Findings

Most serious first. For each:

### <ID> <title>: <severity>, <fixed | open, risk accepted | open, not accepted | open, awaiting decision>

- **Where:** <file and line, resource, or host and port>
- **What an attacker could do:** <one plain sentence>
- **Evidence:** <what shows it is real; no secret values>
- **Found by:** <scanners>
- **Fix:** <what was changed and the commit, or what the user must do>
- **If open:** <why it could not be fixed, mitigation in place, date to revisit>

## Accepted risks

<From `risk-acceptance.md`: each finding, when and in what words it was accepted, and the revisit date.>

## Recommendations

<A short ordered list: what to do next, including anything only the user can do, such as rotating credentials or applying cloud changes.>

## Limits of this review

This was an automated review using open-source scanners, within the scope and intensity recorded in the authorization. It finds known classes of weakness. It is not a full penetration test, did not test behaviour under load, and cannot show that no vulnerabilities exist. Rules and vulnerability databases change daily; results reflect the date above.
