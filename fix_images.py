#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove o lazy-loading do WP Rocket de TODOS os HTMLs do projeto.

Para cada <img>:
  - Substitui src="data:image/svg+xml..." pelo valor real de data-lazy-src
  - Remove data-lazy-src, data-lazy-srcset, data-lazy-sizes
  - Remove classes lazyloading/lazyloaded/rocket-lazyload

Para backgrounds (elementor e-con):
  - Remove o CSS inline que bloqueia background-image com none !important
  - A regra existente ia-bg-fix ja supre o restante
"""

import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

SVG_PLACEHOLDER = re.compile(
    r'src="data:image/svg\+xml[^"]*"',
    re.IGNORECASE
)

DATA_LAZY_SRC = re.compile(
    r'\s*data-lazy-src="([^"]*)"',
    re.IGNORECASE
)

DATA_LAZY_SRCSET = re.compile(
    r'\s*data-lazy-srcset="[^"]*"',
    re.IGNORECASE
)

DATA_LAZY_SIZES = re.compile(
    r'\s*data-lazy-sizes="[^"]*"',
    re.IGNORECASE
)

LAZY_CLASS = re.compile(
    r'\s*(lazyloading|lazyloaded|rocket-lazyload)',
    re.IGNORECASE
)

# Bloco CSS do Elementor que bloqueia backgrounds enquanto nao for lazy-loaded
# Formato: .e-con.e-parent:nth-of-type(n+X):not(.e-lazyloaded)... { background-image: none !important }
BG_BLOCK_CSS = re.compile(
    r'<style>\s*'
    r'\.e-con\.e-parent:nth-of-type\(n\+\d+\)[^}]+background-image:\s*none\s*!important[^}]*}'
    r'[\s\S]*?</style>',
    re.IGNORECASE
)


def fix_img_lazy(html: str) -> tuple[str, int]:
    """Substitui todos os src placeholder por data-lazy-src real."""
    count = 0

    def replace_img(m):
        nonlocal count
        tag = m.group(0)

        # Extrai o valor real de data-lazy-src
        lazy_m = DATA_LAZY_SRC.search(tag)
        if not lazy_m:
            return tag  # nao tem data-lazy-src, nao mexe

        real_src = lazy_m.group(1)

        # Substitui o src placeholder pelo real
        tag = SVG_PLACEHOLDER.sub(f'src="{real_src}"', tag)

        # Remove atributos de lazy-load
        tag = DATA_LAZY_SRC.sub('', tag)
        tag = DATA_LAZY_SRCSET.sub('', tag)
        tag = DATA_LAZY_SIZES.sub('', tag)

        count += 1
        return tag

    # Processa cada tag <img ...>
    result = re.sub(r'<img\b[^>]*/?>',  replace_img, html, flags=re.DOTALL | re.IGNORECASE)
    return result, count


def fix_bg_block(html: str) -> tuple[str, bool]:
    """Remove o bloco de CSS inline que bloqueia background-image."""
    # Busca o bloco inline especifico do Elementor (3-5 linhas com nth-of-type)
    pattern = re.compile(
        r'<style>\s*\n\s*\.e-con\.e-parent:nth-of-type'
        r'[\s\S]*?</style>',
        re.IGNORECASE
    )
    new_html = pattern.sub('<!-- ia: elementor-bg-lazyload-removed -->', html, count=1)
    changed = new_html != html
    return new_html, changed


def process_file(filepath: str) -> list[str]:
    changes = []

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    original = html

    # 1. Fix <img> lazy-load
    html, img_count = fix_img_lazy(html)
    if img_count:
        changes.append(f'{img_count} imagens corrigidas')

    # 2. Remove CSS de bloqueio de background
    html, bg_fixed = fix_bg_block(html)
    if bg_fixed:
        changes.append('CSS de bloqueio de background removido')

    if html == original:
        return []

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    return changes


def main():
    print('\n' + '='*60)
    print('  FIX IMAGES — Remove WP Rocket lazy-load')
    print('='*60 + '\n')

    total_files = 0
    for dirpath, _, filenames in os.walk(ROOT):
        for fname in filenames:
            if not fname.endswith(('.html', '.htm')):
                continue
            fpath = os.path.join(dirpath, fname)
            rel = os.path.relpath(fpath, ROOT)
            changes = process_file(fpath)
            if changes:
                total_files += 1
                print(f'  [OK] {rel}')
                for c in changes:
                    print(f'       >> {c}')

    print(f'\n  {total_files} arquivo(s) modificado(s).')
    print('='*60 + '\n')


if __name__ == '__main__':
    main()
