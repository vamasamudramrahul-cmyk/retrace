# Retrace Screen Build Report v1.0

**Baseline:** `base.zip` (`abnf-home-prototype/`)
**Map Screen:** Excluded from this build by owner instruction.
**Build scope:** Destination filters (Moon and Mars), Compare, Full Details, Quiz, Contact Us, Send Feedback, Report an Issue.
**Preserved modules:** Home, header, footer, Universal Search, Updates, Sources & Evidence, Glossary, About Website, and their existing data files were not edited. The global router was extended only to connect the approved screen routes.

## Implemented

- Moon and Mars destination screens with independent filters, five-field search, type/status controls, sort choices, seven-status key, result counts, exact empty-state copy, independent reset, and destination-specific browser storage for filter state.
- Compare screen with initially empty selectors, destination/mission grouping, duplicate prevention, independent clear controls, continuous 30-row comparison table, and the six report sections. Only direct source fields with clear semantic equivalence are mapped.
- Full Details screen with eight continuous sections, text-only actions, contextual route parameters, share/copy attempt, browser print-to-PDF, source links and missing-information labels.
- Quiz equipment search/filter and question-count gating. A five-question attempt is not enabled unless five questions exist for the selected record. Retry avoids the immediately previous question IDs and is blocked when five different questions are unavailable.
- Contact, feedback and issue-report forms with required categories/messages, character limits, optional fields, client-side validation, category explanations, page URL context, email-draft workflow and privacy disclosure.
- Issue-report screenshot validation and local preview, remove/replace control, and manual email-attachment disclosure.

## Data integrity boundaries

The supplied baseline contains 10 sample equipment records. This build does not add records, assign permanent equipment IDs, create new NASA facts, or change the supplied JSON data.

The existing records do not contain canonical `operational_status`, normalized ISO launch/deployment dates, permanent equipment IDs, or the technical fields needed for the full Compare/Details specifications. Accordingly:

- Status filter options are derived only from canonical status values present in the records; none are fabricated. The seven-value status key is shown separately.
- Date sorting does not parse narrative date strings. Until normalized dates and permanent IDs are supplied, date-sort choices retain source order and the UI discloses the limitation.
- Compare maps only Destination, Equipment type and Mission from direct fields. Other attributes remain `Not recorded`.
- Full Details displays supplied short descriptions, story hooks, record claims and record-level source links with explicit caveats. Unsupported section content remains “Information currently unavailable.”
- No canonical equipment status is inferred from mission completion, last contact, or free-text status wording.
- The Details handoff's five-status presentation conflicts with the project-wide seven-status taxonomy. This build does not assign or display an unsupported canonical classification; owner resolution remains required.
- Quiz content currently has one sample question for each of five equipment records, not 15 questions per equipment. Five-question attempts therefore remain unavailable until sufficient approved questions exist.

## Contact workflow limitations

Forms prepare a `mailto:` draft to `retrace.space@gmail.com`. The website does not transmit or store submissions and does not claim that an email has been sent. The selected issue screenshot is not automatically attached; the visitor is told to attach it manually in the email application.

## Verification

- JavaScript syntax checks: **PASS** (`node --check` for all JS modules).
- JSON parse checks: **PASS** (all JSON files in the baseline parse).
- Baseline preservation comparison: **PASS**; only `js/main.js` and `css/styles.css` were modified, and `js/upgrade-pages.js` plus this report were added.
- Existing Playwright acceptance suite: **NOT RUN**; the configured Playwright Chromium executable was unavailable.
- Additional browser route test: **BLOCKED**; the environment blocked local HTTP navigation (`ERR_BLOCKED_BY_ADMINISTRATOR`).
- Real email-client behaviour, screenshot attachment, NASA image URL availability, assistive-technology behaviour, cross-browser/device behaviour and WCAG 2.2 AA conformance: **NOT VERIFIED**.

## Not included

- Map Screen.
- Old prototype code/data; no old-prototype modules were selected for this build.
- Backend, CMS, database, analytics, submission storage, authentication, production deployment, or new NASA research records.
- The Full Details section-jump navigation is not added as a separate horizontal bar because the selected baseline requires the global header/mobile drawer to remain untouched. Integrating the eight section links into those preserved shared components requires a separate owner-approved integration decision.
