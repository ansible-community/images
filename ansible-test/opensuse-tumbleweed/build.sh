#!/bin/bash
# Builds a archlinux image suitable for use with ansible-test
# Based on the centos8-stream image from this repository
set -ex

SCRIPT_DIR=$(cd `dirname $0` && pwd -P)
DEPENDENCIES="$(cat ${SCRIPT_DIR}/dependencies.txt | tr '\n' ' ')"

build=$(buildah from docker.io/opensuse/tumbleweed:latest)

buildah run "${build}" -- /bin/bash -c "zypper --non-interactive --gpg-auto-import-keys refresh --services --force && \
    zypper --non-interactive update --auto-agree-with-licenses --no-recommends && \
    zypper --non-interactive install --auto-agree-with-licenses --no-recommends ${DEPENDENCIES} && \
    zypper clean --all"

# Disable PEP 668 marker
buildah run "${build}" -- /bin/bash -c "rm /usr/lib64/python3.13/EXTERNALLY-MANAGED"

# systemd path differs from rhel
buildah config --env LIBSYSTEMD=/usr/lib/systemd/system "${build}"
buildah run "${build}" -- /bin/bash -c "(cd \${LIBSYSTEMD}/sysinit.target.wants/; for i in *; do [ \$i == systemd-tmpfiles-setup.service ] || rm -f \$i; done); \
    rm -f \${LIBSYSTEMD}/multi-user.target.wants/*; \
    rm -f /etc/systemd/system/*.wants/*; \
    rm -f \${LIBSYSTEMD}/local-fs.target.wants/*; \
    rm -f \${LIBSYSTEMD}/sockets.target.wants/*udev*; \
    rm -f \${LIBSYSTEMD}/sockets.target.wants/*initctl*; \
    rm -f \${LIBSYSTEMD}/basic.target.wants/*;"

# don't create systemd-session for ssh connections
buildah run "${build}" -- /bin/bash -c "sed -i /pam_systemd/d /etc/pam.d/common-session-pc"

buildah run "${build}" -- /bin/bash -c "ssh-keygen -A"
# explicitly enable the service, opensuse default to disabled services
buildah run "${build}" -- /bin/bash -c "systemctl enable sshd.service"

# Extra python dependencies
buildah run --volume ${SCRIPT_DIR}:/tmp/src:z "${build}" -- /bin/bash -c "pip3 install --disable-pip-version-check --no-cache-dir -r /tmp/src/requirements.txt"

buildah config --env container=docker "${build}"
buildah config --cmd "/sbin/init" "${build}"
buildah commit "${build}" "${1:-localhost/test-image:opensuse-tumbleweed}"
