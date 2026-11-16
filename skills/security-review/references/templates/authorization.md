# Security review authorization: <product>

**Authorized by:** <name>, <role or relationship to the systems>
**Date:** <date>   **Valid for scans until:** <date>

## In scope

| # | Target | Identifier | Environment | Intensity | Tied to account (how verified) |
|---|---|---|---|---|---|
| 1 | Repository | `<path or URL>` | - | static | - |
| 2 | AWS account | `<account id>`, regions `<list>` | production | passive (configuration audit) | identity check `<date>` |
| 3 | Application | `https://<host>` | staging | thorough | resolves to `<resource>` in target 2 |

## Out of scope

- <Third-party services the product uses, by name>
- <Anything the user excluded>

## What will run

- Static: code, secrets (including git history), dependencies and images, infrastructure code.
- Live, read-only: cloud configuration audit of targets <n>.
- Live, network: <port and service discovery, TLS checks> on targets <n>.
- Live, application: <passive scan | active scan with test payloads> on targets <n>.

## What will not run

No denial-of-service or load testing. No password guessing or cracking. No exploitation of findings, data extraction, or movement between systems. No changes to any live resource.

## Credentials

- Cloud: <read-only role or identity, by name; how supplied>. No secret values are recorded here.
- Application: <test account, by name>.

## Provider rules checked

| Provider | Policy consulted (link, date) | Relevant limits | Approval or notice needed? |
|---|---|---|---|
| <AWS> | <...> | <...> | <no / yes: obtained on ...> |

## Statements by the person authorizing

- I own, or am authorized by the owner to test, every target listed as in scope.
- I have read the provider rules above and this review stays within them.
- I understand that active scanning at the "thorough" level can create test data and trigger alerts, and that the environments listed at that level have recent backups.
- I understand this is automated scanning, not a full penetration test, and that a clean result is not a guarantee.

**Confirmed by the user:** "<their words>" on <date and time>
