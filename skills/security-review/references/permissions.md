# Resource scope and audit permissions

Part of Stage 1. Two things are settled here before the authorization record is written: exactly which cloud resources will be evaluated, and the read-only identity the audit will use. You prepare both; the user creates the identity. You never create, change, or delete an identity or policy yourself.

## 1. The resource scope

The review evaluates a named set of resources and nothing else. It does not audit the rest of the account.

**After a build.** The scope is the resources that belong to the current build. Assemble the list from, in order of reliability:

1. Deployed infrastructure state: the resources in the build's Terraform state, CloudFormation or Bicep stack, Pulumi stack, or Kubernetes namespace.
2. The build's infrastructure code and `architecture.md`, for anything defined but not found in state (say so; it may not be deployed).
3. The build's tag. Builds tag every resource they define with `wb-build=<slug>`; use it to confirm the list and to catch resources created indirectly.

**Direct invocation.** The scope is exactly what the user specifies: resource identifiers (ARNs, Azure resource IDs, GCP resource names), a resource group, a project, a tag, a stack, or hostnames. Ask until the list is concrete. "Everything in the account" is accepted only if the user says it in those words, and is recorded as such.

Write the result to `docs/security/<slug>/scope.md`: one row per resource with its identifier, type, platform, region, and where it came from. Show it to the user. It becomes part of the authorization record, and a resource not on it is not evaluated.

**Account-wide settings** (root or owner account protection, password policy, account-level audit logging, tenant identity settings) are not resources of the build. Leave them out by default. Offer them as an explicit opt-in, because they affect the build's security but belong to the whole account; if the user opts in, list them in `scope.md` as a separate group.

## 2. How the scope is enforced

Three layers, because no single one is complete on every platform:

1. **Permissions** scoped as narrowly as the platform allows (section 4).
2. **Scanner filters**: run the audit against only the in-scope subscription, project, resource tag, or resource identifiers. Check the scanner's current help for its filter options before running.
3. **Result filter**: before triage, drop every result whose resource is not in `scope.md`. Do not verify, report, or keep notes on out-of-scope resources. Record only the count dropped, so the user knows the filter did something.

If a scan reveals something alarming outside the scope (a public data store that is not part of the build), do not investigate it. Tell the user in one sentence that something outside the scope may deserve a look, and leave it there.

## 3. Ask how the user wants the permissions delivered

Ask two questions, then generate.

**Form:**

- **Commands**: the command-line steps to run, in order, with a short note on what each does, plus the commands to remove everything afterwards.
- **Files**: policy and role definition files (and a CloudFormation or Terraform template if they prefer) written to `docs/security/<slug>/permissions/`, with a `README.md` that says what each file is, how to apply it in the console or with a tool, and how to remove it.

**Breadth** (where the platform gives a choice, chiefly AWS):

- **Standard**: the scanner's documented read-only permission set. Every check can run. The identity can read configuration across the account, but only in-scope resources are evaluated.
- **Strict**: a minimal policy built from `scope.md`, covering only the services in scope, limited to the specific resources wherever the platform supports it. The identity can see far less. Some checks will not be able to run and are reported as gaps.

Recommend Standard when the account holds only this product, and Strict when it is shared with other workloads.

## 4. What to generate, by platform

Before generating, read the scanner's current permissions documentation and the permission files in its repository, and build from those. The baselines below were correct when written and are the fallback; say in the hand-over which source you used and its date. Use the placeholders consistently and fill in every value you know from `scope.md`.

Common to every platform:

- Name the identity `wb-security-review-<slug>` so it is recognisable and easy to remove.
- Prefer short-lived access (role assumption, impersonation, a token with an expiry) over long-lived keys. If a key is unavoidable, tell the user to delete it when the review ends.
- Read-only actions only: get, list, describe, read. If a source file contains anything that writes, leave it out and tell the user.
- Always include the removal steps.
- Never include, request, or echo a secret value. The user runs the steps in their own terminal.

### AWS

Identity: an IAM role the user's own identity can assume, with a one-hour session.

*Standard*

- AWS managed policy `arn:aws:iam::aws:policy/SecurityAudit`
- AWS managed policy `arn:aws:iam::aws:policy/job-function/ViewOnlyAccess`
- Prowler's additional read-only policy, `permissions/prowler-additions-policy.json` in the Prowler repository, as an inline policy

Prowler also publishes a CloudFormation template for this role (`permissions/templates/cloudformation/prowler-scan-role.yml`); offer it when the user chose files.

Commands form:

```
# 1. Who am I? (gives the account id and the identity allowed to assume the role)
aws sts get-caller-identity

# 2. Trust policy: only that identity may assume the role
cat > trust.json <<'JSON'
{ "Version": "2012-10-17",
  "Statement": [{ "Effect": "Allow",
    "Principal": { "AWS": "<ARN from step 1>" },
    "Action": "sts:AssumeRole" }] }
JSON

# 3. Create the role and attach read-only permissions
aws iam create-role --role-name wb-security-review-<slug> \
  --assume-role-policy-document file://trust.json --max-session-duration 3600
aws iam attach-role-policy --role-name wb-security-review-<slug> \
  --policy-arn arn:aws:iam::aws:policy/SecurityAudit
aws iam attach-role-policy --role-name wb-security-review-<slug> \
  --policy-arn arn:aws:iam::aws:policy/job-function/ViewOnlyAccess
aws iam put-role-policy --role-name wb-security-review-<slug> \
  --policy-name prowler-additions --policy-document file://prowler-additions-policy.json

# 4. Use it: add a profile that assumes the role, then tell me the profile name
#    [profile wb-security-review]
#    role_arn = arn:aws:iam::<account id>:role/wb-security-review-<slug>
#    source_profile = <your profile>

# Remove afterwards
aws iam detach-role-policy --role-name wb-security-review-<slug> --policy-arn arn:aws:iam::aws:policy/SecurityAudit
aws iam detach-role-policy --role-name wb-security-review-<slug> --policy-arn arn:aws:iam::aws:policy/job-function/ViewOnlyAccess
aws iam delete-role-policy --role-name wb-security-review-<slug> --policy-name prowler-additions
aws iam delete-role --role-name wb-security-review-<slug>
```

*Strict*

Write a custom policy from `scope.md` in place of the two managed policies:

- Include only the services that appear in the scope.
- For each, allow only read actions (`Get*`, `List*`, `Describe*`, and the service's specific read actions the checks need).
- Set `Resource` to the in-scope ARNs for every action that supports resource-level permissions. Many list and describe actions do not; those need `"Resource": "*"`. Keep them in a separate statement and tell the user plainly that this part cannot be narrowed on AWS, so the identity can list resources of those types across the account even though only in-scope ones are evaluated.
- Add a condition on the build tag (`aws:ResourceTag/wb-build`) where the service supports it.
- Have the user validate it with IAM Access Analyzer's policy validation before attaching.

Scanner filter: restrict the run to the in-scope regions and to the in-scope resources by ARN or by the build tag.

### Azure

Identity: a service principal, with role assignments scoped to the resource group or groups in `scope.md`. Azure role assignments scope natively, so the identity cannot read anything outside them. Use subscription scope only if the scope is the whole subscription.

- Built-in role `Reader`
- Prowler's custom role `ProwlerRole`, defined in `permissions/prowler-azure-custom-role.json` in the Prowler repository (a few read permissions `Reader` lacks)

Tenant identity checks need Microsoft Graph application permissions (`AuditLog.Read.All`, `Directory.Read.All`, `Policy.Read.All`) with admin consent. These are tenant-wide, so they fall under account-wide settings: leave them out unless the user opted in.

Commands form:

```
# 1. Create the service principal with Reader on the in-scope resource group
az ad sp create-for-rbac --name wb-security-review-<slug> --role Reader \
  --scopes /subscriptions/<subscription id>/resourceGroups/<resource group>

# 2. Create the custom role (edit assignableScopes in the file to the same scope) and assign it
az role definition create --role-definition prowler-azure-custom-role.json
az role assignment create --assignee <appId from step 1> --role ProwlerRole \
  --scope /subscriptions/<subscription id>/resourceGroups/<resource group>

# 3. Use it: set AZURE_CLIENT_ID, AZURE_TENANT_ID and AZURE_CLIENT_SECRET in your terminal
#    from step 1's output. Do not paste them into the conversation.

# Remove afterwards
az ad sp delete --id <appId>
az role definition delete --name ProwlerRole   # only if nothing else uses it
```

Repeat the scope argument for each resource group. Scanner filter: the in-scope subscription, then the result filter for resource groups.

### Google Cloud

Identity: a service account in the in-scope project, used by impersonation so no key file is created. Bind roles at project level; the identity then cannot read other projects.

- `roles/viewer`
- `roles/serviceusage.serviceUsageConsumer`
- A custom role `ProwlerRole` with the permission `storage.buckets.getIamPolicy`, which `roles/viewer` does not include

Commands form:

```
# 1. Create the service account
gcloud iam service-accounts create wb-security-review-<slug> --project <project id>

# 2. Grant read-only roles on the project
SA=wb-security-review-<slug>@<project id>.iam.gserviceaccount.com
gcloud projects add-iam-policy-binding <project id> --member serviceAccount:$SA --role roles/viewer
gcloud projects add-iam-policy-binding <project id> --member serviceAccount:$SA \
  --role roles/serviceusage.serviceUsageConsumer
gcloud iam roles create ProwlerRole --project <project id> \
  --title ProwlerRole --permissions storage.buckets.getIamPolicy
gcloud projects add-iam-policy-binding <project id> --member serviceAccount:$SA \
  --role projects/<project id>/roles/ProwlerRole

# 3. Let yourself impersonate it, then log in as it
gcloud iam service-accounts add-iam-policy-binding $SA \
  --member user:<your email> --role roles/iam.serviceAccountTokenCreator
gcloud auth application-default login --impersonate-service-account $SA

# Remove afterwards
gcloud iam service-accounts delete $SA
gcloud iam roles delete ProwlerRole --project <project id>
```

A project is the narrowest scope these roles support. If the scope is only some resources in a project, the identity can still read the rest of that project; say so, and rely on the scanner and result filters. For a stricter identity, replace `roles/viewer` with the per-service viewer roles for the services in `scope.md`.

Scanner filter: the in-scope project IDs.

### DigitalOcean

Identity: a personal access token with read-only scopes and the shortest expiry offered, created by the user in the control panel's API settings. If custom scopes are available, select read access only for the resource types in `scope.md`.

DigitalOcean tokens apply to a whole team, not to individual resources, so permissions cannot narrow the scope further; the result filter does that. Tell the user this.

Check DigitalOcean's current documentation for token scopes and how to create one before writing the instructions; do not rely on this file for the exact steps. Deliver them as written instructions in either form, since creation happens in the control panel. Supplied as an environment variable in the user's terminal. Removal: delete the token in the control panel.

## 5. After the user has set it up

Before any audit runs:

1. Confirm the identity you are now using is the review identity and belongs to the account, subscription, or project in the record.
2. Confirm it is read-only: list its attached policies or role assignments and check that none grants write access. If anything does, stop and ask the user to remove it. Do not test write access by trying to write.
3. Record in the authorization file: the identity's name, its permissions (Standard or Strict), its scope, and when it should be removed.

At the end of the review, remind the user to run the removal steps, and note in the report whether they confirmed doing so.
