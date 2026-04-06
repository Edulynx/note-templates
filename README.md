# EduLynx Note Templates

LaTeX templates for mass-producing English literature note worksheets. Converted from Canva DOCX originals with pixel-accurate fidelity — matching fonts, colours, emoji, tables, and layout.

## Templates

| Template | Style | Preview |
|----------|-------|---------|
| `lang_note_template` | Purple, Source Serif Pro headers | Designing note-taking templates |
| `apply_test_template` | Teal, Kalam handwritten headers | Applying and testing notes |
| `research_common_template` | Dark teal, Roboto modern headers | Researching literary elements |
| `copy_apply_test_template` | Teal (spare copy) | Same as apply_test |

## Quick Start

### Prerequisites

- **LuaLaTeX** — [MiKTeX](https://miktex.org/download) (Windows) or `sudo apt install texlive-full` (Linux) or [MacTeX](https://tug.org/mactex/) (Mac)
- **Python 3** — [python.org/downloads](https://python.org/downloads/) (Windows: tick "Add to PATH")

### Create a note

**Double-click** `new_note.bat` (Windows) or `new_note.sh` (Mac/Linux), pick a template, type a name. Your note appears in `notes/<name>/`.

Or via terminal:

```
python scripts/new_note.py lang_note_template macbeth_themes
```

### Edit the note

Open `notes/<name>/<name>.tex` in any text editor (Notepad, Notepad++, TextEdit). Replace the placeholder text with your own content. Use ChatGPT or Claude to generate it — see the [User Guide](USER-GUIDE.pdf) for a ready-to-copy prompt.

### Build the PDF

**Double-click** `build_all.bat` (Windows) or `build_all.sh` (Mac/Linux) to build all notes.

Or build a single note:

```
python scripts/build_pdf.py notes/macbeth_themes/
```

## Project Structure

```
├── fonts/                      Bundled fonts (do not delete)
├── lang_note_template/         Purple template (base design)
├── apply_test_template/        Teal template (base design)
├── research_common_template/   Dark teal template (base design)
├── copy_apply_test_template/   Spare teal template
├── notes/                      Your notes go here (created by new_note)
├── originals/                  Original DOCX files (reference)
├── scripts/
│   ├── new_note.py             Create a note from a template
│   ├── build_pdf.py            Build a note into a PDF
│   └── extract_docx.py         Extract images from DOCX files
├── user_guide/                 User guide source
├── USER-GUIDE.pdf              User guide (start here)
├── new_note.bat / .sh          Double-click to create a note
├── build_all.bat / .sh         Double-click to build all notes
├── setup.py                    One-time Python environment setup
└── requirements.txt
```

## User Guide

See **[USER-GUIDE.pdf](USER-GUIDE.pdf)** for detailed instructions including:

- Step-by-step setup for Windows, Mac, and Linux
- How to open and use a terminal (for beginners)
- Editing templates — what to change, what to leave alone
- Using AI to generate worksheet content
- Troubleshooting common errors

## Technical Notes

- **Engine:** LuaLaTeX (required for Noto Color Emoji via HarfBuzz). pdfLaTeX and XeLaTeX will not work.
- **Fonts:** All bundled in `fonts/` with relative paths — no system font installation needed.
- **Cross-platform:** All scripts and font paths work on Windows, Mac, and Linux.
- Templates are never modified directly. Notes are copies created by `new_note.py`, which adjusts font paths automatically.
