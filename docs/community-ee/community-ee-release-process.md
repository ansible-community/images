# Releasing community-ee-* execution environments

## Release Cadence

Ansible community execution environments (EEs), both the base and minimal variants, are released the same week as the Ansible community package. For example, when `ansible` 11.5.0 with `ansible-core` 2.18.5 is released, the base and minimal EEs version 2.18.5-1 are released within the same week.

## EE tag versioning

The EE versioning convention is core tag plus patch number, for example:

    - EE with core `2.16.2` comes out -> `community-ee:2.16.2-1`
    - EE with core `2.16.3` comes out -> `community-ee:2.16.3-1`

## Credentials

- Access to the https://github.com/ansible-community/images repository.
- Join the [Release Management working Matrix room](https://app.element.io/?updated=1.11.38#/room/#release-management:ansible.com) and the [Execution Envs group in Forum Group](https://forum.ansible.com/g/ExecutionEnvs).
- Access to Ansible Release Management Group in Github.
- Access to the [eercheck](https://github.com/anweshadas/eercheck) repository.

## Prerequisites

- Join the [Release Management working group](https://forum.ansible.com/g/release-managers) and [Execution Environment group](https://forum.ansible.com/g/ExecutionEnvs).
- Understand [Ansible execution environments](https://forum.ansible.com/t/execution-environments-getting-started-guide-community-ee-images-availability/1341).
- Read about the [eerelease.yml](/.github/workflows/eerelease.yml)  GitHub workflow.
- Show intention and book the date for the releasing of the EE.
- Prepare the release announcement drafts for the emails and matrix communication.
- Shadow the release manager before doing the actual release.

## Build Steps

Open a new terminal window and then complete the following steps:

1. Check the ansible-core version [here](https://pypi.org/project/ansible-core/)
2. Verify ansible collection versions for `ansible.posix`, `ansible.utils` and  `ansible.windows` for `deps` file of the ansible version for the related release  [ansible-build-data repo](https://github.com/ansible-community/ansible-build-data).
3. Change to the `images/execution-environments` directory.
4. Create a git branch following the naming convention of `ansible-core-<ee_version>`, where <ee_version> matches the related version; for example, 2.17.1-1.

```
	git checkout main
	git pull upstream main
	git checkout -b core_version-ee_version
```
5. Update the ansible-core and collection versions in the  `/images/execution-environments/community-ee-base/execution-environment.yml` file.
6. Update the ansible-core version in the  `/images/execution-environments/community-ee-minimal/execution-environment.yml` file.
7. Open a PR with the changes.

```
	git add -u
	git status
	git commit -m "Updates ansible-core & collection versions for Base and Minimal"
	git push origin branch_name
```
8. Tag @felix and @anweshadas to the PR.
9. Wait for the PR to get merged.
10. Fork [eercheck repo](https://github.com/anweshadas/eercheck) for testing the versions of thw ansible-core and collections.
11. Create the branch with `git branch <branchname>` (naming convention `ansible-core-ee_version` (name it in the related version eg: 2.17.1-1)).
12. Open the eerchek/vars.json file and edit the `ansible-core`, `fedora-image` and `ansible-collections` versions there (as mentioned above),
13. Assign @anweshadas to the PR.
14. Wait for the PR to get merged.
15. Once both the abovementioned PRs are merged go to your browser and open  [ansible-community/images](https://github.com/ansible-community/images) repo .
16. Click on the `Actions` to open the `Workflows`
17. Click on  the `Release Ansible Excuetion Environment`  and click on the `Run Workflow` Dropdown Button.
18. Click on the Drop down Button and choose the type of the Execution Environment, (whether it is `community-ee-base` and `community-ee-minimal`)
19. Write down the version of execution environment (to be appended to the ansible-core version) .
20. Click on the button if this is the `latest` release of  the particular execution environment
21. Click on the `Run workflow` button to run the workflow for `community-ee-base` or `community-ee-minimal` as the case may be.
22. After the successful run of the workflow, check if the image is published in [here](https://github.com/orgs/ansible-community/packages/container) and get the sha256 sum of the published image (to be used in the announcement).

## Communicate the release

- For announcement in Forum follow the "./annoucement.md"
- Make the announcement in the #release-management and #community-working-group Matrix room, Forum and the Bullhorn.
- For the Release Management Channel  and Community working group in matrix and the Bullhorn just share the link to the forum post.

