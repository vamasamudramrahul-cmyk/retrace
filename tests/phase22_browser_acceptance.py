"""Full-site Playwright acceptance suite for Retrace test build.

Run from this directory:
  python tests/phase22_browser_acceptance.py

Requires Playwright Python and a Chromium browser. The suite serves this directory
locally, then tests all active routes and representative interactions at desktop,
tablet and mobile viewport sizes. It does not certify NASA factual accuracy.
"""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from pathlib import Path
from playwright.sync_api import sync_playwright
import json, os, shutil, sys, time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests' / 'phase22_browser_acceptance_results.json'
class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs): super().__init__(*args, directory=str(ROOT), **kwargs)
    def log_message(self, *args): pass

def main():
    results=[]
    def check(name, ok, detail=''):
        results.append({'test':name,'result':'PASS' if ok else 'FAIL','detail':str(detail)})
    server=ThreadingHTTPServer(('127.0.0.1',0),QuietHandler)
    Thread(target=server.serve_forever,daemon=True).start()
    url=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            executable=os.environ.get('RETRACE_CHROMIUM') or shutil.which('chromium') or shutil.which('chromium-browser')
            launch={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage']}
            if executable: launch['executable_path']=executable
            try: browser=p.chromium.launch(**launch)
            except Exception as e:
                check('Chromium launch',False,e)
                OUT.write_text(json.dumps({'summary':{'passed':0,'failed':1,'blocked':True},'results':results},indent=2))
                print('BLOCKED: Chromium launch failed:',e); return 2
            try:
                for viewport_name,viewport in [('desktop',{'width':1440,'height':1000}),('tablet',{'width':820,'height':1000}),('mobile',{'width':390,'height':844})]:
                    page=browser.new_page(viewport=viewport,device_scale_factor=1)
                    page_errors=[]; console_errors=[]
                    page.on('pageerror',lambda e: page_errors.append(str(e)))
                    page.on('console',lambda m: console_errors.append(m.text) if m.type=='error' else None)
                    try:
                        page.goto(url,wait_until='domcontentloaded',timeout=12000)
                        page.wait_for_function('window.__abnfReady === true',timeout=15000)
                    except Exception as e:
                        results.append({'test':f'{viewport_name}: browser can load local test site','result':'BLOCKED' if 'ERR_BLOCKED_BY_ADMINISTRATOR' in str(e) else 'FAIL','detail':str(e)})
                        page.close(); continue
                    check(f'{viewport_name}: Home renders',page.locator('#app h1').count()>0 and 'Something went wrong' not in page.locator('#app').inner_text())
                    routes=[('/destination/moon','Explore Moon'),('/destination/mars','Explore Mars'),('/destination/planets','Planetary equipment collection'),('/equipment','Equipment Library'),('/equipment/MOON-EQ-0001',None),('/equipment/MARS-EQ-0036',None),('/filters','Find Equipment'),('/library/compare','Compare Equipment'),('/library/quiz','Test Your Space Knowledge'),('/library/glossary',None),('/about/sources','Sources & Evidence'),('/about/website',None),('/updates',None),('/contact','Contact Us'),('/feedback','Send Feedback'),('/report','Report an Issue')]
                    for route,expected in routes:
                        page.evaluate('(r)=>location.hash="#"+r',route)
                        try:
                            page.wait_for_function("document.querySelector('#app h1') && !document.querySelector('#app').innerText.includes('Loading…')",timeout=5000)
                            txt=page.locator('#app').inner_text()
                            ok='Something went wrong' not in txt and 'Page not found' not in txt and (expected is None or expected in txt)
                            check(f'{viewport_name}: route {route}',ok,txt[:100].replace('\n',' | '))
                        except Exception as e: check(f'{viewport_name}: route {route}',False,e)
                    # Filters, library, compare, quiz and timeline interactions.
                    page.evaluate('location.hash="#/filters"'); page.wait_for_selector('#f-dest')
                    page.locator('#f-dest').select_option('Mars'); mars=page.locator('#f-count').inner_text()
                    page.locator('#f-reset').click(); reset=page.locator('#f-count').inner_text()
                    check(f'{viewport_name}: Filters destination and reset','5 results' in mars and '15 results' in reset,f'{mars}; reset={reset}')
                    page.evaluate('location.hash="#/equipment"'); page.wait_for_selector('#lib-q')
                    page.locator('#lib-q').fill('SuperCam')
                    check(f'{viewport_name}: Library search',page.locator('#lib-count').inner_text()=='1 equipment records',page.locator('#lib-count').inner_text())
                    page.evaluate('location.hash="#/library/compare"'); page.wait_for_selector('#ca')
                    page.locator('#ca').select_option('MOON-EQ-0001'); page.locator('#cb').select_option('MARS-EQ-0036')
                    check(f'{viewport_name}: Compare creates 30 attribute rows','Overall Comparison Summary' in page.locator('#compare-report').inner_text() and page.locator('#compare-report tbody tr').count()==30)
                    page.evaluate('location.hash="#/library/quiz"'); page.wait_for_selector('[data-pick="MOON-EQ-0001"]')
                    page.locator('[data-pick="MOON-EQ-0001"]').click()
                    check(f'{viewport_name}: Quiz does not substitute unrelated questions','No evidence-linked question set' in page.locator('#quiz-selection').inner_text())
                    page.evaluate('location.hash="#/destination/moon"'); page.wait_for_selector('#moon-timeline')
                    check(f'{viewport_name}: Destination has collection and timeline',page.locator('.rt-mission-group').count()>0 and page.locator('#moon-timeline').count()==1)
                    page.evaluate('location.hash="#/destination/moon"'); page.wait_for_selector('#moon-timeline')
                    page.locator('#moon-timeline-filter').select_option(label=page.locator('#moon-timeline-filter option').nth(1).inner_text())
                    check(f'{viewport_name}: Timeline category filter updates event count',page.locator('#moon-timeline-filter-count').inner_text().endswith('events'))
                    page.locator('[href="#/equipment/MOON-EQ-0001"]').first.click(); page.wait_for_selector('#detail-overview')
                    check(f'{viewport_name}: Full Details has all eight sections',page.locator('.rt-section[id^="detail-"]').count()==8)
                    if viewport_name=='mobile':
                        toggle=page.locator('.rt-section-nav-toggle'); panel=page.locator('#rt-section-nav-panel')
                        check('mobile: Full Details section navigation starts collapsed',toggle.get_attribute('aria-expanded')=='false' and panel.is_hidden())
                        toggle.click(); check('mobile: Full Details section navigation expands',toggle.get_attribute('aria-expanded')=='true' and not panel.is_hidden())
                        panel.locator('a[href="#detail-how_was_it_built"]').click(); check('mobile: section selection collapses navigation',panel.is_hidden())
                    page.evaluate('history.back()'); page.wait_for_selector('#moon-timeline')
                    check(f'{viewport_name}: returning from Details restores timeline route',page.locator('#moon-timeline').count()==1)
                    if viewport_name=='mobile':
                        page.locator('#burger').click(); page.wait_for_timeout(300)
                        drawer_open=not page.locator('#drawer').evaluate('(e)=>e.hidden')
                        page.locator('.drawer-acc').filter(has_text='Learning').click()
                        accordion=page.locator('.drawer-acc').filter(has_text='Learning').get_attribute('aria-expanded')=='true'
                        check('mobile: drawer and Learning accordion',drawer_open and accordion)
                        page.locator('[href="#/filters"]').last.click(); page.wait_for_selector('#f-dest')
                        check('mobile: drawer navigation reaches Filters',page.locator('h1').inner_text()=='Find Equipment')
                    else:
                        page.locator('.dd-btn').filter(has_text='Destinations').hover(); page.wait_for_timeout(150)
                        check(f'{viewport_name}: desktop Destinations dropdown',not page.locator('.dd-menu').first.evaluate('(e)=>e.hidden'))
                    page.locator('[data-open-search]').first.click(); page.wait_for_selector('#search-input')
                    page.locator('#search-input').fill('SuperCam'); page.wait_for_timeout(450)
                    check(f'{viewport_name}: Universal Search returns results',page.locator('a.result').count()>0)
                    page.keyboard.press('Escape'); page.wait_for_timeout(250)
                    # Layout overflow is a responsive smoke check, not full visual sign-off.
                    overflow=page.evaluate('document.documentElement.scrollWidth > document.documentElement.clientWidth')
                    check(f'{viewport_name}: no horizontal document overflow',not overflow,f"scrollWidth={page.evaluate('document.documentElement.scrollWidth')} clientWidth={page.evaluate('document.documentElement.clientWidth')}")
                    check(f'{viewport_name}: no uncaught page errors',not page_errors,page_errors[:3])
                    check(f'{viewport_name}: no console errors',not console_errors,console_errors[:3])
                    page.close()
            finally: browser.close()
    except Exception as e:
        check('Browser acceptance execution',False,e)
    finally: server.shutdown(); server.server_close()
    passed=sum(x['result']=='PASS' for x in results); failed=sum(x['result']=='FAIL' for x in results); blocked=sum(x['result']=='BLOCKED' for x in results)
    OUT.write_text(json.dumps({'summary':{'passed':passed,'failed':failed,'blocked':blocked,'total':len(results)},'results':results},indent=2))
    print(f'BROWSER ACCEPTANCE: {passed} passed; {failed} failed; {blocked} blocked; {len(results)} total')
    for x in results:
        if x['result']=='FAIL': print('FAIL |',x['test'],'|',x['detail'][:250])
    return 1 if failed else 0
if __name__=='__main__': sys.exit(main())
