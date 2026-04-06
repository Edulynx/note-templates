#!/usr/bin/env python3
"""Extract images from a DOCX file into a LaTeX project's images/ directory.

Usage:
    python scripts/extract_docx.py <input.docx> <output_dir>

Example:
    python scripts/extract_docx.py originals/LangNote.docx lang_note_template/
"""

import sys
import zipfile
from pathlib import Path


# Map of relationship target -> friendly filename
IMAGE_NAMES = {
    "media/image1.png": "header_banner.png",
    "media/image2.png": "design_placeholder.png",
    "media/image3.png": "teaching_icon.png",
}


def extract_images(docx_path: str, output_dir: str) -> None:
    docx = Path(docx_path)
    out = Path(output_dir) / "images"
    out.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(docx, "r") as zf:
        media_files = [n for n in zf.namelist() if n.startswith("word/media/")]
        if not media_files:
            print(f"No media files found in {docx_path}")
            return

        for media_path in media_files:
            rel_path = media_path.replace("word/", "", 1)
            friendly = IMAGE_NAMES.get(rel_path, Path(media_path).name)
            dest = out / friendly
            dest.write_bytes(zf.read(media_path))
            print(f"  Extracted: {media_path} -> {dest}")

    print(f"\nDone. {len(media_files)} image(s) extracted to {out}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    extract_images(sys.argv[1], sys.argv[2])
