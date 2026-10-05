#!/usr/bin/env python3
"""Generate Markdown announcements for an Execution Environment release."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

IMAGE_NAMES = ("community-ee-minimal", "community-ee-base")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
EXACT_PIN = re.compile(r"^(?P<name>[A-Za-z0-9_.-]+)==(?P<version>\S+)$")
FORUM_URL_PLACEHOLDER = "FORUM_ANNOUNCEMENT_URL"


@dataclass(frozen=True)
class ImageMetadata:
    """Source and registry metadata used in an announcement."""

    name: str
    base_image: str
    packages: dict[str, str]
    collections: tuple[tuple[str, str], ...]
    digest: str


def _load_yaml(path: Path) -> object:
    """Load a YAML document from ``path``."""
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def _exact_pins(path: Path) -> dict[str, str]:
    """Return exact package pins from a requirements input file."""
    pins: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        match = EXACT_PIN.fullmatch(line)
        if match is None:
            continue
        name = match.group("name")
        if name in pins:
            raise ValueError(f"{path}: duplicate exact pin for {name}")
        pins[name] = match.group("version")
    return pins


def _collections(path: Path) -> tuple[tuple[str, str], ...]:
    """Return collection names and versions, or an empty tuple when absent."""
    if not path.exists():
        return ()
    document = _load_yaml(path)
    if not isinstance(document, dict) or not isinstance(
        document.get("collections"), list
    ):
        raise ValueError(f"{path}: expected a collections list")

    collections = []
    for item in document["collections"]:
        if not isinstance(item, dict) or not all(
            isinstance(item.get(key), str) for key in ("name", "version")
        ):
            raise ValueError(f"{path}: every collection needs a name and version")
        collections.append((item["name"], item["version"]))
    return tuple(collections)


def _image_metadata(
    images_directory: Path, digests: dict[str, str]
) -> list[ImageMetadata]:
    """Read announcement metadata for every released image."""
    images = []
    for name in IMAGE_NAMES:
        image_directory = images_directory / name
        definition_path = image_directory / "execution-environment.yml"
        definition = _load_yaml(definition_path)
        try:
            base_image = definition["images"]["base_image"]["name"]
        except (KeyError, TypeError) as error:
            raise ValueError(
                f"{definition_path}: base image name is missing"
            ) from error
        if not isinstance(base_image, str):
            raise ValueError(f"{definition_path}: base image name must be a string")

        requirements_path = image_directory / "requirements-explicit.in"
        packages = _exact_pins(requirements_path)
        for required_package in ("ansible-core", "ansible-runner"):
            if required_package not in packages:
                raise ValueError(
                    f"{requirements_path}: missing exact pin for {required_package}"
                )

        digest = digests.get(name, "")
        if DIGEST.fullmatch(digest) is None:
            raise ValueError(f"{name}: expected a sha256 container digest")

        images.append(
            ImageMetadata(
                name=name,
                base_image=base_image,
                packages=packages,
                collections=_collections(image_directory / "requirements.yml"),
                digest=digest,
            )
        )
    return images


def _friendly_name(image_name: str) -> str:
    """Return the human-readable image name."""
    suffix = image_name.removeprefix("community-ee-").title()
    return f"Ansible Community Execution Environment {suffix}"


def _short_name(image_name: str) -> str:
    """Return the short human-readable image name."""
    return image_name.removeprefix("community-ee-").title()


def _forum_announcement(
    tag: str, registry_namespace: str, images: list[ImageMetadata]
) -> str:
    """Render the full Ansible Forum announcement."""
    released = " and ".join(f"{_friendly_name(image.name)} `{tag}`" for image in images)
    lines = [
        "Hello everyone,",
        "",
        f"We’re happy to announce the release of {released}!",
        "",
        "## What are Execution Environments?",
        "",
        "Read the [Getting started with Execution Environments]"
        "(https://docs.ansible.com/projects/ansible/latest/"
        "getting_started_ee/index.html) "
        "guide to learn how to benefit from running Ansible automation in containers.",
        "",
        "## What’s included?",
        "",
        "### Core components",
        "",
        "| Component | "
        + " | ".join(_short_name(image.name) for image in images)
        + " |",
        "| --- | " + " | ".join("---" for _image in images) + " |",
        "| Base image | "
        + " | ".join(f"`{image.base_image}`" for image in images)
        + " |",
        "| `ansible-core` | "
        + " | ".join(f"`{image.packages['ansible-core']}`" for image in images)
        + " |",
        "| `ansible-runner` | "
        + " | ".join(f"`{image.packages['ansible-runner']}`" for image in images)
        + " |",
        "",
        "### Collections",
        "",
    ]

    images_without_collections = [image for image in images if not image.collections]
    if images_without_collections:
        names = " and ".join(f"`{image.name}`" for image in images_without_collections)
        verb = "does" if len(images_without_collections) == 1 else "do"
        lines.extend([f"{names} {verb} not include any collections.", ""])

    images_with_collections = [image for image in images if image.collections]
    if images_with_collections:
        lines.extend(
            [
                "| Collection | "
                + " | ".join(
                    _short_name(image.name) for image in images_with_collections
                )
                + " |",
                "| --- | "
                + " | ".join("---" for _image in images_with_collections)
                + " |",
            ]
        )
        collection_names = dict.fromkeys(
            name
            for image in images_with_collections
            for name, _version in image.collections
        )
        for collection_name in collection_names:
            versions = []
            for image in images_with_collections:
                image_collections = dict(image.collections)
                version = image_collections.get(collection_name)
                versions.append(f"`{version}`" if version else "—")
            lines.append(f"| `{collection_name}` | " + " | ".join(versions) + " |")
    else:
        lines.append("Neither image includes any collections.")

    lines.extend(["", "## Pull the images"])

    for image in images:
        image_reference = f"ghcr.io/{registry_namespace}/{image.name}"
        lines.extend(
            [
                "",
                f"### `{image.name}`",
                "",
                "```console",
                "# Immutable digest",
                f"podman pull {image_reference}@{image.digest}",
                "",
                "# Release tag",
                f"podman pull {image_reference}:{tag}",
                "",
                "# Latest tag",
                f"podman pull {image_reference}:latest",
                "```",
            ]
        )

    lines.extend(
        [
            "",
            "## Follow future releases",
            "",
            "Join the [Ansible Community Forum](https://forum.ansible.com) to follow "
            "along and participate in the discussions.",
            "",
            "Subscribe to the [Bullhorn]"
            "(https://forum.ansible.com/c/news/bullhorn/17) for release dates, "
            "announcements, and Ansible community contributor news.",
            "",
            "On behalf of the Ansible community, thank you and happy automating!",
            "",
            "Cheers,",
            "Ansible Community Team",
            "",
        ]
    )
    return "\n".join(lines)


def _matrix_announcement(tag: str, images: list[ImageMetadata]) -> str:
    """Render the short Matrix announcement."""
    released = " and ".join(f"{_friendly_name(image.name)} `{tag}`" for image in images)
    return "\n".join(
        [
            f"We’re happy to announce the release of {released}!",
            "",
            "[Read the full announcement on the Ansible Forum]"
            f"({FORUM_URL_PLACEHOLDER}).",
            "",
            "On behalf of the Ansible community, thank you and happy automating!",
            "",
        ]
    )


def _digest_arguments(values: list[str]) -> dict[str, str]:
    """Parse and validate ``IMAGE=DIGEST`` command-line values."""
    digests = {}
    for value in values:
        name, separator, digest = value.partition("=")
        if not separator or name not in IMAGE_NAMES:
            raise ValueError(f"invalid digest argument: {value!r}")
        if name in digests:
            raise ValueError(f"duplicate digest argument for {name}")
        digests[name] = digest
    missing = set(IMAGE_NAMES) - digests.keys()
    if missing:
        raise ValueError(f"missing digest argument for {', '.join(sorted(missing))}")
    return digests


def generate_summary(
    tag: str,
    registry_namespace: str,
    images_directory: Path,
    digests: dict[str, str],
) -> str:
    """Generate a GitHub workflow summary containing the announcements."""
    images = _image_metadata(images_directory, digests)
    forum = _forum_announcement(tag, registry_namespace, images)
    matrix = _matrix_announcement(tag, images)
    return "\n".join(
        [
            "After publishing the Forum post, replace `FORUM_ANNOUNCEMENT_URL` "
            "in the Matrix message with its URL.",
            "",
            "## Forum announcement",
            "",
            forum,
            "",
            "## Matrix announcement",
            "",
            matrix,
            "",
        ]
    )


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("release_tag")
    parser.add_argument("registry_namespace")
    parser.add_argument("images_directory", type=Path)
    parser.add_argument(
        "--digest",
        action="append",
        default=[],
        metavar="IMAGE=DIGEST",
        help="published digest for an image (required once per image)",
    )
    return parser.parse_args()


def main() -> int:
    """Generate announcement files, reporting invalid metadata cleanly."""
    args = _parse_args()
    try:
        print(
            generate_summary(
                args.release_tag,
                args.registry_namespace,
                args.images_directory,
                _digest_arguments(args.digest),
            )
        )
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
