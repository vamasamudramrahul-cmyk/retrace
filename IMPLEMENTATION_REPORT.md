# RETRACE Website Test Build — Verification Report

**Version:** 0.1  
**Date:** 2026-11-13 (project local date)  
**Verdict:** TEST PACKAGE CREATED — NOT READY FOR PRODUCTION

## 1. Dataset audit

| Check | Result |
|---|---|
| Moon records | 5 — MOON-EQ-0001 to MOON-EQ-0005 |
| Mars records | 5 — MARS-EQ-0036 to MARS-EQ-0040 |
| Total unique permanent IDs | 10 |
| Raw source records retained | 10 |
| Primary source arrays present | 10/10 |
| Publication state | Draft in all 10 source records |
| Mars exact numeric coordinates | 0/5 |
| Moon coordinate-bearing location records | 2 records: MOON-EQ-0002 and MOON-EQ-0004 |

The two Moon coordinate contexts are not interchangeable: one is an ALSEP array deployment-site coordinate and the other is an instrument-specific location. The map index preserves each record's own location type and caveat.

## 2. Screen coverage

| Screen | Included in test build | Verification status |
|---|---|---|
| Home | Yes | Static/data wiring checks only |
| Header and footer | Base B shell retained | Browser interaction pending |
| Universal Search | Base B search engine, shared ten records | Browser interaction pending |
| Destinations | Moon, Mars, overview | Static route declaration checked |
| Equipment Library | All ten records | Data smoke check passed |
| Moon Filters | Destination page controls | Full approved sort/persistence rules pending |
| Mars Filters | Destination page controls | Full approved sort/persistence rules pending |
| Full Details | Eight source-driven sections | Content mapping present; browser test pending |
| Compare | 30 attributes | Static presence; projection audit pending |
| Map | Coordinate-evidence index | Interactive planetary map not implemented |
| Quiz | Honest unavailable state | No verified question bank for selected IDs |
| Glossary | Base B content retained | Evidence audit pending |
| Sources & Evidence | Sources from all ten records | Static mapping present; live links unchecked |
| About Website | Base B content retained | Browser check pending |
| Updates | Empty approved state | No mock updates shown |
| eLearning | Supplied preview embedded | Source limitations retained; browser check pending |
| Contact Us | Mailto form | Email client test pending |
| Send Feedback | Mailto form | Email client test pending |
| Report an Issue | Mailto form + optional screenshot metadata | Email client test pending |

## 3. Automated checks

- `tests/test_build_smoke.py`: PASS.
- JavaScript syntax (`node --check` for all `js/*.js`): PASS.
- JSON parsing for active JSON and eLearning seed files: PASS.
- Local HTTP server response for `index.html`: HTTP 200.
- Playwright/Chromium route run: BLOCKED by environment (`ERR_BLOCKED_BY_ADMINISTRATOR` for local browser navigation); no browser pass is claimed.

## 4. Blocking issues before release

- Map technical architecture, NASA layer verification, 2D/3D interaction and export tests.
- Filters exact sorting and interval grouping, state persistence, accessibility tests.
- Compare projection schema and full 30-field mapping audit.
- Resolve Full Details five-status vs master seven-status conflict.
- Verify eLearning curriculum reconciliation and source content; connect or clearly gate personal tools.
- Build and verify equipment-specific quiz question banks.
- Browser/responsive/accessibility testing for every route.
- Test mailto workflows on supported devices and clients.
- Complete source reachability and claim-level verification.

## 5. Release decision

This package is suitable for local integration review and early screen testing. It is not a production release, not a final NASA-verified public dataset, and not evidence that every approved screen handoff is fully implemented.


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
