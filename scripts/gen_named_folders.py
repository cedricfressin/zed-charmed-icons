#!/usr/bin/env python3
"""Wire named directory icons into all four Charmed icon themes.

Maps real-world directory names (and common aliases) to the upstream
`folder_*` icons from littensy/charmed-icons (already vendored under
icons/_named/), then writes the `named_directory_icons` block into each
theme JSON in place.
"""
import os
import re
import json

ROOT = os.path.join(os.path.dirname(__file__), "..")
ICONS = os.path.join(ROOT, "icons", "_named")
THEMES = ["base", "light", "soft", "warm"]

# Available upstream icon base names (folder_<base>.svg).
BASES = [
    "admin", "animation", "assets", "audio", "auth", "benchmark", "bin",
    "builder", "camera", "changesets", "client", "commands", "component",
    "config", "connection", "constant", "content", "context", "coverage",
    "database", "dist", "docs", "effects", "error", "event", "fonts",
    "function", "github", "hooks", "image", "input", "javascript", "json",
    "layout", "lib", "luau", "lune", "marketing", "middleware", "model",
    "module", "node", "nuxt", "package", "page", "provider", "roblox",
    "routes", "script", "server", "service", "source", "storybook", "styles",
    "svg", "temp", "template", "test", "types", "typescript", "util", "video",
    "vscode", "web", "yarn",
]

# directory name -> icon base. Direct base names are added automatically;
# this dict holds aliases and real-world directory names.
ALIASES = {
    # source / app
    "src": "source", "sources": "source", "app": "source", "apps": "source",
    "features": "source", "feature": "source",
    # components / ui
    "components": "component", "ui": "component", "widgets": "component",
    # hooks
    "hook": "hooks",
    # api / server / client
    "api": "server", "apis": "server", "backend": "server", "servers": "server",
    "clients": "client", "frontend": "client",
    # routing
    "router": "routes", "pages": "page",
    # assets / media
    "static": "assets", "public": "assets",
    "images": "image", "img": "image", "imgs": "image",
    "icons": "svg", "svgs": "svg",
    "media": "video", "videos": "video", "movies": "video",
    "sounds": "audio", "sound": "audio",
    "font": "fonts",
    # styles
    "style": "styles", "css": "styles", "scss": "styles", "sass": "styles",
    # tests
    "tests": "test", "__tests__": "test", "spec": "test", "specs": "test",
    "e2e": "test", "__mocks__": "test", "mocks": "test",
    # docs
    "doc": "docs", "documentation": "docs",
    # vcs / ci
    ".github": "github", ".gitlab": "github",
    # deps / build output
    "node_modules": "node", ".pnpm": "package", "packages": "package",
    "build": "dist", "out": "dist", "output": "dist", ".output": "dist",
    ".next": "dist", ".turbo": "temp",
    ".nuxt": "nuxt",
    # config
    "configs": "config", ".config": "config", "settings": "config",
    ".vscode": "vscode", ".vs": "vscode",
    # types
    "type": "types", "@types": "types", "typings": "types",
    # data / state
    "store": "database", "stores": "database", "state": "database",
    "redux": "database", "db": "database", "data": "database",
    "convex": "database", "migrations": "database", "migration": "database",
    "prisma": "database", "drizzle": "database", "schema": "database",
    "schemas": "database",
    # domain layers
    "contexts": "context", "providers": "provider",
    "services": "service", "models": "model",
    "constants": "constant", "const": "constant",
    "cmds": "commands", "scripts": "script",
    "libs": "lib", "libraries": "lib", "vendor": "lib",
    "utils": "util", "utilities": "util", "helpers": "util", "helper": "util",
    "middlewares": "middleware", "layouts": "layout",
    "authentication": "auth",
    "errors": "error", "events": "event", "effect": "effects",
    "animations": "animation", "anim": "animation",
    "connections": "connection", "network": "connection",
    "contents": "content", "inputs": "input",
    "functions": "function", "fn": "function",
    "modules": "module", "templates": "template",
    "tmp": "temp", ".temp": "temp", ".tmp": "temp",
    "cache": "temp", ".cache": "temp",
    "benchmarks": "benchmark", "bench": "benchmark",
    ".changeset": "changesets",
    ".storybook": "storybook", "stories": "storybook",
    "www": "web", ".yarn": "yarn",
    "js": "javascript", "ts": "typescript",
}


def build_mapping():
    mapping = {}
    for b in BASES:
        mapping[b] = b
    mapping.update(ALIASES)
    # keep only entries whose icon files exist
    out = {}
    for name, base in sorted(mapping.items()):
        coll = os.path.join(ICONS, f"folder_{base}.svg")
        opened = os.path.join(ICONS, f"folder_{base}_open.svg")
        if os.path.exists(coll) and os.path.exists(opened):
            out[name] = base
        else:
            print(f"  skip {name!r}: missing icon for base {base!r}")
    return out


def block_str(mapping):
    lines = ['            "named_directory_icons": {']
    items = list(mapping.items())
    for i, (name, base) in enumerate(items):
        comma = "," if i < len(items) - 1 else ""
        lines.append(f'                {json.dumps(name)}: {{')
        lines.append(f'                    "collapsed": "./icons/_named/folder_{base}.svg",')
        lines.append(f'                    "expanded": "./icons/_named/folder_{base}_open.svg"')
        lines.append(f'                }}{comma}')
    lines.append("            },")
    return "\n".join(lines) + "\n"


def patch_theme(path, block):
    t = open(path).read()
    t = t.replace("icon_themes/v0.2.0.json", "icon_themes/v0.3.0.json")
    pat = re.compile(
        r'            "named_directory_icons": \{.*?\n            \},\n',
        re.DOTALL,
    )
    if pat.search(t):
        t = pat.sub(block, t, count=1)
    else:
        anchor = '            "file_stems": {'
        assert anchor in t, f"no anchor in {path}"
        t = t.replace(anchor, block + anchor, 1)
    open(path, "w").write(t)


def main():
    mapping = build_mapping()
    block = block_str(mapping)
    for name in THEMES:
        p = os.path.join(ROOT, "icon_themes", f"{name}-theme.json")
        patch_theme(p, block)
        json.load(open(p))  # validate
        print(f"patched {name}-theme.json ({len(mapping)} dirs)")


if __name__ == "__main__":
    main()
