#!/usr/bin/env python3
"""
Cross-platform setup script for EduLynx LaTeX Templates.
Works on Windows, macOS, and Linux.

Usage:
    python setup.py
"""

import os
import platform
import shutil
import subprocess
import sys
import venv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TEMPLATES = [
    "lang_note_template",
    "apply_test_template",
    "copy_apply_test_template",
    "research_common_template",
]


def banner(msg: str) -> None:
    print(f"\n{'=' * 50}")
    print(f"  {msg}")
    print(f"{'=' * 50}\n")


def check_command(name: str) -> bool:
    return shutil.which(name) is not None


def check_dependencies() -> list[str]:
    missing = []

    if not check_command("lualatex"):
        if platform.system() == "Windows":
            missing.append("LuaLaTeX - Install MiKTeX from https://miktex.org/download")
        elif platform.system() == "Darwin":
            missing.append("LuaLaTeX - Install MacTeX from https://tug.org/mactex/")
        else:
            missing.append("LuaLaTeX - Install with: sudo apt install texlive-full")

    if not check_command("python3") and not check_command("python"):
        missing.append("Python 3 - Download from https://python.org/downloads/")

    # Check bundled fonts exist
    fonts_dir = ROOT / "fonts"
    required_fonts = [
        "Arimo-Regular.ttf",
        "Arimo-Bold.ttf",
        "SourceSerifPro-Regular.otf",
        "Kalam-Bold.ttf",
        "Roboto-Regular.ttf",
        "NotoColorEmoji.ttf",
    ]
    for font in required_fonts:
        if not (fonts_dir / font).exists():
            missing.append(f"Font missing: fonts/{font}")

    return missing


def setup_venv() -> Path:
    venv_dir = ROOT / "venv"
    if not venv_dir.exists():
        print("Creating virtual environment...")
        venv.create(str(venv_dir), with_pip=True)
        print(f"  Created: {venv_dir}")
    else:
        print(f"  Virtual environment already exists: {venv_dir}")

    # Determine pip path
    if platform.system() == "Windows":
        pip = venv_dir / "Scripts" / "pip.exe"
        python = venv_dir / "Scripts" / "python.exe"
    else:
        pip = venv_dir / "bin" / "pip"
        python = venv_dir / "bin" / "python"

    # Install requirements
    print("  Installing Python packages...")
    subprocess.run(
        [str(pip), "install", "--upgrade", "pip", "-q"],
        check=True,
    )
    subprocess.run(
        [str(pip), "install", "-r", str(ROOT / "requirements.txt"), "-q"],
        check=True,
    )
    print("  Done.")
    return python


def copy_originals() -> None:
    originals = ROOT / "originals"
    originals.mkdir(exist_ok=True)
    for docx in ROOT.glob("*.docx"):
        dest = originals / docx.name
        if not dest.exists():
            shutil.copy2(docx, dest)
            print(f"  Copied: {docx.name}")


def extract_images(python: Path) -> None:
    extract_script = ROOT / "scripts" / "extract_docx.py"
    docx_map = {
        "Lang Note Template.docx": "lang_note_template",
        "Apply and Test a Notes Template.docx": "apply_test_template",
        "Copy of Apply and Test a Notes Template.docx": "copy_apply_test_template",
        "Research Common Elements in Literature Notes.docx": "research_common_template",
    }
    for docx_name, tdir in docx_map.items():
        docx_path = ROOT / "originals" / docx_name
        tdir_path = ROOT / tdir
        if docx_path.exists() and tdir_path.exists():
            subprocess.run(
                [str(python), str(extract_script), str(docx_path), str(tdir_path)],
                check=True,
            )


def main() -> None:
    banner("EduLynx LaTeX Templates - Setup")

    # 1. Check dependencies
    print("Checking dependencies...")
    missing = check_dependencies()
    if missing:
        print("\n  WARNING - Missing dependencies:")
        for dep in missing:
            print(f"    - {dep}")
        print("\n  Setup will continue, but PDF building may fail.\n")
    else:
        print("  All dependencies found.\n")

    # 2. Setup venv
    print("Setting up Python environment...")
    python = setup_venv()

    # 3. Copy originals
    print("\nCopying DOCX originals...")
    copy_originals()

    # 4. Extract images
    print("\nExtracting images from DOCX files...")
    extract_images(python)

    # 5. Print usage
    is_win = platform.system() == "Windows"

    banner("Setup Complete!")

    if is_win:
        activate = r"venv\Scripts\activate"
        py = "python"
    else:
        activate = "source venv/bin/activate"
        py = "python"

    print("To get started:\n")
    print(f"  1. Activate the environment:")
    print(f"     {activate}\n")
    print(f"  2. Build a single template:")
    print(f"     {py} scripts/build_pdf.py lang_note_template/\n")
    print(f"  3. Build all templates:")
    for t in TEMPLATES:
        print(f"     {py} scripts/build_pdf.py {t}/")
    print()


if __name__ == "__main__":
    main()
