#!/usr/bin/env python3
"""Pick the best subtitle track from a yt-dlp output dir.

Alphabetical order would hand back a machine translation ahead of the
original track, so rank by the video's own language first, then by the
caller's preference list.
"""

import glob
import json
import os
import sys


def track_lang(path):
    return os.path.basename(path).split(".")[-2].lower()


def main():
    out_dir, video_id, langs = sys.argv[1], sys.argv[2], sys.argv[3]
    files = sorted(glob.glob(os.path.join(out_dir, "*.vtt")))
    if not files:
        return
    try:
        info = json.load(open(os.path.join(out_dir, f"{video_id}.info.json"), encoding="utf-8"))
        native = info.get("language")
    except Exception:
        native = None
    prefs = ([native] if native else []) + langs.split(",")
    for want in prefs:
        want = want.strip().lower()
        for f in files:
            if want and track_lang(f) == want:
                print(f)
                return
    print(files[0])


if __name__ == "__main__":
    main()
