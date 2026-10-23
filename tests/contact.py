"""Teste local: intercepta o POST; nenhum e-mail real é enviado."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page()
 sent=[]
 def intercept(route):
  sent.append(route.request)
  route.fulfill(status=200,content_type='text/html',body='<h1>Provedor simulado</h1>')
 page.route('https://formsubmit.co/**',intercept)
 page.goto('http://localhost:3000/contato/')
 form=page.locator('[data-form="contact"]')
 assert form.get_attribute('action')=='https://formsubmit.co/entrenos.contato13@gmail.com'
 assert form.get_attribute('method').lower()=='post'
 form.locator('button').click();assert not sent
 form.locator('[name="name"]').fill('Teste local')
 form.locator('[name="email"]').fill('teste@example.com')
 form.locator('[name="message"]').fill('Teste interceptado, sem envio real.')
 form.locator('button').click();assert not sent
 form.locator('[name="privacy_consent"]').check()
 form.locator('button').click()
 page.wait_for_selector('h1:text("Provedor simulado")')
 assert len(sent)==1 and sent[0].method=='POST'
 assert 'teste%40example.com' in sent[0].post_data
 assert 'privacy_consent' in sent[0].post_data
 assert '_captcha=false' not in sent[0].post_data
 b.close()
print('OK: destino, POST, validação e consentimento; envio interceptado, sem mensagem real.')
