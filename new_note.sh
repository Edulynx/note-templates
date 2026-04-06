#!/usr/bin/env bash
cd "$(dirname "$0")"
python3 scripts/new_note.py
read -p "Press Enter to close..."
