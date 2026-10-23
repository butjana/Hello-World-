from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, os
PREFIX=urlsplit(os.environ.get("SITE_URL", "")).path.rstrip("/")
from xml.etree import ElementTree
ROOT=Path(__file__).resolve().parent.parent/'dist'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.h1=0;self.links=[];self.ids=[];self.schema=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if 'id' in a:self.ids.append(a['id'])
  if tag in ('a','link') and 'href' in a:self.links.append(a['href'])
  if tag=='img':assert a.get('alt'), 'Imagem sem descrição'
  if tag=='script' and a.get('type')=='application/ld+json':self.schema=True
pages=list(ROOT.rglob('*.html'))
for file in pages:
 p=Page();p.feed(file.read_text());assert p.h1==1,(file,p.h1)
 assert len(p.ids)==len(set(p.ids)),f'IDs duplicados em {file}'
 assert p.schema,file
 for link in p.links:
  parts=urlsplit(link)
  if parts.scheme or parts.netloc:continue
  if not parts.path:
   if parts.fragment:assert unquote(parts.fragment) in p.ids,(file,link)
   continue
  local=parts.path
  if PREFIX and (local==PREFIX or local.startswith(PREFIX+'/')):local=local[len(PREFIX):] or '/'
  target=ROOT/local.lstrip('/')
  if parts.path.endswith('/'):target/='index.html'
  assert target.is_file(),(file,link)
  if parts.fragment:
   dest=Page();dest.feed(target.read_text());assert unquote(parts.fragment) in dest.ids,(file,link)
posts=json.loads((ROOT/'assets/search.json').read_text())
assert len(posts)==7
assert len({p['slug'] for p in posts})==7
ElementTree.parse(ROOT/'sitemap.xml')
print(f'OK: {len(pages)} páginas, H1 único, imagens com alt, JSON-LD presente, IDs e links locais válidos; 7 artigos no índice de busca; sitemap XML válido.')

from content import POSTS
manifest=json.loads((ROOT.parent/'data/affiliate-products.json').read_text())['products']
achadinhos=(ROOT/'achadinhos/index.html').read_text()
assert len(manifest)==5
for item in manifest:
 assert achadinhos.count('href="'+item['affiliate_url']+'"')==1
assert achadinhos.count('rel="sponsored noopener noreferrer"')==5
print('OK: cinco links afiliados preservados exatamente, identificados e sem associação aos produtos demonstrativos.')
