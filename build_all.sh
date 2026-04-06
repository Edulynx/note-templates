#!/usr/bin/env bash
# Double-click or run this to build all note PDFs.

set -e
cd "$(dirname "$0")"

echo "============================================"
echo "  EduLynx - Build All Notes PDFs"
echo "============================================"
echo

if [ ! -d "notes" ] || [ -z "$(ls -A notes 2>/dev/null)" ]; then
    echo "No notes found. Create one first with:"
    echo "  python scripts/new_note.py"
    echo
    read -p "Press Enter to close..."
    exit 0
fi

count=0
for d in notes/*/; do
    if ls "$d"*.tex 1>/dev/null 2>&1; then
        name=$(basename "$d")
        echo "Building $name..."
        cd "$d"
        lualatex -interaction=nonstopmode *.tex > /dev/null 2>&1 && echo "  Done." || echo "  FAILED"
        cd "$(dirname "$0")"
        count=$((count + 1))
    fi
done

if [ "$count" -eq 0 ]; then
    echo "No notes found."
else
    echo
    echo "All done! PDFs are inside notes/<each-note>/"
fi
echo
read -p "Press Enter to close..."
