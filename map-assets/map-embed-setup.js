
(function () {
  'use strict';
  const params = new URLSearchParams(location.search);
  const requested = params.get('destination') || 'moon';
  const destinations = requested === 'all' ? ['moon', 'mars'] : [requested === 'mars' ? 'mars' : 'moon'];
  const labels = { moon: 'Moon', mars: 'Mars' };

  function panel(key) {
    const name = labels[key];
    return `
      <section class="map-embed-section" aria-labelledby="${key}-map-heading">
        <div class="map-embed-heading">
          <div><p class="map-embed-kicker">RETRACE DESTINATION MAP</p><h2 id="${key}-map-heading">${name} explorer</h2></div>
          <span class="map-embed-tag">3D globe · 2D surface view</span>
        </div>
        <div class="globe-viewport-container enhanced-map-viewport map-explorer-viewport eyes-map-viewport eyes-map-${key}" id="${key}GlobeContainer">
          <div class="map-mode-bar eyes-map-modebar map-mode-top-right">
            <div class="map-mode-switch" role="group" aria-label="Select ${name} map view">
              <button class="map-mode-btn is-active" type="button" data-map-key="${key}" data-map-mode="3d" aria-pressed="true">3D Globe</button>
              <button class="map-mode-btn" type="button" data-map-key="${key}" data-map-mode="surface" aria-pressed="false">Surface Map</button>
            </div>
          </div>
          <canvas class="globe-canvas" id="${key}GlobeCanvas" aria-label="Interactive textured 3D ${name} globe. Drag to rotate and use zoom controls."></canvas>
          <div class="map-surface-view" id="${key}SurfaceView" hidden>
            <div class="map-surface-stage" id="${key}SurfaceStage">
              <img class="map-surface-image" id="${key}SurfaceImage" alt="${name} global surface appearance view" crossorigin="anonymous" loading="eager">
              <div class="map-surface-markers" id="${key}SurfaceMarkers" aria-label="Mapped equipment locations"></div>
            </div>
            <span class="surface-map-help">Drag to pan · Use + / − to zoom</span>
          </div>
          <div class="map-loading-overlay is-visible" id="${key}MapLoading" role="status" aria-live="polite">
            <div class="map-loader-spinner" aria-hidden="true"></div><strong>Loading 3D</strong><span>Loading map appearance imagery</span>
          </div>
          <button class="map-controls-toggle" type="button" data-map-controls-toggle="${key}" aria-controls="${key}MapLayers" aria-expanded="false" aria-label="Open ${name} map controls">»</button>
          <div class="map-utility-controls" aria-label="${name} map tools">
            <button class="map-utility-btn" type="button" data-map-action="info" data-map-key="${key}" aria-label="Map information" title="Map information">i</button>
            <button class="map-utility-btn" type="button" data-map-action="layers" data-map-key="${key}" aria-label="Map layers" title="Map layers">▱</button>
            <span class="map-utility-divider" aria-hidden="true"></span>
            <button class="map-utility-btn" type="button" data-map-action="zoom-in" data-map-key="${key}" aria-label="Zoom in" title="Zoom in">+</button>
            <button class="map-utility-btn" type="button" data-map-action="zoom-out" data-map-key="${key}" aria-label="Zoom out" title="Zoom out">−</button>
            <button class="map-utility-btn" type="button" data-map-action="fullscreen" data-map-key="${key}" aria-label="Toggle fullscreen map" title="Fullscreen">⛶</button>
          </div>
          <div class="map-popover map-layers-popover rich-map-layers" id="${key}MapLayers" hidden>
            <strong>Map layers</strong>
            <p class="map-layer-help">Only evidence-linked equipment positions with numeric coordinates can appear as equipment markers.</p>
            <label><input type="checkbox" checked data-map-key="${key}" data-map-layer="equipment"> Equipment locations</label>
            <label><input type="checkbox" checked data-map-key="${key}" data-map-layer="grid"> Coordinate grid</label>
            <label><input type="checkbox" checked data-map-key="${key}" data-map-layer="labels"> Location labels</label>
          </div>
          <div class="globe-marker-popup" id="${key}MarkerPopup" role="group" aria-label="Selected map location">
            <div class="popup-title" id="${key}PopupTitle">Selected equipment</div>
            <p class="map-popup-meta" id="${key}PopupMeta"></p>
            <button class="popup-link" id="${key}PopupBtnDetails" type="button">Explore Details →</button>
          </div>
          <div class="eyes-map-bottombar">
            <div class="eyes-map-ready"><span class="eyes-ready-dot" aria-hidden="true"></span><strong>MAP VIEW</strong><span class="eyes-map-ready-caption">TEST</span></div>
            <button class="map-toolbar-button map-bottom-download" id="${key}MapDownload" type="button" aria-label="Download current ${name} map view">↓ Download map</button>
            <div class="eyes-map-status-slot"><span class="map-source-status" id="${key}MapLayerStatus" role="status">Preparing ${name} map…</span></div>
          </div>
        </div>
        <p class="map-source-footnote" id="${key}MapSourceFootnote"></p>
      </section>`;
  }

  const root = document.getElementById('map-root');
  root.innerHTML = destinations.map(panel).join('');
  if (requested === 'all') root.classList.add('map-embed-grid');
  else root.classList.add('map-embed-single');
  document.getElementById('map-destination-note').textContent =
    requested === 'mars'
      ? 'Mars equipment markers are absent because the selected Mars records do not contain independently verified instrument or rover coordinates. The Mars sphere is an illustrative appearance fallback, not a scientific basemap.'
      : requested === 'moon'
        ? 'One Moon equipment marker is available: MOON-EQ-0004, based on a NASA report location claim. Its displayed coordinate precision reproduces the source notation and does not establish absolute positional accuracy. The ALSEP array-site coordinate in MOON-EQ-0002 is intentionally not represented as a separate equipment position.'
        : 'The Moon view has one evidence-linked instrument-position marker. Mars has no eligible equipment markers in this selection. Missing coordinates and non-equipment-specific array-site coordinates are not converted into equipment positions.';
})();
