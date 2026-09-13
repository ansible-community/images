"""Fixtures for the Execution Environment pytest suite.

Builds each EE with ``ansible-builder`` and yields a running container together
with the values parsed from its definition files: ``execution-environment.yml``,
``requirements.yml`` and ``bindep.txt``.
"""

from __future__ import annotations

import subprocess
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml
from pytest_container.container import (
    Container,
    ContainerData,
    ContainerLauncher,
    EntrypointSelection,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
EE_ROOT = REPO_ROOT / "execution-environments"
EE_DEFINITION = "execution-environment.yml"

# System packages and galaxy collections are always declared in these files.
BINDEP_FILE = "bindep.txt"
REQUIREMENTS_FILE = "requirements.yml"

# EEs under test. A test module can narrow this by defining ``EE_IMAGES``.
ALL_EE_IMAGES = ("community-ee-base", "community-ee-minimal")


@dataclass(frozen=True)
class EESpec:
    """Values parsed from an EE's definition files.

    Attributes:
        name: Directory name of the execution environment.
        directory: Absolute path to the EE directory.
        fedora_version: Fedora major release derived from the base image tag.
        ansible_core_version: Pinned ansible-core version from the definition.
        system_packages: Package names listed in the EE's ``bindep.txt``.
        collections: Galaxy collections from the EE's ``requirements.yml``, if it
            declares any.
    """

    name: str
    directory: Path
    fedora_version: int
    ansible_core_version: str
    system_packages: list[str]
    collections: list[dict]


def _parse_bindep(path: Path) -> list[str]:
    """Return the package names declared in a bindep file.

    Args:
        path: Path to the ``bindep.txt`` file.

    Returns:
        The package names, with comments and ``[profile]`` headers removed.
    """
    packages: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or line.startswith("["):
            continue
        packages.append(line.split()[0])
    return packages


def _parse_ee(name: str) -> EESpec:
    """Parse an EE's definition files into an :class:`EESpec`.

    System packages are always read from ``bindep.txt`` and galaxy collections
    from ``requirements.yml`` if that file exists, following the layout every EE
    in this repository uses.

    Args:
        name: Directory name of the execution environment.

    Returns:
        The parsed specification.

    Raises:
        ValueError: If the base image tag is not a numeric Fedora release or the
            ansible-core requirement is not pinned with ``==``.
    """
    ee_dir = EE_ROOT / name
    data = yaml.safe_load((ee_dir / EE_DEFINITION).read_text(encoding="utf-8"))

    base_image = data["images"]["base_image"]["name"]
    release = base_image.rsplit(":", 1)[-1]
    if not release.isdigit():
        raise ValueError(
            f"{name}: base image {base_image!r} does not pin a numeric Fedora "
            "release; the suite cannot derive the expected version."
        )

    dependencies = data["dependencies"]
    core_pip = dependencies["ansible_core"]["package_pip"]
    _, _, core_version = core_pip.partition("==")
    if not core_version:
        raise ValueError(
            f"{name}: ansible_core.package_pip {core_pip!r} is not pinned with '=='"
        )

    requirements = ee_dir / REQUIREMENTS_FILE
    collections: list[dict] = []
    if requirements.is_file():
        manifest = yaml.safe_load(requirements.read_text(encoding="utf-8"))
        collections = list(manifest.get("collections", []))

    return EESpec(
        name=name,
        directory=ee_dir,
        fedora_version=int(release),
        ansible_core_version=core_version,
        system_packages=_parse_bindep(ee_dir / BINDEP_FILE),
        collections=collections,
    )


def _build_ee(spec: EESpec) -> str:
    """Build the EE with ansible-builder and return its local image reference.

    Args:
        spec: Specification of the execution environment to build.

    Returns:
        The locally tagged image reference, e.g. ``localhost/name:pytest``.
    """
    tag = f"localhost/{spec.name}:pytest"
    subprocess.run(
        ["ansible-builder", "build", "-v", "3", "--tag", tag],
        cwd=spec.directory,
        check=True,
    )
    return tag


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Parametrize ``ee_name`` over ``EE_IMAGES``, defaulting to all EEs.

    Args:
        metafunc: The pytest metafunc for the collecting test module.
    """
    if "ee_name" in metafunc.fixturenames:
        names = list(getattr(metafunc.module, "EE_IMAGES", ALL_EE_IMAGES))
        metafunc.parametrize("ee_name", names, ids=names, indirect=True)


@pytest.fixture(scope="session")
def ee_name(request: pytest.FixtureRequest) -> str:
    """Return the name of the EE under test.

    Args:
        request: Pytest request carrying the parametrized ``ee_name`` value.

    Returns:
        The EE directory name.
    """
    return request.param


@pytest.fixture(scope="session")
def ee_spec(ee_name: str) -> EESpec:
    """Return the parsed definition of the EE under test.

    Args:
        ee_name: Name of the EE under test.

    Returns:
        The parsed specification.
    """
    return _parse_ee(ee_name)


@pytest.fixture(scope="session")
def ee_container(
    ee_spec: EESpec,
    container_runtime,
    pytestconfig: pytest.Config,
) -> Iterator[ContainerData]:
    """Build the EE image, launch it, and yield its container data.

    Build and launch live in the same fixture so the ordering is guaranteed.

    Args:
        ee_spec: Specification of the execution environment to build.
        container_runtime: Container runtime selected by pytest-container.
        pytestconfig: Pytest config used to resolve build/run arguments.

    Yields:
        The launched container and its testinfra connection.
    """
    tag = _build_ee(ee_spec)
    container = Container(
        url=f"containers-storage:{tag}",
        entry_point=EntrypointSelection.BASH,
    )
    with ContainerLauncher.from_pytestconfig(
        container=container,
        container_runtime=container_runtime,
        pytestconfig=pytestconfig,
    ) as launcher:
        launcher.launch_container()
        yield launcher.container_data
