# Maintaining Execution Environments

This document covers the repository maintenance and test workflow for the execution
environments. For instructions on building and using the images, see the
[execution-environments README](../../execution-environments/README.md).

## Generating locked Python dependencies

Each EE installs Python packages from its generated `requirements.txt`. Locking direct
and transitive versions improves supply chain security by making the exact dependency
set reviewable and traceable in Git.

The shared [generator](../../execution-environments/scripts/generate_python_requirements.py)
uses the `scripts` dependency group in the repository's root `uv` project. Run the
generator from the repository root after changing a collection, an explicit Python
requirement, or a constraint:

```bash
uv run --group scripts \
  execution-environments/scripts/generate_python_requirements.py \
  execution-environments/community-ee-base

uv run --group scripts \
  execution-environments/scripts/generate_python_requirements.py \
  execution-environments/community-ee-minimal
```

The files have separate ownership and purposes:

| File                          | Ownership           | Purpose                                                                                                                                            |
| ----------------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `requirements.yml`            | Maintained manually | Declares Galaxy collections. The generator installs them under `/tmp` and uses `ansible-builder introspect` to discover their Python dependencies. |
| `requirements.in`             | Generated           | Contains Python requirements discovered from collection metadata. Do not edit it.                                                                  |
| `requirements-explicit.in`    | Maintained manually | Adds packages that the EE must install independently of collection metadata.                                                                       |
| `requirements-constraints.in` | Maintained manually | Restricts package versions without adding packages.                                                                                                |
| `requirements.txt`            | Generated           | Contains the dependency lock resolved by `uv pip compile`. Do not edit it.                                                                         |

## Running the test suite

The repository's root [uv](https://docs.astral.sh/uv/) project provides a `test`
dependency group that builds each execution environment with
[`ansible-builder`](https://github.com/ansible/ansible-builder/) and verifies the
resulting image with [`pytest-container`](https://github.com/dcermak/pytest_container/).
The tests read the expected Fedora release, explicitly pinned Python package
versions (`requirements-explicit.in`), system packages (`bindep.txt`) and galaxy
collections (`requirements.yml`) from each EE's definitions.

```bash
CONTAINER_RUNTIME=docker uv run --group test pytest -v
```

Lint and formatting are enforced with [ruff](https://docs.astral.sh/ruff/):

```bash
uv run --group dev ruff format --check .
uv run --group dev ruff check .
```

A working `podman` or `docker` runtime is required. The test container plugin
defaults to Podman when it is available. To explicitly use Docker instead, set
`CONTAINER_RUNTIME=docker` when running the tests. The first run pulls the Fedora
base image and installs collections, so it is slow.

To test one already-built image, select the matching EE and pass its local image
reference:

```bash
CONTAINER_RUNTIME=docker uv run --group test pytest -v \
  --ee-name community-ee-base \
  --image-ref localhost/community-ee-base:pytest
```
