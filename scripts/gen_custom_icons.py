#!/usr/bin/env python3
"""Generate the custom Expo file icon and wire it into all four themes.

- expo: file icon for app.json / eas.json / app.config.{ts,js,mjs,cjs}
  (Expo "A" mark, white). Shared across themes via icons/_custom/.
"""
import os
import json

ROOT = os.path.join(os.path.dirname(__file__), "..")
CUSTOM = os.path.join(ROOT, "icons", "_custom")

HEADER = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">'
WHITE = "#FFFFFF"

# Expo "A" mark (simple-icons, 24x24).
EXPO_D = (
    "M0 20.084c.043.53.23 1.063.718 1.778.58.849 1.576 1.315 2.303.567.49-.505 "
    "5.794-9.776 8.35-13.29a.761.761 0 011.248 0c2.556 3.514 7.86 12.785 8.35 "
    "13.29.727.748 1.723.282 2.303-.567.57-.835.728-1.42.728-2.046 0-.426-8.26-"
    "15.798-9.092-17.078-.8-1.23-1.044-1.498-2.397-1.542h-1.032c-1.353.044-1.597."
    "311-2.398 1.542C8.267 3.991.33 18.758 0 19.77Z"
)

FILE_ICONS_BLOCK = (
    '                "expo": {\n'
    '                    "path": "./icons/_custom/expo.svg"\n'
    '                },\n'
)

FILE_STEMS_BLOCK = (
    '                "app.json": "expo",\n'
    '                "eas.json": "expo",\n'
    '                "app.config.ts": "expo",\n'
    '                "app.config.js": "expo",\n'
    '                "app.config.mjs": "expo",\n'
    '                "app.config.cjs": "expo",\n'
)


def expo_file():
    return (
        f"{HEADER}\n"
        f'<g transform="translate(1.2 1.7) scale(0.575)">\n'
        f'<path d="{EXPO_D}" fill="{WHITE}"/>\n'
        f"</g>\n"
        f"</svg>\n"
    )


def wire_theme(path):
    import re
    t = open(path).read()
    # Drop any previously inserted custom file_icons / file_stems entries.
    t = re.sub(r'                "(agent-doc|claude|expo)": \{\n'
               r'                    "path": "\./icons/_custom/[^"]+"\n'
               r'                \},\n', "", t)
    t = re.sub(r'                "(CLAUDE\.md|AGENTS\.md|app\.json|eas\.json|'
               r'app\.config\.(ts|js|mjs|cjs))": "[^"]+",\n', "", t)
    t = t.replace('            "file_icons": {\n',
                  '            "file_icons": {\n' + FILE_ICONS_BLOCK, 1)
    t = t.replace('            "file_stems": {\n',
                  '            "file_stems": {\n' + FILE_STEMS_BLOCK, 1)
    open(path, "w").write(t)


def main():
    os.makedirs(CUSTOM, exist_ok=True)
    open(os.path.join(CUSTOM, "expo.svg"), "w").write(expo_file())
    print("wrote expo.svg")
    for name in ["base", "light", "soft", "warm"]:
        p = os.path.join(ROOT, "icon_themes", f"{name}-theme.json")
        wire_theme(p)
        json.load(open(p))
        print(f"wired {name}-theme.json")


if __name__ == "__main__":
    main()
