"""Tests for release announcement generation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "generate_release_announcements.py"
)


def _write_image(
    images_directory: Path, name: str, *, with_collections: bool = False
) -> None:
    """Write the source files needed to describe a test image."""
    image_directory = images_directory / name
    image_directory.mkdir(parents=True)
    (image_directory / "execution-environment.yml").write_text(
        yaml.safe_dump({"images": {"base_image": {"name": "example.test/os:1"}}}),
        encoding="utf-8",
    )
    (image_directory / "requirements-explicit.in").write_text(
        "ansible-core==2.21.3\nansible-runner==2.4.3\n",
        encoding="utf-8",
    )
    if with_collections:
        (image_directory / "requirements.yml").write_text(
            yaml.safe_dump(
                {
                    "collections": [
                        {"name": "ansible.posix", "version": "2.2.2"},
                        {"name": "ansible.utils", "version": "6.1.0"},
                    ]
                }
            ),
            encoding="utf-8",
        )


def _run_generator(tmp_path: Path, *, digest: str | None = None):
    """Create representative metadata and run the generator CLI."""
    images_directory = tmp_path / "images"
    _write_image(images_directory, "community-ee-minimal")
    _write_image(images_directory, "community-ee-base", with_collections=True)
    valid_digest = f"sha256:{'a' * 64}"
    image_digest = digest if digest is not None else valid_digest

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "2.21.3-1",
            "ansible-community",
            str(images_directory),
            "--digest",
            f"community-ee-minimal={image_digest}",
            "--digest",
            f"community-ee-base={image_digest}",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    return result


def test_generates_copyable_forum_and_matrix_markdown(tmp_path: Path) -> None:
    """Both announcements must contain their destination-specific information."""
    result = _run_generator(tmp_path)

    assert result.returncode == 0, result.stderr
    summary = result.stdout

    assert "# Release announcements" not in summary
    assert "## Forum announcement" in summary
    assert "## Matrix announcement" in summary
    assert "Execution Environment Minimal `2.21.3-1`" in summary
    assert "Execution Environment Base `2.21.3-1`" in summary
    assert "| Component | Minimal | Base |" in summary
    assert "| `ansible-core` | `2.21.3` | `2.21.3` |" in summary
    assert "| `ansible-runner` | `2.4.3` | `2.4.3` |" in summary
    assert "`community-ee-minimal` does not include any collections." in summary
    assert "| Collection | Base |" in summary
    assert "| `ansible.posix` | `2.2.2` |" in summary
    assert "## Pull the images" in summary
    assert "## What’s inside" not in summary
    assert "ghcr.io/ansible-community/community-ee-base@sha256:" in summary
    assert "ghcr.io/ansible-community/community-ee-minimal:2.21.3-1" in summary
    assert "\nHello everyone,\n" in summary
    assert "    Hello everyone," not in summary
    assert "### Image digest" not in summary
    assert "(FORUM_ANNOUNCEMENT_URL)." in summary


@pytest.mark.parametrize(
    "digest",
    ["", "not-a-digest", "sha256:abc", f"sha512:{'a' * 64}"],
)
def test_rejects_invalid_image_digest(tmp_path: Path, digest: str) -> None:
    """An announcement must never publish a malformed image digest."""
    result = _run_generator(tmp_path, digest=digest)

    assert result.returncode != 0
    assert "expected a sha256 container digest" in result.stderr
