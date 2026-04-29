import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(ROOT, 'index.html')

def process_html():
    with open(FILE_PATH, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    original = html

    # 1. Remover atributos srcset e sizes das tags que contêm as imagens novas
    # Para as imagens de serviço e logo:
    imgs = ['logo.jpg', 'servico-bancario.jpg', 'servico-empresas.jpg', 'servico-imobiliario.jpg']
    
    for img_name in imgs:
        # Regex para encontrar a tag img inteira que contem este src
        pattern = re.compile(r'<img[^>]+src="'+re.escape(img_name)+r'"[^>]*>')
        def remove_srcset(m):
            tag = m.group(0)
            tag = re.sub(r'\s*srcset="[^"]*"', '', tag)
            tag = re.sub(r'\s*sizes="[^"]*"', '', tag)
            return tag
        html = pattern.sub(remove_srcset, html)

    # 2. Forçar a imagem de fundo com !important
    html = html.replace("url('hero-bg.jpg')", "url('hero-bg.jpg') !important")
    
    if html != original:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(html)
        print("HTML corrigido: srcset removido e background forcado!")
    else:
        print("Nenhuma modificação pendente.")

if __name__ == '__main__':
    process_html()
