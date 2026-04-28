#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrige 3 bugs do site estatico no Hostinger:
1. Hero preto: forca background-images via CSS direto (bypass WP Rocket lazy-load)
2. Spinner de Areas de Atuacao: substitui jet-listing-grid por HTML estatico
3. Nav comprimida: ja corrigida pelo CSS (gap entre itens)
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(ROOT, "index.html")

# ── AREAS DE ATUACAO — HTML estatico ──────────────────────────────
AREAS_HTML = '''<div class="ia-areas-grid">
  <div class="ia-area-card">
    <div class="ia-area-icon">
      <svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
    </div>
    <h3 class="elementor-heading-title">Advocacia Especializada em Direito Banc&#225;rio</h3>
    <p>Defesa em execu&#231;&#245;es e revis&#227;o de contratos banc&#225;rios abusivos. Protegemos seus direitos contra cobran&#231;as indevidas e cl&#225;usulas ilegais.</p>
    <a href="areas-de-atuacao/advocacia-especializada-em-direito-bancario/index.html" class="elementor-button elementor-button-link elementor-size-sm">Saiba mais</a>
  </div>
  <div class="ia-area-card">
    <div class="ia-area-icon">
      <svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
    </div>
    <h3 class="elementor-heading-title">Suspens&#227;o de Leil&#227;o de Im&#243;veis</h3>
    <p>Atua&#231;&#227;o r&#225;pida para suspender leil&#245;es extrajudiciais ilegais e defender seu patrim&#244;nio imobili&#225;rio com seguran&#231;a jur&#237;dica.</p>
    <a href="areas-de-atuacao/suspensao-de-leilao-de-imoveis/index.html" class="elementor-button elementor-button-link elementor-size-sm">Saiba mais</a>
  </div>
  <div class="ia-area-card">
    <div class="ia-area-icon">
      <svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
    </div>
    <h3 class="elementor-heading-title">Aquisi&#231;&#227;o de Im&#243;vel de Leil&#227;o</h3>
    <p>Assessoria completa para compra segura de im&#243;veis em leil&#245;es judiciais e extrajudiciais, com an&#225;lise jur&#237;dica pr&#233;via.</p>
    <a href="areas-de-atuacao/aquisicao-de-imovel-de-leilao/index.html" class="elementor-button elementor-button-link elementor-size-sm">Saiba mais</a>
  </div>
  <div class="ia-area-card">
    <div class="ia-area-icon">
      <svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
    </div>
    <h3 class="elementor-heading-title">Desconto para Quita&#231;&#227;o de Financiamento</h3>
    <p>Negocia&#231;&#227;o estrat&#233;gica com institui&#231;&#245;es financeiras para obter descontos significativos na quita&#231;&#227;o antecipada de financiamentos.</p>
    <a href="areas-de-atuacao/desconto-para-quitacao-antecipada-de-financiamento/index.html" class="elementor-button elementor-button-link elementor-size-sm">Saiba mais</a>
  </div>
  <div class="ia-area-card">
    <div class="ia-area-icon">
      <svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>
    </div>
    <h3 class="elementor-heading-title">Defesa de Empresas Endividadas</h3>
    <p>Blindagem patrimonial e reestrutura&#231;&#227;o de d&#237;vidas para empresas, garantindo a continuidade dos neg&#243;cios com segurança jurídica.</p>
    <a href="areas-de-atuacao/defesa-de-empresas-endividadas-e-blindagem-patrimonial/index.html" class="elementor-button elementor-button-link elementor-size-sm">Saiba mais</a>
  </div>
</div>'''

# ── CSS inline para corrigir backgrounds ──────────────────────────
BG_FIX_CSS = """<style id="ia-bg-fix">
/* Fix WP Rocket lazy-load backgrounds no site estatico */
/* Remove o bloqueio de background para todos os containers */
.e-con.e-parent:not(.e-lazyloaded):not(.e-no-lazyload),
.e-con.e-parent:not(.e-lazyloaded):not(.e-no-lazyload) * {
  background-image: unset;
}
/* Hero principal (desktop) */
.elementor-8 .elementor-element.elementor-element-c2afc41 {
  background-image: url('wp-content/uploads/2023/08/bannerc.jpg') !important;
  background-size: cover !important;
  background-position: center center !important;
  background-repeat: no-repeat !important;
  min-height: 85vh;
}
/* Banner modelo 2 */
.elementor-8 .elementor-element.elementor-element-e5a17be {
  background-image: url('wp-content/uploads/2023/07/banner-adv-modelo-home-2.jpg') !important;
  background-size: cover !important;
  background-position: center center !important;
  background-repeat: no-repeat !important;
}
.elementor-8 .elementor-element.elementor-element-e5a17be::before {
  background-image: url('wp-content/uploads/2023/07/banner-adv-modelo-home-2.jpg') !important;
}
/* Banner modelo 1 */
.elementor-8 .elementor-element.elementor-element-77d1c79 {
  background-image: url('wp-content/uploads/2023/07/banner-adv-modelo-home-1.jpg') !important;
  background-size: cover !important;
  background-position: center center !important;
  background-repeat: no-repeat !important;
}
/* Overlay escuro sobre os banners para manter legibilidade */
.elementor-8 .elementor-element.elementor-element-c2afc41::before,
.elementor-8 .elementor-element.elementor-element-e5a17be::after,
.elementor-8 .elementor-element.elementor-element-77d1c79::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(27,42,74,0.55);
  z-index: 0;
  pointer-events: none;
}
</style>"""

SPINNER_OLD = '<div class="jet-listing-grid jet-listing-grid--lazy-load jet-listing jet-listing-grid-loading" data-lazy-load="{&quot;offset&quot;:&quot;0px&quot;,&quot;post_id&quot;:8,&quot;queried_id&quot;:&quot;8|WP_Post&quot;}"><div class="jet-listing-grid__loader"><div class="jet-listing-grid__loader-spinner"></div></div></div>'


def fix_index():
    with open(INDEX, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()

    changed = []

    # 1. Inject background-image fix CSS right before </head>
    if "ia-bg-fix" not in html:
        html = html.replace("</head>", BG_FIX_CSS + "\n</head>", 1)
        changed.append("CSS de fundo injetado")

    # 2. Replace jet-listing-grid spinner with static areas HTML
    if "ia-areas-grid" not in html:
        new_section = f'<div class="jet-listing-grid">{AREAS_HTML}</div>'
        if SPINNER_OLD in html:
            html = html.replace(SPINNER_OLD, new_section)
            changed.append("jet-listing-grid substituido por HTML estatico")
        else:
            # Fallback: find any jet-listing-grid-loading div
            html = re.sub(
                r'<div class="jet-listing-grid jet-listing-grid--lazy-load[^"]*"[^>]*>.*?</div></div>',
                new_section,
                html,
                count=1,
                flags=re.DOTALL,
            )
            changed.append("jet-listing-grid substituido (fallback regex)")

    if not changed:
        print("  [--] index.html — sem alteracoes necessarias")
        return

    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(html)

    for c in changed:
        print(f"  [OK] index.html — {c}")


def add_css_fixes():
    css_path = os.path.join(
        ROOT,
        "wp-content", "uploads", "elementor", "css", "ia-professional.css"
    )

    addition = """

/* ================================================================
   CORRECOES DE LAYOUT — Adicionado apos deploy
   ================================================================ */

/* Nav: espaco entre itens (fix compressao) */
.elementor-nav-menu--main .elementor-nav-menu {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 0 28px !important;
  align-items: center !important;
}

.elementor-nav-menu--main .elementor-item {
  padding: 8px 0 !important;
  white-space: nowrap !important;
}

/* Areas de Atuacao — grid estatico */
.ia-areas-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
  padding: 16px 0 32px;
  width: 100%;
}

.ia-area-card {
  background: #FFFFFF;
  border-radius: 10px;
  border-left: 4px solid #C3A84C;
  box-shadow: 0 2px 12px rgba(27,42,74,0.08);
  padding: 28px 24px 32px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: transform 0.32s ease, box-shadow 0.32s ease;
}

.ia-area-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 32px rgba(27,42,74,0.15);
  border-left-color: #1B2A4A;
}

.ia-area-icon {
  color: #C3A84C;
  line-height: 1;
}

.ia-area-card h3.elementor-heading-title {
  font-size: 1.05rem !important;
  line-height: 1.35 !important;
  margin-bottom: 0 !important;
  padding-bottom: 0 !important;
  color: #1B2A4A !important;
}

.ia-area-card h3.elementor-heading-title::after { display: none !important; }

.ia-area-card p {
  font-size: 0.88rem !important;
  line-height: 1.65 !important;
  color: #666 !important;
  flex: 1;
}

.ia-area-card .elementor-button {
  margin-top: 4px !important;
  align-self: flex-start !important;
  padding: 10px 20px !important;
  font-size: 11px !important;
  animation: none !important;
}

/* Hero: garante texto legivel sobre o banner */
.elementor-element-c2afc41,
.elementor-element-e5a17be,
.elementor-element-77d1c79 {
  position: relative;
}

.elementor-element-c2afc41 .e-con-inner,
.elementor-element-e5a17be .e-con-inner,
.elementor-element-77d1c79 .e-con-inner {
  position: relative;
  z-index: 1;
}

/* Responsivo — areas grid */
@media screen and (max-width: 1024px) {
  .ia-areas-grid { grid-template-columns: repeat(2, 1fr); gap: 20px; }
}

@media screen and (max-width: 640px) {
  .ia-areas-grid { grid-template-columns: 1fr; gap: 16px; }
  .ia-area-card { padding: 20px 18px 24px; }
}
"""

    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()

    if "CORRECOES DE LAYOUT" in css:
        print("  [--] ia-professional.css — ja atualizado")
        return

    with open(css_path, "a", encoding="utf-8") as f:
        f.write(addition)

    print("  [OK] ia-professional.css — nav fix + areas grid adicionados")


def main():
    print("\n" + "="*60)
    print("  FIX STATIC SITE — Hostinger")
    print("="*60 + "\n")
    fix_index()
    add_css_fixes()
    print("\n" + "="*60)
    print("  Concluido.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
