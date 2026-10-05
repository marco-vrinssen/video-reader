#!/usr/bin/env python3
"""Convert a WebVTT subtitle file into timestamped plain text.

YouTube auto-captions ship as rolling cues where each cue repeats the
previous line plus a few new words, so naive extraction triples the
token count. Dedupe against the last emitted line to undo that.
"""

import re
import sys

TAG = re.compile(r"<[^>]*>")
CUE_TIME = re.compile(r"(\d{2}):(\d{2}):(\d{2})[.,](\d{3})\s+-->")
ENTITIES = {"&nbsp;": " ", "&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&#39;": "'"}


def stamp(h, m, s):
    h, m, s = int(h), int(m), int(s)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def clean(line):
    line = TAG.sub("", line)
    for k, v in ENTITIES.items():
        line = line.replace(k, v)
    return " ".join(line.split())


def parse(text):
    out = []
    last = None
    current = None
    for raw in text.splitlines():
        hit = CUE_TIME.search(raw)
        if hit:
            current = stamp(*hit.groups()[:3])
            continue
        if not raw.strip() or raw.startswith(("WEBVTT", "Kind:", "Language:", "NOTE", "STYLE")):
            continue
        if raw.strip().isdigit():
            continue
        line = clean(raw)
        if not line or line == last:
            continue
        last = line
        out.append((current or "0:00", line))
    return out


def group(cues, gap=30):
    """Merge cues into paragraphs, stamping one timestamp per `gap` seconds."""
    blocks = []
    buf = []
    anchor = None

    def secs(t):
        parts = [int(p) for p in t.split(":")]
        return parts[0] * 3600 + parts[1] * 60 + parts[2] if len(parts) == 3 else parts[0] * 60 + parts[1]

    for ts, line in cues:
        if anchor is None:
            anchor = ts
        elif secs(ts) - secs(anchor) >= gap:
            blocks.append((anchor, " ".join(buf)))
            buf, anchor = [], ts
        buf.append(line)
    if buf:
        blocks.append((anchor or "0:00", " ".join(buf)))
    return blocks


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: vtt_to_text.py <file.vtt> [group_seconds]")
    gap = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    with open(sys.argv[1], encoding="utf-8", errors="replace") as fh:
        cues = parse(fh.read())
    for ts, text in group(cues, gap):
        print(f"[{ts}] {text}")


if __name__ == "__main__":
    main()
