#!/usr/bin/env python3
"""Check for latest golang version."""
import urllib.request
import sys

try:
    with urllib.request.urlopen("https://go.dev/VERSION?m=text") as response:
        version_text = response.read().decode('utf-8')
        # First line is like "go1.25.5"
        version = version_text.split('\n')[0].strip()
        # Strip "go" prefix
        if version.startswith('go'):
            version = version[2:]
        print(version)
        sys.exit(0)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
