#!/usr/bin/env python3
"""Build PDF from a LaTeX template using LuaLaTeX.

Usage:
    python scripts/build_pdf.py <template_dir> [--open]

Example:
    python scripts/build_pdf.py lang_note_template/
    python scripts/build_pdf.py lang_note_template/ --open
"""

import platform
import subprocess
import sys
from pathlib import Path


def build_pdf(template_dir: str, open_after: bool = False) -> None:
    tdir = Path(template_dir).resolve()
    tex_files = list(tdir.glob("*.tex"))
    if not tex_files:
        print(f"No .tex files found in {tdir}")
        sys.exit(1)

    tex_file = tex_files[0]
    print(f"Building: {tex_file.name}")

    # Run lualatex twice for cross-references
    for pass_num in (1, 2):
        print(f"  Pass {pass_num}/2...")
        result = subprocess.run(
            [
                "lualatex",
                "-interaction=nonstopmode",
                "-output-directory",
                str(tdir),
                str(tex_file),
            ],
            capture_output=True,
            text=True,
            cwd=str(tdir),
        )
        if result.returncode != 0:
            print(f"  LuaLaTeX error on pass {pass_num}:")
            lines = result.stdout.strip().split("\n")
            for line in lines[-20:]:
                print(f"    {line}")
            sys.exit(1)

    pdf_path = tdir / tex_file.with_suffix(".pdf").name
    if pdf_path.exists():
        print(f"\nSuccess: {pdf_path.name} ({pdf_path.stat().st_size / 1024:.0f} KB)")
    else:
        print("Error: PDF was not generated")
        sys.exit(1)

    if open_after:
        system = platform.system()
        if system == "Windows":
            subprocess.run(["start", "", str(pdf_path)], shell=True, check=False)
        elif system == "Darwin":
            subprocess.run(["open", str(pdf_path)], check=False)
        else:
            subprocess.run(["xdg-open", str(pdf_path)], check=False)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    open_flag = "--open" in sys.argv
    dirs = [a for a in sys.argv[1:] if a != "--open"]
    for d in dirs:
        build_pdf(d, open_after=open_flag)
