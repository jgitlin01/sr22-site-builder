#!/usr/bin/env python3
"""Fetch real Google Places photos + attribution into a resumable manifest.

Usage:
    python fetch_photos.py <site-root> <places.json>

places.json is a list of {"key": "...", "query": "..."} — key is a stable id you'll
use to look the photo up when generating pages, query is what to search Places for:

    [
      {"key": "landmark::naples::Naples Pier", "query": "Naples Pier, Naples, FL"},
      {"key": "hood::naples::old-naples",      "query": "Old Naples, Naples, FL"}
    ]

Reads GOOGLE_PLACES_API_KEY from <site-root>/.env
Writes images to <site-root>/assets/images/places/ and a manifest to
<site-root>/places_manifest.json

Resumable: entries already marked ok are skipped, so reruns don't re-bill.
"""
import json
import os
import re
import sys
import time
import urllib.request

SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
FIELD_MASK = "places.id,places.displayName,places.photos,places.formattedAddress"


def load_key(root):
    env = os.path.join(root, ".env")
    if not os.path.exists(env):
        sys.exit(f"No .env at {env} (need GOOGLE_PLACES_API_KEY=...)")
    for line in open(env):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            if k.strip() == "GOOGLE_PLACES_API_KEY":
                return v.strip()
    sys.exit("GOOGLE_PLACES_API_KEY not found in .env")


def slugify(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def search_text(query, key):
    req = urllib.request.Request(
        SEARCH_URL,
        data=json.dumps({"textQuery": query}).encode(),
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": key,
            "X-Goog-FieldMask": FIELD_MASK,
        },
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())


def download(photo_name, dest, key, max_w=1000):
    url = f"https://places.googleapis.com/v1/{photo_name}/media?maxWidthPx={max_w}&key={key}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    root, places_file = sys.argv[1], sys.argv[2]
    key = load_key(root)
    places = json.load(open(places_file))

    out_dir = os.path.join(root, "assets", "images", "places")
    os.makedirs(out_dir, exist_ok=True)
    manifest_path = os.path.join(root, "places_manifest.json")
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}

    def save():
        json.dump(manifest, open(manifest_path, "w"), indent=1)

    for i, item in enumerate(places, 1):
        k, query = item["key"], item["query"]
        if manifest.get(k, {}).get("ok"):
            continue  # resumable
        try:
            res = search_text(query, key)
            hits = res.get("places", [])
            if not hits or not hits[0].get("photos"):
                print(f"  NO PHOTO: {query}")
                manifest[k] = {"ok": False, "reason": "no_photo", "query": query}
            else:
                p = hits[0]
                photo = p["photos"][0]
                fname = f"{slugify(k)}.jpg"
                size = download(photo["name"], os.path.join(out_dir, fname), key)
                attrs = photo.get("authorAttributions") or [{}]
                manifest[k] = {
                    "ok": True,
                    "file": f"assets/images/places/{fname}",
                    "bytes": size,
                    "credit": attrs[0].get("displayName", "Google Maps contributor"),
                    "matched_name": p.get("displayName", {}).get("text", ""),
                    "address": p.get("formattedAddress", ""),
                    "query": query,
                }
                print(f"  OK: {query} -> {fname} ({size}b, {manifest[k]['credit']})")
        except Exception as e:
            print(f"  ERROR: {query} -> {e}")
            manifest[k] = {"ok": False, "reason": str(e), "query": query}
        if i % 10 == 0:
            save()
        time.sleep(0.05)

    save()
    ok = sum(1 for v in manifest.values() if v.get("ok"))
    print(f"\ntotal={len(manifest)} ok={ok} failed={len(manifest) - ok}")
    print("NEXT: run contact_sheet.py and review every photo before generating pages.")


if __name__ == "__main__":
    main()
