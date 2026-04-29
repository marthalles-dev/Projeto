# 📚 Manual de Gestão do Site - IA Advocacia Empresarial

Este documento contém as instruções necessárias para você gerenciar seu site, fazer novas postagens no blog e alterar configurações básicas de forma autônoma, garantindo a performance e padronização que implementamos.

---

## 📝 1. Como Publicar Novas Notícias no Blog

Você tem um sistema de blog fácil de manter e que não depende do Elementor. Toda a formatação profissional que criamos se aplicará automaticamente se você seguir estes passos:

### Passo A: Criar a Página da Notícia
1. Vá até a pasta `Projeto`.
2. Escolha uma pasta de uma notícia já existente (ex: `stj-veta-penhora-de-imovel-com-alienacao-fiduciaria...`).
3. **Copie e cole** essa pasta.
4. **Renomeie a cópia** com o nome da sua nova notícia usando apenas letras minúsculas e hifens (ex: `como-evitar-leilao-de-imovel`).
5. Abra a nova pasta, clique com o botão direito no arquivo `index.html` e abra-o com um editor de texto (pode ser o Bloco de Notas ou VS Code).
6. Altere os textos (Títulos `<h1>`, Parágrafos `<p>`) para o conteúdo da sua nova matéria. Salve e feche.

### Passo B: Adicionar a Notícia na Vitrine (Página do Blog)
Para que sua notícia apareça na lista de postagens para os usuários clicarem:
1. Volte na pasta `Projeto` e abra a pasta `blog`.
2. Edite o arquivo `index.html` com o Bloco de Notas.
3. Procure o código que se parece com este:
   ```html
   <article style="...">
       ...
   </article>
   ```
4. **Copie** esse bloco inteiro `<article> ... </article>` e cole logo abaixo dele (criando um novo cartão).
5. No bloco que você colou, altere:
   - O título `<h3>`
   - O resumo `<p>`
   - O link `<a href="...">` para apontar para a pasta da sua nova notícia (ex: `../como-evitar-leilao-de-imovel/index.html`).
6. Salve o arquivo.

---

## 🖼️ 2. Como Alterar a Imagem de Fundo (Hero Background)
Se futuramente você quiser trocar a imagem do banner principal:
1. Escolha uma imagem de alta qualidade (preferencialmente formato retangular / paisagem).
2. Redimensione-a para o tamanho ideal de tela cheia: **1920x1080 pixels**. (Use sites como *ImageResizer* ou o *Paint*).
3. Salve a imagem com o nome **EXATO** de `hero-bg.jpg`.
4. Substitua o arquivo `hero-bg.jpg` existente na raiz da sua pasta `Projeto`.
5. Faça o upload das alterações via Git. (A camada escura por cima da imagem será aplicada automaticamente via CSS).

---

## ✨ 3. Como Alterar a Logo
O sistema do site foi configurado para puxar um único arquivo raiz para a Logo, para não ter conflito.
1. Salve sua nova logo com o nome exato de `logo.jpg`.
2. Para melhor performance, tente manter um tamanho aproximado de `800x450` ou similar (não use imagens de 3000px, isso deixa o site lento).
3. Substitua o arquivo `logo.jpg` na raiz da pasta `Projeto`.
4. *Atenção:* O Favicon (aquele ícone que fica na aba do navegador) fica armazenado em `wp-content/uploads/2021/11/fav-300x300.png`. Se quiser trocar o ícone da aba, basta substituir esse arquivo mantendo o mesmo nome e extensão `.png`.

---

## 🚀 4. Como Enviar as Atualizações para o Ar (Deploy)
Sempre que você fizer qualquer alteração (seja adicionar um novo blog post, ou trocar uma imagem):
1. Abra o **Terminal** ou **Git Bash** na pasta `Projeto`.
2. Digite: `git add .` (e aperte Enter)
3. Digite: `git commit -m "Adicionando nova postagem no blog"` (e aperte Enter)
4. Digite: `git push` (e aperte Enter)
5. Aguarde alguns minutos. A plataforma Easypanel/Hostinger irá puxar os novos arquivos automaticamente.

*Dica: Se a alteração não aparecer logo de cara, tente abrir o site em uma aba anônima (Ctrl+Shift+N), pois navegadores costumam fazer "cache" (salvar versões antigas) das imagens e estilos.*
