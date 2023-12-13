## Release Cadence

Community EE is to be built and published on the next day and/or the day after ansible-core is released.

## EE tag versioning

Versioning would be the core tag + a patch number, e.g

    - EE with core `2.15.2` comes out -> `community-ee:2.15.2-1`
    - EE with core `2.15.3` comes out -> `community-ee:2.15.3-1`


## Dependencies

-   Podman/Docker

##  Credentials

- Access to  https://github.com/ansible/ansible repo
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



## Community-ee-minimal

```

cd /home/adas/code/redhat/images/execution-environments/community-ee-minimal
```


```
ansible-builder build --tag ghcr.io/ansible-community/community-ee-minimal:2.16.0-1
```

```
podman images
```

```
podman tag <image id> ghcr.io/ansible-community/community-ee-minimal:latest
```


### Test

podman run --rm -it ghcr.io/ansible-community/community-ee-minimal:2.15.7-1 /bin/bash
cat /etc/os-release
ansible --version
ansible-galaxy collection list



```
podman push ghcr.io/ansible-community/community-ee-minimal:2.15.5-1

```

```
podman push ghcr.io/ansible-community/community-ee-minimal:latest
```




Release Announcement

```
Hello everyone,

We’re happy to announce the release of the

Base Ansible Community Excution Environment 2.16.1-1
Base Ansible Community Excution Environment 2.16.1-1
Minimal Ansible Community Excution Environment 2.16.0-1
Minimal Ansible Community Excution Environment 2.16.0-1



## Whats inside community-ee-minimal ?

Ansible community-ee-minimal is a container image. <Ansible community-ee version> includes :

- `base_image`: fedora-minimal

- `ansible-core`: ansible-core 2.16.0 (latest version of ansible-core)

- `collections`: The following set of collections

    - ansible.posix <version>
    - ansible.utils <version>
    - ansible.windows <version>

## sha256 sum value of the container image :

7849a7f261d1080c47d38718169bae13b1a05cd65b34c7ffba4a2a9604db730d

## How to get community-ee-minimal?

### Install from command line via @sha256_sum_value of the image

`podman pull http://ghcr.io/ansible-community/community-ee-minimal@sha256:7849a7f261d1080c47d38718169bae13b1a05cd65b34c7ffba4a2a9604db730d`

### Install from command line via image tag

`podman pull ghcr.io/ansible-community/community-ee-minimal:latest`
`podman pull ghcr.io/ansible-community/community-ee-minimal:2.16.0-1`



## Whats inside community-ee-base?

- `base_image`: fedora-minimal

- `ansible-core`: ansible-core 2.16.0 (latest version of ansible-core)

## sha256 sum value of the container image :

24863f44ca9cce42f4d3015dce728bab4de3ad16cd2c7d4737196ccde6f8cef8

## How to get community-ee-base?

### Install from command line via @sha256_sum_value of the image

`podman pull http://ghcr.io/ansible-community/community-ee-base@sha256:24863f44ca9cce42f4d3015dce728bab4de3ad16cd2c7d4737196ccde6f8cef8`

### Install from command line via image tag

`podman pull ghcr.io/ansible-community/community-ee-base:latest`
`podman pull ghcr.io/ansible-community/community-ee-base:2.16.0-1`


## To know about the future releases

Join the new Ansible Community Forum to follow along and participate
in all the discussions and release related discussions and
announcements. Feel free to share your thoughts, ideas and concerns
there.

Register here to join the Ansible Forum:

https://forum.ansible.com

Subscribe to the Bullhorn for all future release dates, announcements,
and Ansible community contributor news at:

[https://bit.ly/subscribe-bullhorn](https://bit.ly/subscribe-bullhorn)

You can find all past Bullhorn issues on the official wiki page:
[https://github.com/ansible/community/wiki/News#the-bullhorn](https://github.com/ansible/community/wiki/News#the-bullhorn)

On behalf of the Ansible community, thank you and happy automating!

Cheers,
Ansible Community Team

```


After uploading an image to ghcr.io the sha256 sum is not matching the with local digest value. I am finding the local value in the build machine via `podman inspect ghcr.io/repo/image-name:tag-name |grep Digest`. Any tips what I am doing wrong

1a224490e5025eb6a96e0831a3f6d5f5f1d236f65a56e33d88f406869ba3d41a




# Forum post

Release announcement to be done  in the  [Ecosystem Releases category](https://forum.ansible.com/c/news/releases)  under the News and Announcement section.

`ghcr.io/ansible-community/community-ee-base:latest`