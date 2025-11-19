#!/usr/bin/env python3
"""Validate TaggerScript syntax using Picard's internal parser"""

import sys
from picard.script import ScriptParser

if len(sys.argv) < 2:
    print("Usage: validate_tagger.py <script.pts>")
    sys.exit(1)

path = sys.argv[1]

try:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    parser = ScriptParser()
    parser.parse(text)

    print("✅ TaggerScript syntax is valid.")
    sys.exit(0)

except FileNotFoundError:
    print(f"❌ ERROR: File '{path}' not found")
    sys.exit(1)

except Exception as e:
    print("❌ TaggerScript syntax error:")
    print(str(e))
    sys.exit(1)
