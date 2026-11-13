import json, pathlib, sys
R=pathlib.Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text())
reg=load('data/projections/compare-mapping-registry.json')
proj=load('data/projections/compare-index.json')
eq=load('data/canonical/equipment.json')['records']
checks=[]
def ck(name,ok):
 checks.append((name,bool(ok))); print(('PASS' if ok else 'FAIL')+' | '+name)
expected=['destination','equipment_type','mission','class','program','operational_status','launch_date','landing_date','landing_site','latitude','longitude','launch_mass','deployed_mass','primary_power_source','secondary_power_source','mobility_capabilities','major_discoveries','scientific_legacy','primary_landing_type','landing_mechanism','deployment_date','mission_end_date','last_contact_date','mission_duration','equipment_dimensions','communication_system','data_collection_capability','navigation_system','equipment_design_life','instruments_payload']
ck('Registry defines exactly 30 ordered attributes',[x['key'] for x in reg['attributes']]==expected and reg['attribute_count']==30)
ck('Every attribute has a mapping status and missing-state policy',all(x.get('mapping_status') and x.get('missing_state_policy') for x in reg['attributes']))
ck('All five missing-value states are documented',all(x in reg['missing_value_states'] for x in ['NOT_RECORDED','INSUFFICIENT_EVIDENCE','NOT_APPLICABLE','UNKNOWN','CONFLICTING_EVIDENCE']) and True)
ck('Compare projection covers all canonical equipment',set(x['equipment_id'] for x in proj['records'])==set(x['equipment_id'] for x in eq))
ck('Every equipment projection has all 30 attributes',all(list(x['attributes'])==expected for x in proj['records']))
ck('Every attribute entry has a valid state',all(v.get('state') in {'PRESENT','NOT_RECORDED','NOT_APPLICABLE','INSUFFICIENT_EVIDENCE','UNKNOWN','CONFLICTING_EVIDENCE'} for x in proj['records'] for v in x['attributes'].values()))
ck('Present values are non-empty',all(v.get('value') not in (None,'') for x in proj['records'] for v in x['attributes'].values() if v['state']=='PRESENT'))
ck('Missing values carry a reason',all(v.get('reason') for x in proj['records'] for v in x['attributes'].values() if v['state']!='PRESENT'))
ck('No automatic similarity/difference conclusions in projection', 'similarities' not in proj and 'differences' not in proj)
js=(R/'js/retrace-pages.js').read_text()
ck('Compare renderer uses reason-aware states',all(x in js for x in ['INSUFFICIENT_EVIDENCE','NOT_RECORDED','CONFLICTING_EVIDENCE','compareCell']))
print(f'\nSUMMARY: {sum(ok for _,ok in checks)}/{len(checks)} Phase 26 checks passed')
sys.exit(0 if all(ok for _,ok in checks) else 1)
