#!/usr/bin/env python3
"""Create a new note from an existing template.

Copies a template folder into notes/<name>, ready for editing.

Usage:
    python scripts/new_note.py                  (interactive)
    python scripts/new_note.py <template> <name> (direct)

Examples:
    python scripts/new_note.py lang_note_template macbeth_themes
    python scripts/new_note.py apply_test_template romeo_juliet_act1
"""

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT / "notes"
TEMPLATES = [
    d.name
    for d in sorted(ROOT.iterdir())
    if d.is_dir() and (d / "images").is_dir() and list(d.glob("*.tex"))
    and d.name != "user_guide" and d.name != "notes"
]


def slugify(name: str) -> str:
    """Turn a human name into a safe folder/file name."""
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = s.strip("_")
    return s


def pick_template() -> str:
    print("\nAvailable templates:\n")
    for i, t in enumerate(TEMPLATES, 1):
        print(f"  {i}. {t}")
    print()
    while True:
        choice = input("Pick a template (number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(TEMPLATES):
            return TEMPLATES[int(choice) - 1]
        print("  Invalid choice, try again.")


def pick_name() -> str:
    print()
    while True:
        name = input("Note name (e.g. macbeth_themes): ").strip()
        if name:
            return slugify(name)
        print("  Name cannot be empty.")


def create_note(template_name: str, note_name: str) -> Path:
    template_dir = ROOT / template_name
    if not template_dir.is_dir():
        print(f"Error: Template '{template_name}' not found.")
        sys.exit(1)

    note_slug = slugify(note_name)
    note_dir = NOTES_DIR / note_slug
    if note_dir.exists():
        print(f"Error: '{note_dir}' already exists.")
        sys.exit(1)

    NOTES_DIR.mkdir(exist_ok=True)

    # Copy template folder
    shutil.copytree(template_dir, note_dir)

    # Rename the .tex file
    tex_files = list(note_dir.glob("*.tex"))
    if tex_files:
        old_tex = tex_files[0]
        new_tex = note_dir / f"{note_slug}.tex"
        old_tex.rename(new_tex)

        # Update internal references if the PDF name matters
        # (LuaLaTeX uses the .tex filename for the .pdf output)

    # Remove any leftover PDFs from the template
    for pdf in note_dir.glob("*.pdf"):
        pdf.unlink()

    # Fix font paths -- notes are one level deeper (notes/<name>/)
    # Templates use ../fonts/, notes need ../../fonts/
    new_tex = note_dir / f"{note_slug}.tex"
    if new_tex.exists():
        content = new_tex.read_text(encoding="utf-8")
        content = content.replace("Path = ../fonts/", "Path = ../../fonts/")
        new_tex.write_text(content, encoding="utf-8")

    return note_dir


def main() -> None:
    print("=" * 48)
    print("  Create a New Note from a Template")
    print("=" * 48)

    if len(sys.argv) == 3:
        template_name = sys.argv[1]
        note_name = sys.argv[2]
    elif len(sys.argv) == 1:
        template_name = pick_template()
        note_name = pick_name()
    else:
        print(__doc__)
        sys.exit(1)

    note_dir = create_note(template_name, note_name)

    print(f"\nCreated: {note_dir.relative_to(ROOT)}/")
    print(f"\nNext steps:")
    print(f"  1. Open {note_dir.name}/{note_dir.name}.tex in a text editor")
    print(f"  2. Replace the placeholder content with your own")
    print(f"  3. Build the PDF:")
    print(f"     python scripts/build_pdf.py notes/{note_dir.name}/")
    print()


if __name__ == "__main__":
    main()
