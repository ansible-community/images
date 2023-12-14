## Release Cadence

Community EE is to be built and published on the next day and/or the day after ansible-core is released.

## EE tag versioning

Versioning would be the core tag + a patch number, e.g

    - EE with core `2.16.2` comes out -> `community-ee:2.16.2-1`
    - EE with core `2.16.3` comes out -> `community-ee:2.16.3-1`


## Dependencies

-   Podman/Docker

##  Credentials

- Access to  https://github.com/ansible-community/images repo
- Access to ghcr.io


## Build steps for Community-ee-base

1. Go to the working directory

`cd images/execution-environments/community-ee-base`

2. List images in local storage

`podman images`

3. Delete the existing community-ee base and fedora images

```
podman rmi <podman_community-ee-base_IMAGE_ID>
podman rmi <podman_community-ee-fedora_IMAGE_ID>
```
4. Create a virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```
5. Install `ansible-builder` and `setuptools`

```
python3 -m pip install ansible-builder
python3 -m pip install setuptools
```

6. Pull the latest feodra image

`podman pull fedora:latest`

7. Build the ansible community-ee-base podman image with ansible-builder. (versioning : 2.16.1-1)

`ansible-builder build --tag ghcr.io/ansible-community/community-ee-base:<ansible-core-version-base-ee-version>`

8. Check if the image has been created or not and get the < image ID> of `community-ee-base`

`podman images`

9. Build latest tag for the community-ee-base image

`podman tag <image id> ghcr.io/ansible-community/community-ee-base:latest`

10. Create the Github token

Go to Github UI and create Personal Token (classic).

Select `write:packages` scope while creating the token.
Copy the token from Github UI and then pass the token on the following command.


11. Login to Github Registry

`echo TOKEN | podman login ghcr.io -u USERNAME --password-stdin`

12. Push both the images (general versioning and the latest) to Github Registry

```
podman push ghcr.io/ansible-community/community-ee-base:<ansible-core-version-base-ee-version>
podman push ghcr.io/ansible-community/community-ee-base:latest
```
13.   Check the community-ee-base images [here](https://github.com/orgs/ansible-community/packages/container/package/community-ee-base)  and get the sha256 sum.



## Build steps for Community-ee-minimal

1. Go to the working directory

`cd images/execution-environments/community-ee-minimal`

2. List images in local storage

`podman images`

3. Delete the existing community-ee-minimal image

`podman rmi <podman_community-ee-minimal_IMAGE_ID>`

4. Build the ansible community-ee-minimal podman image with ansible-builder. (versioning : 2.16.1-1)

`ansible-builder build --tag ghcr.io/ansible-community/community-ee-minimal:<ansible-core-version-minimal-ee-version>`

5. Check if the image has been created or not and get the < image ID> of `community-ee-minimal`

`podman images`

6. Build `latest` tag for the community-ee-minimal image

`podman tag <image id> ghcr.io/ansible-community/community-ee-minimal:latest`

7. Push both the images (general versioning and the latest) to Github Registry by using the Github Token created before

```
podman push ghcr.io/ansible-community/community-ee-minimal:<ansible-core-version-minimal-ee-version>
podman push ghcr.io/ansible-community/community-ee-minimal:latest
```
10.   Check the community-ee-minimal images [here](https://github.com/orgs/ansible-community/packages/container/package/community-ee-minimal)  and get the sha256 sum.

