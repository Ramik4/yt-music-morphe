#!/usr/bin/env python3
"""
Translations of the notes for the GitHub release, from changelog/<language>.md (the in-app translations):
one collapsible section per language whose first line is <!-- VERSION -->, as Markdown on stdout.

Usage: translations.py VERSION
"""
import glob
import os
import sys

LANGUAGES = {"tr": "🇹🇷 Türkçe", "ru": "🇷🇺 Русский"}


def main():
    version = sys.argv[1].lstrip("v")
    out = []
    for code, title in LANGUAGES.items():
        path = os.path.join("changelog", f"{code}.md")
        if not os.path.isfile(path):
            continue
        lines = open(path, encoding="utf-8").read().splitlines()
        if not lines or lines[0].replace(" ", "") != f"<!--{version}-->":
            continue
        body = []
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            if line.startswith("•"):
                body.append(f"* {line[1:].strip()}")
            else:
                body += ["", f"**{line}**", ""]
        out += [f"<details><summary>{title}</summary>", "", *body, "", "</details>", ""]
    print("\n".join(out).strip())


if __name__ == "__main__":
    main()
