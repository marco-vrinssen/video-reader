# video-reader

## Rules

- A single-plugin repo. The plugin sits at the root and the skill lives in `skills/`. It is listed in the marketplace repo `marco-vrinssen/marcovrinssen`, not here.
- The plugin is named `video-reader` and its skill stays `youtube`. A brand as plugin name triggers a review hold in the plugin directory, and `/youtube` keeps working.

## Checks

- `claude plugin validate --strict .claude-plugin/plugin.json` checks the plugin. Fix every warning.
- `npx skills add . --list` confirms that other agents find the skill.
- The Validate workflow runs both on every push to `main` and every pull request.

## Release

1. Bump `version` in `.claude-plugin/plugin.json`, or installed copies never update.
2. Add the changes to `CHANGELOG.md`.
3. Push and wait for the Validate workflow to pass.
4. Tag `vX.Y.Z` and create a GitHub release.
