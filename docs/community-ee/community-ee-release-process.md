# Releasing the community-ee-* execution environments

## Release Cadence

The community EEs are to be built and published on the next day and/or the day after ansible-core is released.

## EE tag versioning

Versioning would be the core tag + a patch number, e.g

    - EE with core `2.16.2` comes out -> `community-ee:2.16.2-1`
    - EE with core `2.16.3` comes out -> `community-ee:2.16.3-1`


## Dependencies

- Podman/Docker

##  Credentials

    - Access to  https://github.com/ansible-community/images repo
    - Access to ghcr.io

## Prerequisites

- Join the [Release Management working group](https://forum.ansible.com/g/release-managers) and [Execution Environment group](https://forum.ansible.com/g/ExecutionEnvs).
- Understand [Ansible execution environments](https://forum.ansible.com/t/execution-environments-getting-started-guide-community-ee-images-availability/1341).
- Read about the [eerelease.yml](/.github/workflows/eerelease.yml)  GitHub workflow.
- Show intention and book the date for the releasing of the EE.

## Announcement before the release

  Post this message in the channel before working on the release, using the correct release number.

  ```
  📯📯📯 I am working on the `Ansible Execution Environment Base and Minimal 2.x.y-1` Release. I will keep the room updated about the progress.📦️
  ```

## Actual Build Steps :

### On the terminal

1. Check the most recent [ansible-core version](https://pypi.org/project/ansible-core/)
2. Verify ansible collection versions for ``ansible.posix``, ``ansible.utils`` and  ``ansible.windows`` for `deps` file of the Ansible community package version for the related release  in the [ansible-build-data repo](https://github.com/ansible-community/ansible-build-data).
3. Go to the images/execution-environments directory.
4. Create the correct `git branch` (name it in the related version eg: 2.17.1-1)

        ```
            cd images/execution-environments
            git checkout main
            git pull upstream main
            git checkout -b coreversion-eeversion

        ```

5. Update the ansible-core and collection versions in the  `/images/execution-environments/community-ee-base/execution-environment.yml` file.
      - Update the ansible-core version in the  `/images/execution-environments/community-ee-minimal/execution-environment.yml` file, commit the changes and create a PR.

        ```
            vim community-ee-base/execution-environment.yml
            git add -u
            git status
            git commit -m "Updates ansible-core & collection versions for Base and Minimal"
            git push origin branch_name
        ```
Once the PR is merged, it is the time to start with the github workflow.


### Triggering the release workflow

1. Go to the [ansible-community/images](https://github.com/ansible-community/images) repo.
2. Click on the ![`Actions`](action-workflow-block.png) tab to view the available workflows.
3. Go to the `Release Ansible Execution Environment` workflow and then select ![`Run Workflow`](docs/community-ee/dropdown-workflow.png).
4. Click on the Drop down Button and choose the type of the Execution Environment, (whether it is `community-ee-base` or `community-ee-minimal`)
5. Write down the patch number of execution environment (to be appended to the ansible-core version) .
      This is typically 1.
6. Check on the button if this is `latest` release of  the particular execution environment
7. Click on the ![`Run workflow` button](docs/community-ee/workflow_block.png) to run the workflow
8. After the successful run of the workflow, go on and check if the [image is published](https://github.com/orgs/ansible-community/packages/container) and get the sha256 sum of the published image (to be used in the announcement).
9. Make the announcement in the #release-management and #community-working-group Matrix room, Forum, and Bullhorn according to the instructions in `docs/community-ee/community-ee-announcement.md`.

