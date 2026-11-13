import { loadData, store } from './data.js';
import { loadCanonicalData, canonicalStore } from './canonical-data.js';
import { renderHeader, setHeaderMode, bindSearchOpener, closeDrawer, refreshBell } from './header.js';
import { initSearch, open as openSearch, close as closeSearch } from './search.js';
import { homeView } from './home.js';
import { placeholderPage, notFoundPage, directoryPage, detailPage, updatesPage, planetsScopePage } from './pages.js';
import { comparePage, glossaryPage, quizPage, sourcesPage, aboutWebsitePage } from './extra-pages.js';
import { destinationPage, libraryPage, filtersPage, fullDetailsPage, canonicalComparePage, canonicalEvidencePage, canonicalQuizPage, contactFormPage } from './retrace-pages.js';
import { FOOTER_COLUMNS, FOOTER_DESCRIPTION, FINAL_NAME_PLACEHOLDER, PLACEHOLDER_ROUTES } from './content.js';
import { watchImageErrors } from './media.js';
import { $, esc, ICONS, announce, reducedMotion } from './util.js';

const app = () => document.getElementById('app');

// ---------- Footer ----------
function renderFooter() {
  const f = document.getElementById('site-footer');
  f.innerHTML = `<div class="foot-wrap">
    <div class="foot-grid">
      <div class="foot-col foot-id"><h2 class="foot-h">${esc(FINAL_NAME_PLACEHOLDER)}</h2>
        <p class="foot-p">${esc(FOOTER_DESCRIPTION)}</p><p class="foot-p">NASA Space Apps Challenge 2026</p></div>
      ${FOOTER_COLUMNS.map((c) => `<nav class="foot-col" aria-label="${esc(c.heading)}"><h2 class="foot-h">${esc(c.heading)}</h2>
        <ul>${c.links.map((l) => `<li><a href="${l.href}">${esc(l.label)}</a></li>`).join('')}</ul></nav>`).join('')}
    </div>
    <div class="foot-bottom"><p class="copy">© 2026 ${esc(FINAL_NAME_PLACEHOLDER)}</p>
      <button type="button" class="to-top" id="to-top" aria-label="Back to top" hidden>${ICONS.arrowUp}</button></div></div>`;
  const btn = $('#to-top');
  const sync = () => { btn.hidden = window.scrollY < 300; };
  window.addEventListener('scroll', sync, { passive: true });
  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: reducedMotion() ? 'auto' : 'smooth' });
    $('#main').focus({ preventScroll: true });
  });
  sync();
}

// ---------- Router (hash based: works on any static host and supports Back/Forward) ----------
let cleanup = null, first = true;
const RETURN_STATE_KEY = 'retrace.returnState.v1';
function captureReturnState(targetHref) {
  const target = targetHref.replace(/^#/, '').split('?')[0];
  if (!/^\/equipment\/[^/]+$/.test(target)) return;
  const route = location.hash || '#/';
  if (/^#\/equipment\//.test(route)) return;
  const controls = [...app().querySelectorAll('input[id],select[id]')].map(el => ({id:el.id,value:el.value}));
  const tracks = [...app().querySelectorAll('.rt-carousel-track[id]')].map(el => ({id:el.id,left:el.scrollLeft}));
  try { sessionStorage.setItem(RETURN_STATE_KEY, JSON.stringify({route,scrollY:window.scrollY,controls,tracks,at:Date.now()})); } catch {}
}
function restoreReturnState(route, root) {
  let state; try { state=JSON.parse(sessionStorage.getItem(RETURN_STATE_KEY)||'null'); } catch { state=null; }
  if (!state || state.route !== (location.hash || '#/') || route.path.startsWith('/equipment/')) return;
  try { sessionStorage.removeItem(RETURN_STATE_KEY); } catch {}
  requestAnimationFrame(()=>{
    (state.controls||[]).forEach(item=>{const el=document.getElementById(item.id);if(el){el.value=item.value;el.dispatchEvent(new Event('change',{bubbles:true}));el.dispatchEvent(new Event('input',{bubbles:true}));}});
    (state.tracks||[]).forEach(item=>{const el=document.getElementById(item.id);if(el)el.scrollLeft=item.left;});
    window.scrollTo({top:Number(state.scrollY)||0,behavior:'instant'});
  });
}
function parse() {
  const raw = location.hash.replace(/^#/, '') || '/';
  const [path, qs] = raw.split('?');
  return { path: (path || '/').replace(/\/+$/, '') || '/', query: Object.fromEntries(new URLSearchParams(qs || '')) };
}

function resolve({ path, query }) {
  if (path === '/') return { view: homeView(), home: true };
  if (path === '/equipment') return { view: libraryPage() };
  if (path === '/filters') return { view: filtersPage() };
  if (path === '/contact') return { view: contactFormPage('contact') };
  if (path === '/feedback') return { view: contactFormPage('feedback') };
  if (path === '/report') return { view: contactFormPage('report') };
  if (path === '/destination/moon') return { view: destinationPage('Moon') };
  if (path === '/destination/mars') return { view: destinationPage('Mars') };
  if (path === '/destination/planets') return { view: planetsScopePage() };
  let m;
  if ((m = path.match(/^\/equipment\/([^/]+)$/))) return { view: fullDetailsPage(decodeURIComponent(m[1])) };
  if (path === '/updates') return { view: updatesPage() };
  if (path === '/about/sources') return { view: canonicalEvidencePage() };
  if (path === '/about/website') return { view: aboutWebsitePage() };
  if (path === '/library/compare') return { view: canonicalComparePage() };
  if (path === '/library/glossary') return { view: glossaryPage() };
  if (path === '/library/quiz') return { view: canonicalQuizPage() };
  if (PLACEHOLDER_ROUTES[path]) return { view: placeholderPage(path) };
  return { view: notFoundPage() };
}

function render() {
  const route = parse();
  cleanup && cleanup(); cleanup = null;
  closeSearch(false); closeDrawer(false);
  const { view, home } = resolve(route);
  const el = app();
  el.innerHTML = view.html;
  document.title = home ? 'Abandoned but Not Forgotten' : `${view.title} · Abandoned but Not Forgotten`;
  setHeaderMode(!!home, route.path);
  window.scrollTo({ top: 0, behavior: 'instant' });
  document.getElementById('site-header').classList.remove('is-hidden');
  if (view.mount) cleanup = view.mount(el) || null;
  restoreReturnState(route, el);
  if (!first) {
    announce(`${view.title} page`);
    (el.querySelector('h1') || $('#main'))?.focus({ preventScroll: true });
  }
  first = false;
  refreshBell();
}

function showFatal(err) {
  console.error(err);
  app().innerHTML = `<div class="page"><div class="page-wrap"><h1 class="page-h1">Something went wrong</h1>
    <p>The site data could not be loaded (${esc(err.message || err)}). If you opened index.html directly from disk, serve the folder over HTTP instead (see README.md).</p>
    <button type="button" class="btn-primary" id="retry-load">Retry</button></div></div>`;
  $('#retry-load').addEventListener('click', () => location.reload());
}

async function boot() {
  watchImageErrors();
  $('[data-skip]')?.addEventListener('click', (e) => { e.preventDefault(); $('#main').focus(); });
  app().innerHTML = '<p class="state-msg" role="status">Loading…</p>';
  try {
    await loadData();
    await loadCanonicalData();
    window.__retraceCanonical = canonicalStore;
    const [g, so, q] = await Promise.all([fetch('data/glossary.json').then(r=>r.json()), fetch('data/sources_library.json').then(r=>r.json()), fetch('data/quiz_sample.json').then(r=>r.json())]);
    window.__glossaryRecords = g.records || []; window.__sourceRecords = so.sources || []; window.__quizQuestions = q.questions || [];
  } catch (err) { renderHeader(); renderFooter(); showFatal(err); return; }
  renderHeader();
  initSearch();
  bindSearchOpener((from) => openSearch(from));
  renderFooter();
  document.addEventListener('click', (e)=>{const a=e.target.closest('a[href^="#"]');if(a)captureReturnState(a.getAttribute('href'));}, true);
  window.addEventListener('hashchange', render);
  render();
  window.__abnfReady = true;
  if (store.issues.length) console.warn('Data issues:', store.issues);
}
boot();
