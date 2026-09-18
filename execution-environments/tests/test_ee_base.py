"""Contracts specific to community-ee-base: the galaxy collections."""

from __future__ import annotations

from pytest_container.container import ContainerData

from conftest import EESpec, installed_collections

# Restrict this module to the base EE only.
EE_IMAGES = ["community-ee-base"]


def test_declared_collections_installed(
    ee_container: ContainerData, ee_spec: EESpec
) -> None:
    """Assert each collection from ``requirements.yml`` is installed and pinned.

    Args:
        ee_container: Running container under test.
        ee_spec: Parsed definition of the EE under test.
    """
    assert ee_spec.collections, "base EE declares no galaxy collections"
    installed = installed_collections(ee_container)
    expected = {collection["name"] for collection in ee_spec.collections}

    for collection in ee_spec.collections:
        name = collection["name"]
        version = collection.get("version")
        assert name in installed, f"{name} not installed; found: {sorted(installed)}"
        if version:
            assert installed[name] == version, (
                f"{name}: expected {version}, got {installed[name]}"
            )

    unexpected = set(installed) - expected
    assert not unexpected, f"unexpected collections installed: {sorted(unexpected)}"
