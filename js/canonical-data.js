// Retrace canonical test-data adapter.
// Keeps the original Base ZIP featured/Home dataset separate and unchanged.

const BASE = 'data/canonical/';
const PROJECTIONS = 'data/projections/';

async function readJSON(path) {
  const response = await fetch(path, { cache: 'no-cache' });
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  return response.json();
}

export const canonicalStore = {
  records: [], byId: new Map(), missions: [], missionById: new Map(),
  claims: [], sources: [], events: [], library: [], filtersIndex: [],
  compareIndex: [], timeline: [], issues: []
};

export async function loadCanonicalData() {
  const [equipment, missions, claims, sources, events, library, filters, compare, timeline] = await Promise.all([
    readJSON(BASE + 'equipment.json'),
    readJSON(BASE + 'missions.json'),
    readJSON(BASE + 'claims.json'),
    readJSON(BASE + 'sources.json'),
    readJSON(BASE + 'events.json'),
    readJSON(PROJECTIONS + 'library.json'),
    readJSON(PROJECTIONS + 'filters-index.json'),
    readJSON(PROJECTIONS + 'compare-index.json'),
    readJSON(PROJECTIONS + 'timeline.json')
  ]);

  const issues = [];
  const records = Array.isArray(equipment.records) ? equipment.records : [];
  const byId = new Map();
  for (const record of records) {
    const id = record.equipment_id;
    if (!id || record.id !== id) { issues.push(`Invalid canonical equipment identity: ${id || '(missing)'}`); continue; }
    if (byId.has(id)) { issues.push(`Duplicate canonical equipment ID: ${id}`); continue; }
    byId.set(id, record);
  }
  const missionList = missions.missions || [];
  const missionById = new Map();
  for (const mission of missionList) {
    if (!mission.mission_id) { issues.push('Mission entry missing mission_id'); continue; }
    if (missionById.has(mission.mission_id)) issues.push(`Duplicate mission ID: ${mission.mission_id}`);
    else missionById.set(mission.mission_id, mission);
  }
  for (const mission of missionList) {
    for (const id of mission.equipment_ids || []) if (!byId.has(id)) issues.push(`Mission ${mission.mission_id} references unknown equipment ${id}`);
  }
  for (const record of records) {
    for (const missionId of record.mission_ids || []) if (!missionById.has(missionId)) issues.push(`${record.equipment_id} references missing mission ${missionId}`);
  }

  Object.assign(canonicalStore, {
    records, byId, missions: missionList, missionById,
    claims: claims.records || [], sources: sources.records || [], events: events.records || [],
    library: library.records || [], filtersIndex: filters.records || [],
    compareIndex: compare.records || [], timeline: timeline.records || [], issues
  });
  if (issues.length) console.warn('[canonical test data]', issues);
  return canonicalStore;
}
