#!/usr/bin/env python3
"""make_thumbnail.py — deterministic 1280x720 YouTube thumbnail.

Real photo + bold headline rendered by code (HTML -> PNG via headless Chrome).
Same inputs -> same clean result, perfect text, every time. No AI generation.

Usage:
  make_thumbnail.py --headline "AI ISN'T|HAPPENING|TO YOU" \
      [--photo /abs/path.png] [--out thumbnail.png] [--accent "#ffd400"]

  --headline  Required. Use "|" to break lines (2-4 short lines is the sweet spot,
              3-5 words total). The LAST line gets the accent color (the pop).
  --photo     Real photo on the right. Defaults to the bundled approved photo.
  --out       Output PNG path. Default: ./thumbnail.png
  --accent    Accent hex color for the last line + underline. Default: #ffd400

COMPLIANCE: the headline is yours — keep it curiosity-driven. NO tenure / rank /
income / credential / success claims (FTC). The skill never adds any text.
"""
import argparse, html, os, shutil, subprocess, sys, tempfile

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(SKILL_DIR, "assets")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def font_size_for(lines):
    """Scale headline down as line count / longest line grows, so it never clips."""
    longest = max((len(l) for l in lines), default=0)
    size = 104
    if len(lines) >= 4 or longest >= 12:
        size = 84
    if len(lines) >= 5 or longest >= 16:
        size = 70
    return size


def build_headline_html(headline, accent):
    lines = [l.strip() for l in headline.split("|") if l.strip()]
    if not lines:
        sys.exit("ERROR: --headline is empty")
    out = []
    for i, line in enumerate(lines):
        cls = "line accent" if i == len(lines) - 1 else "line"
        out.append(f'<span class="{cls}">{html.escape(line)}</span>')
    return "".join(out), font_size_for(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--headline", required=True)
    ap.add_argument("--photo", default=os.path.join(ASSETS, "default-photo.png"))
    ap.add_argument("--out", default="thumbnail.png")
    ap.add_argument("--accent", default="#ffd400")
    args = ap.parse_args()

    if not os.path.exists(CHROME):
        sys.exit(f"ERROR: headless Chrome not found at {CHROME}")
    if not os.path.exists(args.photo):
        sys.exit(f"ERROR: --photo not found: {args.photo}")

    headline_html, font_size = build_headline_html(args.headline, args.accent)
    template = open(os.path.join(ASSETS, "template.html")).read()

    work = tempfile.mkdtemp(prefix="thumb_")
    try:
        shutil.copytree(os.path.join(ASSETS, "fonts"), os.path.join(work, "fonts"))
        shutil.copy(args.photo, os.path.join(work, "photo.png"))
        filled = (template
                  .replace("__HEADLINE_HTML__", headline_html)
                  .replace("__FONTSIZE__", str(font_size))
                  .replace("__ACCENT__", args.accent)
                  .replace("__PHOTO__", "photo.png"))
        index = os.path.join(work, "index.html")
        open(index, "w").write(filled)

        out_abs = os.path.abspath(args.out)
        png = os.path.join(work, "shot.png")
        cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
               "--force-device-scale-factor=1", "--window-size=1280,720",
               "--virtual-time-budget=2500", f"--screenshot={png}",
               f"file://{index}"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if not os.path.exists(png):
            sys.exit(f"ERROR: Chrome did not produce a screenshot.\n{r.stderr}")
        shutil.move(png, out_abs)
        print(f"OK -> {out_abs}  (1280x720, headline {font_size}px)")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
