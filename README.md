# pkg

> Might be AI slop, but it's functional AI slop.

A minimal, relocatable YAML-based package installer for Linux. Useful when you:

- Don't want to deal with your system package manager
- Want portable installs into `~/bin` or any custom location
- Like to define your own simple install recipes

## Features

- Install from `.tar.gz`, `.zip`, direct binaries, or `git` sources
- Recipes defined in simple YAML
- Support for build steps (e.g., `make`)
- Jinja2 templating for dynamic URLs and paths
- Variables with `literal:` or `shell:` values
- Installation metadata stored for `list`/`uninstall`/`upgrade`
- Override install destinations or DB paths via CLI or env

## Usage

```bash
pkg install recipes/helm.yaml
pkg install stern
pkg install https://example.com/mytool.yaml
```

## Recipe Lookup Behavior

If the argument to `pkg install` is not a file or URL, it is treated as a **recipe name** and fetched from a recipe repository.

By default, this is:
```
https://raw.githubusercontent.com/jctanner/pkg/main/recipes/<name>.yaml
```

You can override this with:
- `--recipe-repo` command-line argument
- `PKG_RECIPE_REPO` environment variable

Example:
```bash
PKG_RECIPE_REPO=https://raw.githubusercontent.com/myorg/myrecipes/main pkg install k9s
```

## Commands

```bash
pkg install <recipe>      # install a tool from YAML file, URL, or short name
pkg list                  # list installed tools and versions
pkg uninstall <install_id> # remove a previously installed tool
```

## Example YAML (tarball)

```yaml
name: k9s
version: 0.50.6

variables:
  os: { literal: linux }
  arch: { shell: uname -m | sed 's/x86_64/amd64/' }

url: https://github.com/derailed/k9s/releases/download/v{{ version }}/k9s_{{ os }}_{{ arch }}.tar.gz
archive: tar
extract:
  - k9s
dest: ~/bin/k9s
chmod: "0755"
```

## Example YAML (git + make)

```yaml
name: oc
version: git-main

git: https://github.com/openshift/oc
build:
  - make
artifact: oc
dest: ~/bin/oc
chmod: "0755"
```

---

This project scratches an itch. Portable tools, YAML recipes, no root required.
Feel free to hack it to your liking.
