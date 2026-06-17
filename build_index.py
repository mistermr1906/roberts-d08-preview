#!/usr/bin/env python3
"""Regenerate index.html (the all-chapters grid) from the portfolio src/ SVGs.
Run from this repo dir:  python3 build_index.py
Reads ../portfolio-diagrams/src/dXX-*-{a,b}.svg, inlines each into the grid.
Add a chapter to CHAPTERS when its A+B land in src/."""
import os, re

SRC = os.path.join(os.path.dirname(__file__), "..", "portfolio-diagrams", "src")

# (file-stem, display name) — order = grid order. Only chapters with A+B in src/.
CHAPTERS = [
    ("d01-information-architecture", "D01 · Information Architecture"),
    ("d02-motion-design",           "D02 · Motion Design"),
    ("d03-ux-design",               "D03 · UX Design"),
    ("d04-web-development",          "D04 · Web Development"),
    ("d05-web-conversion",          "D05 · Web Conversion"),
    ("d06-branding",                "D06 · Branding"),
    ("d07-ui-design",               "D07 · UI Design"),
    ("d08-business-strategy",       "D08 · Business Strategy"),
    ("d09-web-copywriting",         "D09 · Web Copywriting"),
]

HEAD = ('<!doctype html><html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>robertsPortfolio — diagrams</title>\n<style>\n'
        ' body{margin:0;background:#0f0f0e;color:#cfcfca;font:14px/1.4 -apple-system,Helvetica,Arial,sans-serif}\n'
        ' header{padding:28px 32px 6px} header h1{margin:0;font-weight:600;font-size:18px}\n'
        ' header p{margin:4px 0 0;color:#8a8a86}\n'
        ' .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:22px;padding:24px 32px 48px}\n'
        ' figure{margin:0;background:#161614;border:1px solid #2a2a27;border-radius:10px;overflow:hidden}\n'
        ' .fig{aspect-ratio:1/1} .fig svg{width:100%;height:100%;display:block}\n'
        ' figcaption{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;\n'
        '   border-top:1px solid #2a2a27;font-size:13px;color:#c9c9c4}\n'
        ' figcaption span{color:#7e817f;font-size:11px;letter-spacing:.04em}\n'
        '</style></head><body>\n'
        '<header><h1>robertsPortfolio — all diagrams</h1>\n'
        '<p>Browser-rendered, full &amp; uncropped. Resize the window to test legibility at any size.</p></header>\n'
        '<div class="grid">')


def load_svg(stem, fam):
    path = os.path.join(SRC, f"{stem}-{fam}.svg")
    with open(path) as fh:
        s = fh.read().strip()
    s = re.sub(r"^<\?xml[^>]*\?>\s*", "", s)  # strip any xml declaration
    return s


def main():
    parts = [HEAD]
    for stem, name in CHAPTERS:
        for fam in ("a", "b"):
            svg = load_svg(stem, fam)
            parts.append(f'<figure><div class="fig">{svg}</div>'
                         f'<figcaption>{name}<span>{fam.upper()}</span></figcaption></figure>')
    parts.append("</div>\n</body></html>")
    out = "".join(parts)
    with open(os.path.join(os.path.dirname(__file__), "index.html"), "w") as fh:
        fh.write(out)
    print(f"wrote index.html — {len(CHAPTERS)*2} figures, {len(out)} bytes")


if __name__ == "__main__":
    main()
