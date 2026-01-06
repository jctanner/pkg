#!/bin/bash
# Check for latest kubectl version from Kubernetes stable release

# Build curl command with authentication if GITHUB_TOKEN is set
# Note: dl.k8s.io doesn't require GitHub token, but we keep the pattern consistent
CURL_CMD="curl -L -s"

version=$(eval $CURL_CMD https://dl.k8s.io/release/stable.txt)
if [ -z "$version" ]; then
    exit 1
fi

# Strip the 'v' prefix
echo "$version" | sed 's/^v//'
