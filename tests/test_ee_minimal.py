"""Contracts specific to community-ee-minimal: ansible-core only."""

from __future__ import annotations

from pathlib import Path

from pytest_container.container import ContainerData

from conftest import EESpec

#: Restrict this module to the minimal EE only.
EE_IMAGES = ["community-ee-minimal"]

#: Collections the base EE installs that must stay out of the minimal EE.
BASE_ONLY_COLLECTIONS = ("ansible.posix", "ansible.utils", "ansible.windows")


def test_definition_declares_no_collections(ee_spec: EESpec) -> None:
    """Assert the minimal EE definition declares no galaxy collections.

    Args:
        ee_spec: Parsed definition of the EE under test.
    """
    assert ee_spec.collections == []
    assert not (Path(ee_spec.directory) / "requirements.yml").exists()


def test_base_only_collections_absent(ee_container: ContainerData) -> None:
    """Assert none of the base EE's collections are installed.

    Args:
        ee_container: Running container under test.
    """
    listing = ee_container.connection.run_expect(
        [0], "ansible-galaxy collection list"
    ).stdout
    for name in BASE_ONLY_COLLECTIONS:
        assert name not in listing, f"{name} should not be installed in the minimal EE"
