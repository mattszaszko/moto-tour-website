"""
Convert Nepal story JPGs to WebP, delete placeholders and originals.
Run from project root: python scripts/convert_nepal_jpgs.py
"""
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    print("Install Pillow: pip install Pillow")
    raise

DIR = Path(__file__).resolve().parent.parent / "assets" / "img" / "stories-images" / "nepal-2700-kms"
QUALITY = 80
ORIENTATION_TAG = 274


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
    # Convert all JPGs to WebP
    for p in DIR.glob("*.jpg"):
        webp_path = p.with_suffix(".webp")
        if webp_path.exists() and webp_path.stat().st_mtime > p.stat().st_mtime:
            print(f"Skip (newer exists): {p.name}")
            continue
        img = Image.open(p)
        img = apply_orientation(img)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(webp_path, "WEBP", quality=QUALITY)
        img.close()
        print(f"OK: {p.name} -> {webp_path.name}")

    # Delete JPGs
    for p in DIR.glob("*.jpg"):
        p.unlink()
        print(f"Deleted: {p.name}")

    # Delete old placeholder WebPs (nepal-1 through nepal-14)
    for i in range(1, 15):
        placeholder = DIR / f"nepal-{i}.webp"
        if placeholder.exists():
            placeholder.unlink()
            print(f"Deleted placeholder: {placeholder.name}")

    # Delete old hero if it exists and we have new one (nepal-hero.webp stays, we overwrote via conversion)
    # The new nepal-hero.jpg was converted to nepal-hero.webp - so we're good. Old hero was already overwritten.
    print("Done.")


if __name__ == "__main__":
    main()
