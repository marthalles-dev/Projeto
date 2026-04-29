#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. Troca logo e favicon para fav-3Wx3W.png em todos os HTMLs
2. Adiciona inline style no hero para forcar background-image
   (inline style nao pode ser sobrescrito por CSS de stylesheets)
3. Zera overlay do hero via CSS variable inline
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

def depth_prefix(filepath):
    rel = os.path.relpath(filepath, ROOT).replace('\\', '/')
    depth = rel.count('/')
    return '../' * depth


def fix_logo(html, prefix):
    """Substitui src de todos os <img> de logo por fav-3Wx3W.png"""
    count = 0
    logo_file = prefix + 'fav-3Wx3W.png'

    def rep(m):
        nonlocal count
        tag = m.group(0)
        # Detecta imagens de logo pelos ids/classes/src anteriores
        if any(kw in tag for kw in ('wp-image-1104', 'wp-image-582', 'src="logo.jpg"',
                                     'src="../logo.jpg"', 'src="../../logo.jpg"')):
            src_m = re.search(r'src\s*=\s*"[^"]*"', tag, re.IGNORECASE)
            if src_m:
                tag = tag.replace(src_m.group(0), f'src="{logo_file}"')
                count += 1
        return tag

    html = re.sub(r'<img\b[^>]*/?>',  rep, html, flags=re.IGNORECASE | re.DOTALL)
    return html, count


def fix_favicon(html, prefix):
    """Atualiza links de favicon para fav-3Wx3W.png"""
    fav = prefix + 'fav-3Wx3W.png'
    changed = False

    # Substitui links de favicon existentes
    new_html = re.sub(
        r'<link[^>]*rel=["\'](?:icon|shortcut icon)["\'][^>]*>',
        f'<link rel="icon" href="{fav}" sizes="any" type="image/png">',
        html, flags=re.IGNORECASE
    )
    if new_html != html:
        changed = True
        html = new_html

    # Se nao tinha favicon, injeta antes de </head>
    if 'rel="icon"' not in html and '</head>' in html:
        tag = f'  <link rel="icon" href="{fav}" sizes="any" type="image/png">\n'
        html = html.replace('</head>', tag + '</head>', 1)
        changed = True

    return html, changed


def fix_hero_inline(html):
    """
    Adiciona style inline diretamente no div do hero (c2afc41).
    Inline style tem prioridade maxima — nenhum CSS de stylesheet sobrescreve.
    """
    # Padrao: encontra o div de abertura do container hero
    pattern = re.compile(
        r'(<div\b[^>]*\belementor-element-c2afc41\b[^>]*)',
        re.IGNORECASE
    )

    hero_style = (
        "background-image:url('hero-bg.jpg');"
        "background-size:cover;"
        "background-position:center center;"
        "background-repeat:no-repeat;"
        "--overlay-opacity:0.25;"
    )

    def replacer(m):
        tag = m.group(1)
        # Remove style anterior se existir para nao duplicar
        tag = re.sub(r'\s*style\s*=\s*"[^"]*"', '', tag, flags=re.IGNORECASE)
        return tag + f' style="{hero_style}"'

    new_html = pattern.sub(replacer, html, count=1)
    changed = new_html != html
    return new_html, changed


def process(filepath):
    changes = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()
    original = html
    prefix = depth_prefix(filepath)

    html, n = fix_logo(html, prefix)
    if n: changes.append(f'logo: {n} img(s) -> fav-3Wx3W.png')

    html, ch = fix_favicon(html, prefix)
    if ch: changes.append('favicon atualizado para fav-3Wx3W.png')

    # Hero inline style — apenas no index.html da raiz
    if os.path.relpath(filepath, ROOT).replace('\\', '/') == 'index.html':
        html, ch = fix_hero_inline(html)
        if ch: changes.append('hero: inline style adicionado (background + overlay)')

    if html == original:
        return []
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return changes


def main():
    print('\n' + '='*60)
    print('  LOGO + FAVICON + HERO INLINE FIX')
    print('='*60 + '\n')
    total = 0
    for dirpath, _, fnames in os.walk(ROOT):
        for fname in fnames:
            if not fname.endswith(('.html', '.htm')):
                continue
            fp = os.path.join(dirpath, fname)
            rel = os.path.relpath(fp, ROOT)
            ch = process(fp)
            if ch:
                total += 1
                print(f'  [OK] {rel}')
                for c in ch:
                    print(f'       >> {c}')
    print(f'\n  {total} arquivo(s) modificado(s).')
    print('='*60 + '\n')


if __name__ == '__main__':
    main()
