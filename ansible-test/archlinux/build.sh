#!/bin/bash
# Builds a archlinux image suitable for use with ansible-test
# Based on the centos8-stream image from this repository

SCRIPT_DIR=$(cd `dirname $0` && pwd -P)
DEPENDENCIES="$(cat ${SCRIPT_DIR}/dependencies.txt | tr '\n' ' ')"

build=$(buildah from docker.io/library/archlinux:latest)
buildah run "${build}" -- /bin/bash -c "pacman -Syyu --noconfirm && pacman -S ${DEPENDENCIES} --noconfirm && pacman -Scc --noconfirm"

# Extra python dependencies
buildah run --volume ${SCRIPT_DIR}:/tmp/src:z "${build}" -- /bin/bash -c "pip3 install -r /tmp/src/requirements.txt"

# Ansible-specific setup: Generate new SSH host keys, remove requiretty, set up a default inventory
buildah run "${build}" -- /bin/bash -c "ssh-keygen -A && sed -i -e 's/^\(Defaults\s*requiretty\)/#--- \1/' /etc/sudoers"
buildah run "${build}" -- /bin/bash -c "mkdir -p /etc/ansible && echo -e '[local]\nlocalhost ansible_connection=local' > /etc/ansible/hosts"

# TODO: What is the container env variable used for ?
buildah config --env container=docker "${build}"
buildah config --cmd "/usr/sbin/init" "${build}"
buildah commit "${build}" "${1:-localhost/test-image:archlinux}"
