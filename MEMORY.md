# video-reader memory

Updated 2026-10-05. Version 1.0.0. Its own marketplace under the same name, installed as `video-reader@video-reader`.

## Layout

Single-plugin repo: plugin and marketplace at the root (`source: "./"`), marketplace named like the plugin, skill in `skills/`. CI runs `claude plugin validate --strict` and `npx skills add . --list` on every push.

## Release checklist

1. Bump `version` in `.claude-plugin/plugin.json`, or installed copies never update.
2. Add the changes to `CHANGELOG.md`.
3. Push, wait for the Validate workflow to pass, then tag `vX.Y.Z` and create a GitHub release.

## Decisions

- The plugin is named `video-reader` while its skill stays `youtube`, because a brand as plugin name triggers a directory review hold and `/youtube` keeps working.
