#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Injeta SEO meta tags, ia-professional.css e ia-animations.js
em todas as paginas HTML do projeto.
"""

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

# ── SEO por pagina ──────────────────────────────────────────────
SEO_DATA = {
    "index.html": {
        "description": (
            "Escritório de advocacia empresarial especializado em Direito Bancário, "
            "Imobiliário e Leilão de Imóveis em Belo Horizonte - MG. "
            "Defendemos seus interesses em execuções, usucapião e contratos bancários."
        ),
        "og_title":  "IA Advocacia Empresarial | Direito Bancário e Imobiliário - BH",
        "og_url":    "https://iaadvocaciaempresarial.com.br/",
        "canonical": "https://iaadvocaciaempresarial.com.br/",
        "depth":     0,
        "schema": {
            "@context":    "https://schema.org",
            "@type":       "LegalService",
            "name":        "IA Advocacia Empresarial",
            "description": "Advocacia empresarial especializada em Direito Bancário, Imobiliário e Leilão de Imóveis em Belo Horizonte - MG.",
            "url":         "https://iaadvocaciaempresarial.com.br",
            "telephone":   "+55-31-9229-2541",
            "email":       "contato@iaadvocaciaempresarial.com.br",
            "priceRange":  "$$",
            "address": {
                "@type":           "PostalAddress",
                "streetAddress":   "Rua Guerra Junqueiro, n. 11",
                "addressLocality": "Belo Horizonte",
                "addressRegion":   "MG",
                "postalCode":      "31565-230",
                "addressCountry":  "BR"
            },
            "geo": {
                "@type":     "GeoCoordinates",
                "latitude":  -19.9167,
                "longitude": -43.9345
            },
            "openingHoursSpecification": {
                "@type":     "OpeningHoursSpecification",
                "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
                "opens":     "09:00",
                "closes":    "18:00"
            },
            "sameAs": ["https://www.instagram.com/iaadvocaciaempresarial/"],
            "image": "https://iaadvocaciaempresarial.com.br/wp-content/uploads/2021/11/Logomarca-1-1024x566.jpg",
            "areaServed": {
                "@type":  "City",
                "name":   "Belo Horizonte"
            }
        },
    },
    "contato/index.html": {
        "description": (
            "Entre em contato com a IA Advocacia Empresarial. "
            "Atendemos em Belo Horizonte - MG. "
            "WhatsApp: (31) 9229-2541 | contato@iaadvocaciaempresarial.com.br"
        ),
        "og_title":  "Contato | IA Advocacia Empresarial - Belo Horizonte",
        "og_url":    "https://iaadvocaciaempresarial.com.br/contato/",
        "canonical": "https://iaadvocaciaempresarial.com.br/contato/",
        "depth":     1,
    },
    "quem-somos/index.html": {
        "description": (
            "Conheça a IA Advocacia Empresarial — escritório especializado em "
            "Direito Bancário, Imobiliário e Leilão de Imóveis, com sede em "
            "Belo Horizonte - MG."
        ),
        "og_title":  "Quem Somos | IA Advocacia Empresarial - Belo Horizonte",
        "og_url":    "https://iaadvocaciaempresarial.com.br/quem-somos/",
        "canonical": "https://iaadvocaciaempresarial.com.br/quem-somos/",
        "depth":     1,
    },
    "politica-de-privacidade/index.html": {
        "description": (
            "Politica de privacidade da IA Advocacia Empresarial. "
            "Saiba como tratamos seus dados pessoais."
        ),
        "og_title":  "Politica de Privacidade | IA Advocacia Empresarial",
        "og_url":    "https://iaadvocaciaempresarial.com.br/politica-de-privacidade/",
        "canonical": "https://iaadvocaciaempresarial.com.br/politica-de-privacidade/",
        "depth":     1,
    },
}

OG_IMAGE = "https://iaadvocaciaempresarial.com.br/wp-content/uploads/2021/11/Logomarca-1-1024x566.jpg"

MARKER_SEO  = "ia-seo-injected"
MARKER_CSS  = "ia-professional-css"
MARKER_JS   = "ia-animations-js"


def rel_path(depth, filename):
    prefix = "../" * depth
    return prefix + filename


def build_seo_block(data, depth):
    import json
    lines = []

    lines.append(f'  <meta name="description" content="{data["description"]}" />')
    lines.append(f'  <meta name="robots" content="index, follow" />')
    lines.append(f'  <meta name="author" content="IA Advocacia Empresarial" />')
    lines.append(f'  <link rel="canonical" href="{data["canonical"]}" />')

    # Open Graph
    lines.append(f'  <meta property="og:type"        content="website" />')
    lines.append(f'  <meta property="og:site_name"   content="IA Advocacia Empresarial" />')
    lines.append(f'  <meta property="og:title"       content="{data["og_title"]}" />')
    lines.append(f'  <meta property="og:description" content="{data["description"]}" />')
    lines.append(f'  <meta property="og:url"         content="{data["og_url"]}" />')
    lines.append(f'  <meta property="og:image"       content="{OG_IMAGE}" />')
    lines.append(f'  <meta property="og:locale"      content="pt_BR" />')

    # Twitter Card
    lines.append(f'  <meta name="twitter:card"        content="summary_large_image" />')
    lines.append(f'  <meta name="twitter:title"       content="{data["og_title"]}" />')
    lines.append(f'  <meta name="twitter:description" content="{data["description"]}" />')
    lines.append(f'  <meta name="twitter:image"       content="{OG_IMAGE}" />')

    # JSON-LD schema (only for pages that have it)
    schema = data.get("schema")
    if schema:
        schema_json = json.dumps(schema, ensure_ascii=False, indent=4)
        lines.append(f'  <script type="application/ld+json">\n{schema_json}\n  </script>')

    lines.append(f'  <!-- {MARKER_SEO} -->')
    return "\n".join(lines)


def process_page(rel_key):
    filepath = os.path.join(ROOT, rel_key.replace("/", os.sep))
    if not os.path.exists(filepath):
        return False, f"nao encontrado: {rel_key}"

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    changed = False
    data = SEO_DATA[rel_key]
    depth = data["depth"]

    # 1. SEO meta block
    if MARKER_SEO not in content:
        seo_block = build_seo_block(data, depth)
        # Insert after <head> opening or after first <meta charset>
        if '<meta charset' in content:
            content = re.sub(
                r'(<meta charset=[^>]+>)',
                r'\1\n' + seo_block,
                content, count=1
            )
        else:
            content = content.replace('<head>', '<head>\n' + seo_block, 1)
        changed = True

    # 2. Professional CSS
    if MARKER_CSS not in content:
        css_path = rel_path(depth, "wp-content/uploads/elementor/css/ia-professional.css")
        css_tag = (
            f'  <link rel="stylesheet" href="{css_path}" '
            f'media="all" id="{MARKER_CSS}" />'
        )
        content = content.replace('</head>', css_tag + '\n</head>', 1)
        changed = True

    # 3. Animations JS (before </body>)
    if MARKER_JS not in content:
        js_path = rel_path(depth, "wp-content/uploads/elementor/js/ia-animations.js")
        js_tag = (
            f'  <script src="{js_path}" defer id="{MARKER_JS}"></script>'
        )
        if '</body>' in content:
            content = content.replace('</body>', js_tag + '\n</body>', 1)
        else:
            content += '\n' + js_tag
        changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True, "atualizado"
    return False, "sem alteracoes necessarias"


def main():
    print("\n" + "="*60)
    print("  INJECAO PROFESSIONAL: SEO + CSS + JS")
    print("="*60 + "\n")

    for key in SEO_DATA:
        ok, msg = process_page(key)
        status = "[OK]" if ok else "[--]"
        print(f"  {status} {key:50s} {msg}")

    print("\n" + "="*60)
    print("  Concluido.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
