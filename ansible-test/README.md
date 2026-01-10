# Ansible Community `ansible-test` Images

## About ansible-test

ansible-test provides ways to test ansible itself as well as ansible-core and ansible collections with [unit tests](https://docs.ansible.com/projects/ansible/latest/dev_guide/testing_units.html#testing-units), [sanity tests](https://docs.ansible.com/projects/ansible/latest/dev_guide/testing_sanity.html#testing-sanity) and [integration tests](https://docs.ansible.com/projects/ansible/latest/dev_guide/testing_integration.html#testing-integration).

Since integration tests can result in changes to a system (such as installing packages or changing files and configuration), it may be preferred to run them inside a container image to avoid making unnecessary changes to the host on which the tests are run.
Container images also happen to be useful and convenient for quickly testing different operating systems and versions of python.

Some container images are provided and supported by ansible-test, such as the following (from the `devel` branch at time of writing):

```bash
ansible-test integration --help
# [...]
target docker images and supported python version (choose one):
  base (3.13, 3.8, 3.9, 3.10, 3.11, 3.12)
  default (3.13, 3.8, 3.9, 3.10, 3.11, 3.12)
  alpine320 (3.12)
  fedora40 (3.12)
  ubuntu2204 (3.10)
  ubuntu2404 (3.12)
  {image}  # python must be specified for custom images
# [...]
```

ansible-test supports specifying custom images instead and the purpose of this repository is to provide suitable images for it.

## Important ⚠️

Images provided by this repository are tailored for development, testing and CI purposes.
**They are maintained by the community and are not supported by Red Hat**: they can and will break or run out of maintenance.
Do not use these images for production!

You are encouraged to use (or fork) the examples provided here in order to learn how to build and customize your own images tailored to your needs.

Thank you!

## Building and using images from this repository

Example:

```bash
dnf -y install podman buildah
./archlinux/build.sh

pip install ansible-core --user
git clone https://github.com/ansible-collections/community.general ansible_collections/community/general
cd ansible_collections/community/general
ansible-test integration --python 3.14 --docker localhost/test-image:archlinux ini_file
```

## Available images

| image              | py27 | py36 | py38 | py39 | py3.10 | py3.11 | py3.12 | py3.13 | py3.14 | Notes                                       |
|--------------------|------|------|------|------|--------|--------|--------|--------|--------|---------------------------------------------|
| [archlinux]        |      |      |      |      |        |        |        |        |   ✔️    |                                             |
| [debian-bullseye]  |      |      |      |  ✔️   |        |        |        |        |        | Based on [ubuntu2004 ansible-test image]    |
| [debian-bookworm]  |      |      |      |      |        |   ✔️    |        |        |        | Based on debian-bullseye ansible-test image |
| [debian-13-trixie] |      |      |      |      |        |        |        |   ✔️    |        | Based on debian-bookworm ansible-test image |


Note that these images from only work with ansible-test from ansible-core 2.14.0 or later.

[archlinux]: https://quay.io/ansible-community/test-image:archlinux
[debian-bullseye]: https://quay.io/ansible-community/test-image:debian-bullseye
[debian-bookworm]: https://quay.io/ansible-community/test-image:debian-bookworm
[debian-13-trixie]: https://quay.io/ansible-community/test-image:debian-13-trixie

[ubuntu2004 ansible-test image]: https://github.com/ansible/distro-test-containers/blob/c4fe28818f5a33b675652637e3057bafe50039ee/ubuntu2004-test-container/Dockerfile
