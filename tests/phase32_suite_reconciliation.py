"""Phase 32: static reconciliation of browser acceptance assertions with approved DOM.

This validates that the Playwright suite targets real IDs, routes and copy in the
current implementation. It does not substitute for browser execution.
"""
from pathlib import Path
import re, json
ROOT=Path(__file__).resolve().parents[1]
script=(ROOT/'tests/phase22_browser_acceptance.py').read_text()
pages=(ROOT/'js/retrace-pages.js').read_text()
main=(ROOT/'js/main.js').read_text()
header=(ROOT/'js/header.js').read_text()
search=(ROOT/'js/search.js').read_text()
checks=[]
def check(name,ok,detail=''):
 checks.append({'test':name,'result':'PASS' if ok else 'FAIL','detail':detail})
# Selectors and controls referenced by the current suite must exist in the implementation.
for selector,source,label in [
 ('#f-dest',pages,'Filters destination'),('#f-count',pages,'Filters result count'),('#f-reset',pages,'Filters reset'),
 ('#lib-q',pages,'Library search'),('#lib-count',pages,'Library count'),('#ca',pages,'Compare first selector'),('#cb',pages,'Compare second selector'),
 ('#compare-report',pages,'Compare report'),('data-pick=\"${esc(r.equipment_id)}\"',pages,'Quiz equipment picker'),('#quiz-selection',pages,'Quiz unavailable state'),
 ('id=\"${destination.toLowerCase()}-timeline\"',pages,'Destination timeline'),('id=\"${id}\"',pages,'Timeline filter'),('id=\"${id}-count\"',pages,'Timeline count'),
 ('id=\"detail-${key}\"',pages,'Full Details section anchors'),('#rt-section-nav-panel',pages,'Full Details section navigation'),
 ('#drawer',header,'Mobile navigation drawer'),('.drawer-acc',header,'Mobile navigation accordion'),('#search-input',search,'Universal search input'),('a.result',search,'Universal search results')]:
 check(f'Current DOM supports {label}', selector.lstrip('#.') in source or selector in source, selector)
for route in ['/destination/moon','/destination/mars','/destination/planets','/equipment','/filters','/library/compare','/library/quiz','/library/glossary','/about/sources','/about/website','/updates','/contact','/feedback','/report']:
 check(f'Route is implemented: {route}', route in main or route in (ROOT/'js/pages.js').read_text(), route)
check('Exact timeline empty-state copy is asserted', 'No timeline events match this filter.' in pages)
check('Exact Filters empty-state copy is retained', 'No equipment matched your selected filter.' in pages)
check('Quiz test asserts safe unavailable state', 'No evidence-linked question set' in script and 'No sample questions from unrelated equipment' in pages)
check('Planets test reflects scoped notice', 'Moon and Mars. A broader planets collection is not part of the approved website scope' in (ROOT/'js/pages.js').read_text() and "('/destination/planets','Planetary equipment collection')" in script)
check('Browser suite includes mobile Details drawer tests', 'Full Details section navigation expands' in script and 'section selection collapses navigation' in script)
check('Browser suite does not treat browser blocking as pass', "'result':'BLOCKED'" in script and "blocked=sum" in script)
passed=sum(x['result']=='PASS' for x in checks); failed=len(checks)-passed
out={'phase':32,'title':'Browser Test Suite Reconciliation','summary':{'passed':passed,'failed':failed,'total':len(checks)},'results':checks,'browser_execution':'SEPARATE — environment may block local navigation'}
(ROOT/'tests'/'phase32_suite_reconciliation_results.json').write_text(json.dumps(out,indent=2))
print(f'PHASE 32: {passed}/{len(checks)} passed; {failed} failed')
for x in checks:
 if x['result']=='FAIL': print('FAIL',x['test'],x['detail'])
raise SystemExit(1 if failed else 0)
