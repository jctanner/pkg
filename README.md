# pkg

**`pkg`** is a dumb, functional, YAML-based local package manager for installing CLI tools outside the system package manager.  
It’s probably AI slop. But it’s *useful* AI slop — and it scratches an itch in my workflow.

## Why?

- I want relocatable installs in `~/bin`, `/tmp/something/bin`, or anywhere else.
- I don’t want to wrestle with `dnf`, `apt`, or `brew` when I just want `kubectl`.
- I want minimal, declarative recipes I can version in a Git repo.
- I want it to be easy to rip out a tool without touching my system.

## What it does

- Installs a binary from a URL or builds from a git repo + make.
- Extracts from `.tar.gz` or `.zip` archives.
- Uses YAML files with support for:
  - Jinja2 templating (`{{ version }}`, `{{ arch }}`, etc.)
  - Shell-based variable resolution
- Tracks install metadata in `~/.local/share/pkg` (or override with `--install-db`)
- Lets you:
  - `pkg install recipes/thing.yaml`
  - `pkg list`
  - `pkg uninstall <install-id>`

## Example YAML

```yaml
name: stern
version: 1.32.0

variables:
  os:
    literal: linux
  arch:
    shell: uname -m | sed 's/x86_64/amd64/'

url: https://github.com/stern/stern/releases/download/v{{ version }}/stern_{{ version }}_{{ os }}_{{ arch }}.tar.gz
archive: tar
extract:
  - "stern"
dest: ~/bin/stern
chmod: "0755"
```
