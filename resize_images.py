import os
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
DEST_DIR = os.path.join(ROOT, 'wp-content', 'uploads')
os.makedirs(DEST_DIR, exist_ok=True)

TARGETS = {
    'hero-bg.jpg': (1920, 1080),
    'logo.jpg': (400, 150),
    'logo.png': (400, 150),
    'servico-bancario.jpg': (800, 600),
    'servico-empresas.jpg': (800, 600),
    'servico-imobiliario.jpg': (800, 600),
    'servico-leilao.jpg': (800, 600),
    'quem-somos.jpg': (1200, 800),
    'icone-agilidade.jpg': (128, 128),
    'icone-agilidade.png': (128, 128),
    'icone-especialista.jpg': (128, 128),
    'icone-especialista.png': (128, 128)
}

def resize_images():
    count = 0
    for filename, size in TARGETS.items():
        src_path = os.path.join(ROOT, filename)
        if not os.path.exists(src_path):
            continue
        
        try:
            with Image.open(src_path) as img:
                # Converter para RGB se for salvar como JPG e tiver transparencia (apenas prevencao)
                if filename.endswith('.jpg') and img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # ImageOps.fit redimensiona mantendo a proporcao cortando o excesso
                resized = ImageOps.fit(img, size, Image.Resampling.LANCZOS)
                
                dest_path = os.path.join(DEST_DIR, filename)
                resized.save(dest_path, quality=85)
                print(f"Resized {filename} to {size}")
                count += 1
        except Exception as e:
            print(f"Failed to process {filename}: {e}")
            
    print(f"Total processed: {count}")

if __name__ == '__main__':
    resize_images()
