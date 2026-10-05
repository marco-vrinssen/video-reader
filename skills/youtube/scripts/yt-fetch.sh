#!/usr/bin/env bash
# Fetch metadata + transcript for one YouTube video into a cache dir.
# Prints the cache dir path; never downloads the video stream.
# Usage: yt-fetch.sh <url> [lang_prefs] [group_seconds]
set -euo pipefail

URL="${1:?usage: yt-fetch.sh <url> [langs] [group_seconds]}"
LANGS="${2:-en,en-US,en-GB,de,de-DE}"
GAP="${3:-30}"

command -v yt-dlp >/dev/null || { echo "yt-dlp missing, see https://github.com/yt-dlp/yt-dlp#installation" >&2; exit 127; }

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ID="$(yt-dlp --no-playlist --skip-download --print "%(id)s" "$URL" | head -1)"
DIR="${TMPDIR:-/tmp}/claude-youtube/$ID"
mkdir -p "$DIR"

# Manual captions win over auto-generated ones when both exist.
yt-dlp --no-playlist --skip-download \
  --write-info-json \
  --write-subs --write-auto-subs \
  --sub-langs "$LANGS" --sub-format vtt --convert-subs vtt \
  -o "$DIR/%(id)s" "$URL" >/dev/null 2>"$DIR/yt-dlp.log" || true

[ -f "$DIR/$ID.info.json" ] || { echo "fetch failed, see $DIR/yt-dlp.log" >&2; exit 1; }
python3 "$HERE/meta.py" "$DIR/$ID.info.json" > "$DIR/meta.txt"

VTT="$(python3 "$HERE/pick_vtt.py" "$DIR" "$ID" "$LANGS")"
if [ -z "$VTT" ]; then
  echo "NO_CAPTIONS" > "$DIR/transcript.txt"
else
  python3 "$HERE/vtt_to_text.py" "$VTT" "$GAP" > "$DIR/transcript.txt"
fi

echo "$DIR"
