import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(ROOT, 'index.html')
UPLOADS_DIR = os.path.join(ROOT, 'wp-content', 'uploads')

# 1. Copiar as imagens redimensionadas de volta para a raiz (sobrescrevendo as originais pesadas)
imagens = [
    'hero-bg.jpg', 'logo.jpg', 'servico-bancario.jpg', 
    'servico-empresas.jpg', 'servico-imobiliario.jpg', 
    'icone-agilidade.jpg'
]

for img in imagens:
    src = os.path.join(UPLOADS_DIR, img)
    dest = os.path.join(ROOT, img)
    if os.path.exists(src):
        shutil.copy(src, dest)

# 2. Atualizar o HTML para apontar para a raiz e tentar trocar as imagens de servico
def process_html():
    with open(FILE_PATH, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()
        
    original = html

    # Corrigir o Hero Bg
    html = html.replace("url('wp-content/uploads/hero-bg.jpg')", "url('hero-bg.jpg')")
    
    # Corrigir a Logo
    html = html.replace('src="wp-content/uploads/logo.jpg"', 'src="logo.jpg"')
    
    # Tentar substituir imagens genéricas de serviços. Vamos buscar palavras chaves perto de tags img
    # "Bancário"
    bancario_idx = html.find('Direito Bancário')
    if bancario_idx != -1:
        # Encontrar a imagem antes disso (geralmente o icone/foto fica antes do titulo no Elementor)
        img_match = list(re.finditer(r'<img[^>]+src="([^"]+)"', html[:bancario_idx]))
        if img_match:
            last_img = img_match[-1]
            old_src = last_img.group(1)
            html = html[:last_img.start()] + last_img.group(0).replace(old_src, 'servico-bancario.jpg') + html[last_img.end():]
            
    empresarial_idx = html.find('Defesa de Empresas')
    if empresarial_idx == -1:
        empresarial_idx = html.find('Direito Empresarial')
    if empresarial_idx != -1:
        img_match = list(re.finditer(r'<img[^>]+src="([^"]+)"', html[:empresarial_idx]))
        if img_match:
            last_img = img_match[-1]
            old_src = last_img.group(1)
            html = html[:last_img.start()] + last_img.group(0).replace(old_src, 'servico-empresas.jpg') + html[last_img.end():]

    imobiliario_idx = html.find('Direito Imobiliário')
    if imobiliario_idx != -1:
        img_match = list(re.finditer(r'<img[^>]+src="([^"]+)"', html[:imobiliario_idx]))
        if img_match:
            last_img = img_match[-1]
            old_src = last_img.group(1)
            html = html[:last_img.start()] + last_img.group(0).replace(old_src, 'servico-imobiliario.jpg') + html[last_img.end():]

    if html != original:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(html)
        print("HTML atualizado com caminhos na raiz!")
    else:
        print("Nenhuma alteração necessária no HTML.")

if __name__ == '__main__':
    process_html()
