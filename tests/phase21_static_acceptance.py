"""Phase 21 static acceptance checks for the Retrace multi-screen test build.
These checks inspect route/data contracts only; they do not replace browser acceptance.
Run: python tests/phase21_static_acceptance.py
"""
from pathlib import Path
import json, re, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]
checks=[]
def check(name, ok, detail=''):
    checks.append((name, bool(ok), str(detail)))

main=(ROOT/'js/main.js').read_text()
header=(ROOT/'js/header.js').read_text()
content=(ROOT/'js/content.js').read_text()
pages=(ROOT/'js/retrace-pages.js').read_text()
adapter=(ROOT/'js/canonical-data.js').read_text()

# Exact route handlers for active screens and supporting forms.
routes={
 '/':'homeView()', '/destination/moon':"destinationPage('Moon')", '/destination/mars':"destinationPage('Mars')",
 '/equipment':'libraryPage()', '/filters':'filtersPage()', '/library/compare':'canonicalComparePage()',
 '/library/quiz':'canonicalQuizPage()', '/library/glossary':'glossaryPage()',
 '/about/sources':'canonicalEvidencePage()', '/about/website':'aboutWebsitePage()', '/updates':'updatesPage()',
 '/contact':"contactFormPage('contact')", '/feedback':"contactFormPage('feedback')", '/report':"contactFormPage('report')"
}
for route, handler in routes.items(): check(f'Route {route}', handler in main, handler)
check('Dynamic equipment details route', r"^\\/equipment\\/([^/]+)$" in main or "fullDetailsPage(decodeURIComponent(m[1]))" in main)
check('Header uses shared NAV config', 'NAV.map(desktopItem)' in header and 'NAV.map(drawerItem)' in header)
expected_nav=['Home','Destinations','Learning','Sources & Evidence','About']
nav_labels=re.findall(r"label:\s*'([^']+)'", content)
check('Approved top-level navigation labels', all(x in nav_labels for x in expected_nav), nav_labels)
footer_block=content.split('export const FOOTER_COLUMNS =',1)[1].split('// DRAFT short description',1)[0]
check('eLearning removed from footer configuration', 'eLearning' not in footer_block)

# Required renderer exports and content contracts.
for fn in ['destinationPage','libraryPage','filtersPage','fullDetailsPage','canonicalComparePage','canonicalEvidencePage','canonicalQuizPage','contactFormPage']:
    check(f'Renderer {fn}', f'function {fn}' in pages or f' {fn}(' in pages or f'export function {fn}' in pages)
for marker in ['Overview','Its Story','Why Is It There?','How Was It Built?','Discoveries and Contributions','Mission Timeline','Current Status and Location','Images and Media']:
    check(f'Full Details section: {marker}', marker in pages)
check('Compare has two initially empty selectors', 'id=\"ca\"' in pages and 'id=\"cb\"' in pages and pages.count('<option value=\"\">Select equipment</option>') >= 2)
check('Quiz avoids unrelated sample question fallback', 'No evidence-linked question set is currently available' in pages)
check('Timeline preserves unclassified ownership', 'UNCLASSIFIED' in pages and 'Ownership:' in pages)
check('Timeline preserves neutral status explanation', 'Event status not classified' in pages)
check('Canonical adapter loads all 9 data files', all(x in adapter for x in ['equipment.json','missions.json','claims.json','sources.json','events.json','library.json','filters-index.json','compare-index.json','timeline.json']))

# Dataset validation.
files=list(ROOT.rglob('*.json'))
json_errors=[]
for f in files:
    try: json.loads(f.read_text(encoding='utf-8'))
    except Exception as e: json_errors.append(f'{f.relative_to(ROOT)}: {e}')
check('All JSON files parse', not json_errors, f'{len(files)} files; {json_errors[:2]}')

def records(path): return json.loads((ROOT/path).read_text())['records']
eq=records('data/canonical/equipment.json')
ids=[r.get('equipment_id') for r in eq]
check('15 canonical equipment records', len(eq)==15, len(eq))
check('Canonical equipment IDs unique', len(ids)==len(set(ids)) and None not in ids)
check('id alias matches equipment_id', all(r.get('id')==r.get('equipment_id') for r in eq))
check('All records retain eight Full Details sections', all(all(k in r.get('details',{}) for k in ['overview','its_story','why_is_it_there','how_was_it_built','discoveries_and_contributions','mission_timeline','current_status_and_location','images_and_media']) for r in eq))
check('All publication states remain Draft', all(r.get('publication_state')=='Draft' for r in eq))
claims=records('data/canonical/claims.json'); sources=records('data/canonical/sources.json')
claim_ids={c.get('claim_id') for c in claims}; source_ids={s.get('source_id') for s in sources}
check('Claim records exist', len(claims)>0, len(claims))
check('Source records exist', len(sources)>0, len(sources))
events=records('data/canonical/events.json')
check('All timeline events retain source/claim arrays', all(isinstance(e.get('claim_ids'),list) and isinstance(e.get('source_ids'),list) for e in events))
check('Event claim references resolve', all(cid in claim_ids for e in events for cid in e.get('claim_ids',[])))
check('Event source references resolve', all(sid in source_ids for e in events for sid in e.get('source_ids',[])))

# Syntax checks.
js=list(ROOT.rglob('*.js')); failures=[]
for f in js:
    p=subprocess.run(['node','--check',str(f)],capture_output=True,text=True)
    if p.returncode: failures.append((str(f.relative_to(ROOT)),p.stderr.strip()))
check('All JavaScript modules pass node --check', not failures, f'{len(js)} files; {failures[:2]}')

for name, ok, detail in checks:
    print(('PASS' if ok else 'FAIL')+' | '+name+((' | '+detail) if detail else ''))
passed=sum(ok for _,ok,_ in checks)
print(f'\nSUMMARY: {passed}/{len(checks)} static checks passed')
print('NOTE: Browser, interaction, keyboard, touch, screenshot and responsive acceptance are not covered.')
if passed != len(checks): sys.exit(1)
