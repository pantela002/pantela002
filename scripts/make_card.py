# Builds assets/card.svg: a colored ASCII portrait of my GitHub avatar next to a
# neofetch-style info block. Background is removed with rembg first.
#
#   pip install pillow numpy "rembg[cpu]"
#   python scripts/make_card.py
import io
import urllib.request
from xml.sax.saxutils import escape

import numpy as np
from PIL import Image, ImageFilter
from rembg import remove

AVATAR_URL = "https://avatars.githubusercontent.com/u/90989221?s=460"
COLS, ROWS = 120, 60
# The color of each glyph carries the photo; the glyph itself only adds texture,
# so everything but the darkest cells uses a dense character.
RAMP = ".:-=+*%#&@"  # light -> dense

INFO = [
    ("uros@github", None),
    ("-" * 11, None),
    ("OS", "Windows 11 + WSL Ubuntu"),
    ("Uni", "University of Belgrade, EE"),
    ("Status", "Open to SWE / ML infra roles"),
    ("Prev", "Nextesy, Tenstorrent, Microsoft"),
    ("Languages", "Python, C++, Java, TypeScript"),
    ("Backend", "FastAPI, Django, Postgres, Redis"),
    ("ML", "PyTorch, JAX/Flax, HuggingFace"),
    ("Interests", "distributed systems, LLM infra"),
    ("Web", "pantelicu.space"),
]

BG, FG, KEY, DIM = "#0d1117", "#c9d1d9", "#e3b341", "#484f58"
PALETTE = ["#f85149", "#e3b341", "#3fb950", "#58a6ff", "#bc8cff", "#39c5cf", "#c9d1d9"]


def load_cutout():
    raw = urllib.request.urlopen(AVATAR_URL).read()
    return remove(Image.open(io.BytesIO(raw)).convert("RGB")).convert("RGBA")


def ascii_cells(img):
    img = img.crop((20, 12, 440, 395))
    rgb = img.convert("RGB")
    # local contrast first (big radius), then fine detail, so the glasses and eyes survive downscaling
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=24, percent=50, threshold=0))
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    small = rgb.resize((COLS, ROWS), Image.LANCZOS)
    alpha = np.asarray(img.getchannel("A").resize((COLS, ROWS), Image.LANCZOS)) / 255.0
    px = np.asarray(small).astype(float)
    lum = (0.299 * px[..., 0] + 0.587 * px[..., 1] + 0.114 * px[..., 2]) / 255.0
    # stretch over the subject only, so the face uses the whole ramp
    lo, hi = np.percentile(lum[alpha > 0.5], [2, 98])
    lum = np.clip((lum - lo) / (hi - lo), 0, 1)
    cells = []
    for y in range(ROWS):
        row = []
        for x in range(COLS):
            if alpha[y, x] < 0.5:
                row.append((" ", None))
                continue
            ch = RAMP[int(lum[y, x] ** 0.45 * (len(RAMP) - 1))]
            r, g, b = px[y, x]
            # lift the midtones: the face sits in shadow next to a bright white hoodie
            r, g, b = (int(255 * (c / 255) ** 0.62) for c in (r, g, b))
            row.append((ch, f"#{r:02x}{g:02x}{b:02x}"))
        cells.append(row)
    return cells


def build_svg(cells):
    cw, lh, pad = 5.4, 9.6, 26
    info_x = pad + COLS * cw + 40
    width = int(info_x + 440 + pad)
    height = int(pad * 2 + ROWS * lh)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="16">\n<style>.a{{font-size:9px;font-weight:700}}</style>',
        f'<rect width="100%" height="100%" rx="12" fill="{BG}"/>',
        '<g class="a" xml:space="preserve">',
    ]
    for y, row in enumerate(cells):
        ty = pad + (y + 1) * lh - 3
        spans, run, color = [], "", None
        for ch, c in row + [(" ", "end")]:
            if c != color and run:
                spans.append((run, color))
                run = ""
            run += ch
            color = c
        x = pad
        for text, c in spans:
            if c and text.strip():
                out.append(f'<text x="{x:.1f}" y="{ty}" fill="{c}" textLength="{len(text) * cw:.1f}">{escape(text)}</text>')
            x += len(text) * cw
    out.append("</g>")

    top = pad + (ROWS * lh - (len(INFO) + 2) * 26) / 2
    for i, (k, v) in enumerate(INFO):
        ty = top + (i + 1) * 26
        if v is None:
            fill = KEY if i == 0 else DIM
            out.append(f'<text x="{info_x}" y="{ty:.0f}" fill="{fill}" font-weight="{700 if i == 0 else 400}">{escape(k)}</text>')
        else:
            out.append(
                f'<text x="{info_x}" y="{ty:.0f}" xml:space="preserve"><tspan fill="{KEY}">{escape(k)}:</tspan>'
                f'<tspan x="{info_x + 125}" fill="{FG}">{escape(v)}</tspan></text>'
            )
    sy = top + (len(INFO) + 1.2) * 26
    for i, c in enumerate(PALETTE):
        out.append(f'<rect x="{info_x + i * 28}" y="{sy:.0f}" width="24" height="15" rx="2" fill="{c}"/>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    src = Image.open(sys.argv[1]).convert("RGBA") if len(sys.argv) > 1 else load_cutout()
    with open("assets/card.svg", "w") as f:
        f.write(build_svg(ascii_cells(src)))
