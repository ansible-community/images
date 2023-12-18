We annouce both community-ee-base and community-ee-minimal together

# Forum Announcement

Release announcement to be done  in the  [Ecosystem Releases category](https://forum.ansible.com/c/news/releases)  under the News and Announcement section.

# E-Mail Announcement

`ansible-annouce` Google Groups

# Community-ee (both Base and Minimal) announcement

```
Hello everyone,

We’re happy to announce the release of the

Ansible Community Execution Environment Minimal <ansible-core-version-minimal-ee-version> and Ansible Community Execution Environment Base <ansible-core-version-base-ee-version>!


## Whats inside community-ee-minimal <ansible-core-version-minimal-ee-version>?

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

`podman pull http://ghcr.io/ansible-community/community-ee-minimal@sha256:sha_value`

### Install from command line via image tag

`podman pull ghcr.io/ansible-community/community-ee-minimal:latest`
`podman pull ghcr.io/ansible-community/community-ee-minimal:<ansible-core-version-minimal-ee-version>`



## Whats inside community-ee-base?

- `base_image`: fedora-minimal

- `ansible-core`: ansible-core 2.16.0 (latest version of ansible-core)

## sha256 sum value of the container image:



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

# Matrix Announcement

Inform the Ansible users - Matrix: #users:ansible.com

Inform Discussions on community and collections related topics - Matrix: #community:ansible.com

Inform the Release Managers Working Group: /#release-management:ansible.com

Inform Community social room - Matrix: #social:ansible.com
Posting news for the Bullhorn newsletter @newbot


```
We’re happy to announce the release of the

Ansible Community Execution Environment Minimal <ansible-core-version-minimal-ee-version> and Ansible Community Execution Environment Base <ansible-core-version-base-ee-version>!

Get the details of both the images [here](<link to the forum post>).

On behalf of the Ansible community, thank you and happy automating!
```
