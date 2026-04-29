#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix definitivo para site estatico IA Advocacia Empresarial.

Problema raiz: tags <source srcset="https://..."> dentro de <picture>
fazem o browser usar a URL absoluta externa (que falha) ignorando o <img src>.

Acoes:
1. Remove TODOS os <source> com srcset absoluto de <picture> elements
2. Remove srcset/sizes de <img> com URLs absolutas
3. Remove <noscript> com imagens duplicadas
4. Corrige o background do hero via HTML (inline style com !important)
5. Adiciona e-lazyloaded nos containers do hero
6. Atualiza referencias de imagem para arquivos na raiz onde existem
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

# Imagens novas na raiz do projeto → mapeadas para os seletores relevantes
ROOT_IMAGES = {
    'logo.jpg':                 ['logo', 'logomarca'],
    'hero-bg.jpg':              ['bannerc'],
    'servico-bancario.jpg':     ['bancario', 'bancaria'],
    'servico-imobiliario.jpg':  ['imobiliario', 'imobiliaria'],
    'servico-empresas.jpg':     ['empresa', 'endividada'],
    'icone-agilidade.jpg':      ['agilidade'],
}

# Prefixo relativo para imagens na raiz, partindo de subdiretorios
def root_prefix(filepath: str) -> str:
    depth = len(os.path.relpath(filepath, ROOT).replace('\\','/').split('/')) - 1
    return '../' * depth


def remove_picture_sources(html: str) -> tuple[str, int]:
    """Remove <source> tags com srcset apontando para URLs absolutas."""
    count = 0
    def replacer(m):
        nonlocal count
        tag = m.group(0)
        if 'srcset=' in tag and ('https://' in tag or 'http://' in tag):
            count += 1
            return ''
        return tag
    result = re.sub(r'<source\b[^>]*/?>',  replacer, html, flags=re.IGNORECASE | re.DOTALL)
    return result, count


def remove_abs_srcset_from_img(html: str) -> tuple[str, int]:
    """Remove srcset e sizes de <img> quando srcset aponta para URL absoluta."""
    count = 0
    def replacer(m):
        nonlocal count
        tag = m.group(0)
        has_abs_srcset = bool(re.search(r'srcset\s*=\s*"https?://', tag, re.IGNORECASE))
        if not has_abs_srcset:
            return tag
        # Remove srcset e sizes
        tag = re.sub(r'\s*srcset\s*=\s*"[^"]*"', '', tag, flags=re.IGNORECASE)
        tag = re.sub(r'\s*sizes\s*=\s*"[^"]*"',  '', tag, flags=re.IGNORECASE)
        count += 1
        return tag
    result = re.sub(r'<img\b[^>]*/?>',  replacer, html, flags=re.IGNORECASE | re.DOTALL)
    return result, count


def remove_noscript_images(html: str) -> tuple[str, int]:
    """Remove blocos <noscript> que contem <img> duplicadas."""
    count = 0
    def replacer(m):
        nonlocal count
        if '<img' in m.group(1):
            count += 1
            return ''
        return m.group(0)
    result = re.sub(r'<noscript>([\s\S]*?)</noscript>', replacer, html, flags=re.IGNORECASE)
    return result, count


def fix_hero_background(html: str) -> tuple[str, bool]:
    """
    Adiciona e-lazyloaded nos tres containers do hero
    e garante que o ia-bg-fix nao use 'unset'.
    """
    changed = False

    # Adiciona e-lazyloaded nos containers do hero
    for eid in ('elementor-element-c2afc41', 'elementor-element-e5a17be', 'elementor-element-77d1c79'):
        pattern = re.compile(
            r'(<div[^>]+class="[^"]*' + eid + r'[^"]*")',
            re.IGNORECASE
        )
        def add_lazyloaded(m, _eid=eid):
            tag = m.group(1)
            if 'e-lazyloaded' not in tag:
                tag = tag.replace('class="', 'class="e-lazyloaded ')
                return tag
            return tag
        new_html = pattern.sub(add_lazyloaded, html)
        if new_html != html:
            changed = True
            html = new_html

    # Corrige ia-bg-fix: troca background-image:unset pelo background real
    old_unset = re.compile(
        r'\.e-con\.e-parent:not\(\.e-lazyloaded\):not\(\.e-no-lazyload\),\s*'
        r'\.e-con\.e-parent:not\(\.e-lazyloaded\):not\(\.e-no-lazyload\) \* \{\s*'
        r'background-image: unset;\s*\}',
        re.IGNORECASE
    )
    if old_unset.search(html):
        html = old_unset.sub('', html)
        changed = True

    return html, changed


def update_image_refs(html: str, filepath: str) -> tuple[str, int]:
    """Atualiza src de <img> para usar imagens da raiz onde disponiveis."""
    count = 0
    prefix = root_prefix(filepath)

    def img_replacer(m):
        nonlocal count
        tag = m.group(0)
        src_m = re.search(r'\bsrc\s*=\s*"([^"]*)"', tag, re.IGNORECASE)
        if not src_m:
            return tag
        current_src = src_m.group(1)
        for new_img, keywords in ROOT_IMAGES.items():
            for kw in keywords:
                if kw.lower() in current_src.lower():
                    new_src = prefix + new_img
                    if current_src != new_src:
                        tag = tag.replace(f'src="{current_src}"', f'src="{new_src}"')
                        count += 1
                    return tag
        return tag

    result = re.sub(r'<img\b[^>]*/?>',  img_replacer, html, flags=re.IGNORECASE | re.DOTALL)
    return result, count


def fix_hero_bg_css(html: str, filepath: str) -> tuple[str, bool]:
    """Atualiza o CSS ia-bg-fix para usar hero-bg.jpg e caminhos corretos."""
    if 'ia-bg-fix' not in html:
        return html, False

    prefix = root_prefix(filepath)
    # Substitui url de bannerc.jpg por hero-bg.jpg
    old = f"url('{prefix}wp-content/uploads/2023/08/bannerc.jpg')"
    new = f"url('{prefix}hero-bg.jpg')"
    new_html = html.replace(old, new)

    # Tambem tenta sem prefix (para index.html na raiz)
    old2 = "url('wp-content/uploads/2023/08/bannerc.jpg')"
    new2 = "url('hero-bg.jpg')"
    new_html = new_html.replace(old2, new2)

    return new_html, new_html != html


def process_html(filepath: str) -> list[str]:
    changes = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()
    original = html

    html, n = remove_picture_sources(html)
    if n: changes.append(f'{n} <source> absolutos removidos')

    html, n = remove_abs_srcset_from_img(html)
    if n: changes.append(f'{n} srcset absolutos removidos de <img>')

    html, n = remove_noscript_images(html)
    if n: changes.append(f'{n} <noscript> removidos')

    html, ch = fix_hero_background(html)
    if ch: changes.append('hero: e-lazyloaded + ia-bg-fix corrigido')

    html, n = update_image_refs(html, filepath)
    if n: changes.append(f'{n} refs atualizadas para imagens da raiz')

    html, ch = fix_hero_bg_css(html, filepath)
    if ch: changes.append('CSS hero-bg.jpg atualizado')

    if html == original:
        return []

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return changes


def main():
    print('\n' + '='*60)
    print('  FIX FINAL — Imagens e backgrounds')
    print('='*60 + '\n')
    total = 0
    for dirpath, _, filenames in os.walk(ROOT):
        for fname in filenames:
            if not fname.endswith(('.html', '.htm')):
                continue
            fp = os.path.join(dirpath, fname)
            rel = os.path.relpath(fp, ROOT)
            changes = process_html(fp)
            if changes:
                total += 1
                print(f'  [OK] {rel}')
                for c in changes:
                    print(f'       >> {c}')
    print(f'\n  {total} arquivo(s) modificado(s).')
    print('='*60 + '\n')


if __name__ == '__main__':
    main()
