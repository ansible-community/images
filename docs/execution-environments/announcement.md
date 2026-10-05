# Execution Environment Release Announcements

The [release workflow](../../.github/workflows/ee-release.yml) displays the Markdown
announcements in its workflow summary after both Execution Environment images have
been published. The Forum announcement includes image contents, immutable digests,
and pull commands. The shorter Matrix announcement links readers to the Forum post.

Apart from adding the Forum URL to the Matrix message, the generated release values
come from the tagged source and the published images in GHCR and should not need
manual editing.

## Publish the announcements

1. Open the summary of the successful release workflow run.
2. Copy the Markdown under **Forum announcement** into a new topic in the
   [Ecosystem Releases](https://forum.ansible.com/c/news/releases/18) Forum
   category and publish it.
3. Copy the Markdown under **Matrix announcement** and replace
   `FORUM_ANNOUNCEMENT_URL` with the URL of the published Forum topic.
4. Share the Matrix message in:
   - `#community:ansible.com`
   - `#social:ansible.com`
5. Mention `@newsbot` in the social room so the release can be considered for
   the Bullhorn newsletter.

## Generate announcements locally

For testing, pass each published image digest to the generator. It writes the
workflow-summary Markdown to standard output:

```console
uv run --locked --group scripts \
  execution-environments/scripts/generate_release_announcements.py \
  2.21.3-1 \
  ansible-community \
  execution-environments \
  --digest 'community-ee-minimal=sha256:<digest>' \
  --digest 'community-ee-base=sha256:<digest>'
```
