"""Static smoke checks for the Retrace 10-record website testing build."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def main():
    data = load("data/retrace_test_equipment.json")
    raw = load("data/retrace_test_equipment_raw.json")
    records = data["records"]
    ids = [r["id"] for r in records]
    assert len(records) == 10, len(records)
    assert len(set(ids)) == 10, "duplicate permanent IDs"
    assert sum(r["destination"] == "Moon" for r in records) == 5
    assert sum(r["destination"] == "Mars" for r in records) == 5
    assert all(r.get("raw_record", {}).get("equipment_id") == r["id"] for r in records)
    assert len(raw["records"]) == 10
    assert all(r.get("primary_sources") for r in records), "source references missing"
    assert all((r.get("raw_record") or {}).get("publication_state") == "Draft" for r in records)

    expected = {f"MOON-EQ-{i:04d}" for i in range(1, 6)} | {f"MARS-EQ-{i:04d}" for i in range(36, 41)}
    assert set(ids) == expected, set(ids)
    selection = load("data/featured_selection.json")
    assert len(selection["featured_ids"]) == selection["expected_count"] == 10
    assert set(selection["featured_ids"]) == set(ids)

    for rel in ["elearning-test/index.html", "elearning-test/data/elearning_test_seed.json", "elearning-test/assets/What Is Space Junk and Abandoned Space Hardware.pdf"]:
        assert (ROOT / rel).exists(), rel

    main_js = (ROOT / "js/main.js").read_text(encoding="utf-8")
    pages_js = (ROOT / "js/retrace-pages.js").read_text(encoding="utf-8")
    for route in ["/equipment", "/destination/moon", "/destination/mars", "/destination/planets", "/map", "/library/compare", "/library/quiz", "/elearning", "/contact", "/feedback", "/report"]:
        assert route in main_js, f"route missing: {route}"
    for component in ["destinationPage", "equipmentLibraryPage", "detailTestPage", "compareTestPage", "mapTestPage", "contactPage", "feedbackPage", "reportPage", "elearningTestPage"]:
        assert component in pages_js, f"screen factory missing: {component}"

    print("PASS: 10 unique permanent IDs (5 Moon, 5 Mars)")
    print("PASS: all selected source records retained and linked to primary sources")
    print("PASS: all ten featured IDs resolve within the shared test collection")
    print("PASS: eLearning preview, seed data and source PDF are packaged")
    print("PASS: required test routes and screen factories are present")
    print("NOTE: static checks only; browser, external NASA links, mail-client, responsive and backend tests remain pending")

if __name__ == "__main__":
    main()
