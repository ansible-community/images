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

## Pre Requisite:

      - Join [Release Management working Matrix room](https://app.element.io/?updated=1.11.38#/room/#release-management:ansible.com) and [Execution Envs group in Forum Group](https://forum.ansible.com/g/ExecutionEnvs).
      - Read about the Ansible Execution Environment in [here](https://forum.ansible.com/t/execution-environments-getting-started-guide-community-ee-images-availability/1341) and in [this](https://forum.ansible.com/t/execution-environments-getting-started-guide-community-ee-images-availability/1341) Forum Post.
      - Read about  Github workflow `.github/workflows/eerelease.yml` .
      - Show intention and book the date for the releasing of the EE.

## Announcement before the release

  Post this message in the channel before working on the release.

  ```
  📯📯📯 I am working on the `Ansible Execution Environment Base and Minimal 2.17.1-1` Release. I will keep the room updated about the progress.📦️
  ```

## Actual Build Steps :

### On the terminal

      - Check the ansible-core version [here](https://pypi.org/project/ansible-core/)
      - Verify ansible collection versions for ansible.posix, ansible.utils and  ansible.windows for `deps` file of the ansible version for the related release  [ansible-build-data repo](https://github.com/ansible-community/ansible-build-data).
      - Go to the images/execution-environments directory.
      - Create the correct `git branch` (name it in the related version eg: 2.17.1-1)

        ```
            cd images/execution-environments
            git checkout main
            git pull upstream main
            git checkout -b coreversion-eeversion

        ```

      - Update the ansible-core and collection versions in the  `/images/execution-environments/community-ee-base/execution-environment.yml` file.
      - Update the ansible-core version in the  `/images/execution-environments/community-ee-minimal/execution-environment.yml` file, commit the changes and create a PR.

        ```
            vim community-ee-base/execution-environment.yml`
            git add -u
            git status
            git commit -m "Updates ansible-core & collection versions for Base and Minimal"
            git push origin branch_name
        ```
      - Once the PR is merged, it is the time to start with the github action workflow.


### On your browser :

      - Go to the [ansible-community/images](https://github.com/ansible-community/images) repo
      - Click on the ![`Actions`](action-workflow-block.png) to open the `Workflows`
      - Go to the `Release Ansible Excution Environment` and click on the ![`Run Workflow` Dropdown Button](docs/community-ee/dropdown-workflow.png)
      - Click on the Drop down Button and choose the type of the Execution Environment, (whether it is `community-ee-base` and `community-ee-minimal`)
      - Write down the version of execution environment (to be appended to the ansible-core version) .
      -  Check on the button if this is `latest` release of  the particular execution environment
      -  Click on the ![`Run workflow` button](docs/community-ee/workflow_block.png) to run the workflow
      - After the successful run of the workflow, go on and check if the image is published in  [here](https://github.com/orgs/ansible-community/packages/container) and get the sha256 sum of the published image (to be used in the announcement).
      - Make the announcement in the #release-management and #community-working-group Matrix room, Forum and Bullhorn following the `docs/community-ee/community-ee-announcement.md` file.

