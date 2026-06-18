#!/usr/bin/env python3
"""Regenerate the Downloads page + the SVG bundle for Robert.

Run from this repo dir:  python3 build_downloads.py

- Copies ../portfolio-diagrams/src/dXX-*-{a,b}.svg into ./svg/
- Writes downloads.html (one card per family, inline preview + Download button)
- Writes roberts-diagrams-svg.zip (all the SVGs in one click)
Add a chapter to CHAPTERS when its A+B land in src/."""
import os, re, shutil, zipfile

HERE = os.path.dirname(__file__)
SRC = os.path.join(HERE, "..", "portfolio-diagrams", "src")
SVG_DIR = os.path.join(HERE, "svg")
ZIP_PATH = os.path.join(HERE, "roberts-diagrams-svg.zip")

# (file-stem, display name) — order = page order. Only chapters with A+B in src/.
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
    ("d11-designing-with-ai",       "D11 · Designing with AI"),
]
FAM_LABEL = {"a": "Dark / line", "b": "Pale / mass"}

HEAD = ('<!doctype html><html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>JR Design Portfolio — diagram downloads</title>\n<style>\n'
        ' body{margin:0;background:#0f0f0e;color:#cfcfca;font:14px/1.5 -apple-system,Helvetica,Arial,sans-serif}\n'
        ' header{padding:34px 32px 8px} header h1{margin:0;font-weight:600;font-size:20px}\n'
        ' header p{margin:6px 0 0;color:#8a8a86;max-width:60ch}\n'
        ' .all{display:inline-block;margin:16px 0 4px;padding:11px 18px;background:#D2EF15;color:#15150f;\n'
        '   text-decoration:none;border-radius:8px;font-weight:600;font-size:13px}\n'
        ' .all:hover{filter:brightness(1.06)}\n'
        ' .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:22px;padding:24px 32px 56px}\n'
        ' figure{margin:0;background:#161614;border:1px solid #2a2a27;border-radius:10px;overflow:hidden}\n'
        ' .fig{aspect-ratio:1/1} .fig svg{width:100%;height:100%;display:block}\n'
        ' figcaption{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:11px 14px;\n'
        '   border-top:1px solid #2a2a27;font-size:13px;color:#c9c9c4}\n'
        ' .meta{display:flex;flex-direction:column} .meta span{color:#7e817f;font-size:11px;letter-spacing:.04em}\n'
        ' .dl{flex:none;padding:7px 13px;border:1px solid #3a3a36;border-radius:7px;color:#dcdcd6;\n'
        '   text-decoration:none;font-size:12px;white-space:nowrap}\n'
        ' .dl:hover{border-color:#D2EF15;color:#fff}\n'
        '</style></head><body>\n'
        '<header><h1>JR Design Portfolio — diagram files</h1>\n'
        '<p>Download the source SVGs. Each is a square 1200&times;1200 vector — scales to any size with no quality '
        'loss. Each chapter comes in two styles: a dark line version and a pale mass version.</p>\n'
        '<a class="all" href="roberts-diagrams-svg.zip" download>&#8595;&nbsp; Download all (.zip)</a>\n'
        '</header>\n<div class="grid">')


def load_svg(stem, fam):
    with open(os.path.join(SRC, f"{stem}-{fam}.svg")) as fh:
        s = fh.read().strip()
    return re.sub(r"^<\?xml[^>]*\?>\s*", "", s)  # strip any xml declaration


def main():
    os.makedirs(SVG_DIR, exist_ok=True)
    parts = [HEAD]
    files = []
    for stem, name in CHAPTERS:
        for fam in ("a", "b"):
            fname = f"{stem}-{fam}.svg"
            shutil.copyfile(os.path.join(SRC, fname), os.path.join(SVG_DIR, fname))
            files.append(fname)
            svg = load_svg(stem, fam)
            parts.append(
                f'<figure><div class="fig">{svg}</div>'
                f'<figcaption><span class="meta">{name}<span>{FAM_LABEL[fam]}</span></span>'
                f'<a class="dl" href="svg/{fname}" download>&#8595; SVG</a></figcaption></figure>')
    parts.append("</div>\n</body></html>")
    with open(os.path.join(HERE, "downloads.html"), "w") as fh:
        fh.write("".join(parts))

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
        for fname in files:
            z.write(os.path.join(SVG_DIR, fname), arcname=f"jr-design-diagrams/{fname}")

    print(f"wrote downloads.html + svg/ ({len(files)} files) + roberts-diagrams-svg.zip")


if __name__ == "__main__":
    main()
