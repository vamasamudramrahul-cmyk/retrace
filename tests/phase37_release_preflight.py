"""Phase 37 release preflight checks; static only, not browser acceptance."""
from pathlib import Path
import json, re, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def ck(name, ok, detail=''):
    checks.append((name,bool(ok),str(detail)))
css=(ROOT/'css/styles.css').read_text()
ck('Dual-layer focus indicator uses white inner outline and navy outer ring', ':focus-visible{outline:3px solid #fff;outline-offset:2px;box-shadow:0 0 0 5px #000080' in css)
ck('Search input retains visible focus indicator', '#search-input:focus-visible{outline:3px solid #fff;outline-offset:2px;box-shadow:0 0 0 5px #000080' in css)
ck('Reduced motion preference retained', 'prefers-reduced-motion' in css)
ck('Responsive breakpoints retained', '@media' in css)
# Publication and evidence safety gates.
eq=json.loads((ROOT/'data/canonical/equipment.json').read_text())['records']
ck('All equipment remain Draft pending approval', len(eq)==15 and all(x.get('publication_state')=='Draft' for x in eq))
ck('Two unknown equipment statuses remain null', sum(x.get('equipment_status') is None for x in eq)==2 and all(x.get('equipment_status') is None for x in eq if x.get('equipment_id') in {'MARS-EQ-0039','MARS-EQ-0040'}))
quiz=(ROOT/'js/retrace-pages.js').read_text()
ck('Quiz remains unavailable without approved evidence-linked bank', 'No evidence-linked question set is currently available' in quiz)
compare=json.loads((ROOT/'data/projections/compare-index.json').read_text())
ck('Compare projection covers all equipment', len(compare.get('records',[]))==15)
reg=json.loads((ROOT/'data/projections/compare-mapping-registry.json').read_text())
ck('Compare registry retains 30 approved attributes', len(reg.get('attributes',[]))==30)
# Validate all JSON and JS syntax.
errs=[]
for f in ROOT.rglob('*.json'):
    try: json.loads(f.read_text())
    except Exception as e: errs.append(f'{f}: {e}')
ck('All JSON parses', not errs, errs[:2])
js=list(ROOT.rglob('*.js')); bad=[]
for f in js:
    p=subprocess.run(['node','--check',str(f)],capture_output=True,text=True)
    if p.returncode: bad.append((str(f.relative_to(ROOT)),p.stderr))
ck('All JavaScript passes syntax validation', not bad, bad[:2])
for n,o,d in checks: print(('PASS' if o else 'FAIL')+' | '+n+((' | '+d) if d else ''))
p=sum(o for _,o,_ in checks)
print(f'\nSUMMARY: {p}/{len(checks)} phase 37 checks passed')
if p!=len(checks): sys.exit(1)
