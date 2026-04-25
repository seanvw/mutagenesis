#!/usr/bin/env python3
"""Generate commits.json from `git log` for the checkpoints page.

Run before committing/pushing if you want the latest history visible
on the live site. The newest commit will not include itself in the
JSON it ships — regenerate again afterwards if that matters.
"""
import json
import subprocess
from pathlib import Path

REPO_URL = "https://github.com/seanvw/mutagenesis"

# Null-byte record separator (-z) + Unit Separator field separator (%x1f)
# keeps multi-line commit bodies intact through one parse.
GIT_FORMAT = "%H%x1f%h%x1f%s%x1f%b%x1f%aI%x1f%an"


def main() -> None:
    here = Path(__file__).parent
    result = subprocess.run(
        ["git", "log", "-z", f"--format={GIT_FORMAT}"],
        capture_output=True, text=True, cwd=here, check=True,
    )
    out = []
    for record in result.stdout.split("\x00"):
        if not record:
            continue
        parts = record.split("\x1f", 5)
        if len(parts) != 6:
            continue
        sha, short, subject, body, date, author = parts
        out.append({
            "sha": sha,
            "short_sha": short,
            "subject": subject,
            "body": body.strip(),
            "date": date,
            "author": author,
            "url": f"{REPO_URL}/commit/{sha}",
        })
    (here / "commits.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"Wrote {len(out)} commits to commits.json")


if __name__ == "__main__":
    main()
