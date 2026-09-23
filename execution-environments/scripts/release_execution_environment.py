#!/usr/bin/env python3
"""Build, test, tag, and publish an Execution Environment image."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

RELEASE_TAG = re.compile(
    r"^(?P<ansible_core>[0-9]+\.[0-9]+\.[0-9]+)-(?P<ee_revision>[0-9]+)$"
)


def _ansible_core_from_tag(tag: str) -> str:
    """Return the ansible-core component of an EE release tag."""
    match = RELEASE_TAG.fullmatch(tag)
    if match is None:
        raise ValueError(
            f"release tag {tag!r} must match <major>.<minor>.<patch>-<revision>"
        )
    return match.group("ansible_core")


def _pinned_ansible_core(requirements_path: Path) -> str:
    """Read the single exact ansible-core pin from a requirements input file."""
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


def _run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    """Run one release command and stop immediately if it fails."""
    subprocess.run(command, cwd=cwd, env=env, check=True)


def publish(
    *, repository_root: Path, ee_name: str, release_tag: str, image_name: str
) -> None:
    """Build, test, tag, and push one Execution Environment release."""
    ansible_core = _ansible_core_from_tag(release_tag)
    ee_directory = repository_root / "execution-environments" / ee_name
    requirements_path = ee_directory / "requirements-explicit.in"
    pinned_ansible_core = _pinned_ansible_core(requirements_path)
    if ansible_core != pinned_ansible_core:
        raise ValueError(
            f"release tag uses ansible-core {ansible_core}, but "
            f"{requirements_path.name} pins {pinned_ansible_core}"
        )

    versioned_image = f"{image_name}:{release_tag}"
    latest_image = f"{image_name}:latest"
    tests_directory = repository_root / "execution-environments" / "tests"

    _run(
        ["ansible-builder", "build", "-v", "3", "--tag", versioned_image],
        cwd=ee_directory,
    )
    test_environment = os.environ.copy()
    test_environment["CONTAINER_RUNTIME"] = "podman"
    _run(
        [
            "pytest",
            "-v",
            "--ee-name",
            ee_name,
            "--image-ref",
            versioned_image,
        ],
        cwd=tests_directory,
        env=test_environment,
    )
    _run(["podman", "tag", versioned_image, latest_image], cwd=repository_root)
    _run(["podman", "push", versioned_image], cwd=repository_root)
    _run(["podman", "push", latest_image], cwd=repository_root)


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_tag = subparsers.add_parser(
        "check-tag", help="report whether a tag is an EE release tag"
    )
    check_tag.add_argument("release_tag")

    publish_parser = subparsers.add_parser(
        "publish", help="build, test, tag, and publish one EE"
    )
    publish_parser.add_argument(
        "--repository-root", type=Path, default=Path.cwd(), help=argparse.SUPPRESS
    )
    publish_parser.add_argument("--ee-name", required=True)
    publish_parser.add_argument("--release-tag", required=True)
    publish_parser.add_argument("--image-name", required=True)
    return parser.parse_args()


def main() -> int:
    """Run the requested release operation."""
    args = _parse_args()
    if args.command == "check-tag":
        print(str(RELEASE_TAG.fullmatch(args.release_tag) is not None).lower())
        return 0

    try:
        publish(
            repository_root=args.repository_root.resolve(),
            ee_name=args.ee_name,
            release_tag=args.release_tag,
            image_name=args.image_name,
        )
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
