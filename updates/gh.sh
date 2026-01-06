#!/bin/bash
# Check for latest gh (GitHub CLI) version from GitHub releases

# Build curl command with authentication if GITHUB_TOKEN is set
CURL_CMD="curl -s"
if [ -n "$GITHUB_TOKEN" ]; then
    CURL_CMD="curl -s -H \"Authorization: token $GITHUB_TOKEN\""
fi

tag=$(eval $CURL_CMD https://api.github.com/repos/cli/cli/releases/latest | jq -r '.tag_name')
if [ "$tag" = "null" ] || [ -z "$tag" ]; then
    exit 1
fi

# Strip the 'v' prefix
echo "$tag" | sed 's/^v//'
