from pathlib import Path
import json, subprocess
ROOT = Path(__file__).resolve().parents[1]
for path in ROOT.rglob('*.json'):
    json.loads(path.read_text(encoding='utf-8'))
for path in (ROOT / 'js').glob('*.js'):
    subprocess.run(['node', '--check', str(path)], check=True)
source = (ROOT / 'js' / 'upgrade-pages.js').read_text(encoding='utf-8')
assert source.count("['Destination','destination']") == 1
assert "['Instruments & Payload','instruments_payload']" in source
assert "No equipment matched your selected filter." in source
assert "const STATUS = ['ABANDONED','INACTIVE','LOST','RETIRED','CRASHED','DECOMMISSIONED','OPERATIONAL']" in source
assert "Quiz" in source and "Contact Us" in source and "Send Feedback" in source and "Report an Issue" in source
print('Static validation passed: JSON, JavaScript syntax and required screen markers.')
