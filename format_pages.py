import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

# O CSS base sem a classe do hero-overlay (pois o usuario pediu para tirar o fundo preto nas internas)
CSS_FIXES = """
<style id="ia-custom-fixes">
/* Smooth Scroll */
html { scroll-behavior: smooth; }

/* Resets e Acessibilidade */
:focus { outline: 2px solid #0c4da2; outline-offset: 2px; }
img { max-width: 100%; height: auto; }
.skip-link {
    position: absolute;
    top: -40px; left: 0;
    background: #0c4da2; color: white;
    padding: 8px; z-index: 100000;
}
.skip-link:focus { top: 0; }
</style>
"""

def process_html(filepath):
    # Calcular o nível de diretório para usar caminho relativo ou absoluto
    # Se hospedado na raiz, /logo.jpg funciona bem, mas vamos usar ../ para ser flexível dependendo da profundidade
    rel_path = os.path.relpath(ROOT, os.path.dirname(filepath))
    if rel_path == '.':
        base_url = ''
    else:
        base_url = rel_path + '/'

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    original = html

    # 1. Injetar o CSS Fixes (se não existir)
    if '<style id="ia-custom-fixes">' not in html:
        html = html.replace('</head>', f'{CSS_FIXES}\n</head>')

    # 2. Corrigir a Logo
    # Regex flexível para achar a tag img da logo antiga
    logo_pattern = re.compile(r'<img[^>]*src="[^"]*(?:Logomarca-1-[^"]*|logo\.jpg)"[^>]*>')
    def repl_logo(m):
        tag = m.group(0)
        # Remover srcset e sizes
        tag = re.sub(r'\s*srcset="[^"]*"', '', tag)
        tag = re.sub(r'\s*sizes="[^"]*"', '', tag)
        # Substituir o src
        tag = re.sub(r'src="[^"]*"', f'src="{base_url}logo.jpg"', tag)
        return tag
    
    html = logo_pattern.sub(repl_logo, html)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

def main():
    count = 0
    # Percorrer tudo na pasta Projeto
    for root_dir, dirs, files in os.walk(ROOT):
        # Ignorar pastas indesejadas
        if '.git' in root_dir or 'wp-content' in root_dir or 'wp-includes' in root_dir:
            continue
            
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root_dir, file)
                # Ignorar a index.html principal porque já formatamos ela
                if filepath == os.path.join(ROOT, 'index.html'):
                    continue
                    
                if process_html(filepath):
                    count += 1
                    print(f"Formatada: {os.path.relpath(filepath, ROOT)}")
                    
    print(f"Total de páginas internas formatadas: {count}")

if __name__ == '__main__':
    main()
