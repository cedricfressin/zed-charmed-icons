#!/usr/bin/env python3
"""Generate custom Charmed-style icons not present upstream.

- agent-doc: shared file icon for CLAUDE.md / AGENTS.md (AI sparkle).
- expo: shared file icon for app.json / eas.json / app.config.* (Expo mark).
- folder_agent: shared folder icon for .claude / .codex (sparkle on folder).

Output goes to icons/_custom/ (files) and icons/_named/ (folders), both
referenced by all four themes regardless of appearance, so colors are
chosen to read on light and dark backgrounds.
"""
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
CUSTOM = os.path.join(ROOT, "icons", "_custom")
NAMED = os.path.join(ROOT, "icons", "_named")

HEADER = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">'

CORAL = "#D97757"       # Claude brand coral — readable on light + dark
CORAL_LIGHT = "#F0AB91"
EXPO = "#4F46E5"        # indigo, visible on both appearances
EXPO_LIGHT = "#A5B4FC"

# Folder body shapes (from icons/base) reused for the folder variant.
FOLDER_FILLED = (
    "M1 10V5.2C1 4.0799 1 3.51984 1.21799 3.09202C1.40973 2.71569 1.71569 2.40973 "
    "2.09202 2.21799C2.51984 2 3.0799 2 4.2 2H7L9 4H11C12.4001 4 13.1002 4 13.635 "
    "4.27248C14.1054 4.51217 14.4878 4.89462 14.7275 5.36502C15 5.8998 15 6.59987 "
    "15 8V10C15 11.4001 15 12.1002 14.7275 12.635C14.4878 13.1054 14.1054 13.4878 "
    "13.635 13.7275C13.1002 14 12.4001 14 11 14H5C3.59987 14 2.8998 14 2.36502 "
    "13.7275C1.89462 13.4878 1.51217 13.1054 1.27248 12.635C1 12.1002 1 11.4001 1 10Z"
)
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

# Expo "A" mark from simple-icons (24x24 viewBox), scaled into 16x16.
EXPO_PATH_24 = (
    "M0 20.084c.043.53.23 1.063.718 1.778.58.849 1.576 1.315 2.303.567.49-.505 "
    "5.794-9.776 8.35-13.29a.761.761 0 011.248 0c2.556 3.514 7.86 12.785 8.35 "
    "13.29.727.748 1.723.282 2.303-.567.57-.835.728-1.42.728-2.046 0-.426-8.26-"
    "15.798-9.092-17.078-.8-1.23-1.044-1.498-2.397-1.542h-1.032c-1.353.044-1.597."
    "311-2.398 1.542C8.267 3.991.33 18.758 0 19.77Z"
)


def sparkle(cx, cy, r, color):
    """4-point concave star centered at (cx, cy)."""
    t = f"{cx} {cy - r}"
    rgt = f"{cx + r} {cy}"
    bot = f"{cx} {cy + r}"
    lft = f"{cx - r} {cy}"
    c = f"{cx} {cy}"
    d = f"M{t} Q{c} {rgt} Q{c} {bot} Q{c} {lft} Q{c} {t} Z"
    return f'<path d="{d}" fill="{color}"/>'


def agent_doc():
    # large coral sparkle + small light sparkle, logo-style
    return (
        f"{HEADER}\n"
        f"{sparkle(7, 8.6, 5.1, CORAL)}\n"
        f"{sparkle(12.4, 4, 2.2, CORAL_LIGHT)}\n"
        f"</svg>\n"
    )


def expo_file():
    return (
        f"{HEADER}\n"
        f'<g transform="translate(1.2 1.7) scale(0.575)">\n'
        f'<path d="{EXPO_PATH_24}" fill="{EXPO}"/>\n'
        f"</g>\n"
        f"</svg>\n"
    )


def folder_agent_collapsed():
    return (
        f"{HEADER}\n"
        f'<path opacity="0.85" d="{FOLDER_FILLED}" fill="{CORAL}"/>\n'
        f"{sparkle(8, 9.6, 3.0, CORAL_LIGHT)}\n"
        f"</svg>\n"
    )


def folder_agent_open():
    return (
        f"{HEADER}\n"
        f'<path d="{FOLDER_OPEN}" stroke="{CORAL}" stroke-width="1.5"/>\n'
        f"{sparkle(8, 9.6, 3.0, CORAL)}\n"
        f"</svg>\n"
    )


THEMES = ["base", "light", "soft", "warm"]

FILE_ICONS_BLOCK = (
    '                "agent-doc": {\n'
    '                    "path": "./icons/_custom/agent-doc.svg"\n'
    '                },\n'
    '                "expo": {\n'
    '                    "path": "./icons/_custom/expo.svg"\n'
    '                },\n'
)

FILE_STEMS_BLOCK = (
    '                "CLAUDE.md": "agent-doc",\n'
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
    if '"agent-doc"' not in t:
        t = t.replace('            "file_icons": {\n',
                       '            "file_icons": {\n' + FILE_ICONS_BLOCK, 1)
        t = t.replace('            "file_stems": {\n',
                       '            "file_stems": {\n' + FILE_STEMS_BLOCK, 1)
        open(path, "w").write(t)


def main():
    os.makedirs(CUSTOM, exist_ok=True)
    os.makedirs(NAMED, exist_ok=True)
    open(os.path.join(CUSTOM, "agent-doc.svg"), "w").write(agent_doc())
    open(os.path.join(CUSTOM, "expo.svg"), "w").write(expo_file())
    open(os.path.join(NAMED, "folder_agent.svg"), "w").write(folder_agent_collapsed())
    open(os.path.join(NAMED, "folder_agent_open.svg"), "w").write(folder_agent_open())
    print("wrote agent-doc.svg, expo.svg, folder_agent.svg, folder_agent_open.svg")
    import json
    for name in THEMES:
        p = os.path.join(ROOT, "icon_themes", f"{name}-theme.json")
        wire_theme(p)
        json.load(open(p))  # validate
        print(f"wired {name}-theme.json")


if __name__ == "__main__":
    main()
