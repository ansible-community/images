"""Contracts specific to community-ee-base: the galaxy collections."""

from __future__ import annotations

import json

from pytest_container.container import ContainerData

from conftest import EESpec

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
    raw = ee_container.connection.run_expect(
        [0], "ansible-galaxy collection list --format json"
    ).stdout

    # Output is {"/install/path": {"ns.name": {"version": "x.y.z"}, ...}, ...}
    by_path: dict[str, dict[str, dict[str, str]]] = json.loads(raw)
    installed: dict[str, str] = {
        name: meta["version"]
        for path_collections in by_path.values()
        for name, meta in path_collections.items()
    }

    for collection in ee_spec.collections:
        name = collection["name"]
        version = collection.get("version")
        assert name in installed, f"{name} not installed; found: {sorted(installed)}"
        if version:
            assert installed[name] == version, (
                f"{name}: expected {version}, got {installed[name]}"
            )
