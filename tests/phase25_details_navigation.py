from pathlib import Path
root=Path(__file__).resolve().parents[1]
main=(root/'js/main.js').read_text()
pages=(root/'js/retrace-pages.js').read_text()
css=(root/'css/styles.css').read_text()
checks={
 'Details section navigation has accessible disclosure button':'rt-section-nav-toggle' in pages and 'aria-expanded="false"' in pages and 'aria-controls="rt-section-nav-panel"' in pages,
 'Section navigation has accessible named landmark':'aria-label="On this page"' in pages,
 'Mobile navigation panel starts collapsed':'aria-label="On this page" hidden' in pages,
 'Disclosure updates expanded state and hidden state':"toggle.setAttribute('aria-expanded',String(!open));nav.hidden=open" in pages,
 'Selecting a section closes mobile navigation':"nav.addEventListener('click',e=>{if(e.target.closest('a'))" in pages,
 'Mobile navigation uses a bounded scrollable drawer':'.rt-section-nav{display:none;position:absolute' in css and 'max-height:min(65vh,420px)' in css and 'overflow:auto' in css,
 'Desktop section navigation remains visible':'@media(min-width:601px){.rt-section-nav[hidden]{display:flex}}' in css,
 'Return state records originating route and scroll':'RETURN_STATE_KEY' in main and 'scrollY:window.scrollY' in main,
 'Return state records filters and carousel positions':'controls,tracks,at:Date.now()' in main,
 'Return state restores controls, carousels and scroll':'state.controls||[]' in main and 'state.tracks||[]' in main and 'window.scrollTo({top:Number(state.scrollY)||0' in main,
 'Return state is captured for equipment detail links':'captureReturnState(a.getAttribute(\'href\'))' in main,
 'Return state restores after originating view mounts':'restoreReturnState(route, el)' in main,
}
for name,ok in checks.items(): print(('PASS' if ok else 'FAIL')+' | '+name)
print(f'\nSUMMARY: {sum(checks.values())}/{len(checks)} targeted checks passed')
raise SystemExit(0 if all(checks.values()) else 1)
