"""
Fetch story images from Medium CDN and convert to WebP.
Usage: python scripts/fetch_story_images.py <story>
Story: nepal | parvathamalai
"""
import sys
import urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install Pillow")
    raise

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUALITY = 80
ORIENTATION_TAG = 274
MEDIUM_BASE = "https://miro.medium.com/v2/"

# Nepal: 15 images (hero + 14 in-body). Medium IDs from JSON - some have 0* prefix.
NEPAL_IMAGES = [
    ("1*cm6hbUT3nayDwne3tEVxgw.png", "nepal-hero"),
    ("0*CQU_Z97sSvJNtVmh.", "nepal-1"),
    ("0*Cn_f68ksYeX2I-vJ.", "nepal-2"),
    ("0*USFE-Wr4kD_F2pfU.", "nepal-3"),
    ("0*FJaRxpqK54SW9DMd.", "nepal-4"),
    ("0*nxzkH0RsysMy2dOk.", "nepal-5"),
    ("0*tQ29iZJABnuqIrYz.", "nepal-6"),
    ("0*qGfk-Xc1mAtIjC8_.", "nepal-7"),
    ("0*-JCQKABfkmOilSyK.", "nepal-8"),
    ("0*6qbVvXm2ifZHdu-F.", "nepal-9"),
    ("0*odCB-8EJ9VTbu-sm.", "nepal-10"),
    ("0*TTSpLJDw1tOlOyRL.", "nepal-11"),
    ("0*aHD7MF0CESjEwGmS.", "nepal-12"),
    ("0*yKMcjaTfZz-NPJzy.", "nepal-13"),
    ("0*U82MiIO5tJLethNZ.", "nepal-14"),
]

# Parvathamalai: 21 images. First 10 inline, last 11 in grid.
PARVATHAMALAI_IMAGES = [
    ("1*AvdcIRdmNSl_w_77HhfPSA.jpeg", "parvathamalai-hero"),
    ("1*swh1qdjhInhXrdPhtUgMiw.jpeg", "parvathamalai-1"),
    ("1*_YlvTYitPsR5fL_2t49Z2Q.jpeg", "parvathamalai-2"),
    ("1*7v9HcMSPhuiiDR95UnRETg.jpeg", "parvathamalai-3"),
    ("1*LdpNJQYfkJVQ-1zUd0_CZw.png", "parvathamalai-4"),
    ("1*0cOuclpfIDrWOYuaAnxRmA.png", "parvathamalai-5"),
    ("1*qQnH33vxTOr-vKqPnZGSyw.jpeg", "parvathamalai-6"),
    ("1*gwwa_nA8w8mWsUNpWOs2gw.jpeg", "parvathamalai-7"),
    ("1*6axCm551nNm77E18Gkh1fA.jpeg", "parvathamalai-8"),
    ("1*FBBhUzUHxJuYJtl4PoagDw.jpeg", "parvathamalai-9"),
    ("1*cTfiNoYWhXmktlzqpHtcWw.jpeg", "parvathamalai-grid-1"),
    ("1*SQkzKF4Qr1qzAeQCKom8JA.jpeg", "parvathamalai-grid-2"),
    ("1*qpGClcFYBlPZvMdcGTz9rg.jpeg", "parvathamalai-grid-3"),
    ("1*cTGX92M-xNwfyyd1Z2VsfA.jpeg", "parvathamalai-grid-4"),
    ("1*1ppCu8kbvDlkBnOvulGD_A.jpeg", "parvathamalai-grid-5"),
    ("1*4F09APBCsjwyPqDgRgUg9Q.jpeg", "parvathamalai-grid-6"),
    ("1*mgRso8oujTsPOlBjbmsp0A.jpeg", "parvathamalai-grid-7"),
    ("1*RlTHzM087fe454cKJR_XJw.jpeg", "parvathamalai-grid-8"),
    ("1*S5QA8fWHSsajKTffcntvCQ.jpeg", "parvathamalai-grid-9"),
    ("1*vZ5K0RgRKGD-B7um7NYDbg.jpeg", "parvathamalai-grid-10"),
    ("1*N7BIISe7nb0Gt0bFTgeXpw.jpeg", "parvathamalai-grid-11"),
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


def normalize_medium_id(medium_id):
    """Ensure ID has an extension for URL (for 1* IDs). 0* stay as-is."""
    if medium_id.startswith("0*"):
        return medium_id  # old format, no extension
    if medium_id.endswith(".") and "." not in medium_id[:-1]:
        return medium_id + "png"
    return medium_id


def medium_url(medium_id):
    """Older 0* IDs use v1 and no extension."""
    if medium_id.startswith("0*"):
        return "https://miro.medium.com/v1/" + medium_id
    return MEDIUM_BASE + normalize_medium_id(medium_id)


def fetch_images(images_list, folder_name):
    out_dir = PROJECT_ROOT / "assets" / "img" / "stories-images" / folder_name
    out_dir.mkdir(parents=True, exist_ok=True)
    for medium_id, base_name in images_list:
        raw_id = medium_id
        url = medium_url(medium_id)
        medium_id_norm = normalize_medium_id(medium_id)
        ext = Path(medium_id_norm).suffix if "." in medium_id_norm and not medium_id_norm.startswith("0*") else ".png"
        if not ext or ext == ".":
            ext = ".png"
        local_path = out_dir / (base_name + ext)
        webp_path = out_dir / (base_name + ".webp")

        if webp_path.exists():
            print(f"Skip (exists): {base_name}.webp")
            continue

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"},
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
        except Exception as e:
            print(f"Download failed {raw_id}: {e}")
            continue

        local_path.write_bytes(data)
        try:
            img = Image.open(local_path)
        except Exception as e:
            print(f"Open failed {base_name}: {e}")
            local_path.unlink(missing_ok=True)
            continue
        img = apply_orientation(img)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(webp_path, "WEBP", quality=QUALITY)
        img.close()
        local_path.unlink(missing_ok=True)
        print(f"OK: {base_name}.webp")
    print(f"Done: {folder_name}")


def main():
    which = (sys.argv[1:] or ["nepal", "parvathamalai"])[0].lower()
    if which == "nepal":
        fetch_images(NEPAL_IMAGES, "nepal-2700-kms")
    elif which == "parvathamalai":
        fetch_images(PARVATHAMALAI_IMAGES, "parvathamalai")
    else:
        print("Usage: python fetch_story_images.py nepal|parvathamalai")
        sys.exit(1)


if __name__ == "__main__":
    main()
