#!/usr/bin/env python3
"""Build labeled contact sheets so every fetched photo gets a human/model look.

Usage:
    python contact_sheet.py <site-root> [out-dir] [--dir <folder-of-images>]

Default: reads <site-root>/places_manifest.json and sheets every ok photo.
--dir mode: sheets a flat folder (used for reviewing replacement candidates).

Why this exists: Places returns photos in an uncurated order, so the top photo for a
quiet residential place is often a parked car, a restaurant interior, or someone's fish.
Reviewing 120 images one file at a time is impractical; 6 contact sheets is ~6 glances.
Read the output with an image-capable Read tool and flag anything that isn't
recognizably the place.

Requires Pillow (pip install pillow).
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

THUMB = 260
COLS = 5
PAD = 6
LABEL_H = 34
PER_SHEET = 20


def font():
    for p in ("/System/Library/Fonts/Helvetica.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, 12)
            except Exception:
                pass
    return ImageFont.load_default()


def build(items, out_dir, prefix="sheet"):
    """items: list of (label, image_path)"""
    os.makedirs(out_dir, exist_ok=True)
    f = font()
    paths = []
    for start in range(0, len(items), PER_SHEET):
        batch = items[start:start + PER_SHEET]
        rows = (len(batch) + COLS - 1) // COLS
        W = COLS * (THUMB + PAD) + PAD
        H = rows * (THUMB + LABEL_H + PAD) + PAD
        sheet = Image.new("RGB", (W, H), "white")
        draw = ImageDraw.Draw(sheet)
        for idx, (label, path) in enumerate(batch):
            r, c = divmod(idx, COLS)
            x = PAD + c * (THUMB + PAD)
            y = PAD + r * (THUMB + LABEL_H + PAD)
            try:
                im = Image.open(path).convert("RGB")
                im.thumbnail((THUMB, THUMB))
                sheet.paste(im, (x + (THUMB - im.width) // 2,
                                 y + (THUMB - im.height) // 2))
            except Exception:
                draw.rectangle([x, y, x + THUMB, y + THUMB], outline="red")
            draw.text((x, y + THUMB + 2), label[:40], fill="black", font=f)
            if len(label) > 40:
                draw.text((x, y + THUMB + 16), label[40:80], fill="black", font=f)
        out = os.path.join(out_dir, f"{prefix}_{start // PER_SHEET:02d}.png")
        sheet.save(out)
        paths.append(out)
        print(out)
    return paths


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") \
        else os.path.join(root, "_contact_sheets")

    if "--dir" in sys.argv:
        folder = sys.argv[sys.argv.index("--dir") + 1]
        items = [(fn.rsplit(".", 1)[0], os.path.join(folder, fn))
                 for fn in sorted(os.listdir(folder))
                 if fn.lower().endswith((".jpg", ".jpeg", ".png"))]
        build(items, out_dir, prefix="candidates")
        return

    manifest = json.load(open(os.path.join(root, "places_manifest.json")))
    items = [(k.replace("landmark::", "L:").replace("hood::", "H:"),
              os.path.join(root, v["file"]))
             for k, v in sorted(manifest.items()) if v.get("ok")]
    build(items, out_dir)
    print(f"\n{len(items)} photos across {(len(items) + PER_SHEET - 1) // PER_SHEET} sheets.")
    print("Review every sheet. Anything not recognizably the place -> re-fetch "
          "candidates 2-5 for that place, or drop it (ok:false) and let the page "
          "fall back to text + map.")


if __name__ == "__main__":
    main()
