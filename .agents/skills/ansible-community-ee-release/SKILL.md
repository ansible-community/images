---
name: ansible-community-ee-release
description: Prepare ansible-community/images execution environments for an Ansible Community Package release. Use when updating community-ee-base and community-ee-minimal from ansible-build-data.
---

# Ansible Community EE Release

Accept an Ansible Community Package version such as `14.6.0`. Work in the
`ansible-community/images` checkout.

## Release data

Run the bundled extractor from the repository root rather than reading or parsing
the manifests manually:

```bash
uv run --group scripts python \
  .agents/skills/ansible-community-ee-release/scripts/extract_release_versions.py \
  "${package_version}"
```

It derives the release series from the package version, fetches both tagged build
data manifests, validates their expected structure, and emits only the package
version, `ansible-core` version, and the three relevant collection versions. Use
that output as the source of truth rather than remembered versions.

Truncated example output:

```json
{
  "ansible_core_version": "2.21.6",
  "collection_versions": {
    "ansible.posix": "2.2.2",
    "ansible.utils": "6.1.1",
    "ansible.windows": "3.9.2"
  },
  "package_version": "14.6.0"
}
```

## Prepare the change

1. Inspect the worktree, current branch, and remotes. Stop before overwriting or
   mixing unrelated user changes.
2. Treat `ansible-community/images` as the canonical upstream repository. Inspect
   the configured remotes and, if `upstream` does not exist, add it with:

   ```bash
   git remote add upstream git@github.com:ansible-community/images.git
   ```

   If `upstream` exists but points somewhere else, stop and report the mismatch
   instead of replacing it. Fetch and prune both the contributor's fork and
   `upstream`, then update safely to the latest `upstream/main`; use a fast-forward
   when possible and do not rewrite user history.
3. Compare the release data with both `requirements-explicit.in` files and
   `execution-environments/community-ee-base/requirements.yml`.
4. Pin the release's `ansible-core` version in both explicit requirement files.
   Update collection pins only for `ansible.posix`, `ansible.utils`, and
   `ansible.windows`, and only when the extractor reports a different version. Do
   not add or update any other collection.
5. Regenerate both derived locks from the repository root by following the
   [dependency-locking instructions](https://github.com/ansible-community/images/blob/main/docs/execution-environments/README.md#generating-locked-python-dependencies)
   and the [release preparation guide](https://github.com/ansible-community/images/blob/main/docs/execution-environments/release-process.md#prepare-the-execution-environments).
   Never hand-edit generated `requirements.txt` or `requirements-implicit.in`
   files.
6. If the branch does not already exist, create it with this exact command,
   preserving the prepared changes:

   ```bash
   git switch -c "prepare/${ansible_core_version}" upstream/main
   ```

   If it exists, inspect it and avoid silently replacing it.

## Validate

Follow the repository's [test suite instructions](https://github.com/ansible-community/images/blob/main/docs/execution-environments/README.md#running-the-test-suite).
Run the Ruff format and lint checks, the non-container unit tests for dependency
generation and release tooling, `validate_ee_release.py` with
`<ansible-core-version>-1` and both explicit requirements, and `git diff --check`.
Review the final diff for unintended files. Do not claim container builds were run
unless they actually completed.

## Approval gate

Before committing, pushing, or opening a pull request, show the proposed title and
complete PR body to the user and wait for explicit approval.

Use this title shape:

```text
chore(deps): prepare execution environments for Ansible <package-version>
```

The PR body should contain only `## Summary` and `## Details`. It must state the
Ansible package and core versions, list changed collections with old and new
versions, note included collections that remain unchanged when useful, and mention
regenerated locks.
Incorporate requested edits and ask for approval again until the user accepts the
body.

## Publish after approval

1. Commit only the intended files after the user approves the PR title and body.
2. Push `prepare/<ansible-core-version>` to the contributor's fork and set its
   upstream tracking branch.
3. Set `fork_owner`, `ansible_core_version`, `pr_title`, and `pr_body` to their
   verified values, then create the pull request with this exact command:

   ```bash
   gh pr create \
     --repo ansible-community/images \
     --base main \
     --head "${fork_owner}:prepare/${ansible_core_version}" \
     --title "${pr_title}" \
     --body "${pr_body}" \
     --assignee "@me" \
     --label "enhancement" \
     --reviewer "ansible-community/release-management-wg"
   ```

4. Verify the PR's title, base, head, body, assignee, label, and requested reviewer,
   then return its URL, commit SHA, and validation summary.
