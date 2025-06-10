# Releasing community-ee-* execution environments

## Release Cadence

Ansible community Execution Environments (both Base and Minimal) are released the same week as the Ansible Community Package is released. For example: When Ansible 11.5.0 (with `ansible-core` 2.18.5) is released, both Ansible Execution Environment Minimal and Base 2.18.5-1 will also be released on that same week. Read about this more at https://docs.ansible.com/ansible/latest/getting_started_ee/index.html.

## EE tag versioning

The EE versioning convention is core tag plus patch number, for example:

    - EE with core `2.16.2` comes out -> `community-ee:2.16.2-1`
    - EE with core `2.16.3` comes out -> `community-ee:2.16.3-1`

## Credentials (for adding a new person as the Release Manager)

- Access to the https://github.com/ansible-community/images repository.
- Join [Release Management working group Matrix room](https://app.element.io/?updated=1.11.38#/room/#release-management:ansible.com) and [Execution Envs group in Forum Group](https://forum.ansible.com/g/ExecutionEnvs).
- Access to the Ansible Release Management Group in Github. (Ask in the aforementioned matrix room.)
- Access to the [eercheck](https://https://github.com/anweshadas/eercheck) repository.

## Prerequisites

- Join the [Release Management working group](https://forum.ansible.com/g/release-managers) and [Execution Environment group](https://forum.ansible.com/g/ExecutionEnvs).
- Understand [Ansible execution environments](https://forum.ansible.com/t/execution-environments-getting-started-guide-community-ee-images-availability/1341).
- Find out ansible-core version [here](https://pypi.org/project/ansible-core/) and ansible [here](https://pypi.org/project/ansible/), i.e `ansible.major.minor` version.
- Verify ansible collection versions for `ansible.posix`, `ansible.utils` and  `ansible.windows` for the `ansible.major.minor` version.
+   For eg: `ansible-11.5.0.yaml` file
+   `ansible.posix 1.6.2`
+   `ansible.utils 5.1.2`
+   `ansible.windows 2.8.0`
+ [ansible-build-data repo](https://github.com/ansible-community/ansible-build-data) repo.(Look into the `deps` file.)
- Read about the [eerelease.yml](/.github/workflows/eerelease.yml) GitHub workflow.
- Show intention and book the date for the releasing of the EE.
- Prepare the release announcement drafts for the emails and matrix communication.
- Shadow the release manager before doing the actual release.

## Build Steps

Open a new terminal window and then complete the following steps:

- Check the ansible-core version [here](https://pypi.org/project/ansible-core/)
- Verify ansible collection versions for `ansible.posix`, `ansible.utils` and  `ansible.windows` for `deps` file of the ansible version for the related release  [ansible-build-data repo](https://github.com/ansible-community/ansible-build-data).
- Go to the images/execution-environments directory.
- Create `git branch` (naming convention `ansible-core-ee_version` (name it in the related version eg: 2.17.1-1)).
- Update the ansible-core and collection versions in the  `/images/execution-environments/community-ee-base/execution-environment.yml` file.
- Update the ansible-core version in the `/images/execution-environments/community-ee-minimal/execution-environment.yml` file.
- Push the changes with the following commit messages: `git commit -m "Updates ansible-core & collection versions for Base and Minimal"`
- Add 'release management team'  as reviewers of your pull request.
- Wait for the PR to get merged.

## Updating the EER check repository

After you complete the build steps, do the following to validate the EE images:

- Fork [eercheck repo](https://github.com/anweshadas/eercheck) for testing the versions of the ansible-core and collections.
- Create the branch with `git branch <branchname>` (naming convention `ansible-core-ee_version` (name it in the related version eg: 2.17.1-1)).
- Open the eerchek/vars.json file and edit the `ansible-core`, `fedora-image` and `ansible-collections` versions there (as mentioned above).
- Assign @anweshadas to the PR.
- Wait for the PR to get merged.

## Run the Workflow

- Once both the abovementioned PRs are merged go to your browser and open  [ansible-community/images](https://github.com/ansible-community/images) repo .
- Click on the `Actions` to open the `Workflows`.
- Click on  the `Release Ansible Excuetion Environment`  and click on the `Run Workflow` Dropdown Button.
- Click on the Drop down Button and choose the type of the Execution Environment, (whether it is `community-ee-base` and `community-ee-minimal`)
- Write down the version of execution environment (to be appended to the ansible-core version) .
- Click on the button if this is the `latest` release of  the particular execution environment.
- Click on the `Run workflow` button to run the workflow for `community-ee-base` or `community-ee-minimal` as the case may be.
- After the successful run of the workflow, check if the image is published in [here](https://github.com/orgs/ansible-community/packages/container) and get the SHA256 sum of the published image (to be used in the announcement).

## Communicate the release

- For announcement in Forum follow the "./annoucement.md" template.
- Make the announcement in the #release-management and #community-working-group Matrix room, Forum and the Bullhorn.
- For the Release Management room and Community working group room in matrix and the Bullhorn just share the link to the forum post.
