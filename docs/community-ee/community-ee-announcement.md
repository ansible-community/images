# Forum Announcement

Release announcement to be done in the  Ecosystem Release sub-category under the News & Announcements category. Follow [forum link](https://forum.ansible.com/c/news/releases/18) to create the announcement post.

```
Hello everyone,

We’re happy to announce the release of the

Ansible Community Execution Environment Minimal <ansible-core-version-minimal-ee-version> and Ansible Community Execution Environment Base <ansible-core-version-base-ee-version>!

## What are Execution Environments?

Read the [Getting started with Execution Environments](https://docs.ansible.com/projects/ansible/latest/getting_started_ee/index.html) guide to learn how to benefit from running Ansible automation in containers.

## What's inside community-ee-minimal <ansible-core-version-minimal-ee-version>?

Ansible community-ee-minimal is a container image. It includes:

- `base_image`: fedora-minimal

- `ansible-core`: <version of ansible-core>

- `collections`: The following set of collections

    - ansible.posix <version>
    - ansible.utils <version>
    - ansible.windows <version>

## sha256 sum value of the container image:


## How to get community-ee-minimal?

### Install from command line via @sha256_sum_value of the image

`podman pull http://ghcr.io/ansible-community/community-ee-minimal@sha256:<sha_sum_value>`

### Install from command line via image tag

`podman pull ghcr.io/ansible-community/community-ee-minimal:latest`
`podman pull ghcr.io/ansible-community/community-ee-minimal:<ansible-core-version-minimal-ee-version>`


## What's inside community-ee-base?

- `base_image`: fedora-minimal

- `ansible-core`: ansible-core <version of ansible-core>

## sha256 sum value of the container image:



## How to get community-ee-base?

### Install from command line via @sha256_sum_value of the image

`podman pull http://ghcr.io/ansible-community/community-ee-base@sha256:<sha_sum_value>`

### Install from command line via image tag

`podman pull ghcr.io/ansible-community/community-ee-base:latest`
`podman pull ghcr.io/ansible-community/community-ee-base:<ansible-core-version-base-ee-version>`


## To know about future releases

Join the [Ansible Community Forum](https://forum.ansible.com) to follow along and participate
in all the discussions.

Subscribe to the [Bullhorn](https://forum.ansible.com/c/news/bullhorn/17) for all future release dates, announcements, and Ansible community contributor news.

On behalf of the Ansible community, thank you and happy automating!

Cheers,
Ansible Community Team

```

## Matrix Announcement

Inform the Ansible users - Matrix: #users:ansible.com

Inform Discussions on community and collections related topics - Matrix: #community:ansible.com

Inform the Release Managers Working Group: Matrix: #release-management:ansible.com

Inform Community social room - Matrix: #social:ansible.com
Posting news for the Bullhorn newsletter @newsbot


```
We’re happy to announce the release of the

Ansible Community Execution Environment Minimal <ansible-core-version-minimal-ee-version> and Ansible Community Execution Environment Base <ansible-core-version-base-ee-version>!

Get the details of both the images [in the forum post](<link to the forum post>).

On behalf of the Ansible community, thank you and happy automating!

```


## Bullhorn Announcement
We’re happy to announce the release of the Ansible Community Execution Environment Minimal image <version> (Latest) and Ansible Community Execution Environment Base image <version>.

Read the whole announcement [in the ansible forum](link to forum announcement).

