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


def knockout_folder(body_color, logo_d, transform):
    """Filled folder with the logo punched out bottom-right (transparent)."""
    return (
        f"{HEADER}\n"
        f'<mask id="ko" maskUnits="userSpaceOnUse" x="0" y="0" width="16" height="16">\n'
        f'<path d="{FOLDER_FILLED}" fill="white"/>\n'
        f'<g transform="{transform}"><path d="{logo_d}" fill="black"/></g>\n'
        f"</mask>\n"
        f'<path opacity="0.9" d="{FOLDER_FILLED}" fill="{body_color}" mask="url(#ko)"/>\n'
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

    # Folder icons (knockout, bottom-right)
    folders = {
        "folder_claude": (CORAL, CLAUDE_D, "translate(6.2 6) scale(0.333)"),
        "folder_codex": (CODEX, OPENAI_D, "translate(5.9 5.65) scale(0.0336)"),
        "folder_expo": (EXPO_INDIGO, EXPO_D, "translate(6.2 6.3) scale(0.333)"),
    }
    for base, (color, d, tf) in folders.items():
        svg = knockout_folder(color, d, tf)
        write(NAMED, f"{base}.svg", svg)
        write(NAMED, f"{base}_open.svg", svg)  # reuse silhouette for expanded

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
