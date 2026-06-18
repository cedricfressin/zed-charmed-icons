#!/usr/bin/env python3
"""Generate named directory icons (colored folder + glyph) for Charmed Icons.

Outputs collapsed (filled) and open (outlined) folder SVGs into icons/_named/.
Named folder icons share one accent-colored design across all four icon sets,
matching the convention used by Material / vscode-icons themes.
"""
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "icons", "_named")

# Filled folder body (collapsed) — from icons/base/_folder.svg.
FOLDER_FILLED = (
    "M1 10V5.2C1 4.0799 1 3.51984 1.21799 3.09202C1.40973 2.71569 1.71569 2.40973 "
    "2.09202 2.21799C2.51984 2 3.0799 2 4.2 2H7L9 4H11C12.4001 4 13.1002 4 13.635 "
    "4.27248C14.1054 4.51217 14.4878 4.89462 14.7275 5.36502C15 5.8998 15 6.59987 "
    "15 8V10C15 11.4001 15 12.1002 14.7275 12.635C14.4878 13.1054 14.1054 13.4878 "
    "13.635 13.7275C13.1002 14 12.4001 14 11 14H5C3.59987 14 2.8998 14 2.36502 "
    "13.7275C1.89462 13.4878 1.51217 13.1054 1.27248 12.635C1 12.1002 1 11.4001 1 10Z"
)
# Open folder outline — from icons/base/_folder_open.svg.
FOLDER_OPEN = (
    "M4.2002 2.75H6.68945L8.68945 4.75H11C11.7124 4.75 12.2018 4.75026 12.5811 "
    "4.78125C12.8593 4.80399 13.0407 4.84156 13.1748 4.88965L13.2949 4.94043C13.583 "
    "5.08727 13.8241 5.31082 13.9922 5.58496L14.0596 5.70508C14.133 5.8491 14.1885 "
    "6.04851 14.2188 6.41895C14.2497 6.7982 14.25 7.28756 14.25 8V10C14.25 10.7124 "
    "14.2497 11.2018 14.2188 11.5811C14.196 11.8593 14.1584 12.0407 14.1104 "
    "12.1748L14.0596 12.2949C13.9127 12.583 13.6892 12.8241 13.415 12.9922L13.2949 "
    "13.0596C13.1509 13.133 12.9515 13.1885 12.5811 13.2188C12.2018 13.2497 11.7124 "
    "13.25 11 13.25H5C4.28756 13.25 3.7982 13.2497 3.41895 13.2188C3.14073 13.196 "
    "2.95934 13.1584 2.8252 13.1104L2.70508 13.0596C2.41699 12.9127 2.17592 12.6892 "
    "2.00781 12.415L1.94043 12.2949C1.86705 12.1509 1.81152 11.9515 1.78125 "
    "11.5811C1.75026 11.2018 1.75 10.7124 1.75 10V5.2002C1.75 4.62777 1.75024 "
    "4.24314 1.77441 3.94727C1.79201 3.73202 1.8202 3.60099 1.85254 3.51074L1.88672 "
    "3.43262C1.99161 3.22681 2.15084 3.05465 2.34668 2.93457L2.43262 2.88672C2.52316 "
    "2.84059 2.66027 2.79788 2.94727 2.77441C3.24314 2.75024 3.62777 2.75 4.2002 2.75Z"
)

# White glyphs, drawn on the folder front (roughly x 4.5..11.5, y 7.5..12.5).
G = "#FFFFFF"
GLYPHS = {
    # </>  code
    "code": (
        f'<path d="M6.6 8.4 4.8 10l1.8 1.6" stroke="{G}" stroke-width="1" '
        'stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
        f'<path d="M9.4 8.4 11.2 10l-1.8 1.6" stroke="{G}" stroke-width="1" '
        'stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
    ),
    # { }  braces
    "braces": (
        f'<path d="M7 8.2c-0.8 0-1 0.4-1 1v0.4c0 0.3-0.2 0.4-0.5 0.4 0.3 0 0.5 0.1 0.5 0.4v0.4c0 0.6 0.2 1 1 1" '
        f'stroke="{G}" stroke-width="0.9" fill="none" stroke-linecap="round"/>'
        f'<path d="M9 8.2c0.8 0 1 0.4 1 1v0.4c0 0.3 0.2 0.4 0.5 0.4-0.3 0-0.5 0.1-0.5 0.4v0.4c0 0.6-0.2 1-1 1" '
        f'stroke="{G}" stroke-width="0.9" fill="none" stroke-linecap="round"/>'
    ),
    # mountains  image
    "image": (
        f'<path d="M5 11.5 7 9l1.4 1.6L9.6 9l1.6 2.5Z" fill="{G}"/>'
        f'<circle cx="6.2" cy="8.2" r="0.7" fill="{G}"/>'
    ),
    # check
    "check": (
        f'<path d="M5.2 10.1 7 11.8l3.6-3.6" stroke="{G}" stroke-width="1.1" '
        'fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # document lines
    "doc": (
        f'<path d="M5.4 8.4h5.2M5.4 10h5.2M5.4 11.6h3.4" stroke="{G}" '
        'stroke-width="0.9" stroke-linecap="round"/>'
    ),
    # branch
    "branch": (
        f'<circle cx="6" cy="8.4" r="0.9" fill="{G}"/>'
        f'<circle cx="6" cy="11.6" r="0.9" fill="{G}"/>'
        f'<circle cx="10" cy="8.4" r="0.9" fill="{G}"/>'
        f'<path d="M6 9.3v1.4M6 10c0-1.6 4-0.4 4-1.6" stroke="{G}" '
        'stroke-width="0.9" fill="none"/>'
    ),
    # hexagon  node
    "hex": (
        f'<path d="M8 7.6 10.6 9.1v2.8L8 13.4 5.4 11.9V9.1Z" stroke="{G}" '
        'stroke-width="0.9" fill="none" stroke-linejoin="round"/>'
    ),
    # cube  build/dist
    "cube": (
        f'<path d="M8 7.8 10.8 9.4 8 11 5.2 9.4Z" fill="{G}"/>'
        f'<path d="M5.2 9.4v2.2L8 13.2v-2.2ZM10.8 9.4v2.2L8 13.2v-2.2Z" '
        f'fill="{G}" opacity="0.6"/>'
    ),
    # hash  styles
    "hash": (
        f'<path d="M6.6 8.2 6 12M9 8.2 8.4 12M5 9.6h4.6M4.8 10.8h4.6" '
        f'stroke="{G}" stroke-width="0.9" stroke-linecap="round"/>'
    ),
    # gear  config
    "gear": (
        f'<circle cx="8" cy="10" r="1.2" stroke="{G}" stroke-width="0.9" fill="none"/>'
        f'<path d="M8 7.6v0.8M8 11.6v0.8M5.6 10h0.8M9.6 10h0.8M6.3 8.3l0.6 0.6'
        f'M9.1 11.1l0.6 0.6M9.7 8.3l-0.6 0.6M6.3 11.7l0.6-0.6" stroke="{G}" '
        'stroke-width="0.8" stroke-linecap="round"/>'
    ),
    # overlapping squares  components
    "component": (
        f'<rect x="5.2" y="7.8" width="3.4" height="3.4" rx="0.5" stroke="{G}" '
        'stroke-width="0.9" fill="none"/>'
        f'<rect x="7.6" y="9.4" width="3.2" height="3.2" rx="0.5" fill="{G}"/>'
    ),
    # hook
    "hook": (
        f'<path d="M9.2 8v2c0 1.2-0.9 2-2 2s-2-0.8-2-1.8" stroke="{G}" '
        'stroke-width="1" fill="none" stroke-linecap="round"/>'
        f'<circle cx="9.2" cy="7.8" r="0.7" fill="{G}"/>'
    ),
    # database cylinder  store/state
    "db": (
        f'<ellipse cx="8" cy="8.4" rx="2.6" ry="0.9" stroke="{G}" stroke-width="0.9" fill="none"/>'
        f'<path d="M5.4 8.4v3c0 0.5 1.2 0.9 2.6 0.9s2.6-0.4 2.6-0.9v-3" '
        f'stroke="{G}" stroke-width="0.9" fill="none"/>'
    ),
}

# name -> (glyph, accent color)
FOLDERS = {
    "src": ("code", "#61AFEF"),
    "source": ("code", "#61AFEF"),
    "app": ("code", "#61AFEF"),
    "types": ("code", "#61AFEF"),
    "api": ("braces", "#98C379"),
    "server": ("braces", "#98C379"),
    "routes": ("braces", "#98C379"),
    "assets": ("image", "#E06C75"),
    "public": ("image", "#E06C75"),
    "images": ("image", "#E06C75"),
    "img": ("image", "#E06C75"),
    "media": ("image", "#E06C75"),
    "test": ("check", "#98C379"),
    "tests": ("check", "#98C379"),
    "__tests__": ("check", "#98C379"),
    "spec": ("check", "#98C379"),
    "docs": ("doc", "#ABB2BF"),
    "doc": ("doc", "#ABB2BF"),
    ".github": ("branch", "#ABB2BF"),
    ".git": ("branch", "#E06C75"),
    "node_modules": ("hex", "#98C379"),
    "dist": ("cube", "#D19A66"),
    "build": ("cube", "#D19A66"),
    "out": ("cube", "#D19A66"),
    ".next": ("cube", "#D19A66"),
    "styles": ("hash", "#C678DD"),
    "css": ("hash", "#C678DD"),
    "scss": ("hash", "#C678DD"),
    "config": ("gear", "#D19A66"),
    ".config": ("gear", "#D19A66"),
    ".vscode": ("gear", "#61AFEF"),
    "components": ("component", "#56B6C2"),
    "ui": ("component", "#56B6C2"),
    "hooks": ("hook", "#C678DD"),
    "store": ("db", "#C678DD"),
    "state": ("db", "#C678DD"),
    "lib": ("hex", "#E5C07B"),
    "utils": ("gear", "#E5C07B"),
}

HEADER = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">'


def filled_svg(color, glyph):
    return (
        f'{HEADER}\n'
        f'<path d="{FOLDER_FILLED}" fill="{color}"/>\n'
        f'{glyph}\n'
        f'</svg>\n'
    )


def open_svg(color, glyph):
    return (
        f'{HEADER}\n'
        f'<path d="{FOLDER_OPEN}" stroke="{color}" stroke-width="1.5"/>\n'
        f'{glyph}\n'
        f'</svg>\n'
    )


def safe(name):
    return name.lstrip(".") if name.startswith(".") else name


def main():
    os.makedirs(OUT, exist_ok=True)
    count = 0
    for name, (glyph_key, color) in FOLDERS.items():
        glyph = GLYPHS[glyph_key]
        base = "folder-" + safe(name)
        with open(os.path.join(OUT, base + ".svg"), "w") as f:
            f.write(filled_svg(color, glyph))
        with open(os.path.join(OUT, base + "-open.svg"), "w") as f:
            f.write(open_svg(color, glyph))
        count += 2
    print(f"wrote {count} svgs for {len(FOLDERS)} folders into {OUT}")


if __name__ == "__main__":
    main()
