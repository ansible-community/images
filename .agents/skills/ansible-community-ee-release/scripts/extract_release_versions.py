#!/usr/bin/env python3
"""Extract ansible-core and collection versions from Ansible build data."""

import argparse
import json
import re
import urllib.request

import yaml

VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
RAW_ROOT = "https://raw.githubusercontent.com/ansible-community/ansible-build-data"
TARGET_COLLECTIONS = ("ansible.posix", "ansible.utils", "ansible.windows")


def fetch(url: str) -> str:
    """Return UTF-8 text from a build-data URL."""
    with urllib.request.urlopen(url, timeout=30) as response:  # noqa: S310
        return response.read().decode("utf-8")


def main() -> None:
    """Fetch the tagged manifests and print their release versions as JSON."""
    parser = argparse.ArgumentParser()
    parser.add_argument("version", help="Ansible package version, for example 14.6.0")
    args = parser.parse_args()

    if not VERSION_PATTERN.fullmatch(args.version):
        parser.error("version must use the X.Y.Z format")

    series = args.version.split(".", 1)[0]
    prefix = f"{RAW_ROOT}/{args.version}/{series}/ansible-{args.version}"
    deps_url = f"{prefix}.deps"
    collections_url = f"{prefix}.yaml"

    deps = dict(
        line.split(": ", 1) for line in fetch(deps_url).splitlines() if ": " in line
    )
    core_version = deps.get("_ansible_core_version")
    if not isinstance(core_version, str) or not core_version:
        raise ValueError(f"{deps_url} has no _ansible_core_version")

    manifest = yaml.safe_load(fetch(collections_url))
    collections = manifest.get("collections") if isinstance(manifest, dict) else None
    if not isinstance(collections, list):
        raise ValueError(f"{collections_url} has no collections list")

    all_collection_versions = {}
    for collection in collections:
        if not isinstance(collection, dict):
            raise ValueError(f"{collections_url} has an invalid collection entry")
        name = collection.get("name")
        version = collection.get("version")
        if not isinstance(name, str) or not isinstance(version, str):
            raise ValueError(f"{collections_url} has an invalid collection entry")
        all_collection_versions[name] = version

    missing = set(TARGET_COLLECTIONS) - all_collection_versions.keys()
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"{collections_url} is missing collections: {names}")

    collection_versions = {
        name: all_collection_versions[name] for name in TARGET_COLLECTIONS
    }

    print(
        json.dumps(
            {
                "ansible_core_version": core_version,
                "collection_versions": collection_versions,
                "package_version": args.version,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
