# Releasing community-ee-* execution environments

## Release Cadence

The community EEs are built and published on the day after `ansible-core` is released.

## EE tag versioning

The EE versioning convention is core tag plus patch number, for example:

    - EE with core `2.16.2` comes out -> `community-ee:2.16.2-1`
    - EE with core `2.16.3` comes out -> `community-ee:2.16.3-1`

## Dependencies

- Podman/Docker

## Credentials

- Access to the https://github.com/ansible-community/images repository
- Access to ghcr.io

## Prerequisites

- Join the [Release Management working group](https://forum.ansible.com/g/release-managers) and [Execution Environment group](https://forum.ansible.com/g/ExecutionEnvs).
- Understand [Ansible execution environments](https://forum.ansible.com/t/execution-environments-getting-started-guide-community-ee-images-availability/1341).
- Read about the [eerelease.yml](/.github/workflows/eerelease.yml)  GitHub workflow.
- Show intention and book the date for the releasing of the EE.

## Making the pre-release announcement

Post this message in the channel before working on the release, using the correct release number.

```markdown
📯📯📯 I am working on the `Ansible Execution Environment Base and Minimal 2.x.y-1` Release. I will keep the room updated about the progress.📦️
```

## Building the EEs

### On the terminal

1. Check the most recent [ansible-core version](https://pypi.org/project/ansible-core/)
2. Verify Ansible collection versions for ``ansible.posix``, ``ansible.utils`` and  ``ansible.windows`` for `deps` file of the Ansible community package version for the related release in the [ansible-build-data repo](https://github.com/ansible-community/ansible-build-data).
3. Change to the `images/execution-environments` directory.
4. Create a `git branch` that has a name corresponding to the version, for example: `2.17.1-1`.

    ```bash
    cd images/execution-environments
    git checkout main
    git pull upstream main
    git checkout -b coreversion-eeversion
    ```

5. Update the `ansible-core` and collection versions in the  `/images/execution-environments/community-ee-base/execution-environment.yml` file.
6. Update the `ansible-core` version in the `/images/execution-environments/community-ee-minimal/execution-environment.yml` file.
7. Commit the changes and create a PR.

    ```bash
    vim community-ee-base/execution-environment.yml
    git add -u
    git status
    git commit -m "Updates ansible-core & collection versions for Base and Minimal"
    git push origin branch_name
    ```

After the PR is merged, it is the time to trigger the release workflow on GitHub.

### Triggering the release workflow

1. Go to the [ansible-community/images](https://github.com/ansible-community/images) repository.
2. Click the `Actions` tab to view the available workflows.
3. Go to the `Release Ansible Execution Environment` workflow and then select `Run Workflow`.
4. Click the drop-down button and choose the type of the Execution Environment, whether `community-ee-base` or `community-ee-minimal`.
5. Provide the patch number of the execution environment that is appended to the `ansible-core` version, which is typically `1`.
6. Select the button if this is `latest` release of the particular execution environment.
7. Click the `Run workflow` to run the workflow.
8. After the successful run of the workflow, check if the [image is published](https://github.com/orgs/ansible-community/packages/container) and get the sha256 sum of the published image for the release announcement.
9. Announce the release in the #release-management and #community-working-group Matrix room, Forum, and Bullhorn according to the instructions in `docs/community-ee/community-ee-announcement.md`.
