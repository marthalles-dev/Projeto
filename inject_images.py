import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(ROOT, 'index.html')

def process_html():
    with open(FILE_PATH, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()
        
    original = html
    
    # Adicionar CSS do overlay
    overlay_css = """
/* Hero Overlay */
.hero-overlay {
    position: relative;
}
.hero-overlay::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.65); /* Escurecimento de 65% */
    z-index: 0;
    pointer-events: none;
}
.hero-overlay > * {
    position: relative;
    z-index: 1;
}
"""
    if '.hero-overlay' not in html:
        # Tenta injetar dentro do nosso style block ia-custom-fixes
        if '<style id="ia-custom-fixes">' in html:
            html = html.replace('<style id="ia-custom-fixes">\n', f'<style id="ia-custom-fixes">\n{overlay_css}')
        else:
            # Se nao tiver, injeta antes do /head
            html = html.replace('</head>', f'<style>{overlay_css}</style>\n</head>')
            
    # Injetar a classe hero-overlay na primeira secao principal
    # Primeiro Elementor section costuma ser o hero
    match = re.search(r'<section\s+class="[^"]*elementor-section[^>]*>', html)
    if match:
        tag = match.group(0)
        if 'hero-overlay' not in tag:
            new_tag = tag.replace('class="', 'class="hero-overlay ', 1)
            # Tentar adicionar o background-image inline para o hero-bg.jpg
            if 'style=' in new_tag:
                new_tag = new_tag.replace('style="', 'style="background-image: url(\'wp-content/uploads/hero-bg.jpg\'); background-size: cover; background-position: center; ')
            else:
                new_tag = new_tag.replace('>', ' style="background-image: url(\'wp-content/uploads/hero-bg.jpg\'); background-size: cover; background-position: center;">')
            html = html.replace(tag, new_tag, 1)

    # Substituir src das logos
    # Buscar tags de imagem que parecem ser logos
    # Simplificando: vamos buscar a primeira ocorrencia da imagem original
    logo_pattern = re.compile(r'<img[^>]*src="[^"]*wp-content/uploads/2021/11/Logomarca-1-1024x566\.jpg"[^>]*>')
    def repl_logo(m):
        tag = m.group(0)
        return re.sub(r'src="[^"]*"', 'src="wp-content/uploads/logo.jpg"', tag)
    
    html = logo_pattern.sub(repl_logo, html)

    if html != original:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(html)
        print("CSS Overlay added and Logo references updated.")
    else:
        print("No changes made to HTML. Overlay might already exist.")

if __name__ == '__main__':
    process_html()
