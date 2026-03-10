"""
Fetch Norway budget story images from Medium CDN and convert to WebP.
Run from project root: python scripts/fetch_norway_budget_images.py
"""
import os
import urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install Pillow")
    raise

OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "img" / "stories-images" / "norway-budget"
QUALITY = 80
ORIENTATION_TAG = 274
MEDIUM_BASE = "https://miro.medium.com/v2/"

# Order and (Medium image ID, optional alt/caption for filename)
IMAGES = [
    ("1*NCvXeRWDgAMtk3AJZI0_NQ.png", "norway-budget-hero"),
    ("1*hX1auRspypgI-fexV7kfmw.png", "norway-budget-1"),
    ("1*qtY0q7FhZ_kmJp3YdR9RVQ.png", "norway-budget-2"),
    ("1*5mwvsYbZjbRjivPqPAIx0g.png", "norway-budget-3"),
    ("1*Ps6eY51DybvmDE7jXRRWVQ.png", "norway-budget-4"),
    ("1*nVbeC5Bv92lSRzWav5joKQ.png", "norway-budget-5"),
    ("1*3bKYQT-XMy__ho4JcvxNSg.png", "norway-budget-6"),
    ("1*bW0-H01QXBEySamjFmuu_g.png", "norway-budget-7"),
    ("1*H7ZCxPxAOxVq1jEIOPgueQ.png", "norway-budget-8"),
    ("1*3cW38ZX19_b_3bzS63rmXg.png", "norway-budget-9"),
    ("1*Qe0KYQCIj0gEsRxMdfZwdg.png", "norway-budget-10"),
    ("1*kY5MEqB3g_aPjMSu-652yw.jpeg", "norway-budget-11"),
    ("1*Qu5JEJIAXR7p8eJEckLOAQ.png", "norway-budget-12"),
]


def apply_orientation(img):
    try:
        exif = img.getexif()
        if not exif:
            return img
        try:
            o = int(exif.get(ORIENTATION_TAG, 1) or 1)
        except (TypeError, ValueError):
            o = 1
        if o == 3:
            return img.rotate(180, expand=True)
        if o == 6:
            return img.rotate(270, expand=True)
        if o == 8:
            return img.rotate(90, expand=True)
    except Exception:
        pass
    return img


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for medium_id, base_name in IMAGES:
        url = MEDIUM_BASE + medium_id
        ext = Path(medium_id).suffix
        local_path = OUT_DIR / (base_name + ext)
        webp_path = OUT_DIR / (base_name + ".webp")

        if webp_path.exists():
            print(f"Skip (exists): {base_name}.webp")
            continue

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
        except Exception as e:
            print(f"Download failed {medium_id}: {e}")
            continue

        local_path.write_bytes(data)
        img = Image.open(local_path)
        img = apply_orientation(img)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(webp_path, "WEBP", quality=QUALITY)
        img.close()
        local_path.unlink()
        print(f"OK: {base_name}.webp")

    print("Done.")


if __name__ == "__main__":
    main()
