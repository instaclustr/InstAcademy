#!/usr/bin/env python3
"""
Generate InstAcademy banner art from one template, so every track looks like
the same programme rather than a folder of unrelated images.

    python3 .github/scripts/make_banners.py

Writes 1280x320 PNGs into assets/banners/. Add a line to TRACKS for a new
track and re-run; do not hand-edit the output.
"""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 320
NAVY = (11, 36, 52)
TEAL_BG = (10, 85, 102)
TEAL = (63, 195, 212)
PALE = (143, 217, 228)
WHITE = (255, 255, 255)

FONTS = "/System/Library/Fonts/Supplemental/"
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(
    ["git", "-C", _HERE, "rev-parse", "--show-toplevel"],
    capture_output=True, text=True, check=True,
).stdout.strip()
OUT = os.path.join(REPO, "assets", "banners")
BADGE_OUT = os.path.join(REPO, "assets", "badges")

COURSES = [
    ("opensearch-01-vector-storage-and-search", "Vector Storage & Search",
     "INSTACADEMY  ·  OPENSEARCH  ·  COURSE 01",
     "k-NN and HNSW, neural pipelines, hybrid search, RAG"),
    ("opensearch-02-advanced-rag", "Advanced RAG",
     "INSTACADEMY  ·  OPENSEARCH  ·  COURSE 02",
     "Chunking, grounded prompting, hybrid retrieval, memory"),
]

# Placeholder badge art. The dashed ring marks these as not-final: replace the
# PNGs in assets/badges/ with the real Credly artwork at the same filenames and
# the README needs no edit.
BADGES = [
    ("opensearch-01-vector-storage-and-search", "01", "OPENSEARCH", "VECTOR STORAGE\n& SEARCH"),
    ("opensearch-02-advanced-rag", "02", "OPENSEARCH", "ADVANCED\nRAG"),
]

TRACKS = [
    ("instacademy", "InstAcademy", "FREE SELF-PACED COURSES  ·  NETAPP INSTACLUSTR",
     "Real clusters. Real data. Real output."),
    ("opensearch", "OpenSearch", "INSTACADEMY  ·  TRACK",
     "Vectors, neural pipelines, hybrid search, and RAG"),
]


def font(name, size):
    for candidate in (name, "Arial.ttf"):
        try:
            return ImageFont.truetype(FONTS + candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def gradient(h=H):
    """Diagonal navy -> teal wash."""
    H = h
    img = Image.new("RGB", (W, h))
    px = img.load()
    for y in range(h):
        for x in range(0, W, 4):
            t = (x / W) * 0.75 + (y / h) * 0.25
            c = (
                int(NAVY[0] + (TEAL_BG[0] - NAVY[0]) * t),
                int(NAVY[1] + (TEAL_BG[1] - NAVY[1]) * t),
                int(NAVY[2] + (TEAL_BG[2] - NAVY[2]) * t),
            )
            for dx in range(4):
                if x + dx < W:
                    px[x + dx, y] = c
    return img


def topology(draw, h=H):
    """A small cluster graph — four nodes around a centre, with satellites."""
    cx, cy, r = 1010, h // 2, 92
    pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    sats = [(cx + r + 105, cy - 62), (cx + r + 105, cy + 62), (cx - r - 105, cy)]

    for i in range(4):
        draw.line([pts[i], pts[(i + 1) % 4]], fill=TEAL + (0,), width=2)
    for a, b in ((0, 2), (1, 3)):
        draw.line([pts[a], pts[b]], fill=TEAL, width=1)
    draw.line([pts[1], sats[0]], fill=TEAL, width=1)
    draw.line([pts[1], sats[1]], fill=TEAL, width=1)
    draw.line([pts[3], sats[2]], fill=TEAL, width=1)
    for i in range(4):
        draw.line([pts[i], pts[(i + 1) % 4]], fill=TEAL, width=2)
    for x, y in pts:
        draw.ellipse([x - 9, y - 9, x + 9, y + 9], fill=TEAL)
    for x, y in sats:
        draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=PALE)


def tracked(draw, xy, text, fnt, fill, spacing):
    """PIL has no letter-spacing, so step the pen manually."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing
    return x


def neighbours(draw, h):
    """A query point and its nearest neighbours — the thing this course is about."""
    import random
    random.seed(7)
    cx, cy = 1010, h // 2
    for _ in range(46):
        x = cx + random.gauss(0, 118)
        y = cy + random.gauss(0, h * 0.20)
        d = ((x - cx) ** 2 + ((y - cy) * 1.7) ** 2) ** 0.5
        if d < 60:
            draw.line([(cx, cy), (x, y)], fill=TEAL, width=1)
            draw.ellipse([x - 6, y - 6, x + 6, y + 6], fill=TEAL)
        else:
            r = 4
            draw.ellipse([x - r, y - r, x + r, y + r], fill=PALE)
    draw.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=WHITE)


def build(slug, title, eyebrow, tagline, h=H, size=66, motif=None):
    img = gradient(h)
    draw = ImageDraw.Draw(img)
    (motif or topology)(draw, h) if motif else topology(draw)

    top = 78 if h >= H else 46
    tracked(draw, (80, top), eyebrow, font("Arial Bold.ttf", 17), PALE, 3.2)
    draw.text((78, top + 30), title, font=font("Arial Black.ttf", size), fill=WHITE)
    draw.text((80, top + 30 + size + 22), tagline, font=font("Arial.ttf", 21), fill=PALE)
    bar = top + 30 + size + 70
    draw.rectangle([80, bar, 152, bar + 4], fill=TEAL)

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{slug}.png")
    img.save(path, "PNG", optimize=True)
    print(f"  {path}  ({os.path.getsize(path) // 1024} KB)")


def build_badge(slug, number, tech, title, size=512):
    """A round placeholder badge, legible at the 150px the README renders it."""
    S = size
    # RGBA with transparent corners, so it reads as a disc on light and dark alike
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = cy = S // 2

    for r, col in ((S // 2 - 6, TEAL_BG + (255,)), (S // 2 - 34, NAVY + (255,))):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

    # dashed outer ring: the signal that this is not final artwork
    r = S // 2 - 20
    for a in range(0, 360, 12):
        draw.arc([cx - r, cy - r, cx + r, cy + r], a, a + 7, fill=TEAL, width=4)

    draw.text((cx, cy - S * 0.20), tech, font=font("Arial Bold.ttf", int(S * 0.055)),
              fill=PALE, anchor="mm")
    draw.text((cx, cy - S * 0.045), number, font=font("Arial Black.ttf", int(S * 0.26)),
              fill=WHITE, anchor="mm")
    draw.line([cx - S * 0.13, cy + S * 0.085, cx + S * 0.13, cy + S * 0.085], fill=TEAL, width=3)
    draw.multiline_text((cx, cy + S * 0.175), title, font=font("Arial Bold.ttf", int(S * 0.062)),
                        fill=WHITE, anchor="mm", align="center", spacing=int(S * 0.022))

    os.makedirs(BADGE_OUT, exist_ok=True)
    path = os.path.join(BADGE_OUT, f"{slug}.png")
    img.save(path, "PNG", optimize=True)
    print(f"  {path}  ({os.path.getsize(path) // 1024} KB)")


if __name__ == "__main__":
    for t in TRACKS:
        build(*t)
    for c in COURSES:
        build(*c, h=224, size=48, motif=neighbours)
    for b in BADGES:
        build_badge(*b)
