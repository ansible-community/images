#!/bin/sh
set -eux
curl https://raw.githubusercontent.com/ansible-community/ansible-build-data/main/7/galaxy-requirements.yaml -o requirements.yml
