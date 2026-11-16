# Stage 1: Scope and authorization

Nothing is scanned until this stage is complete. Scanning systems without permission is illegal in most places, and scanning a cloud provider's platform outside its rules can get the user's account suspended. The authorization record protects the user as much as anyone else.

## 1. Work out what there is to review

From the repository, the build's `architecture.md` if there is one, and the user:

- The repository and any container images it builds.
- Infrastructure code (Terraform, CloudFormation, Bicep, Pulumi, Kubernetes manifests, Dockerfiles).
- Cloud accounts the product is deployed in: AWS accounts, Azure subscriptions, GCP projects, DigitalOcean teams. Get the identifier of each.
- Public entry points: hostnames, IP addresses, URLs, APIs.
- Environments: which of these are production, and whether a staging copy exists.

## 2. Check the provider's rules

For each cloud provider in scope, look up its current penetration testing policy (search for it; do not rely on memory, these change) and note in the record: which services may be tested without prior approval, what is prohibited, and whether notice is required. Every major provider prohibits denial-of-service testing; this skill does none.

If the policy requires approval or notice for something in scope, the user must obtain it before that scan runs.

## 3. Choose the intensity

Offer three levels and recommend one. The user chooses.

| Level | What runs against live systems | Suited to |
|---|---|---|
| **Passive** | Read-only cloud configuration audit. No traffic sent to the application beyond ordinary requests. | Production, when the user wants no risk at all |
| **Standard** (recommended) | Passive, plus port and service discovery, TLS checks, and a passive web scan that observes responses without sending attack payloads. | Production |
| **Thorough** | Standard, plus an active web scan and template-based vulnerability checks that send test payloads. These can create junk records, trigger alerts, and in rare cases upset a fragile service. | Staging, or production with the user's explicit agreement and a recent backup |

Static scans of the repository run at every level.

If a staging environment exists, recommend running Thorough there and Standard on production.

## 4. Credentials

- **Cloud accounts: read-only.** Ask the user to provide a role or identity limited to security auditing, following the scanner's current documentation for the minimum permissions. As a guide at the time of writing: on AWS the managed policies SecurityAudit and ViewOnlyAccess; on Azure the Reader and Security Reader roles; on GCP the Viewer and Security Reviewer roles; on DigitalOcean a read-only token. If the credentials supplied can write, say so and ask for narrower ones; do not proceed on the promise that you will only read.
- **The application:** if it has a login, ask for a dedicated test account, never a real user's.
- **How they are supplied:** through the environment, a named profile, or the provider's own login command, set up by the user in their terminal. Never ask for a secret to be pasted into the conversation, and never write one to a file.

## 5. Write the record and get confirmation

Fill in `templates/authorization.md` and save it as `docs/security/<slug>/authorization.md`. Then show it to the user and ask them to confirm it, in so many words. A general "go ahead" given before they have seen the record is not confirmation.

The record states: who is authorizing, the date, every target by identifier, what is excluded, the intensity level per environment, the scan window, and the user's statements that they own or are authorized to test each target and have checked the provider rules.

**Authorization is specific and it expires.** It covers the listed targets at the listed intensity during the listed window. A new target, a higher intensity, or a later date needs a new confirmation. Re-scans after fixes within the window are covered.

## 6. Tie every live target to the user's account

Before any traffic is sent to a hostname or address, verify from the cloud side that it belongs to an account in the record. Using the read-only credentials:

- Confirm the identity you are using belongs to the listed account, subscription, or project.
- For each hostname or address in scope, find the resource it points to in that account: a load balancer, an instance's address, a distribution, a DNS record in a zone the account hosts.

Record the match in the authorization file. If a target cannot be tied to an authorized account (it resolves to an address the account does not hold, or sits behind a third party's network), do not scan it. Tell the user what you found and ask. A target reached through a content delivery network or managed front door is tested as that provider's policy allows, which generally means the user's own configuration and origin, not the provider's shared edge.

Targets that are not in a cloud account (a server elsewhere) need the user to state in the record how they control it.

## What to do if the user declines or cannot authorize something

Leave it out, record it under "not tested" in the report, and carry on with the rest. Never narrow the record after the fact to match what was actually scanned.
