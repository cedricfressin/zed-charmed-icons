#!/usr/bin/env python3
"""Generate custom Charmed-style icons not present upstream.

File icons (logo badge, full canvas):
- claude:    CLAUDE.md (official Claude mark, coral).
- agent-doc: AGENTS.md (generic AI sparkle, coral).
- expo:      app.json / eas.json / app.config.* (Expo "A", white).

Folder icons (assets/vscode style: brand logo knocked OUT of the folder,
bottom-right — "évidé"):
- folder_claude: .claude  (Claude mark, coral body).
- folder_codex:  .codex   (OpenAI mark, green body).
- folder_expo:   .expo / .eas (Expo "A", indigo body).

Outputs to icons/_custom/ (files) and icons/_named/ (folders), referenced
by all four themes; colors read on light and dark appearances. Logo path
data lives in scripts/logos/*.path.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from svg_path_transform import transform_path

ROOT = os.path.join(os.path.dirname(__file__), "..")
CUSTOM = os.path.join(ROOT, "icons", "_custom")
NAMED = os.path.join(ROOT, "icons", "_named")
LOGOS = os.path.join(os.path.dirname(__file__), "logos")

HEADER = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">'

CORAL = "#D97757"        # Claude brand coral
CORAL_LIGHT = "#F0AB91"
CODEX = "#10A37F"        # OpenAI green
EXPO_INDIGO = "#4F46E5"  # Expo folder body
WHITE = "#FFFFFF"

CLAUDE_D = open(os.path.join(LOGOS, "claude.path")).read().strip()    # viewBox 24x24
OPENAI_D = open(os.path.join(LOGOS, "openai.path")).read().strip()    # viewBox 256x260
# Expo "A" mark (simple-icons, 24x24).
EXPO_D = (
    "M0 20.084c.043.53.23 1.063.718 1.778.58.849 1.576 1.315 2.303.567.49-.505 "
    "5.794-9.776 8.35-13.29a.761.761 0 011.248 0c2.556 3.514 7.86 12.785 8.35 "
    "13.29.727.748 1.723.282 2.303-.567.57-.835.728-1.42.728-2.046 0-.426-8.26-"
    "15.798-9.092-17.078-.8-1.23-1.044-1.498-2.397-1.542h-1.032c-1.353.044-1.597."
    "311-2.398 1.542C8.267 3.991.33 18.758 0 19.77Z"
)

FOLDER_FILLED = (
    "M1 10V5.2C1 4.0799 1 3.51984 1.21799 3.09202C1.40973 2.71569 1.71569 2.40973 "
    "2.09202 2.21799C2.51984 2 3.0799 2 4.2 2H7L9 4H11C12.4001 4 13.1002 4 13.635 "
    "4.27248C14.1054 4.51217 14.4878 4.89462 14.7275 5.36502C15 5.8998 15 6.59987 "
    "15 8V10C15 11.4001 15 12.1002 14.7275 12.635C14.4878 13.1054 14.1054 13.4878 "
    "13.635 13.7275C13.1002 14 12.4001 14 11 14H5C3.59987 14 2.8998 14 2.36502 "
    "13.7275C1.89462 13.4878 1.51217 13.1054 1.27248 12.635C1 12.1002 1 11.4001 1 10Z"
)
# Open folder outline (stroke), from icons/base/_folder_open.svg.
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


def sparkle(cx, cy, r, color):
    t = f"{cx} {cy - r}"
    rgt = f"{cx + r} {cy}"
    bot = f"{cx} {cy + r}"
    lft = f"{cx - r} {cy}"
    c = f"{cx} {cy}"
    d = f"M{t} Q{c} {rgt} Q{c} {bot} Q{c} {lft} Q{c} {t} Z"
    return f'<path d="{d}" fill="{color}"/>'


def file_logo(path_d, transform, color):
    return (
        f"{HEADER}\n"
        f'<g transform="{transform}">\n'
        f'<path d="{path_d}" fill="{color}"/>\n'
        f"</g>\n"
        f"</svg>\n"
    )


def agent_doc():
    return (
        f"{HEADER}\n"
        f"{sparkle(7, 8.6, 5.1, CORAL)}\n"
        f"{sparkle(12.4, 4, 2.2, CORAL_LIGHT)}\n"
        f"</svg>\n"
    )


def _placement(vw, vh, scale, cx, cy):
    return cx - vw * scale / 2, cy - vh * scale / 2


def carved_closed(body_color, glyph_color, logo_d, vw, vh, cx, cy, scale, gap=1.16):
    """Filled folder hollowed by the logo (evenodd), logo redrawn lighter on top.

    Mirrors upstream folder_assets / folder_vscode: the logo silhouette is cut
    out of the body via fill-rule="evenodd" (resvg-safe, unlike <mask>), then a
    slightly smaller copy is painted in a lighter tone, leaving a thin gap.
    """
    tx, ty = _placement(vw, vh, scale * gap, cx, cy)
    cut = transform_path(logo_d, scale * gap, tx, ty)
    dx, dy = _placement(vw, vh, scale, cx, cy)
    return (
        f"{HEADER}\n"
        f'<path fill-rule="evenodd" opacity="0.9" d="{FOLDER_FILLED} {cut}" fill="{body_color}"/>\n'
        f'<g transform="translate({dx:.4f} {dy:.4f}) scale({scale})">'
        f'<path d="{logo_d}" fill="{glyph_color}"/></g>\n'
        f"</svg>\n"
    )


def outline_open(body_color, glyph_color, logo_d, vw, vh, cx, cy, scale):
    """Open folder as a wireframe outline + the logo glyph bottom-right."""
    dx, dy = _placement(vw, vh, scale, cx, cy)
    return (
        f"{HEADER}\n"
        f'<path d="{FOLDER_OPEN}" stroke="{body_color}" stroke-width="1.5"/>\n'
        f'<g transform="translate({dx:.4f} {dy:.4f}) scale({scale})">'
        f'<path d="{logo_d}" fill="{glyph_color}"/></g>\n'
        f"</svg>\n"
    )


def write(dirpath, name, content):
    open(os.path.join(dirpath, name), "w").write(content)


def main():
    os.makedirs(CUSTOM, exist_ok=True)
    os.makedirs(NAMED, exist_ok=True)

    # File icons
    write(CUSTOM, "claude.svg",
          file_logo(CLAUDE_D, "translate(1 1) scale(0.583)", CORAL))
    write(CUSTOM, "agent-doc.svg", agent_doc())
    write(CUSTOM, "expo.svg",
          file_logo(EXPO_D, "translate(1.2 1.7) scale(0.575)", WHITE))

    # Folder icons: closed = body hollowed by logo + lighter logo on top;
    # open = wireframe outline + logo. (vw, vh, cx, cy, scale)
    folders = {
        "folder_claude": (CORAL, "#F7D7CB", CLAUDE_D, 24, 24, 10.7, 10.4, 0.34),
        "folder_codex": (CODEX, "#7FE0C8", OPENAI_D, 256, 260, 10.7, 10.4, 0.0326),
        "folder_expo": (EXPO_INDIGO, WHITE, EXPO_D, 24, 24, 10.7, 10.6, 0.34),
    }
    for base, (body, glyph, d, vw, vh, cx, cy, sc) in folders.items():
        write(NAMED, f"{base}.svg",
              carved_closed(body, glyph, d, vw, vh, cx, cy, sc))
        write(NAMED, f"{base}_open.svg",
              outline_open(body, glyph, d, vw, vh, cx, cy, sc))

    print("wrote claude/agent-doc/expo files + folder_claude/codex/expo")

    # Wire themes
    import json
    for name in ["base", "light", "soft", "warm"]:
        p = os.path.join(ROOT, "icon_themes", f"{name}-theme.json")
        wire_theme(p)
        json.load(open(p))
        print(f"wired {name}-theme.json")


FILE_ICONS_BLOCK = (
    '                "agent-doc": {\n'
    '                    "path": "./icons/_custom/agent-doc.svg"\n'
    '                },\n'
    '                "claude": {\n'
    '                    "path": "./icons/_custom/claude.svg"\n'
    '                },\n'
    '                "expo": {\n'
    '                    "path": "./icons/_custom/expo.svg"\n'
    '                },\n'
)

FILE_STEMS_BLOCK = (
    '                "CLAUDE.md": "claude",\n'
    '                "AGENTS.md": "agent-doc",\n'
    '                "app.json": "expo",\n'
    '                "eas.json": "expo",\n'
    '                "app.config.ts": "expo",\n'
    '                "app.config.js": "expo",\n'
    '                "app.config.mjs": "expo",\n'
    '                "app.config.cjs": "expo",\n'
)


def wire_theme(path):
    t = open(path).read()
    # Remove any previously inserted custom file_icons entries (re-runnable).
    import re
    t = re.sub(r'                "(agent-doc|claude|expo)": \{\n'
               r'                    "path": "\./icons/_custom/[^"]+"\n'
               r'                \},\n', "", t)
    # Remove previously inserted custom file_stems.
    t = re.sub(r'                "(CLAUDE\.md|AGENTS\.md|app\.json|eas\.json|'
               r'app\.config\.(ts|js|mjs|cjs))": "[^"]+",\n', "", t)
    # Insert fresh blocks.
    t = t.replace('            "file_icons": {\n',
                  '            "file_icons": {\n' + FILE_ICONS_BLOCK, 1)
    t = t.replace('            "file_stems": {\n',
                  '            "file_stems": {\n' + FILE_STEMS_BLOCK, 1)
    open(path, "w").write(t)


if __name__ == "__main__":
    main()
