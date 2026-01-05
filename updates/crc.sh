#!/bin/bash
# Check for latest crc version from GitHub tags

# Build curl command with authentication if GITHUB_TOKEN is set
CURL_CMD="curl -s"
if [ -n "$GITHUB_TOKEN" ]; then
    CURL_CMD="curl -s -H \"Authorization: token $GITHUB_TOKEN\""
fi

tag=$(eval $CURL_CMD https://api.github.com/repos/crc-org/crc/tags | jq -r '.[0].name')
if [ "$tag" = "null" ] || [ -z "$tag" ]; then
    exit 1
fi
echo "$tag" | sed 's/^v//'
