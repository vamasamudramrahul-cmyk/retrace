from pathlib import Path
root = Path(__file__).resolve().parents[1]
content = (root/'js/content.js').read_text()
main = (root/'js/main.js').read_text()
pages = (root/'js/pages.js').read_text()
checks = {
    'Protected Home Planets card remains unchanged': "{ id: 'planets', title: 'Planets', href: '#/destination/planets', label: 'Explore Planets'" in content,
    'Planets removed from footer links': "{ label: 'Explore Planets', href: '#/destination/planets' }" not in content,
    'Planets excluded from active placeholder routes': "'/destination/planets': 'Explore Planets'" not in content,
    'Legacy Home link has explicit scope route': "if (path === '/destination/planets') return { view: planetsScopePage() };" in main,
    'Scope page states Moon/Mars-only collection': 'currently documents NASA equipment associated with the Moon and Mars' in pages,
    'Scope page links to Moon and Mars': '#/destination/moon' in pages and '#/destination/mars' in pages,
}
for label, ok in checks.items(): print(('PASS' if ok else 'FAIL') + ' | ' + label)
print(f'\nSUMMARY: {sum(checks.values())}/{len(checks)} passed')
raise SystemExit(0 if all(checks.values()) else 1)
