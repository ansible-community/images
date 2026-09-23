"""Tests for the execution environment release helper."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parents[1] / "scripts" / "release_execution_environment.py"
)


def _run_helper(
    *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess:
    """Run the release helper through its command-line interface."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


@pytest.mark.parametrize(
    "tag",
    ["2.21.3-1", "10.0.12-27"],
)
def test_validate_tag_accepts_a_valid_release_tag(tag: str) -> None:
    """A valid tag must allow the release workflow to continue."""
    result = _run_helper("validate-tag", tag)

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    "tag",
    ["v2.21.3-1", "2.21-1", "2.21.3", "2.21.3-1-rc1", "2.21.3-１"],
)
def test_validate_tag_rejects_an_invalid_release_tag(tag: str) -> None:
    """A malformed tag must fail the release workflow before its build matrix."""
    result = _run_helper("validate-tag", tag)

    assert result.returncode != 0
    assert "must match <major>.<minor>.<patch>-<revision>" in result.stderr


def _write_fake_command(bin_dir: Path, name: str, log_path: Path) -> None:
    """Create an executable that records its working directory and arguments."""
    command = bin_dir / name
    command.write_text(
        "#!/bin/sh\n"
        f'printf "%s|%s|%s|%s\\n" "$PWD" "{name}" "$*" "${{CONTAINER_RUNTIME:-}}" '
        f'>> "{log_path}"\n',
        encoding="utf-8",
    )
    command.chmod(0o755)


def test_publish_builds_tests_tags_and_pushes_the_release_image(tmp_path: Path) -> None:
    """Removing or reordering a release operation must break the release contract."""
    ee_name = "community-ee-base"
    repository_root = tmp_path / "repository"
    ee_directory = repository_root / "execution-environments" / ee_name
    tests_directory = repository_root / "execution-environments" / "tests"
    ee_directory.mkdir(parents=True)
    tests_directory.mkdir()
    (ee_directory / "requirements-explicit.in").write_text(
        "ansible-core==2.21.3\nansible-runner==2.4.3\n",
        encoding="utf-8",
    )

    command_log = tmp_path / "commands.log"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for command in ("ansible-builder", "pytest", "podman"):
        _write_fake_command(bin_dir, command, command_log)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
    image_name = "ghcr.io/ansible-community/community-ee-base"

    result = _run_helper(
        "publish",
        "--repository-root",
        str(repository_root),
        "--ee-name",
        ee_name,
        "--release-tag",
        "2.21.3-1",
        "--image-name",
        image_name,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert command_log.read_text(encoding="utf-8").splitlines() == [
        f"{ee_directory}|ansible-builder|build -v 3 --tag {image_name}:2.21.3-1|",
        f"{tests_directory}|pytest|-v --ee-name {ee_name} "
        f"--image-ref {image_name}:2.21.3-1|podman",
        f"{repository_root}|podman|tag {image_name}:2.21.3-1 {image_name}:latest|",
        f"{repository_root}|podman|push {image_name}:2.21.3-1|",
        f"{repository_root}|podman|push {image_name}:latest|",
    ]


def test_publish_rejects_a_tag_for_a_different_ansible_core(tmp_path: Path) -> None:
    """A release must not publish an image under the wrong core version."""
    ee_name = "community-ee-minimal"
    repository_root = tmp_path / "repository"
    ee_directory = repository_root / "execution-environments" / ee_name
    ee_directory.mkdir(parents=True)
    (ee_directory / "requirements-explicit.in").write_text(
        "ansible-core==2.21.4\n",
        encoding="utf-8",
    )

    result = _run_helper(
        "publish",
        "--repository-root",
        str(repository_root),
        "--ee-name",
        ee_name,
        "--release-tag",
        "2.21.3-1",
        "--image-name",
        "ghcr.io/ansible-community/community-ee-minimal",
    )

    assert result.returncode != 0
    assert "release tag uses ansible-core 2.21.3" in result.stderr
    assert "requirements-explicit.in pins 2.21.4" in result.stderr
