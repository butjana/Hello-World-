from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=__import__('os').environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':1000})
 errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
 page.goto('http://localhost:3000/',wait_until='domcontentloaded')
 page.screenshot(path='/tmp/entre-nos-desktop.png',full_page=True)
 assert page.locator('h1').inner_text()=='Mãe.\nMulher.\nInteira.'
 page.goto('http://localhost:3000/busca/?q=brincadeiras');page.wait_for_selector('#search-results article');assert page.locator('#search-results article').count()>0
 page.locator('#search-input').fill('zzzinexistente');page.locator('#search-form button').click();assert page.locator('#search-results article').count()==0
 page.goto('http://localhost:3000/');form=page.locator('[data-form="newsletter"]');form.locator('[name="name"]').fill('Teste');form.locator('[name="email"]').fill('teste@example.com');form.locator('[type="checkbox"]').check();form.locator('button').click();assert 'não foi realizada' in form.locator('[role="status"]').inner_text()
 page.goto('http://localhost:3000/achadinhos/');page.locator('[data-offer]').first.click();assert 'não há oferta' in page.locator('.product-status').first.inner_text()
 page.goto('http://localhost:3000/contato/');form=page.locator('[data-form="contact"]');form.locator('[name="name"]').fill('Teste');form.locator('[name="email"]').fill('teste@example.com');form.locator('textarea').fill('Mensagem de teste');form.locator('[type="checkbox"]').check();form.locator('button').click();assert 'não foi enviada' in form.locator('[role="status"]').inner_text()
 page.set_viewport_size({'width':390,'height':844});page.goto('http://localhost:3000/');page.locator('.menu-toggle').click();assert page.locator('#navigation').is_visible();page.keyboard.press('Escape');assert not page.locator('#navigation').is_visible()
 for path in ['/','/blog/','/categorias/','/achadinhos/','/contato/','/blog/pequenas-mudancas-na-rotina-aos-3-anos/']:
  page.goto('http://localhost:3000'+path,wait_until='domcontentloaded');assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),path
 page.goto('http://localhost:3000/');page.screenshot(path='/tmp/entre-nos-mobile.png',full_page=True)
 assert not errors, errors
 print('OK: navegador Chromium; busca com e sem resultados; newsletter; contato; aviso de oferta; menu móvel e Escape; 6 rotas sem overflow em 390px; sem erros JavaScript.')
 b.close()
