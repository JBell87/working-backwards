# Stage 2: Scans

Seven layers. Layers 1 to 4 read the repository. Layer 5 is in `cloud.md`. Layers 5 to 7 touch live systems and run only within the authorization record.

Dispatch one agent per scanner with `prompts/scanner.md`. Give each: the scanner, the target, the options allowed here, the raw output path, and the findings path. Check each tool's current documentation for exact flags; they change between versions, and this file deliberately describes what to ask of the tool, not the command line.

Every scanner must be configured to **write machine-readable output to a file** (JSON or SARIF) and to **redact secret values**.

## Layer 1: Code (static analysis)

**Semgrep**, with its maintained rule packs for the languages present plus its security-audit, secrets, and OWASP Top Ten packs. Language-agnostic by design: it selects rules by the files it finds.

Looks for: injection (SQL, command, template), unsafe deserialization, missing or broken authorization checks, weak cryptography, hard-coded credentials, path traversal, server-side request forgery, cross-site scripting, unsafe use of framework features.

## Layer 2: Secrets

**TruffleHog**, over the working tree **and the full git history**, with verification turned on so it distinguishes live credentials from dead ones.

Looks for: passwords, API keys, tokens, private keys, connection strings, in code, configuration, infrastructure code, and old commits.

A secret that was ever committed is compromised even if a later commit removed it. Verified live credentials are critical: tell the user as soon as the scanner reports one, without waiting for the rest of the review, so they can rotate it.

## Layer 3: Dependencies and images

**Trivy** (file system mode for dependencies, image mode for any container image the project builds) or **OSV-Scanner**. Run one; run both if the user wants a second opinion.

Looks for: third-party packages and base images with known vulnerabilities, with the fixed version where one exists.

## Layer 4: Infrastructure code

**Checkov**, or Trivy's configuration mode, over Terraform, CloudFormation, Bicep, Kubernetes manifests, Dockerfiles, and pipeline definitions.

Looks for, before anything is deployed: storage open to the public, missing encryption at rest or in transit, security groups and firewalls open to the internet, databases with public addresses, overly broad identity policies, logging disabled, containers running as root, secrets in configuration.

This layer finds the same problems as the cloud audit, earlier and with a file and line to fix. Where both report an issue, fix it here.

## Layer 5: Live cloud configuration

See `cloud.md`.

## Layer 6: Exposed network services (Standard and Thorough)

Only against hosts tied to the user's account in the authorization record.

**Nmap**: discover open ports and identify services on in-scope hosts. Use its default and "safe" script categories only. Never its brute-force, denial-of-service, exploit, or intrusive categories. Scan at a polite rate.

**testssl.sh** (or sslyze): TLS configuration on every in-scope port that speaks TLS.

Looks for: services exposed that should not be (databases, caches, admin interfaces, remote login open to the world), unencrypted protocols carrying application traffic, out-of-date TLS versions and weak ciphers, expired or mismatched certificates, missing redirect from plain HTTP, services that could be abused to amplify an attack on others (open resolvers, memcached or NTP reachable over UDP).

Compare what is found with `architecture.md`: every open port should be one the design intends.

## Layer 7: The running application

**OWASP ZAP baseline scan** (Standard): crawls the application and inspects responses passively. Sends no attack payloads.

Looks for: missing security headers, cookies without secure flags, information leaking in responses and error pages, mixed content, cross-origin misconfiguration, sensitive data sent in clear text.

**OWASP ZAP full scan** and **Nuclei** (Thorough only, and only on environments the record lists at that level): active checks that send test payloads.

- ZAP active scan at its default strength, with the test account if the application has a login.
- Nuclei with its maintained templates, **excluding** templates tagged for denial of service, brute force, fuzzing, or intrusive behaviour, at a low request rate.

Looks for: injection and cross-site scripting that static analysis missed, broken access control (can the test account read another account's data), known vulnerabilities in exposed software, default credentials pages and exposed admin panels, misconfigured servers.

Before an active scan, remind the user it may create junk data and trigger their alerts, and confirm the environment has a backup. Stop an active scan if the application starts returning errors it was not returning before, and tell the user.

## Resilience to overload (configuration review only)

There is no test that floods anything. Assess from what the other layers found and from the cloud configuration:

- Is there rate limiting on public endpoints, and on login and other expensive operations?
- Is there a content delivery network or managed firewall in front, and can the origin be reached directly, bypassing it?
- Is the provider's DDoS protection enabled at the tier the user intends?
- Do autoscaling limits, timeouts, connection limits, and request size limits exist, and is there a spending alarm so an attack does not become a bill?
- Are any amplification-prone services exposed (from Layer 6)?

Report this as a checklist with evidence for each answer. Say plainly that it is a review of configuration and that behaviour under real load was not tested.

## Coverage record

When the scanners return, write the coverage table in `state.md`: each layer, the tool, the target, run / partly run / not run, and the reason. A scanner that crashed, timed out, or produced no output file did not run. Retry it once; if it fails again, it is "not run".
