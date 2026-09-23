"""Tests for Execution Environment release validation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_ee_release.py"


def _write_requirements(path: Path, ansible_core: str) -> Path:
    """Write an explicit requirements file with an ansible-core pin."""
    path.write_text(
        f"ansible-core=={ansible_core}\nansible-runner==2.4.3\n",
        encoding="utf-8",
    )
    return path


def _validate(tag: str, *requirements: Path) -> subprocess.CompletedProcess:
    """Run release validation through its command-line interface."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), tag, *(str(path) for path in requirements)],
        check=False,
        capture_output=True,
        text=True,
    )


def test_matching_release_and_ansible_core_pins_are_valid(tmp_path: Path) -> None:
    """Matching pins for every EE must allow the release to continue."""
    base = _write_requirements(tmp_path / "base.in", "2.21.3")
    minimal = _write_requirements(tmp_path / "minimal.in", "2.21.3")

    result = _validate("2.21.3-1", base, minimal)

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    "tag",
    ["v2.21.3-1", "2.21-1", "2.21.3", "2.21.3-1-rc1", "2.21.3-１"],
)
def test_invalid_release_tag_is_rejected(tmp_path: Path, tag: str) -> None:
    """Malformed release tags must fail before image builds start."""
    requirements = _write_requirements(tmp_path / "requirements.in", "2.21.3")

    result = _validate(tag, requirements)

    assert result.returncode != 0
    assert "must match <major>.<minor>.<patch>-<revision>" in result.stderr


def test_mismatched_ansible_core_pin_is_rejected(tmp_path: Path) -> None:
    """An image must not be published under a different core version."""
    requirements = _write_requirements(tmp_path / "requirements.in", "2.21.4")

    result = _validate("2.21.3-1", requirements)

    assert result.returncode != 0
    assert "release tag uses ansible-core 2.21.3" in result.stderr
    assert "requirements.in pins 2.21.4" in result.stderr


def test_duplicate_ansible_core_pins_are_rejected(tmp_path: Path) -> None:
    """Ambiguous ansible-core requirements must fail release validation."""
    requirements = tmp_path / "requirements.in"
    requirements.write_text(
        "ansible-core==2.21.3\nansible-core==2.21.3\n",
        encoding="utf-8",
    )

    result = _validate("2.21.3-1", requirements)

    assert result.returncode != 0
    assert "must have exactly one '==' pin" in result.stderr
