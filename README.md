# Video Reader

Lets Claude read a YouTube video. Claude has no video or audio input, so the skill pulls the transcript, chapters and metadata locally with yt-dlp and, when needed, samples still frames for slides, code or UI shown on screen.

## What it does

- Summarizes a video, or answers one question about it, citing timestamps such as `[12:34]`.
- Picks the video's original caption track over machine translations and removes the repetition in auto-captions.
- Jumps through long transcripts by chapter instead of reading them whole.
- Falls back to frames, wider caption languages or local Whisper transcription when a video has no captions. Downloads only happen after you agree.

## Usage

```
/youtube <url> [question]
```

It also triggers on its own when a YouTube link appears and its content matters.

## Install

```
/plugin marketplace add marco-vrinssen/marcovrinssen
/plugin install video-reader@marcovrinssen
```

Codex, Cursor and other agents that read Agent Skills:

```
npx skills add marco-vrinssen/video-reader
```

## Requirements

| Tool | Needed for |
|---|---|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp#installation) | everything, keep it current |
| `python3` and `bash` | the bundled scripts, Git for Windows provides `bash` |
| [ffmpeg](https://ffmpeg.org/download.html) | frames and audio transcription only |

## What it runs and fetches

| Action | Where | Stored in |
|---|---|---|
| yt-dlp reads metadata and captions, never the video stream | youtube.com | your temp folder, `claude-youtube/<video id>` |
| yt-dlp downloads the video at up to 720p, only for frames | youtube.com | same folder |
| ffmpeg extracts still frames from that download | local | same folder |

No hooks, MCP servers or telemetry. Not affiliated with or endorsed by YouTube or Google.

## License

MIT
