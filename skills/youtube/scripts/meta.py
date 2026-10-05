#!/usr/bin/env python3
"""Summarise a yt-dlp info.json into the fields worth reading."""

import json
import sys

info = json.load(open(sys.argv[1], encoding="utf-8"))
print(f"title:    {info.get('title')}")
print(f"channel:  {info.get('uploader')}")
print(f"duration: {info.get('duration_string')}")
print(f"uploaded: {info.get('upload_date')}")
print(f"language: {info.get('language')}")
print(f"url:      {info.get('webpage_url')}")

if info.get("chapters"):
    print("\nchapters:")
    for chapter in info["chapters"]:
        minutes, seconds = divmod(int(chapter.get("start_time") or 0), 60)
        print(f"  [{minutes}:{seconds:02d}] {chapter.get('title')}")

description = (info.get("description") or "").strip()
if description:
    print("\ndescription:")
    print(description[:2000])
