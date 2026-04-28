#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de rebranding completo: Maschio & Pionório → IA Advocacia Empresarial
Paleta: Midnight #1B2A4A | Champagne Gold #C3A84C | Graphite #444444 | Accent #F5A840
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

LOREM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor "
    "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
    "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure "
    "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
)

# ─────────────────────────────────────────────────────────────────────────────
# 1. MAPEAMENTO DE CORES CSS  (minúsculas → nova cor em maiúsculas)
# ─────────────────────────────────────────────────────────────────────────────
COLOR_MAP = {
    # Verdes originais → Champagne Gold (ação)
    "#039618": "#C3A84C",
    "#2cc341": "#C3A84C",
    "#4fe964": "#F5A840",
    "#388442": "#1B2A4A",
    # Verde escuro → Midnight
    "#33743c": "#1B2A4A",
    # Textos escuros → Graphite
    "#232323": "#444444",
    "#1a1a1a": "#444444",
    "#595d60": "#444444",
    "#595959": "#444444",
    "#332f2f": "#444444",
    "#020101": "#1B2A4A",
    # Tons quentes (fundo Elementor) → Marble White
    "#ecdfcf": "#F9F9F9",
    "#9b8e7d": "#C3A84C",
    # Cinza claro → Marble White
    "#eeeeee": "#F9F9F9",
    "#e8e8e8": "#F9F9F9",
    "#f0f0f0": "#F9F9F9",
    # Azul claro elementor default
    "#6ec1e4": "#C3A84C",
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. SUBSTITUIÇÕES DE TEXTO HTML
# ─────────────────────────────────────────────────────────────────────────────
HTML_REPLACEMENTS = [
    # Título/nome do escritório — variantes HTML encoded e plain
    ("Maschio &amp; Pionório Advocacia Especializada", "IA Advocacia Empresarial"),
    ("Maschio &amp; Pionório Advocacia Especializada", "IA Advocacia Empresarial"),
    ("Maschio &amp; Pionório", "IA Advocacia Empresarial"),
    ("Maschio & Pionório Advocacia Especializada", "IA Advocacia Empresarial"),
    ("Maschio & Pionório", "IA Advocacia Empresarial"),
    ("Maschio e Pionório", "IA Advocacia Empresarial"),
    ("Maschio Pionório", "IA Advocacia Empresarial"),

    # E-mail
    ("atendimento.adv@maschiopionorio.com.br", "contato@iaadvocaciaempresarial.com.br"),
    ("mailto:atendimento.adv@maschiopionorio.com.br",
     "mailto:contato@iaadvocaciaempresarial.com.br"),

    # Telefones originais
    ("(11) 91676-2026", "(31) 9229-2541"),
    ("(11) 93380-2035", "(31) 9229-2541"),
    ("11 91676-2026", "31 9229-2541"),
    ("11 93380-2035", "31 9229-2541"),

    # WhatsApp – número antigo (SP) → BH
    ("5511933802035", "5531922925411"),   # link wa.me antigo
    ("5511916762026", "5531922925411"),

    # WhatsApp texto da mensagem no link
    (
        "Ol%C3%A1%2C%20vi%20o%20an%C3%BAncio%20e%20gostaria%20de%20falar%20com%20um(a)%20advogado(a)%20especialista%20em%20Direito%20Banc%C3%A1rio%20e%20Direito%20Imobili%C3%A1rio%2C%20com%20atua%C3%A7%C3%A3o%20em%20Execu%C3%A7%C3%B5es%20de%20Contratos%20Banc%C3%A1rios%2C%20Usucapi%C3%A3o%20e%20Defesa%20de%20Leil%C3%A3o%20de%20Im%C3%B3veis",
        "Ol%C3%A1%2C%20gostaria%20de%20falar%20com%20um%20advogado%20da%20IA%20Advocacia%20Empresarial."
    ),

    # Instagram
    ("https://www.instagram.com/maschiopionorioadvocacia/",
     "https://www.instagram.com/iaadvocaciaempresarial/"),
    ("instagram.com/maschiopionorioadvocacia",
     "instagram.com/iaadvocaciaempresarial"),

    # Facebook → placeholder
    ("https://www.facebook.com/maschiopionorioadvocacia/", "#"),
    ("https://www.facebook.com/maschiopionorioadvocacia", "#"),

    # LinkedIn → placeholder
    ("https://www.linkedin.com/company/maschio-e-pion%C3%B3rio-advocacia", "#"),
    ("https://www.linkedin.com/company/maschiopionorio", "#"),

    # Twitter/X → placeholder
    ("https://twitter.com/maschiopionorio", "#"),

    # Domínio antigo em URLs internas
    ("https://maschiopionorio.com.br", "#"),
    ("http://maschiopionorio.com.br", "#"),
    ("maschiopionorio.com.br", "iaadvocaciaempresarial.com.br"),

    # Endereços originais (São Paulo / Rio)
    (
        "Edifício Antônio Alves Ferreira Guedes<br>Av. Brigadeiro Faria Lima, 3729<br>5º Andar - Itaim Bibi<br>São Paulo - SP - CEP 04538-905",
        "Rua Guerra Junqueiro, n. 11<br>Santa Branca<br>Belo Horizonte - MG<br>CEP 31565-230"
    ),
    (
        "Av. José Silva de Azevedo Neto, 200 - Bloco 4 - Sala 104 - Barra da Tijuca<br>Rio de Janeiro - RJ - CEP 22775-056",
        "Rua Guerra Junqueiro, n. 11<br>Santa Branca<br>Belo Horizonte - MG<br>CEP 31565-230"
    ),
    (
        "Amadeus Business Tower<br>Av. do Contorno, 6594 - 7º Andar - Savassi<br>Belo Horizonte - MG - CEP 30110-044",
        "Rua Guerra Junqueiro, n. 11<br>Santa Branca<br>Belo Horizonte - MG<br>CEP 31565-230"
    ),
    (
        "Edifício Corporate Evolution<br>R. Comendador Araújo, 499 - 10º Andar - Centro Curitiba - PR - CEP 80420-000",
        "Rua Guerra Junqueiro, n. 11<br>Santa Branca<br>Belo Horizonte - MG<br>CEP 31565-230"
    ),
    (
        "Edifício Opus One<br>Av. Carlos Gomes 222 - 8° andar - Boa Vista<br>Porto Alegre - RS - CEP 90480-000",
        "Rua Guerra Junqueiro, n. 11<br>Santa Branca<br>Belo Horizonte - MG<br>CEP 31565-230"
    ),
    (
        "<b>Edifício Opus One<br></b>Av. Carlos Gomes 222 - 8° andar - Boa Vista<br>Porto Alegre - RS - CEP 90480-000",
        "<b>IA Advocacia Empresarial</b><br>Rua Guerra Junqueiro, n. 11<br>Santa Branca<br>Belo Horizonte - MG - CEP 31565-230"
    ),

    # Título da página no <title>
    (
        "Especialista em Direito Bancário, Imobiliário e Leilão de Imovéis. Nossa Especialidade é Defender seus Interesses em Contratos Bancários, Imobiliários e Leilão de Imóveis",
        "Advocacia Empresarial Especializada em Belo Horizonte"
    ),

    # Meta description / rodapé genérico com nome antigo
    ("Maschio", "IA Advocacia"),
    ("Pionório", "Empresarial"),
    ("maschiopionorio", "iaadvocaciaempresarial"),
]

# ─────────────────────────────────────────────────────────────────────────────
# 3. PASTAS DE BLOG / ARTIGOS → Lorem Ipsum nos parágrafos
# ─────────────────────────────────────────────────────────────────────────────
BLOG_DIRS = {
    "afastada-penhora",
    "areas-de-atuacao",
    "banco-pagara",
    "bem-de-familia-nao-pode",
    "bem-de-familia-pode",
    "blog",
    "cabe-usucapiao",
    "consolidacao",
    "desconsideracao",
    "devedor-pode",
    "e-possivel-purgar",
    "reconhecida-usucapiao",
    "stj-invalida",
}

LOREM_BLOCKS = (
    "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor "
    "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
    "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>\n"
    "<p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu "
    "fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa "
    "qui officia deserunt mollit anim id est laborum.</p>\n"
    "<p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium "
    "doloremque laudantium, totam rem aperiam eaque ipsa quae ab illo inventore veritatis "
    "et quasi architecto beatae vitae dicta sunt explicabo.</p>"
)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def apply_css_colors(content: str) -> str:
    """Replace all mapped hex colors (case-insensitive) in a CSS string."""
    def replacer(m):
        key = m.group(0).lower()
        return COLOR_MAP.get(key, m.group(0))

    pattern = re.compile(
        r'#(?:' + '|'.join(re.escape(c[1:]) for c in COLOR_MAP) + r')\b',
        re.IGNORECASE
    )
    return pattern.sub(replacer, content)


def apply_html_text(content: str) -> str:
    for old, new in HTML_REPLACEMENTS:
        content = content.replace(old, new)
    return content


def lorem_paragraphs(content: str) -> str:
    """Replace <p>...</p> blocks inside the article content area with Lorem Ipsum."""
    # Target: content inside elementor-widget-container / entry-content divs
    # Strategy: replace every <p>...</p> that contains more than ~30 chars of text
    def replace_p(m):
        inner = m.group(1)
        # Skip if it looks like structural markup (only tags, no real text)
        text_only = re.sub(r'<[^>]+>', '', inner).strip()
        if len(text_only) < 30:
            return m.group(0)
        return "<p>" + LOREM + "</p>"

    return re.sub(r'<p>(.*?)</p>', replace_p, content, flags=re.DOTALL | re.IGNORECASE)


def is_blog_html(filepath: str) -> bool:
    parts = filepath.replace("\\", "/").split("/")
    return any(p in BLOG_DIRS for p in parts)


def process_file(filepath: str) -> tuple[int, list[str]]:
    """Process a single file. Returns (changes_count, change_descriptions)."""
    ext = os.path.splitext(filepath)[1].lower()
    changes = []

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            original = f.read()
    except Exception as e:
        return 0, [f"ERROR reading: {e}"]

    content = original

    if ext == ".css":
        content = apply_css_colors(content)
        if content != original:
            changes.append("cores CSS substituídas")

    elif ext in (".html", ".htm"):
        content = apply_html_text(content)
        if content != original:
            changes.append("textos HTML substituídos")

        if is_blog_html(filepath):
            before = content
            content = lorem_paragraphs(content)
            if content != before:
                changes.append("parágrafos substituídos por Lorem Ipsum")

    if content == original:
        return 0, []

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        return 0, [f"ERROR writing: {e}"]

    return len(changes), changes


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    total_files = 0
    total_changes = 0

    print(f"\n{'='*60}")
    print("  REBRANDING: IA Advocacia Empresarial")
    print(f"  Diretorio: {ROOT}")
    print(f"{'='*60}\n")

    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Pula pastas de sistema
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__", ".git")]

        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in (".html", ".htm", ".css"):
                continue

            filepath = os.path.join(dirpath, filename)
            rel = os.path.relpath(filepath, ROOT)

            count, descs = process_file(filepath)
            if count > 0:
                total_files += 1
                total_changes += count
                print(f"  [OK] {rel}")
                for d in descs:
                    print(f"      >> {d}")

    print(f"\n{'='*60}")
    print(f"  CONCLUÍDO: {total_files} arquivo(s) modificado(s), {total_changes} tipo(s) de alteração")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
