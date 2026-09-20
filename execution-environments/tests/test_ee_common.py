"""Contracts every Execution Environment image must satisfy.

Values are read from each EE's definition files via ``ee_spec``, so the tests
track the definitions instead of hard-coding versions.
"""

from __future__ import annotations

import re

import pytest
from pytest_container.container import ContainerData

from conftest import EESpec, installed_collections


def test_fedora_release_matches_definition(
    ee_container: ContainerData, ee_spec: EESpec
) -> None:
    """Assert the image's Fedora release matches the base image tag.

    Args:
        ee_container: Running container under test.
        ee_spec: Parsed definition of the EE under test.
    """
    result = ee_container.connection.run_expect([0], "rpm -E %fedora")
    assert result.stdout.strip() == str(ee_spec.fedora_version)


def test_ansible_cli_reports_pinned_core_version(
    ee_container: ContainerData, ee_spec: EESpec
) -> None:
    """Assert ``ansible --version`` reports the pinned ansible-core version.

    Args:
        ee_container: Running container under test.
        ee_spec: Parsed definition of the EE under test.
    """
    result = ee_container.connection.run_expect([0], "ansible --version")
    match = re.search(r"ansible \[core ([^\]]+)\]", result.stdout)
    assert match, f"could not parse ansible-core version from:\n{result.stdout}"
    assert match.group(1) == ee_spec.ansible_core_version


def test_pip_ansible_core_matches_explicit_requirement(
    ee_container: ContainerData, ee_spec: EESpec
) -> None:
    """Assert the pip-installed ansible-core version matches its explicit pin.

    Args:
        ee_container: Running container under test.
        ee_spec: Parsed definition of the EE under test.
    """
    result = ee_container.connection.run_expect(
        [0], "pip show ansible-core | awk '/^Version/ {print $2}'"
    )
    assert result.stdout.strip() == ee_spec.ansible_core_version


def test_pip_ansible_runner_matches_explicit_requirement(
    ee_container: ContainerData, ee_spec: EESpec
) -> None:
    """Assert the pip-installed ansible-runner version matches its explicit pin.

    Args:
        ee_container: Running container under test.
        ee_spec: Parsed definition of the EE under test.
    """
    result = ee_container.connection.run_expect(
        [0], "pip show ansible-runner | awk '/^Version/ {print $2}'"
    )
    assert result.stdout.strip() == ee_spec.ansible_runner_version


@pytest.mark.parametrize("ee_name", ["community-ee-minimal"], indirect=True)
def test_no_collections_installed(ee_container: ContainerData, ee_spec: EESpec) -> None:
    """Assert community-ee-minimal contains no galaxy collections."""
    installed = installed_collections(ee_container)
    assert not installed, f"minimal EE contains collections: {sorted(installed)}"


def test_bindep_packages_installed(
    ee_container: ContainerData, ee_spec: EESpec
) -> None:
    """Assert every package declared in ``bindep.txt`` is installed.

    Args:
        ee_container: Running container under test.
        ee_spec: Parsed definition of the EE under test.
    """
    assert ee_spec.system_packages, "definition declares no system packages to check"
    for package in ee_spec.system_packages:
        assert ee_container.connection.package(package).is_installed, package
