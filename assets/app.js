'use strict';
const menu = document.querySelector('.menu-toggle');
menu?.addEventListener('click', () => {
 const expanded = menu.getAttribute('aria-expanded') === 'true';
 menu.setAttribute('aria-expanded', String(!expanded));
 document.querySelector('#navigation').classList.toggle('open', !expanded);
});
document.addEventListener('keydown', event => {
 if(event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
  menu.setAttribute('aria-expanded','false');document.querySelector('#navigation').classList.remove('open');menu.focus();
 }
});
document.querySelectorAll('[data-form]').forEach(form => form.addEventListener('submit', event => {
 if(form.dataset.form === 'contact' && form.hasAttribute('action')) return;
 event.preventDefault();
 if(!form.reportValidity()) return;
 const status = form.querySelector('.form-status');
 status.textContent = form.dataset.form === 'newsletter'
 ? 'Obrigada pelo interesse! Demonstração validada. Sua inscrição ainda não foi realizada: o serviço de e-mail precisa ser conectado. Nenhum dado foi enviado ou salvo.'
 : 'Mensagem validada nesta demonstração. Ela ainda não foi enviada: o serviço de contato precisa ser conectado. Nenhum dado foi enviado ou salvo.';
}));
document.querySelectorAll('[data-offer]').forEach(button => button.addEventListener('click', () => {
 button.nextElementSibling.textContent = 'Ainda não há oferta ou link de afiliado configurado para este item. A imagem é ilustrativa.';
}));
document.querySelector('[data-share]')?.addEventListener('click', async () => {
 const status=document.querySelector('#share-status');
 try {
  if(navigator.share) {await navigator.share({title:document.title,url:location.href});status.textContent='Leitura compartilhada.';}
  else if(navigator.clipboard && window.isSecureContext) {await navigator.clipboard.writeText(location.href);status.textContent='Link copiado. Agora é só compartilhar.';}
  else {status.textContent='Copie o endereço desta leitura: '+location.href;}
 } catch(error) {if(error.name !== 'AbortError') status.textContent='Você pode compartilhar copiando o endereço: '+location.href;}
});
const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('pt-BR');
const searchForm = document.querySelector('#search-form');
if(searchForm) {
 const input=document.querySelector('#search-input'),results=document.querySelector('#search-results'),count=document.querySelector('#search-count');
 let posts=[];
 function render() {
  const query=input.value.trim();
  const terms=normalize(query).split(/\s+/).filter(Boolean);
  const matches=posts.filter(post=>terms.every(term=>normalize([post.title,post.excerpt,post.categoryName,...post.tags].join(' ')).includes(term)));
  results.replaceChildren();
  count.textContent=matches.length ? `${matches.length} ${matches.length===1?'leitura encontrada':'leituras encontradas'}${query?' para “'+query+'”':''}.` : 'Nenhuma leitura encontrada. Experimente outra palavra, como rotina ou brincar.';
  for(const post of matches) {
   const article=document.createElement('article');article.className='post-card';
   const pictureLink=document.createElement('a');pictureLink.href='/blog/'+post.slug+'/';pictureLink.className='image-link';
   const image=document.createElement('img');image.src=post.imageUrl;image.alt=post.title;image.loading='lazy';image.width=1000;image.height=800;image.addEventListener('error',()=>{image.src='/assets/maternidade-ilustrativa.png';image.alt='Imagem ilustrativa gerada por IA, sem relação com a família da criadora';},{once:true});pictureLink.append(image);
   const eyebrow=document.createElement('div');eyebrow.className='eyebrow';eyebrow.textContent=post.categoryName+' · '+post.minutes+' min de leitura';
   const title=document.createElement('h3'),link=document.createElement('a');link.href=pictureLink.href;link.textContent=post.title;title.append(link);
   const description=document.createElement('p');description.textContent=post.excerpt;article.append(pictureLink,eyebrow,title,description);results.append(article);
  }
 }
 input.value=new URLSearchParams(location.search).get('q')?.slice(0,150)||'';
 searchForm.addEventListener('submit',event=>{event.preventDefault();const url=new URL(location.href);input.value.trim()?url.searchParams.set('q',input.value.trim()):url.searchParams.delete('q');history.replaceState({},'',url);render();});
 fetch('/assets/search.json').then(response=>{if(!response.ok)throw Error('search');return response.json();}).then(data=>{posts=data;render();}).catch(()=>{count.textContent='Não foi possível carregar a busca. Você pode explorar todos os conteúdos no menu.';});
}
// Analytics e Search Console: sem identificadores inventados ou rastreamento ativo.
// Veja README.md para integração futura e consentimento.
// Mantém uma apresentação íntegra se o provedor externo estiver indisponível.
document.querySelectorAll('img[data-fallback]').forEach(image => {
 const fallback = () => {
  const path = image.dataset.fallback;
  if(path && !image.src.endsWith(path)) {
   image.src = path;
   image.alt = path.includes('produto') ? 'Ilustração de curadoria em preparação; produto ainda não selecionado' : 'Fotografia ilustrativa gerada por IA de uma mulher e uma criança brincando; não representa a criadora';
  }
 };
 image.addEventListener('error', fallback, {once:true});
 if(image.complete && !image.naturalWidth) fallback();
});
