"""Execute com build SITE_URL configurado e servidor local em subdiretório.
Exemplo: PORTAL_TEST_URL=http://localhost:3001/Hello-World-/ python3 tests/production.py
Não faz requisições nem envia formulários a serviços de terceiros.
"""
import json
import os
from urllib.parse import urljoin, urlsplit
from playwright.sync_api import sync_playwright
base = os.environ.get('PORTAL_TEST_URL', 'http://localhost:3001/Hello-World-/')
prefix = urlsplit(base).path.rstrip('/')
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'), headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.route('https://**/*', lambda route: route.abort())
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    assert page.goto(base).status == 200
    assert page.locator('link[rel="canonical"]').get_attribute('href') == 'https://butjana.github.io/Hello-World-/'
    page.locator('.menu-toggle').click()
    page.locator('#navigation').get_by_role('link', name='Conteúdos', exact=True).click()
    assert urlsplit(page.url).path == prefix + '/blog/'
    page.goto(urljoin(base, 'busca/?q=brincadeiras'))
    page.wait_for_selector('#search-results article')
    first = page.locator('#search-results h3 a').first
    assert urlsplit(first.get_attribute('href')).path.startswith(prefix + '/blog/')
    first.click()
    assert page.locator('.article-body').is_visible()
    json.loads(page.locator('script[type="application/ld+json"]').text_content())
    page.locator('.article-image').scroll_into_view_if_needed()
    page.wait_for_function('document.querySelector(".article-image").naturalWidth > 0')
    assert page.locator('.article-image').get_attribute('src') == prefix + '/assets/maternidade-ilustrativa.png'
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    for path in ('robots.txt', 'sitemap.xml', 'assets/search.json'):
        response = page.request.get(urljoin(base, path))
        assert response.status == 200, path
        if path == 'robots.txt':
            assert 'Disallow: /\n' not in response.text()
            assert 'Sitemap: https://butjana.github.io/Hello-World-/sitemap.xml' in response.text()
        if path == 'sitemap.xml':
            assert '<loc>https://butjana.github.io/Hello-World-/blog/' in response.text()
    assert not errors, errors
    browser.close()
print('OK: caminho de produção, menu móvel, busca e abertura de artigo, foto local de fallback, canonical, JSON-LD, robots e sitemap. Sem erros JavaScript.')
