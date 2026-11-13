# RETRACE Website Testing Build v0.1

**Build type:** Integrated front-end testing build  
**Master baseline:** `base.zip` (Base B)  
**Reference prototype:** `old prototype.zip` (included under `reference/`)  
**Shared equipment test collection:** 5 Moon + 5 Mars records  
**Release status:** Testing only — not production approved

## Run locally

This is a static website using HTML, CSS and JavaScript ES modules. Serve the project directory over HTTP; do not open `index.html` directly from the file system.

```bash
python3 -m http.server 8765
```

Open `http://localhost:8765/`.

## Shared equipment test collection

The active shared collection is `data/retrace_test_equipment.json` and the complete selected source records are preserved in `data/retrace_test_equipment_raw.json`.

- Moon: `MOON-EQ-0001` through `MOON-EQ-0005`
- Mars: `MARS-EQ-0036` through `MARS-EQ-0040`
- Total: 10 permanent equipment IDs

All ten source records are retained with their original evidence, source references, verification state and publication state. The records are still marked `Draft`; they must not be treated as production-approved records.

All ten IDs appear in the Home featured carousel, Equipment Library, destination screens, universal search and Sources & Evidence. Map and quiz are limited by the evidence/content actually available for those records.

## Screens included

- Home
- Moon, Mars and destination overview
- Equipment Library
- Moon and Mars destination filter views
- Equipment Full Details (eight section structure)
- Compare (30 requested attributes)
- Map location-evidence index
- Glossary
- Quiz availability state
- Sources & Evidence
- About Website
- Updates
- eLearning test preview
- Contact Us
- Send Feedback
- Report an Issue

The existing Base B header/footer framework and global styles are retained as the master shell. The selected Base B screen content is not a complete production implementation of every approved handoff.

## Evidence and content rules

- No new NASA technical facts, coordinates, status dates or quiz answers were invented during packaging.
- Null or unavailable fields remain explicitly unavailable.
- Map view lists only numeric coordinates found in the supplied records. It does not infer a rover position from a parent mission or lander.
- A source link is a reference, not proof that the link was reachable during this packaging run or that every associated claim has passed a fresh audit.
- All selected equipment source records report `publication_state: Draft`.
- No approved public updates or FAQ set was supplied for this test collection, so the Updates screen shows an empty approved state and the Home FAQ block is not rendered.

## Known limitations — do not mistake this for a completed release

1. **Map:** This build provides a location-evidence index, not the approved interactive 2D/3D Moon/Mars map, NASA tile layers, or verified export functions. Only two Moon location records in this selection contain numeric coordinates; the selected Mars records do not contain exact coordinates.
2. **Filters:** Destination and library search/filter controls are usable for test browsing, but the complete approved sorting/interval-overlap rules and persistent filter-state requirements are not yet implemented or verified.
3. **Full Details:** Eight sections render from source-record fields. The five-status rule in the Full Details handoff conflicts with the seven-status master taxonomy; this build displays the source record's status as supplied and does not resolve that policy conflict.
4. **Compare:** The 30-attribute table is present. Some fields are intentionally `Not recorded`; a fully audited projection schema and all mapping rules remain pending.
5. **Quiz:** No quiz question bank was verified against these ten selected permanent IDs. The page therefore explains that verified questions are unavailable instead of displaying unrelated sample questions.
6. **eLearning:** The supplied standalone test preview is embedded. It retains its source-documented Chat 1 curriculum discrepancy, Chat 2 metadata-only state, and demonstration-only personal tools/workspace/teacher resource cards. No cloud persistence is connected.
7. **Contact/Feedback/Report:** Forms prepare a `mailto:` draft to `retrace.space@gmail.com`. They do not submit or store messages. Screenshots must be attached manually by the visitor after the email client opens.
8. **Glossary:** Base B glossary content is retained as starter content; its full term-by-term evidence audit remains pending.
9. **Updates:** No approved public updates were provided; the screen shows that no approved updates are available.
10. **Browser QA:** Automated browser navigation, mobile/responsive checks, keyboard/screen-reader checks, live NASA source reachability, and actual email-client testing remain pending. A local Chromium browser run was blocked by the execution environment's browser network policy; this is not recorded as a passed test.

## Validation performed

Run:

```bash
python tests/test_build_smoke.py
```

The smoke test validates the ten IDs, 5/5 destination split, raw source record retention, source references, featured selection, eLearning assets and expected route declarations.

JavaScript syntax and JSON parsing checks were also run during packaging. These are static checks, not end-to-end browser tests.


# RETRACE Website Testing Build v0.2 — Destination Map Integration

## Change summary
- Integrated the old prototype's interactive planetary map engine into the three destination screens: Destinations overview, Moon, and Mars.
- The map is isolated in `map-embed.html` so its legacy DOM/CSS/engine do not alter unrelated Base B screens.
- Moon and Mars pages each load the corresponding interactive map; Destinations overview displays both.
- Map controls include 3D globe, 2D surface appearance, rotation/pan, zoom, layer controls, information panel, fullscreen, and map image download where the browser and imagery permit.
- Marker selection links back to the parent Retrace Full Details route.

## Location evidence and marker eligibility
- The selected 10-record test dataset is used as the map's source.
- Only MOON-EQ-0004 is currently supplied as an equipment marker. Its NASA-SP-235 instrument-location claim CLM-0034 supports the reported coordinate (-2.970, -23.350). The record remains PARTIALLY_VERIFIED; source-display precision is not absolute positional accuracy.
- MOON-EQ-0002's numeric coordinate is an ALSEP array deployment-site coordinate, not an independently surveyed central-station position; it is intentionally excluded from equipment markers.
- The five selected Mars records do not contain independently verified equipment/rover coordinates; no Mars equipment markers are shown.
- Missing coordinates are never inferred.

## Data-source policy
- The old Mars NASA/JPL/USGS Viking mosaic was not carried into this integration because the corrected Map specification requires NASA-origin production layers. Mars currently uses a clearly disclosed illustrative appearance fallback, not a scientific basemap.
- Moon map attempts the old prototype's NASA Moon Trek LRO WAC WMTS layer and falls back to the NASA LRO WAC global texture or a clearly labelled illustrative fallback if unavailable.
- External imagery and the Three.js CDN require an internet connection. Live availability and CORS behaviour were not verified in this environment.

## Verification performed
- JavaScript syntax checks.
- JSON parsing for the map marker dataset and existing application data.
- Static checks for all three destination embeds and expected map DOM IDs.
- ZIP integrity check.

## Not verified
- Real-browser WebGL rendering, remote NASA imagery, WMTS/CORS, fullscreen, download permissions, marker selection, touch interaction, and responsive layout.
- WCAG 2.2 AA conformance.
- NASA map-service availability or complete technical compatibility.

This is a testing build, not a production release. No scientific claims or map-service availability are implied by static validation.

Map-layer limitation: the mission-linked-sites toggle from the old prototype was omitted because the selected test package has no separate mission-site coordinate dataset. The available map overlays are equipment locations, coordinate grid, and labels.

Mars map note: the Mars 3D and 2D surfaces use a procedural illustrative appearance only. It is explicitly labelled and must not be interpreted as a NASA scientific basemap. The legacy NASA/JPL/USGS Viking texture was excluded under the corrected NASA-origin-only source policy.
