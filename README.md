# gdal-mcp (Moved)

This project has moved to [Wayfinder-Foundry/gdal-mcp](https://github.com/Wayfinder-Foundry/gdal-mcp).

Please update any local clones, submodules, automations, or references to point to the new location.

## Updating Your Local Repository

If you have a local clone of this repository, update your remote URL to point to the new location:

```bash
git remote set-url origin https://github.com/Wayfinder-Foundry/gdal-mcp.git
```

Verify the change:

```bash
git remote -v
```

## Updating Submodules

If you're using this repository as a submodule, update the `.gitmodules` file in your parent repository to reference the new URL:

```ini
[submodule "gdal-mcp"]
    path = path/to/gdal-mcp
    url = https://github.com/Wayfinder-Foundry/gdal-mcp.git
```

Then run:

```bash
git submodule sync
git submodule update --init --recursive
```
