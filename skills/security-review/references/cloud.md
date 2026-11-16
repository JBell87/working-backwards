# Layer 5: Live cloud configuration

A read-only audit of what is deployed, through the provider's own interfaces, using the audit credentials from the authorization record. It sends no traffic to the application and changes nothing, so it runs at every intensity level.

Confirm the identity in use is the review identity from `permissions.md` and belongs to the account in the record before running anything. If the credentials can write, stop and ask for read-only ones.

**Only resources in `scope.md` are evaluated.** Run the scanner with its filters set to the in-scope regions, subscription or project, and resources (by identifier or by the `wb-build` tag), and drop any result for a resource that is not on the list before triage. Account-wide settings are evaluated only if the user opted in.

## AWS, Azure, Google Cloud

**Prowler**, one run per account, subscription, or project in the record, limited to the regions and resources in scope, with output in JSON. Use its default checks; add a compliance framework only if the user asks for one.

Give each run its own agent. Prowler's output is large: the agent keeps the raw file in `raw/` and normalizes only failed checks.

## DigitalOcean and anything else

Check Prowler's current list of supported providers first; it grows. If the provider is not supported:

- Run Layer 4 over the infrastructure code, which covers most of the same ground.
- Use the provider's own command-line tool, read-only, to list resources and check them against the areas below by hand.
- Mark this layer "partly run" in the coverage table and say which areas were checked by hand. Do not present a manual checklist as equivalent to a full audit.

## What the audit must cover

Whichever tool runs, the findings should let you answer each of these for the resources in scope. Skip an area that has no in-scope resources, and mark the identity area as account-wide unless the user opted in. If the tool gives no answer for an area, say so in the coverage record.

| Area | Questions |
|---|---|
| **Storage** | Is any bucket, container, or space readable or listable by the public? Is encryption at rest on? Is access logged? Are there public snapshots, disk images, or backups? |
| **Identity and access** | Is multi-factor authentication on for people, and the root or owner account locked down? Are there long-lived access keys, unused identities, or policies granting everything on everything? Can any identity escalate its own permissions? |
| **Network** | Which resources are reachable from the internet, and should they be? Are remote login and database ports open to the world? Are databases, caches, and queues on private networks only? |
| **Encryption in transit** | Do load balancers, gateways, and distributions accept unencrypted connections or outdated TLS? Do databases and caches require encrypted connections? |
| **Secrets** | Are credentials stored in a secrets manager, or sitting in instance user data, function environment variables, container definitions, or parameter stores in clear text? Are keys rotated? |
| **Data stores** | Are databases publicly addressable? Are backups on and encrypted? Is deletion protection on? |
| **Compute** | Can the instance metadata service be read by a request forged through the application (is the hardened version enforced)? Are functions and containers running with more permissions than they need? Are images and runtimes out of date? |
| **Logging and detection** | Is audit logging on in every region, and protected from deletion? Are the provider's threat detection and configuration recording services on? Does anyone get alerted? |
| **Resilience** | Is DDoS protection enabled at the intended tier? Is there a firewall and rate limiting at the edge? Are there spending alarms? |
| **Functions and serverless** | Do functions hold secrets in their environment or configuration? Are their endpoints public without authentication? Are their roles broader than the function needs? |
| **Service identities** | Do service accounts, managed identities, or instance roles carry more access than the workload uses? Are there long-lived keys for them? Can one workload act as another? |
| **Source and artifacts** | Are code repositories, container registries, or build artifacts hosted in the account readable by the public? |
| **Kubernetes**, if used | Is the control plane public? Are workloads privileged? Are secrets encrypted? Is network policy in place? |

## Reading the results

- Prowler reports hundreds of checks. Normalize failures only, grouped by resource, and carry Prowler's severity as a starting point for triage, not as the answer.
- Relate findings to `architecture.md`. A public bucket that serves the product's website is by design; a public bucket holding database backups is critical. The scanner cannot tell these apart, and you must.
- A resource that exists in the account but not in the architecture or infrastructure code is a finding in its own right: nobody is maintaining it.

## Fixing

Never change a live resource. For each finding to be fixed:

- If the resource is defined in infrastructure code, the fix is a change to that code, made through the normal fix process and applied by the user's own deployment.
- If it is not, write the exact change for the user to make (console steps or a command), and tell them to bring the resource under infrastructure code.

After the user reports a fix is deployed, re-run only the affected checks.
