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


## Build steps for Community-ee-base

1. Go to the working directory.

`cd images/execution-environments/community-ee-base`

2. Create a new release branch

`git checkout -b base-<ansible-core-version-base-ee-version>`

3. Edit the `execution-environment.yml` file to the right `collection version` and `ansible-core version`. Get the correct [ansible-core](https://pypi.org/project/ansible-core/) version and [ansible-<version>.deps](https://github.com/ansible-community/ansible-build-data/blob/main/9/ansible-9.0.1.deps) and edit accordinly.

`vim execution-environments/community-ee-base/execution-environment.yml`

```
version: <base-community-ee with the specific ansible core>
images:
  base_image:
    name: quay.io/fedora/fedora:latest
dependencies:
  ansible_core:
    package_pip: ansible-core==<ansible-core-version>
  ansible_runner:
    package_pip: ansible-runner
  system:
    - openssh-clients
    - sshpass
  galaxy:
    collections:
    - name: ansible.posix
      version: <correct-version>
    - name: ansible.utils
      version: <correct-version>
    - name: ansible.windows
      version: <correct-version>

```

4. List images in local storage

`podman images`

5. Delete the existing community-ee base and fedora images

```
podman rmi <podman_community-ee-base_IMAGE_ID>
podman rmi <podman_community-ee-fedora_IMAGE_ID>
```
6. Create a virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```
7. Install `ansible-builder` and `setuptools`

```
python3 -m pip install ansible-builder
python3 -m pip install setuptools
```

8. Pull the latest fedora image

`podman pull fedora:latest`

9. Build the ansible community-ee-base podman image with ansible-builder. (versioning: 2.16.1-1)

`ansible-builder build --tag ghcr.io/ansible-community/community-ee-base:<ansible-core-version-base-ee-version>`

10. Check if the image has been created or not and get the <image ID> of `community-ee-base`

`podman images`

11. Build latest tag for the community-ee-base image

`podman tag <image id> ghcr.io/ansible-community/community-ee-base:latest`

12. Create the Github token

Go to Github UI and create Personal Token (classic).

Select `write:packages` scope while creating the token.
Copy the token from Github UI and then pass the token on the following command.


13. Login to Github Registry

`echo TOKEN | podman login ghcr.io -u USERNAME --password-stdin`

14. Push both the images (general versioning and the latest) to Github Registry

```
podman push ghcr.io/ansible-community/community-ee-base:<ansible-core-version-base-ee-version>
podman push ghcr.io/ansible-community/community-ee-base:latest
```

15. Commit and push the changes made in the `execution-environments/community-ee-base/execution-environment.yml` to the `https://github.com/ansible-community/images` repo.

```
git add execution-environments/community-ee-base/execution-environment.yml
git commit
git push origin <ansible-core-version-base-ee-version>
```
Compare and create the pull request.

16.   Check the community-ee-base images [here](https://github.com/orgs/ansible-community/packages/container/package/community-ee-base)  and get the sha256 sum.



## Build steps for Community-ee-minimal

1. Go to the working directory

`cd images/execution-environments/community-ee-minimal`

2. Create a new release branch

`git checkout -b base-<ansible-core-version-minimal-ee-version>`

3. Edit the `execution-environment.yml` file to the right `collection version` and `ansible-core version`. Get the correct [ansible-core](https://pypi.org/project/ansible-core/) version and edit accordinly.

`vim execution-environments/community-ee-minimal/execution-environment.yml`

```
version: <minimal-community-ee with the specific ansible core>
images:
  base_image:
    name: quay.io/fedora/fedora:latest
dependencies:
  ansible_core:
    package_pip: ansible-core==<ansible-core-version>
  ansible_runner:
    package_pip: ansible-runner
  system:
    - openssh-clients
    - sshpass

```

4. List images in local storage

`podman images`

5. Delete the existing community-ee-minimal image

`podman rmi <podman_community-ee-minimal_IMAGE_ID>`

6. Build the ansible community-ee-minimal podman image with ansible-builder. (versioning: 2.16.1-1)

`ansible-builder build --tag ghcr.io/ansible-community/community-ee-minimal:<ansible-core-version-minimal-ee-version>`

7. Check if the image has been created or not and get the <image ID> of `community-ee-minimal`

`podman images`

8. Build `latest` tag for the community-ee-minimal image

`podman tag <image id> ghcr.io/ansible-community/community-ee-minimal:latest`

9. Push both the images (general versioning and the latest) to Github Registry by using the Github Token created before

```
podman push ghcr.io/ansible-community/community-ee-minimal:<ansible-core-version-minimal-ee-version>
podman push ghcr.io/ansible-community/community-ee-minimal:latest
```
10. Commit and push the changes made in the `execution-environments/community-ee-minimal/execution-environment.yml` to the `https://github.com/ansible-community/images` repo.

```
git add execution-environments/community-ee-minimal/execution-environment.yml
git commit
git push origin <ansible-core-version-minimal-ee-version>
```
Compare and create the pull request.

11.   Check the community-ee-minimal images [here](https://github.com/orgs/ansible-community/packages/container/package/community-ee-minimal)  and get the sha256 sum.

