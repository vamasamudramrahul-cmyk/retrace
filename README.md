# RETRACE — Website Testing Build v0.1

This is the integrated Retrace front-end testing build based on the uploaded `base.zip` application. It uses the old prototype as a reference and includes a shared 10-record test collection: five Moon records and five Mars records.

## Start the website

Run a local HTTP server from this folder:

```bash
python3 -m http.server 8765
```

Then open `http://localhost:8765/`.

## Read first

- `RETRACE_TEST_BUILD_README.md` — setup, included screens and limitations.
- `RETRACE_TEST_BUILD_VERIFICATION_REPORT.md` — validation results and release blockers.
- `data/retrace_test_equipment.json` — active shared test collection.
- `data/retrace_test_equipment_raw.json` — original selected source records retained in full.
- `reference/old-prototype-reference.zip` — old prototype reference archive.

## Important

This is a testing package, not a production release. All ten equipment source records are marked Draft. Some approved screen specifications remain partially implemented or technically unverified. See the verification report before evaluating the build.


## v0.2 Destination maps
The interactive old-prototype map experience is embedded on Destinations, Moon, and Mars. See `RETRACE_TEST_BUILD_README.md` for location eligibility, imagery policy, and test limitations.
