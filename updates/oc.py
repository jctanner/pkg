#!/usr/bin/env python3
"""Check for latest oc (OpenShift CLI) version from GitHub tags."""
import urllib.request
import json
import re
import sys
import os

try:
    # Fetch all tags from GitHub
    url = "https://api.github.com/repos/openshift/oc/tags?per_page=100"

    # Build request with authentication if GITHUB_TOKEN is set
    req = urllib.request.Request(url)
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        req.add_header("Authorization", f"token {github_token}")

    with urllib.request.urlopen(req) as response:
        tags = json.loads(response.read().decode('utf-8'))

    # Filter for openshift-clients-* tags and sort by version
    tag_data = []
    pattern = re.compile(r'^openshift-clients-(\d+)\.(\d+)\.(\d+)-(\d+)$')

    for tag in tags:
        tag_name = tag.get('name', '')
        match = pattern.match(tag_name)
        if match:
            # Extract version components for sorting
            major = int(match.group(1))
            minor = int(match.group(2))
            patch = int(match.group(3))
            timestamp = int(match.group(4))
            tag_data.append((major, minor, patch, timestamp, tag_name))

    if not tag_data:
        print("No valid versions found", file=sys.stderr)
        sys.exit(1)

    # Sort by version (major, minor, patch, timestamp) in descending order
    tag_data.sort(reverse=True)

    # Return the full tag name of the latest version
    latest_tag = tag_data[0][4]
    print(latest_tag)
    sys.exit(0)

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
