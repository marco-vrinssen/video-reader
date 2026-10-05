#!/usr/bin/env bash
# Sample still frames from a YouTube video so they can be read as images.
# Usage: yt-frames.sh <url> [interval_seconds] [max_frames]
set -euo pipefail

URL="${1:?usage: yt-frames.sh <url> [interval] [max_frames]}"
EVERY="${2:-60}"
MAX="${3:-12}"

command -v yt-dlp >/dev/null || { echo "yt-dlp missing, see https://github.com/yt-dlp/yt-dlp#installation" >&2; exit 127; }
command -v ffmpeg >/dev/null || { echo "ffmpeg missing, see https://ffmpeg.org/download.html" >&2; exit 127; }

ID="$(yt-dlp --no-playlist --skip-download --print "%(id)s" "$URL" | head -1)"
DIR="${TMPDIR:-/tmp}/claude-youtube/$ID"
mkdir -p "$DIR/frames"

# 720p cap keeps the download small; on-screen text stays readable.
[ -f "$DIR/video.mp4" ] || yt-dlp --no-playlist \
  -f "bv*[height<=720]+ba/b[height<=720]/b" --merge-output-format mp4 \
  -o "$DIR/video.mp4" "$URL" >/dev/null 2>>"$DIR/yt-dlp.log"

ffmpeg -nostdin -loglevel error -y -i "$DIR/video.mp4" \
  -vf "fps=1/$EVERY,scale=1280:-2" -frames:v "$MAX" \
  "$DIR/frames/frame_%03d.png"

echo "$DIR/frames"
