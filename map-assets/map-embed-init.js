
(async function () {
  const status = document.getElementById('map-destination-note');
  try {
    const response = await fetch('data/map_equipment_eligible.json');
    if (!response.ok) throw new Error(`Map data could not be loaded (${response.status})`);
    const payload = await response.json();
    if (!window.ABNPlanetaryMaps || typeof window.ABNPlanetaryMaps.mount !== 'function') {
      throw new Error('Map engine did not initialize.');
    }
    window.ABNPlanetaryMaps.mount({ equipment: payload.equipment || [] });
    window.__retraceMapReady = true;
    document.documentElement.dataset.mapReady = 'true';
  } catch (error) {
    status.textContent = `Map unavailable: ${error.message}. The location evidence list remains available on the parent website.`;
    document.documentElement.dataset.mapReady = 'false';
  }
})();
