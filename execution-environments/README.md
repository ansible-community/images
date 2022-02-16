# Ansible Community Execution Environment Images

## About Execution Environments

Execution environments (EE) are container images from which your Ansible commands and playbooks run from.
They are meant to include the Ansible collections, packages and dependencies you need for running Ansible modules and playbooks.

They can be used by [AWX](https://github.com/ansible/awx), [Automation Controller](https://docs.ansible.com/automation-controller/latest/html/administration/index.html) (previously known as Tower) and [ansible-navigator](https://github.com/ansible/ansible-navigator).

They can be built using [ansible-builder](https://github.com/ansible/ansible-builder/) with either [docker or podman](https://ansible-builder.readthedocs.io/en/latest/usage/#container-runtime) using [execution environment definitions](https://ansible-builder.readthedocs.io/en/latest/definition/) provided by this repository.

## Important ⚠️

Images provided by this repository are tailored for development, testing and CI purposes.
**They are maintained by the community and are not supported by Red Hat**: they can and will break or run out of maintenance.
Do not use these images for production!

You are encouraged to use (or fork) the examples provided here in order to learn how to build and customize your own images tailored to your needs.

Thank you!

## Building and using images from this repository

Example:

```bash
dnf -y install podman
pip install --user ansible-builder ansible-navigator

cd 2.12-with_ansible5

ansible-builder build -v 3 -t test-ee:2.12-with-ansible5

ansible-navigator --pull-policy never \
    --execution-environment-image test-ee:2.12-with-ansible5 \
    run tests.yml
```

## Available images

- [test-ee:2.12-with-ansible5](https://quay.io/ansible-community/test-ee:2.12-with-ansible5): [ansible-runner:stable-2.12-latest](https://quay.io/ansible/ansible-runner:stable-2.12-latest) with some extra packages, including ``pip install "ansible>=5,<6" ara``
