from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name, ok, detail=''):
    checks.append((name,bool(ok),detail))

search=(ROOT/'js/search.js').read_text()
renderer=(ROOT/'js/retrace-pages.js').read_text()
equipment=json.loads((ROOT/'data/canonical/equipment.json').read_text())['records']
missions=json.loads((ROOT/'data/canonical/missions.json').read_text())['missions']
sources=json.loads((ROOT/'data/canonical/sources.json').read_text())['records']
claims=json.loads((ROOT/'data/canonical/claims.json').read_text())['records']
events=json.loads((ROOT/'data/canonical/events.json').read_text())['records']

check('Universal search imports canonical store', "import { canonicalStore } from './canonical-data.js'" in search)
check('Universal search indexes canonical equipment', 'for (const r of canonicalStore.records || [])' in search)
check('Universal search indexes canonical mission registry', 'for (const m of canonicalStore.missions || [])' in search)
check('Legacy Home search index remains present', 'for (const r of store.records)' in search)
check('Legacy placeholder routes for quiz/eLearning excluded', "path === '/library/quiz' || path === '/elearning'" in search)
check('Library card includes destination badge', "badge(r.destination||'Destination unknown')" in renderer)
check('Timeline has explicit equipment details CTA', 'View Equipment Details:' in renderer)
check('Timeline displays destination label', 'e.destination||destination' in renderer)
check('Timeline filtered-empty exact copy', 'No timeline events match this filter.' in renderer)
check('Timeline NASA links restricted to HTTPS NASA domains', "u.protocol==='https:'&&/(^|\\.)nasa\\.gov$/i.test(u.hostname)" in renderer)
check('Sources renderer uses source_title', 'x.source_title||x.source_id' in renderer)
check('Claims renderer uses evidence_classification', 'x.evidence_classification' in renderer)
check('Claims link to source_ids', '(x.source_ids||[]).map(id=>sourceFor(id,x.equipment_id))' in renderer)
source_keys={(x['equipment_id'],x['source_id']) for x in sources}
check('Every claim source reference resolves within its equipment record', all((c['equipment_id'],sid) in source_keys for c in claims for sid in c.get('source_ids',[])))
check('All event equipment references resolve', all(e.get('equipment_id') in {r['equipment_id'] for r in equipment} for e in events))
check('Mission registry preserves verified InSight entry and partial Mars 2020 caveat', len(missions)==7 and all(m.get('mission_id') for m in missions) and any(m.get('mission_id')=='MIS-0021' for m in missions) and any(m.get('mission_id')=='MIS-0020' and 'PARTIAL' in str(m.get('registry_status','')) for m in missions))

for name,ok,detail in checks:
    print(('PASS' if ok else 'FAIL')+' | '+name+(f' | {detail}' if detail else ''))
print(f'\nSUMMARY: {sum(ok for _,ok,_ in checks)}/{len(checks)} Phase 24 remediation checks passed')
raise SystemExit(0 if all(ok for _,ok,_ in checks) else 1)
