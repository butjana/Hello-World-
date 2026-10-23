# Entre Nós — maternidade e vida real

Portal editorial responsivo em português. HTML estático com gerador Python, CSS próprio e JavaScript progressivo. Não exige instalação de dependências.

## Desenvolvimento

Requisitos: Python 3.10+ e, opcionalmente, npm para atalhos.

```sh
npm run build
npm test
npm start
```

Sem npm: `python3 scripts/build.py`, `python3 scripts/check.py` e `python3 -m http.server 3000 --directory dist`.

`dist/` é gerado e pode ser hospedado em qualquer serviço de arquivos estáticos. Configure o serviço para usar `404.html` em rotas inexistentes. As páginas são diretórios com `index.html`; não é necessário fallback de SPA.

## Organização

- `scripts/content.py`: artigos, categorias e produtos demonstrativos.
- `scripts/build.py`: componentes e geração de páginas, metadados, JSON-LD, sitemap e robots.
- `assets/style.css`: identidade visual, layout mobile-first e acessibilidade.
- `assets/app.js`: menu acessível, busca local, compartilhamento e formulários demonstrativos.
- `scripts/check.py`: verificação estrutural de todas as páginas e links locais.

## Publicação e SEO

Defina `SITE_URL` com o domínio HTTPS real no ambiente e execute novamente `npm run build`. Essa configuração gera canonical, URLs absolutas no sitemap e a referência no robots.txt. Sem domínio real, robots.txt bloqueia indexação para evitar indexar a demonstração e o sitemap permanece vazio. Nenhum domínio fictício é publicado.

Cadastre o domínio no Search Console pelo DNS ou acrescente a meta tag de verificação no template `page()`. Envie `/sitemap.xml` após publicar. Para Analytics, integre o identificador real somente após definir a política de privacidade e o gerenciamento de consentimento aplicável; não há rastreamento instalado.

## Integrações pendentes

- **Contato:** POST nativo para FormSubmit, destino entrenos.contato13@gmail.com, sem chaves no navegador. A primeira submissão requer ativação pelo destinatário no e-mail enviado pelo provedor. Até confirmar essa etapa, entrega real não foi validada. CAPTCHA padrão mantido, honeypot e consentimento obrigatório. `python3 tests/contact.py` intercepta o POST sem enviar e-mail real.
- **Newsletter:** ainda demonstrativa, sem envio ou persistência. Exige conta e formulário de um provedor de newsletter com confirmação, descadastro e política de tratamento. Não confundir formulário de contato com cadastro para marketing.
- **Afiliados:** cinco links fornecidos pela proprietária em `data/affiliate-products.json`. Ativos com rótulos neutros e `rel="sponsored noopener noreferrer"`, sem fotos ou alegações sobre os produtos. Os destinos não puderam ser verificados pelo ambiente. Complete nomes, imagens autorizadas e características somente após identificar cada anúncio. Preserve o aviso de comissão.
- **Autoria e redes:** substitua a apresentação demonstrativa por biografia aprovada e adicione perfis reais; não existem links sociais fictícios.
- **Documentos legais:** minutas demonstrativas, que devem refletir a responsável, fornecedores e tratamento efetivo antes de coletar dados.
- **Fotos:** imagens externas de `images.unsplash.com` precisam de acesso de rede. Não representam a criadora ou sua família. Substitua por imagens próprias/autorizadas antes de publicar a versão final e confirme as condições de uso. Foto local gerada, quando presente, é identificada como ilustrativa.

## Validação

`npm test` verifica H1 único, descrições das imagens, dados estruturados presentes, IDs únicos, links e âncoras locais, artigos do índice de busca e XML do sitemap. Testes de navegador foram realizados com Chromium em desktop e viewport de 390 px: busca com/sem resultados, menu móvel, Escape, formulários e aviso de ofertas. Essa verificação não substitui testes de integrações reais após conectá-las.

## Publicação no GitHub Pages

O workflow `.github/workflows/publish.yml` gera, verifica e publica o portal a cada envio para `master`. Em GitHub → repositório → Settings → Pages, selecione **GitHub Actions** como Source. A URL efetiva é fornecida pela ação `configure-pages`; links e assets são ajustados automaticamente para subdiretórios, inclusive o endereço gratuito do repositório. Não é necessário comprar domínio para começar.

No primeiro uso, habilite Pages e execute novamente o workflow **Publicar Entre Nós**, se a primeira execução tiver ocorrido antes da habilitação. A publicação só está confirmada quando a execução termina com sucesso e o endereço responde.

Para reproduzir os testes de navegador, com o servidor ligado e Playwright instalado no ambiente de teste: `python3 tests/browser.py`. A variável `CHROMIUM_PATH` permite selecionar o executável Chromium disponível.
