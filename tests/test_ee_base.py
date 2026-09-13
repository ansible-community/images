"""Contracts specific to community-ee-base: the galaxy collections."""

from __future__ import annotations

from pytest_container.container import ContainerData

from conftest import EESpec

#: Restrict this module to the base EE only.
EE_IMAGES = ["community-ee-base"]


def test_declared_collections_are_installed(
    ee_container: ContainerData, ee_spec: EESpec
) -> None:
    """Assert each collection from ``requirements.yml`` is installed and pinned.

    Args:
        ee_container: Running container under test.
        ee_spec: Parsed definition of the EE under test.
    """
    assert ee_spec.collections, "base EE declares no galaxy collections"
    listing = ee_container.connection.run_expect(
        [0], "ansible-galaxy collection list"
    ).stdout

    for collection in ee_spec.collections:
        name = collection["name"]
        version = collection.get("version")
        assert name in listing, f"{name} missing from:\n{listing}"
        if version:
            line = next((ln for ln in listing.splitlines() if name in ln), "")
            assert version in line, f"{name} version {version} not on line {line!r}"
