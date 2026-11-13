# RETRACE — Interactive Website Prototype v1

This is the current interactive Retrace website prototype, assembled from the Phase 37 working build.

## Run locally

The prototype uses plain HTML, CSS and JavaScript ES modules. It has no application build step and no backend requirement.

### Windows
1. Install Python 3 if it is not already installed.
2. Double-click `START_PROTOTYPE_WINDOWS.bat`.
3. Open `http://localhost:8765/` in your browser.

### macOS / Linux
1. Open a terminal in this folder.
2. Run `bash START_PROTOTYPE_MAC_LINUX.sh`.
3. Open `http://localhost:8765/` in your browser.

### Manual start
```bash
python3 -m http.server 8765
```

Then visit `http://localhost:8765/`. Keep the terminal window open while using the prototype. Press Ctrl+C to stop the server.

## What you can explore

- Home and shared navigation
- Moon and Mars destination pages
- Equipment Library and Filters
- Equipment Full Details pages
- Compare
- Glossary
- Quiz availability state
- Sources & Evidence
- About, Updates, Contact, Feedback and Report Issue routes
- Search, navigation menus, carousels and other implemented interactions

Use the website navigation or browser Back/Forward buttons to move between routes.

## Important prototype limitations

- This is a prototype, not a production deployment. It has no production backend, authentication, CMS, or publishing workflow.
- Browser acceptance has **not** been completed in the previous build environment. Run the included Playwright test suite in an authorized browser environment before treating the interface as browser-verified.
- Some external NASA/JPL image URLs and Google Fonts require an internet connection. A neutral image fallback is provided where configured.
- The Quiz intentionally shows an unavailable state until an approved evidence-linked question bank exists. Do not substitute the legacy sample questions.
- All 15 canonical equipment records remain in Draft publication state. Draft data must not be presented as NASA-approved or production-published content.
- Mars 2020 mission registry verification, Compare claim-level citations, and an approved Contact/Feedback/Report recipient remain outstanding.
- Operational status and publication status are separate. Unknown values must remain unknown.

## Tests

Install Playwright and Chromium in an environment that permits local browser navigation:
```bash
python -m pip install playwright
python -m playwright install chromium
```

Run the browser suite:
```bash
python tests/phase22_browser_acceptance.py
```

Run static/targeted checks from this folder:
```bash
python tests/phase21_static_acceptance.py
python tests/phase24_remediation.py
python tests/phase25_details_navigation.py
python tests/phase26_compare_mapping.py
python tests/phase29_navigation_reconciliation.py
python tests/phase32_suite_reconciliation.py
python tests/phase37_release_preflight.py
```

## Project integrity

This package is a copy of the working prototype. It does not replace or modify the original Base ZIP B. NASA evidence, source records, publication states and equipment statuses have not been promoted by packaging this prototype.
