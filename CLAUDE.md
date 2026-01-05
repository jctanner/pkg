# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`pkg` is a minimal, relocatable YAML-based package installer for Linux. It enables installing tools from tarballs, zip files, direct binaries, or git sources into custom locations (typically `~/bin`) without requiring root access or system package managers.

## Architecture

### Single-File Design
The entire tool is implemented in a single Python script (`pkg`) with no external configuration files. All functionality is self-contained:
- Recipe parsing and templating (Jinja2)
- Archive extraction (tar, zip)
- Git cloning and building
- Installation metadata management
- Version tracking

### Recipe System
Recipes are YAML files that define how to install a tool. The system supports:
- **URL-based installs**: Download from a URL, optionally extract from archive
- **Git-based installs**: Clone a repo, run build steps, extract artifact
- **Variable substitution**: Use Jinja2 templating with variables defined via `literal:` or `shell:` evaluation
- **Remote recipe lookup**: If argument isn't a file/URL, fetch from recipe repository (default: `https://raw.githubusercontent.com/jctanner/pkg/main/recipes/<name>.yaml`)

### Installation Database
Metadata is stored in `~/.local/share/pkg/` (or `$PKG_DB`) as individual YAML files:
- Filename format: `PKG_<install_id>.yaml` where install_id is a 12-char SHA256 hash
- Each file contains two YAML documents:
  1. Original recipe spec
  2. Rendered metadata (name, version, install path, timestamp, resolved variables)

### Key Functions
- `resolve_yaml_source()`: Handles local files, URLs, and recipe name lookups
- `collect_variables()`: Evaluates variables from recipe (shell commands or literals)
- `evaluate_template()`: Renders Jinja2 templates with variable context
- `install_tool()`: Main installation flow (download/clone → extract/build → copy → chmod → save metadata)
- `extract_archive()`: Extracts specific files from tar/zip by basename matching
- `list_installed()`: Reads metadata files and displays installed tools
- `uninstall_tool()`: Removes binary and metadata by install ID

## Common Commands

### Basic Usage
```bash
# Install from local recipe
./pkg install recipes/helm.yaml

# Install from recipe name (fetches from remote repo)
./pkg install k9s

# Install from URL
./pkg install https://example.com/mytool.yaml

# List installed tools
./pkg list

# Uninstall by ID (from list output)
./pkg uninstall <install_id>
```

### Overrides
```bash
# Override install destination
./pkg install --dest-dir /custom/path k9s

# Override install database location
./pkg install --install-db ~/.pkg-db k9s

# Override recipe repository
./pkg install --recipe-repo https://raw.githubusercontent.com/myorg/myrecipes/main k9s
PKG_RECIPE_REPO=https://example.com/recipes pkg install k9s
```

### Development Dependencies
```bash
pip install packaging jinja2 pyyaml
```

## Recipe Format

### Tarball Example
```yaml
name: tool-name
version: 1.2.3
variables:
  os: { literal: linux }
  arch: { shell: uname -m | sed 's/x86_64/amd64/' }
url: https://example.com/{{ version }}/tool_{{ os }}_{{ arch }}.tar.gz
archive: tar
extract:
  - tool-binary
dest: ~/bin/tool
chmod: "0755"
```

### Git + Build Example
```yaml
name: tool-name
version: git-main
git: https://github.com/org/repo
build:
  - make
artifact: binary-name
dest: ~/bin/tool
chmod: "0755"
```

### Recipe Fields
- `name`: Tool name (required)
- `version`: Version string (required)
- `variables`: Dict of variables with `literal:` or `shell:` values
- `url`: Download URL (supports Jinja2 templating)
- `archive`: Archive type (`tar` or `zip`)
- `extract`: List of files to extract from archive (matched by basename)
- `git`: Git repository URL
- `build`: List of shell commands to run in cloned repo
- `artifact`: Path to built binary (relative to repo root)
- `dest`: Final installation path (supports `~` expansion and templating)
- `chmod`: Permissions as octal string (e.g., `"0755"`)

## Important Notes

- The script uses `#!/usr/bin/env python3` and requires Python 3.x
- Archive extraction matches files by basename, so `extract: ["helm"]` will match `linux-amd64/helm`
- The install ID is a hash of `name|version|dest|source_yaml` to ensure uniqueness
- Variables can override the top-level `version` field if defined
- GitHub repo URLs are automatically converted to raw.githubusercontent.com URLs for recipe lookup
