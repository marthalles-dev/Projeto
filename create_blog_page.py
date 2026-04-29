import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
HOME_FILE = os.path.join(ROOT, 'index.html')
BLOG_DIR = os.path.join(ROOT, 'blog')
BLOG_FILE = os.path.join(BLOG_DIR, 'index.html')

def create_blog_page():
    os.makedirs(BLOG_DIR, exist_ok=True)
    
    with open(HOME_FILE, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    # Extrair parte superior do HTML ate o fim do header
    header_end = html.find('</header>') + len('</header>')
    if header_end < len('</header>'):
        print("Header não encontrado.")
        return
        
    head_part = html[:header_end]
    
    # Substituir os caminhos do cabeçalho para subir um nível (../)
    # Mas como o header já tem URLs complexas, vamos apenas colocar a tag base para facilitar
    # ou podemos fazer um replace simples
    head_part = head_part.replace('href="wp-content/', 'href="../wp-content/')
    head_part = head_part.replace('src="wp-content/', 'src="../wp-content/')
    head_part = head_part.replace('src="logo.jpg"', 'src="../logo.jpg"')
    head_part = head_part.replace('href="index.html"', 'href="../index.html"')
    head_part = head_part.replace('href="quem-somos/index.html"', 'href="../quem-somos/index.html"')
    head_part = head_part.replace('href="contato/index.html"', 'href="../contato/index.html"')
    head_part = head_part.replace('href="blog/index.html"', 'href="index.html"')
    
    # Adicionar o conteudo do Blog
    blog_content = """
    <main style="padding: 150px 20px 50px 20px; max-width: 1200px; margin: 0 auto; min-height: 60vh;">
        <h1 style="color: #0c4da2; text-align: center; margin-bottom: 40px; font-family: Inter, sans-serif;">Notícias e Artigos</h1>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 30px;">
            <!-- Post Card -->
            <article style="border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); font-family: Inter, sans-serif;">
                <div style="padding: 20px;">
                    <h3 style="font-size: 1.25rem; color: #333; margin-top: 0; line-height: 1.4;">STJ Veta Penhora de Imóvel com Alienação Fiduciária para Quitar Dívida de Condomínio</h3>
                    <p style="color: #666; font-size: 0.95rem; line-height: 1.5; margin-bottom: 20px;">Entenda a decisão do Superior Tribunal de Justiça sobre a proteção de imóveis financiados contra dívidas de condomínio.</p>
                    <a href="../stj-veta-penhora-de-imovel-com-alienacao-fiduciaria-para-quitar-divida-de-condominio/index.html" style="display: inline-block; padding: 10px 20px; background: #0c4da2; color: white; text-decoration: none; border-radius: 4px; font-weight: 500;">Ler Artigo Completo</a>
                </div>
            </article>
            
            <!-- Você pode adicionar mais <article> aqui quando tiver novos posts -->
        </div>
    </main>
    """
    
    # Extrair footer (vamos procurar onde começam os widgets de footer do elementor, ou apenas pegar o final do arquivo)
    footer_start = html.find('<footer')
    if footer_start == -1:
        # Se nao achar a tag footer, pegaremos a ultima section
        footer_start = html.rfind('<section')
        
    footer_part = html[footer_start:]
    footer_part = footer_part.replace('href="wp-content/', 'href="../wp-content/')
    footer_part = footer_part.replace('src="wp-content/', 'src="../wp-content/')
    footer_part = footer_part.replace('src="logo.jpg"', 'src="../logo.jpg"')
    
    final_html = head_part + blog_content + footer_part
    
    with open(BLOG_FILE, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"Página de Blog criada em: {BLOG_FILE}")

if __name__ == '__main__':
    create_blog_page()
