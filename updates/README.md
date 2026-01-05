# Update Check Scripts

This directory contains scripts to check for the latest version of packages.

## How it works

When `pkg check-updates` runs:

1. For each installed package, it looks for `updates/<name>.sh`, `updates/<name>.py`, or `updates/<name>` (any executable)
2. If found, runs the script and expects the latest version number on stdout
3. If not found, falls back to auto-detection (GitHub API for GitHub-hosted packages)
4. Compares latest version with installed version

## Script requirements

- Must be executable (`chmod +x`)
- Must output **only** the version number to stdout (e.g., `1.25.5`)
- Should return exit code 0 on success, non-zero on failure
- Can be any language: bash, python, etc.

## Examples

### Bash script (crc.sh)
```bash
#!/bin/bash
curl -s https://api.github.com/repos/crc-org/crc/tags | jq -r '.[0].name' | sed 's/^v//'
```

### Python script (golang.py)
```python
#!/usr/bin/env python3
import urllib.request
with urllib.request.urlopen("https://go.dev/VERSION?m=text") as response:
    version = response.read().decode('utf-8').split('\n')[0].strip()
    print(version[2:] if version.startswith('go') else version)
```

## When to create update scripts

- Package not hosted on GitHub (e.g., golang from go.dev)
- GitHub URL doesn't follow standard patterns
- Need custom logic to determine latest version
- Auto-detection doesn't work or returns wrong version

## Testing

Test your script directly:
```bash
./updates/golang.py
# Output: 1.25.5

./updates/crc.sh
# Output: 2.57.0
```

Then run check-updates:
```bash
./pkg check-updates
# Shows SOURCE column indicating which method was used
```
