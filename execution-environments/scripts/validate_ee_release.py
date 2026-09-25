#!/usr/bin/env python3
"""Validate an Execution Environment release tag and ansible-core pins."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RELEASE_TAG = re.compile(r"^(?P<ansible_core>[0-9]+\.[0-9]+\.[0-9]+)-[0-9]+$")


def _ansible_core_from_tag(tag: str) -> str:
    """Return the ansible-core component of an EE release tag.

    Args:
        tag: Release tag in ``<major>.<minor>.<patch>-<revision>`` format.

    Returns:
        The ``<major>.<minor>.<patch>`` ansible-core version.

    Raises:
        ValueError: If the tag does not use the required format.
    """
    match = RELEASE_TAG.fullmatch(tag)
    if match is None:
        raise ValueError(
            f"release tag {tag!r} must match <major>.<minor>.<patch>-<revision>"
        )
    return match.group("ansible_core")


def _pinned_ansible_core(requirements_path: Path) -> str:
    """Read the single exact ansible-core pin from a requirements input file.

    Args:
        requirements_path: Path to an EE's ``requirements-explicit.in`` file.

    Returns:
        The exactly pinned ansible-core version.

    Raises:
        OSError: If the requirements file cannot be read.
        ValueError: If the file does not contain exactly one ansible-core pin.
    """
    prefix = "ansible-core=="
    versions = [
        line.removeprefix(prefix).strip()
        for raw_line in requirements_path.read_text(encoding="utf-8").splitlines()
        if (line := raw_line.split("#", 1)[0].strip()).startswith(prefix)
    ]
    if len(versions) != 1 or not versions[0]:
        raise ValueError(
            f"{requirements_path}: ansible-core must have exactly one '==' pin"
        )
    return versions[0]


def validate_release(tag: str, requirements_paths: list[Path]) -> None:
    """Validate a release tag against every EE's ansible-core pin.

    Args:
        tag: Execution Environment release tag.
        requirements_paths: Explicit requirements files for the released EEs.

    Raises:
        OSError: If a requirements file cannot be read.
        ValueError: If the tag or an ansible-core pin is invalid, or if a pin
            does not match the tag's ansible-core version.
    """
    release_core = _ansible_core_from_tag(tag)
    for requirements_path in requirements_paths:
        pinned_core = _pinned_ansible_core(requirements_path)
        if pinned_core != release_core:
            raise ValueError(
                f"release tag uses ansible-core {release_core}, but "
                f"{requirements_path} pins {pinned_core}"
            )


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        The release tag and explicit requirements paths.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("release_tag")
    parser.add_argument("requirements", nargs="+", type=Path)
    return parser.parse_args()


def main() -> int:
    """Run release validation.

    Returns:
        Zero when validation succeeds or one when it fails.
    """
    args = _parse_args()
    try:
        validate_release(args.release_tag, args.requirements)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
