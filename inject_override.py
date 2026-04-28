#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Injeta o link do CSS de override em todos os HTML do projeto."""

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

# Caminho relativo do CSS de override (calculado a partir de cada arquivo HTML)
OVERRIDE_CSS_ABS = os.path.join(
    ROOT, "wp-content", "uploads", "elementor", "css", "rebranding-override.css"
).replace("\\", "/")

INJECT_TAG = '<link rel="stylesheet" href="{path}" media="all" id="rebranding-override-css">'
MARKER = "rebranding-override-css"

TARGET_HTMLS = [
    "index copy.html",
    "contato/index.html",
    "contato/i.html",
    "quem-somos/index.html",
    "quem-somos/i.html",
    "politica-de-privacidade/index.html",
    "politica-de-privacidade/i.html",
]
# Adiciona todos os index*.html da raiz
import glob
for f in glob.glob(os.path.join(ROOT, "index*.html")):
    rel = os.path.relpath(f, ROOT).replace("\\", "/")
    if rel not in TARGET_HTMLS:
        TARGET_HTMLS.append(rel)


def relative_css_path(html_path: str) -> str:
    html_dir = os.path.dirname(html_path)
    rel = os.path.relpath(OVERRIDE_CSS_ABS, html_dir).replace("\\", "/")
    return rel


modified = 0
for rel in TARGET_HTMLS:
    filepath = os.path.join(ROOT, rel.replace("/", os.sep))
    if not os.path.exists(filepath):
        continue

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    if MARKER in content:
        print(f"  [SKIP] {rel} (ja tem override)")
        continue

    css_rel = relative_css_path(filepath)
    tag = INJECT_TAG.format(path=css_rel)

    # Injeta antes de </head>
    if "</head>" in content:
        content = content.replace("</head>", f"  {tag}\n</head>", 1)
    else:
        # Fallback: logo apos <head>
        content = re.sub(r'(<head[^>]*>)', r'\1\n  ' + tag, content, count=1, flags=re.IGNORECASE)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  [OK] {rel}")
    modified += 1

print(f"\nCSS override injetado em {modified} arquivo(s).")
