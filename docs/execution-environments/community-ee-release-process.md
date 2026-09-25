# Releasing Ansible Community Execution Environment Images

## Release cadence

The [`community-ee-base`](../../execution-environments/community-ee-base) and [`community-ee-minimal`](../../execution-environments/community-ee-minimal) execution environments follow the Ansible community package
release cadence. Prepare the image changes first. Publish the execution environment
release only after those changes have merged to the repository.

## Release tag

Use this format for the GitHub Release tag:

```text
<ansible-core-version>-<execution-environment-revision>
```

For example, `2.21.3-1` uses `2.21.3` as the `ansible-core` version and `1` as
the execution environment revision.

The version before the hyphen must match the exact `ansible-core==...` pin in both
of these files:

- [`community-ee-base/requirements-explicit.in`](../../execution-environments/community-ee-base/requirements-explicit.in)
- [`community-ee-minimal/requirements-explicit.in`](../../execution-environments/community-ee-minimal/requirements-explicit.in)

The `execution-environment.yml` files name the `ansible-core` package but do not
contain its version. The explicit requirements files provide the version that
[`validate_ee_release.py`](../../execution-environments/scripts/validate_ee_release.py)
checks against the release tag.

## Access and prerequisites

Release managers need:

- Permission to create releases in the [images repository](https://github.com/ansible-community/images).
- Membership in the [Release Management working group](https://forum.ansible.com/g/release-managers).
- Membership in the [Ansible Forum Execution Environments Crew](https://forum.ansible.com/g/ExecutionEnvs).
- Access to the [Ansible execution environment documentation](https://forum.ansible.com/t/execution-environments-getting-started-guide-community-ee-images-availability/1341).

Before starting a release:

- Confirm the target `ansible-core` version and execution environment revision as described in [Release tag](#release-tag).
- Confirm that both explicit requirements files use the target `ansible-core` pin as described in [Release tag](#release-tag).
- Prepare any required changes to the execution environment inputs in [Prepare the execution environments](#prepare-the-execution-environments), and merge them.
- Draft the release announcement using [`community-ee-announcement.md`](./community-ee-announcement.md).

## Prepare the execution environments

Update the files that define the images. Use the [execution environment maintenance
guide](./README.md) for dependency locking, builds, and tests.

For a release that only updates `ansible-core`, update the two
`requirements-explicit.in` files. Change the other image inputs only when the image
contents need to change.

The main inputs are:

- `execution-environment.yml` controls the base image and `ansible-builder` build configuration.
- `requirements.yml` declares Galaxy collections. The `community-ee-base` image has this file; `community-ee-minimal` image does not.
- `requirements-explicit.in` pins packages that the image must install directly, including `ansible-core`.
- `requirements-constraints.in` adds version constraints without adding packages.

After changing these inputs, regenerate the derived Python requirement files using
[Generating locked Python dependencies](./README.md#generating-locked-python-dependencies),
then run the build and test commands in the maintenance guide. Open a pull request,
add the Release Management team as reviewers, and wait for the pull request to merge
before creating the GitHub Release.

## Publish the release

Create and publish a GitHub Release for the merged commit in the
[images repository](https://github.com/ansible-community/images). Use the release tag
format described above. Publishing the release triggers
[`ee-release.yml`](../../.github/workflows/ee-release.yml).

The workflow then:

1. Checks out the release tag.
2. Validates the tag against the `ansible-core` pins in both execution environments.
3. Builds `community-ee-base` and `community-ee-minimal` with `ansible-builder` and Podman.
4. Tests each image with the repository's [pytest suite](../../execution-environments/tests).
5. Publishes each image to `ghcr.io/ansible-community` with the release tag and `latest` tags.

## Verify the release

After publishing the release:

- Confirm that the release workflow completes successfully.
- Check the [community-ee-base package](https://github.com/orgs/ansible-community/packages/container/package/community-ee-base) and [community-ee-minimal package](https://github.com/orgs/ansible-community/packages/container/package/community-ee-minimal) in GHCR.
- Confirm that both the release tag and `latest` point to the published images.
- Record each image digest for the release announcement.

If tag validation fails, check the tag and both `requirements-explicit.in` files.
The workflow will not build or publish images until the tag matches both pins.

## Communicate the release

Update the [community execution environment announcement](./community-ee-announcement.md)
with the release tag, image digests, and package links.

Publish the announcement in the Forum. Share the Forum link in the
`#release-management` and `#community-working-group` Matrix rooms and in the
Bullhorn.
