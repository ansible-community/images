# Ansible Community Execution Environment Images

## About Execution Environments

Execution environments (EE) are container images from which your Ansible commands and playbooks run from.
They are meant to include the Ansible collections, packages and dependencies you need for running Ansible modules and playbooks.

They can be used by [AWX](https://github.com/ansible/awx), [Automation Controller](https://docs.ansible.com/automation-controller/latest/html/administration/index.html) (previously known as Tower) and [ansible-navigator](https://github.com/ansible/ansible-navigator).

They can be built using [ansible-builder](https://github.com/ansible/ansible-builder/) with either [docker or podman](https://docs.ansible.com/projects/builder/en/latest/usage/#container-runtime) using [execution environment definitions](https://docs.ansible.com/projects/builder/en/latest/definition/) provided by this repository.

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

cd community-ee-base

ansible-builder build -v 3 -t community-ee-base:latest

ansible-navigator -v --pull-policy never \
    --execution-environment-image community-ee-base:latest \
    run tests.yml
```

## Available images

- [community-ee-minimal](https://github.com/orgs/ansible-community/packages/container/package/community-ee-minimal): ansible-core with no collections
- [community-ee-base](https://github.com/orgs/ansible-community/packages/container/package/community-ee-base): ansible-core together with `ansible.posix`, `ansible.utils`, and `ansible.windows`
