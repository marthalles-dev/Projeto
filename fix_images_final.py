#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpeza definitiva de imagens para site estatico.

1. Remove TODOS os <source> de dentro de <picture> (independente do srcset)
2. Remove srcset e sizes de TODOS os <img> (independente do conteudo)
3. Atualiza areas grid com imagens reais da raiz
4. Mapeia imagens da raiz corretamente por profundidade de pasta
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

# Imagens disponiveis na raiz do projeto
ROOT_IMGS = [
    'logo.jpg',
    'hero-bg.jpg',
    'servico-bancario.jpg',
    'servico-imobiliario.jpg',
    'servico-empresas.jpg',
    'icone-agilidade.jpg',
    'logo-br39.png',
    'Logomarca-1-1024x566.jpg',
    'fav-150x150.png',
]

def depth_prefix(filepath):
    """Retorna '../' repetido conforme profundidade do arquivo em relacao a ROOT."""
    rel = os.path.relpath(filepath, ROOT).replace('\\', '/')
    depth = rel.count('/')
    return '../' * depth

# ── Remove todo <source> de dentro de <picture> ──────────────────
def strip_all_sources(html):
    old = html
    html = re.sub(r'<source\b[^>]*/?>',  '', html, flags=re.IGNORECASE | re.DOTALL)
    return html, html != old

# ── Remove srcset e sizes de todo <img> ──────────────────────────
def strip_img_attrs(html):
    count = 0
    def replacer(m):
        nonlocal count
        tag = m.group(0)
        new = re.sub(r'\s+srcset\s*=\s*"[^"]*"', '', tag, flags=re.IGNORECASE)
        new = re.sub(r'\s+sizes\s*=\s*"[^"]*"',  '', new, flags=re.IGNORECASE)
        if new != tag:
            count += 1
        return new
    result = re.sub(r'<img\b[^>]*/?>',  replacer, html, flags=re.IGNORECASE | re.DOTALL)
    return result, count

# ── Remove <noscript> que contem <img> ───────────────────────────
def strip_noscript(html):
    count = [0]
    def replacer(m):
        if '<img' in m.group(1):
            count[0] += 1
            return ''
        return m.group(0)
    result = re.sub(r'<noscript>([\s\S]*?)</noscript>', replacer, html, flags=re.IGNORECASE)
    return result, count[0]

# ── Garante que logo aponta para logo.jpg da raiz ────────────────
def fix_logo_src(html, prefix):
    # Qualquer img com wp-image-1104 (logo principal) ou wp-image-582 (logo footer)
    count = 0
    for cls in ('wp-image-1104', 'wp-image-582'):
        def rep(m, cls=cls):
            nonlocal count
            tag = m.group(0)
            if cls in tag and f'src="{prefix}logo.jpg"' not in tag:
                tag = re.sub(r'\bsrc\s*=\s*"[^"]*"', f'src="{prefix}logo.jpg"', tag, flags=re.IGNORECASE)
                count += 1
            return tag
        html = re.sub(r'<img\b[^>]*/?>',  rep, html, flags=re.IGNORECASE | re.DOTALL)
    return html, count

# ── Atualiza areas grid com imagens reais ────────────────────────
def build_areas_grid(prefix):
    """Gera o HTML do grid de areas com imagens reais da raiz."""
    cards = [
        {
            'img':   f'{prefix}servico-bancario.jpg',
            'alt':   'Direito Bancario',
            'title': 'Advocacia Especializada em Direito Banc&#225;rio',
            'desc':  'Defesa em execu&#231;&#245;es e revis&#227;o de contratos banc&#225;rios abusivos. Protegemos seus direitos contra cobran&#231;as indevidas e cl&#225;usulas ilegais.',
            'href':  f'{prefix}areas-de-atuacao/advocacia-especializada-em-direito-bancario/index.html',
        },
        {
            'img':   f'{prefix}servico-imobiliario.jpg',
            'alt':   'Leilao de Imoveis',
            'title': 'Suspens&#227;o de Leil&#227;o de Im&#243;veis',
            'desc':  'Atua&#231;&#227;o r&#225;pida para suspender leil&#245;es extrajudiciais ilegais e defender seu patrim&#244;nio imobili&#225;rio com seguran&#231;a jur&#237;dica.',
            'href':  f'{prefix}areas-de-atuacao/suspensao-de-leilao-de-imoveis/index.html',
        },
        {
            'img':   f'{prefix}servico-imobiliario.jpg',
            'alt':   'Aquisicao em Leilao',
            'title': 'Aquisi&#231;&#227;o de Im&#243;vel de Leil&#227;o',
            'desc':  'Assessoria completa para compra segura de im&#243;veis em leil&#245;es judiciais e extrajudiciais, com an&#225;lise jur&#237;dica pr&#233;via.',
            'href':  f'{prefix}areas-de-atuacao/aquisicao-de-imovel-de-leilao/index.html',
        },
        {
            'img':   f'{prefix}servico-bancario.jpg',
            'alt':   'Quitacao Financiamento',
            'title': 'Desconto para Quita&#231;&#227;o de Financiamento',
            'desc':  'Negocia&#231;&#227;o estrat&#233;gica com institui&#231;&#245;es financeiras para obter descontos significativos na quita&#231;&#227;o antecipada de financiamentos.',
            'href':  f'{prefix}areas-de-atuacao/desconto-para-quitacao-antecipada-de-financiamento/index.html',
        },
        {
            'img':   f'{prefix}servico-empresas.jpg',
            'alt':   'Defesa de Empresas',
            'title': 'Defesa de Empresas Endividadas',
            'desc':  'Blindagem patrimonial e reestrutura&#231;&#227;o de d&#237;vidas para empresas, garantindo a continuidade dos neg&#243;cios com seguran&#231;a jur&#237;dica.',
            'href':  f'{prefix}areas-de-atuacao/defesa-de-empresas-endividadas-e-blindagem-patrimonial/index.html',
        },
    ]

    html_cards = []
    for c in cards:
        html_cards.append(f'''  <div class="ia-area-card">
    <div class="ia-area-img">
      <img src="{c['img']}" alt="{c['alt']}" loading="lazy">
    </div>
    <h3 class="elementor-heading-title">{c['title']}</h3>
    <p>{c['desc']}</p>
    <a href="{c['href']}" class="elementor-button elementor-button-link elementor-size-sm">Saiba mais</a>
  </div>''')

    return '<div class="ia-areas-grid">\n' + '\n'.join(html_cards) + '\n</div>'

def update_areas_grid(html, prefix):
    pattern = re.compile(
        r'<div class="ia-areas-grid">[\s\S]*?</div>\s*(?=</div>)',
        re.IGNORECASE
    )
    new_grid = build_areas_grid(prefix)
    new_html = pattern.sub(new_grid, html, count=1)
    return new_html, new_html != html


def process(filepath):
    changes = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()
    original = html
    prefix = depth_prefix(filepath)

    html, ch = strip_all_sources(html)
    if ch: changes.append('<source> removidos')

    html, n = strip_img_attrs(html)
    if n: changes.append(f'{n} srcset/sizes removidos de <img>')

    html, n = strip_noscript(html)
    if n: changes.append(f'{n} <noscript> removidos')

    html, n = fix_logo_src(html, prefix)
    if n: changes.append(f'logo.jpg aplicado em {n} img(s)')

    if 'ia-areas-grid' in html:
        html, ch = update_areas_grid(html, prefix)
        if ch: changes.append('areas grid atualizado com imagens reais')

    if html == original:
        return []

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return changes


def main():
    print('\n' + '='*60)
    print('  FIX IMAGES FINAL')
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
