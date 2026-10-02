# v1.03 UX/UI patch: onboarding, phone tab bar + More sheet, bottom sheets, touch menus, About & Legal,
# backup / restore, accessibility, iOS input zoom, toast position, back-button handling.
import json
s = open('src.html', encoding='utf-8').read()
def R(a, b, n=1):
    global s
    c = s.count(a); assert c == n, f'({c}) ' + a[:100]; s = s.replace(a, b)

# ---------------- CSS ----------------
R(".welcome{max-width:640px;margin:60px auto;text-align:center}\n.welcome .logo-mark{width:64px;height:64px;font-size:26px;border-radius:16px;margin:0 auto 14px}",
""".welcome{max-width:760px;margin:0 auto;padding:48px 20px 40px;text-align:center}
.welcome .logo-mark{width:72px;height:72px;font-size:28px;border-radius:18px;margin:0 auto 16px;box-shadow:0 10px 30px rgba(245,158,11,.35)}
.welcome h1{font-size:30px;letter-spacing:-.4px;margin:0}
.welcome .lead{font-size:16px;color:#475569;margin:8px auto 26px;max-width:520px}
.feat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:0 0 26px;text-align:left}
.feat{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px;box-shadow:var(--shadow)}
.feat .fi{width:36px;height:36px;border-radius:10px;display:grid;place-items:center;background:#fff4dc;color:#b45309;margin-bottom:8px}
.feat b{display:block;font-size:13.5px}.feat span{font-size:12.5px;color:var(--muted)}
.cta{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}.cta .btn{padding:11px 18px;font-size:15px}
.trust{margin-top:22px;font-size:12.5px;color:var(--muted);display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.trust span{display:inline-flex;gap:6px;align-items:center}
.lang-chips{display:flex;gap:6px;justify-content:center;margin-top:14px}
.lang-chips button{border:1px solid var(--line2);background:#fff;border-radius:20px;padding:5px 12px;cursor:pointer;font-size:13px}
.lang-chips button.on{background:var(--navy);color:#fff;border-color:var(--navy)}
body.no-project nav{display:none}body.no-project .shell{grid-template-columns:1fr}
.nav-more{display:none}
.sheet-list{display:flex;flex-direction:column;gap:2px;margin:-6px -6px 0}
.sheet-i{display:flex;align-items:center;gap:14px;border:0;background:none;text-align:left;padding:13px 12px;border-radius:10px;cursor:pointer;font-size:15px;color:var(--text);width:100%}
.sheet-i:hover,.sheet-i:active{background:var(--panel2)}.sheet-i.danger{color:var(--red)}.sheet-i.on{background:#fff7e8;color:#9a5b00}
.tmore{display:none;border:0;background:none;width:34px;height:30px;border-radius:6px;place-items:center;color:#475569;cursor:pointer;flex:none}
.about-hero{display:flex;gap:16px;align-items:center}.about-hero .logo-mark{width:58px;height:58px;font-size:22px;border-radius:14px}
.legal{font-size:13.5px;color:#334155;line-height:1.6}.legal h4{margin:16px 0 4px;font-size:14px}.legal p{margin:4px 0}
.lic{width:100%;border-collapse:collapse;font-size:13px}.lic td{padding:7px 8px;border-bottom:1px solid var(--line)}.lic td:first-child{font-weight:600}
:focus-visible{outline:3px solid rgba(245,158,11,.65);outline-offset:2px}
@media (hover:none){.trow .tact{display:none !important}.tmore{display:inline-grid}.trow{min-height:40px}}
@media (pointer:coarse){input,select,textarea{font-size:16px !important}.btn{min-height:38px}.btn.sm{min-height:34px}}
@keyframes sheetUp{from{transform:translateY(40px);opacity:.4}to{transform:none;opacity:1}}
@media (max-width:860px){
  .nav-i.sec{display:none}
  .nav-more{display:flex}
  #toasts{left:16px;right:16px;bottom:calc(88px + var(--ib))}.toast{max-width:none}
  .feat-grid{grid-template-columns:1fr 1fr}
}
@media (max-width:600px){
  .ov{align-items:flex-end;padding:calc(12px + var(--it)) 0 0}
  .modal,.modal.wide{width:100%;max-width:100%;border-radius:18px 18px 0 0;max-height:calc(94dvh - var(--it));animation:sheetUp .22s ease-out}
  .m-head{position:relative;padding-top:20px}.m-head::before{content:"";position:absolute;left:50%;top:7px;width:40px;height:4px;border-radius:2px;background:#cbd5e1;transform:translateX(-50%)}
  .m-foot{border-radius:0;padding-bottom:calc(12px + var(--ib))}
  .modal:not(:has(.m-foot)) .m-body{padding-bottom:calc(16px + var(--ib))}
  .welcome{padding-top:28px}.welcome h1{font-size:25px}
}""")

# ---------------- icons ----------------
R("  flag:'<path", "  more:'<circle cx=\"12\" cy=\"5\" r=\"1.2\"/><circle cx=\"12\" cy=\"12\" r=\"1.2\"/><circle cx=\"12\" cy=\"19\" r=\"1.2\"/>',\n  dots:'<circle cx=\"5\" cy=\"12\" r=\"1.2\"/><circle cx=\"12\" cy=\"12\" r=\"1.2\"/><circle cx=\"19\" cy=\"12\" r=\"1.2\"/>',\n  shield:'<path d=\"M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z\"/>',\n  wifiOff:'<path d=\"M2 2l20 20M8.5 16.5a5 5 0 0 1 7 0M5 13a10 10 0 0 1 5.2-2.8M19 13a10 10 0 0 0-2-1.6M12 20h.01\"/>',\n  flag:'<path")

# ---------------- nav: primary + More (phones) ----------------
R("const NAV = [['dashboard','grid','Dashboard'],", "const PRIMARY = new Set(['dashboard', 'drawings', 'issues', 'reports']);\nconst NAV = [['dashboard','grid','Dashboard'],")
R("['reports','file','Reports'],['settings','sliders','Project Settings']]", "['reports','file','Reports'],['settings','sliders','Project Settings'],['about','info','About']]")
R("""  $('#nav').innerHTML = NAV.map(([k, icon, t]) => `<button class="nav-i ${UI.view === k ? 'on' : ''}" data-view="${k}"><span class="ic">${ic(icon, 18)}</span><span class="nt">${L(t)}</span></button>`).join('')""",
  """  const secOn = !PRIMARY.has(UI.view);
  $('#nav').innerHTML = NAV.map(([k, icon, t]) => `<button class="nav-i ${PRIMARY.has(k) ? '' : 'sec'} ${UI.view === k ? 'on' : ''}" data-view="${k}" aria-label="${esc(L(t))}"><span class="ic">${ic(icon, 18)}</span><span class="nt">${L(t)}</span></button>`).join('')
    + `<button class="nav-i nav-more ${secOn ? 'on' : ''}" id="navMore" aria-label="${esc(L('More'))}"><span class="ic">${ic('dots', 18)}</span><span class="nt">${L('More')}</span></button>`""")
R("""  $('#nav').addEventListener('click', e => { const b = e.target.closest('[data-view]'); if (b) go(b.dataset.view); });""",
  """  $('#nav').addEventListener('click', e => { if (e.target.closest('#navMore')) return openMoreSheet(); const b = e.target.closest('[data-view]'); if (b) go(b.dataset.view); });""")

# ---------------- render: onboarding + about + a11y ----------------
R("""  renderShell(); renderNav(); const m = $('#main'); m.className = '';
  if (!P()) { m.innerHTML = `<div class="welcome"><div class="logo-mark">SC</div><h2>${L('Welcome to SiteCore')}</h2><p class="muted">${L('Create your first project to start managing drawings, punch lists, inspections and reports.')}</p><button class="btn primary" onclick="newProject()">${ic('plus')} ${L('Create project')}</button> <button class="btn" onclick="loadDemo()">${L('Load sample project')}</button></div>`; return; }
  ({dashboard:renderDashboard, drawings:renderDrawings, issues:renderIssues, board:renderBoard, inspections:renderInspections, diary:renderDiary, reports:renderReports, settings:renderSettings}[UI.view] || renderDashboard)();""",
"""  renderShell(); renderNav(); const m = $('#main'); m.className = '';
  document.body.classList.toggle('no-project', !P());
  if (UI.view === 'about') { renderAbout(); return a11y(m); }
  if (!P()) { renderWelcome(); return a11y(m); }
  ({dashboard:renderDashboard, drawings:renderDrawings, issues:renderIssues, board:renderBoard, inspections:renderInspections, diary:renderDiary, reports:renderReports, settings:renderSettings}[UI.view] || renderDashboard)();
  a11y(document.body);""")
R("function refresh() {", r'''/** Accessibility: icon-only buttons get an accessible name from their tooltip. */
function a11y(root) { $$('button', root).forEach(b => { if (!b.getAttribute('aria-label') && b.title && !b.textContent.trim()) b.setAttribute('aria-label', b.title); }); }
function renderWelcome() {
  const feats = [['map', 'Plans & tags', 'Import PDF / JPG plans and pin issues exactly where they are.'], ['list', 'Punch lists', 'Status, photos, markup, responsibility and due dates.'],
    ['check2', 'Inspections', 'Pass / Fail checklists that turn failures into tags.'], ['file', 'PDF reports', 'Branded reports with logos, plans and photos.']];
  $('#main').innerHTML = `<div class="welcome"><div class="logo-mark">SC</div><h1>SiteCore</h1>
    <p class="lead">${L('Field quality, punch lists and professional PDF reports for construction teams.')}</p>
    <div class="feat-grid">${feats.map(([icon, t, d]) => `<div class="feat"><div class="fi">${ic(icon, 20)}</div><b>${L(t)}</b><span>${L(d)}</span></div>`).join('')}</div>
    <div class="cta"><button class="btn primary" id="wNew">${ic('plus')} ${L('Create your first project')}</button><button class="btn" id="wDemo">${ic('layers')} ${L('Explore the sample project')}</button><button class="btn" id="wImp">${ic('download')} ${L('Import')}</button></div>
    <div class="lang-chips">${Object.entries(LANGS).map(([k, v]) => `<button data-lang="${k}" class="${LANG === k ? 'on' : ''}">${esc(v)}</button>`).join('')}</div>
    <div class="trust"><span>${ic('wifiOff', 14)} ${L('Works offline')}</span><span>${ic('shield', 14)} ${L('Your data stays on this device')}</span><span>${ic('info', 14)} SiteCore v${APP_VERSION}</span></div></div>`;
  $('#wNew').onclick = newProject; $('#wDemo').onclick = loadDemo; $('#wImp').onclick = importAny;
  $$('[data-lang]').forEach(b => b.onclick = () => setLang(b.dataset.lang));
}
/** Generic bottom action sheet. items: [key, icon, label, danger?]. Resolves with the chosen key or null. */
function actionSheet(title, items) {
  return new Promise(res => {
    const ov = modal({title, body:`<div class="sheet-list">${items.map(([k, icon, label, danger, on]) => `<button class="sheet-i ${danger ? 'danger' : ''} ${on ? 'on' : ''}" data-k="${k}">${ic(icon, 19)}<span>${esc(label)}</span></button>`).join('')}</div>`});
    ov._onclose = () => res(null);
    $$('[data-k]', ov).forEach(b => b.onclick = () => { ov._onclose = null; ov.close(); res(b.dataset.k); });
  });
}
async function openMoreSheet() {
  const items = NAV.filter(([k]) => !PRIMARY.has(k)).map(([k, icon, t]) => [k, icon, L(t), false, UI.view === k]);
  items.push(['_share', 'share', L('Share / Export')], ['_import', 'download', L('Import')], ['_lang', 'globe', L('Language') + ': ' + LANGS[LANG]]);
  const k = await actionSheet(L('More'), items); if (!k) return;
  if (k === '_share') return exportPackage(); if (k === '_import') return importAny();
  if (k === '_lang') { const l = await actionSheet(L('Language'), Object.entries(LANGS).map(([c, v]) => [c, 'globe', v, false, c === LANG])); if (l) setLang(l); return; }
  go(k);
}
function renderAbout() {
  const libs = [['pdf.js', 'Mozilla', 'Apache License 2.0', 'https://github.com/mozilla/pdf.js'], ['jsPDF', 'James Hall / yWorks', 'MIT License', 'https://github.com/parallax/jsPDF'],
    ['jsPDF-AutoTable', 'Simon Bengtsson', 'MIT License', 'https://github.com/simonbengtsson/jsPDF-AutoTable'], ['Capacitor', 'Ionic', 'MIT License', 'https://github.com/ionic-team/capacitor'],
    ['Noto Sans Lao / Noto Sans Thai', 'Google', 'SIL Open Font License 1.1', 'https://fonts.google.com/noto'], ['Icons (paths after Lucide)', 'Lucide contributors', 'ISC License', 'https://lucide.dev']];
  $('#main').innerHTML = `<div class="page" style="max-width:900px"><div class="page-head"><div class="about-hero"><div class="logo-mark">SC</div><div><h2>SiteCore</h2><p>${L('Version')} ${APP_VERSION} · ${CREDIT}</p></div></div></div>
    <div class="card" style="margin-bottom:16px"><div class="card-b legal"><p>${L('SiteCore helps construction and MEP teams manage drawings, punch lists, inspections and site diaries, and produce professional PDF reports — online or offline.')}</p></div></div>
    <div class="card" style="margin-bottom:16px"><div class="card-h"><h3>${ic('shield')} ${L('Privacy policy')}</h3></div><div class="card-b legal">
      <p><b>${L('Summary')}:</b> ${L('SiteCore does not collect, transmit or sell any personal data. There are no accounts, no ads and no analytics.')}</p>
      <h4>${L('Data you enter')}</h4><p>${L('Projects, drawings, tags, photos, inspections and diary entries are stored only on this device (app storage / browser storage). They are not sent to us or to any third party.')}</p>
      <h4>${L('Camera and files')}</h4><p>${L('The camera and file picker are used only when you choose to add a photo, drawing, logo or import file. Files are processed on the device.')}</p>
      <h4>${L('Sharing')}</h4><p>${L('Reports, CSV files and project packages leave the device only when you choose to share or save them, using the apps you select.')}</p>
      <h4>${L('Deleting data')}</h4><p>${L('Delete a project in Project Settings, or uninstall the app / clear site data to remove everything. Create a backup first if you need one.')}</p>
      <h4>${L('Children')}</h4><p>${L('SiteCore is a professional tool and is not directed at children.')}</p></div></div>
    <div class="card" style="margin-bottom:16px"><div class="card-h"><h3>${ic('file')} ${L('Open-source licences')}</h3></div><div class="card-b" style="overflow-x:auto">
      <table class="lic">${libs.map(([n, a, l, u]) => `<tr><td>${esc(n)}</td><td>${esc(a)}</td><td>${esc(l)}</td><td class="muted">${esc(u)}</td></tr>`).join('')}</table></div></div>
    <div class="card"><div class="card-b legal"><p class="muted">© ${new Date().getFullYear()} SiteCore · ${CREDIT}. ${L('Report header logos and project data belong to their respective owners.')}</p></div></div></div>`;
}
function refresh() {''')

# ---------------- tree: touch "more" menu ----------------
R("""  return `<div><div class="trow ${lv === 0 ? 'lv0' : lv === 1 ? 'lv1' : 'lvs'}" data-toggle="${n.id}"><span class="caret">${ic(open ? 'down' : 'right', 13)}</span>${icon}<span class="tlabel" title="${esc(nodePath(n))}">${esc(nodeLabel(n))}</span>
    <span class="tact">${acts}</span>${treeCounts""",
  """  return `<div><div class="trow ${lv === 0 ? 'lv0' : lv === 1 ? 'lv1' : 'lvs'}" data-toggle="${n.id}"><span class="caret">${ic(open ? 'down' : 'right', 13)}</span>${icon}<span class="tlabel" title="${esc(nodePath(n))}">${esc(nodeLabel(n))}</span>
    <span class="tact">${acts}</span><button class="tmore" data-act="menu" data-id="${n.id}" aria-label="${esc(L('More actions'))}">${ic('more', 18)}</button>${treeCounts""")
R("""<button data-act="delLayout" data-id="${l.id}" title="${L('Delete')}">${ic('trash')}</button></span>${treeCounts(issuesOf(l.id))}</div>`).join('');""",
  """<button data-act="delLayout" data-id="${l.id}" title="${L('Delete')}">${ic('trash')}</button></span><button class="tmore" data-act="lmenu" data-id="${l.id}" aria-label="${esc(L('More actions'))}">${ic('more', 18)}</button>${treeCounts(issuesOf(l.id))}</div>`).join('');""")
R("""  const n = nodeById(id), l = S.layouts.find(x => x.id === id);""",
  """  const n = nodeById(id), l = S.layouts.find(x => x.id === id);
  if (act === 'menu') { const lv = levelOf(n);
    const k = await actionSheet(nodeLabel(n), [['addChild', 'plus', lv === 0 ? L('Add floor / level') : L('Add sub-system')], ...(lv > 0 ? [['upload', 'upload', L('Upload layout (PDF / JPG / PNG)')]] : []),
      ['edit', 'edit', L('Edit')], ['up', 'up', L('Move up')], ['del', 'trash', L('Delete'), true]]);
    return k && treeAction(k, id); }
  if (act === 'lmenu') { const k = await actionSheet(l.name, [['open', 'map', L('Open layout')], ['editLayout', 'edit', L('Layout info')], ['delLayout', 'trash', L('Delete'), true]]);
    if (k === 'open') { $('#drw')?.classList.remove('show-tree'); return openLayout(id); } return k && treeAction(k, id); }""")

# ---------------- modal a11y ----------------
R("  document.body.appendChild(ov); modalStack.push(ov);\n  ov.close = () => { ov.remove();",
  "  document.body.appendChild(ov); modalStack.push(ov); ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); a11y(ov);\n  ov.close = () => { ov.remove();")

# ---------------- backup / restore ----------------
R("""async function exportPackage() {
  const p = P(); if (!p) return; busy(L('Packaging project…'));
  try {
    const nodes = discs().flatMap(d => [d, ...subtree(d.id)]), ls = projLayouts(), lids = new Set(ls.map(l => l.id)), iss = S.issues.filter(i => lids.has(i.layoutId)), diary = S.diary.filter(x => x.projectId === p.id);
    const fileIds = [...LOGO_SLOTS.map(([k]) => p[k]), ...ls.map(l => l.imageId), ...iss.flatMap(i => i.photoIds), ...diary.flatMap(x => x.photoIds || [])].filter(Boolean), files = {};
    for (const id of fileIds) { const v = await getFile(id); if (v) files[id] = v; }
    const pkg = {app:'SiteCore', format:2, appVersion:APP_VERSION, exportedAt:new Date().toISOString(), exportedBy:S.user, project:p, nodes, layouts:ls, issues:iss,
      inspections:S.inspections.filter(x => x.projectId === p.id), diary, logs:S.logs.filter(x => x.projectId === p.id), reports:S.reports.filter(x => x.projectId === p.id), templates:S.templates, files};
    await saveFile""",
"""/** Builds a self-contained package (all records + files) for one project. */
async function buildPackage(p) {
  const nodes = discs(p.id).flatMap(d => [d, ...subtree(d.id)]), ls = discs(p.id).flatMap(d => layoutsUnder(d.id)), lids = new Set(ls.map(l => l.id)), iss = S.issues.filter(i => lids.has(i.layoutId)), diary = S.diary.filter(x => x.projectId === p.id);
  const fileIds = [...LOGO_SLOTS.map(([k]) => p[k]), ...ls.map(l => l.imageId), ...iss.flatMap(i => i.photoIds), ...diary.flatMap(x => x.photoIds || [])].filter(Boolean), files = {};
  for (const id of fileIds) { const v = await getFile(id); if (v) files[id] = v; }
  return {app:'SiteCore', format:2, appVersion:APP_VERSION, exportedAt:new Date().toISOString(), exportedBy:S.user, project:p, nodes, layouts:ls, issues:iss,
    inspections:S.inspections.filter(x => x.projectId === p.id), diary, logs:S.logs.filter(x => x.projectId === p.id), reports:S.reports.filter(x => x.projectId === p.id), templates:S.templates, files};
}
async function exportBackup() {
  if (!S.projects.length) return toast(L('Nothing to export'), 'err'); busy(L('Packaging project…'));
  try { const packages = []; for (const p of S.projects) packages.push(await buildPackage(p));
    await saveFile(new Blob([JSON.stringify({app:'SiteCore', format:'backup', appVersion:APP_VERSION, exportedAt:new Date().toISOString(), packages})], {type:'application/json'}), `SiteCore_Backup_${today()}.sitecore.json`);
    S.lastBackup = Date.now(); save(); toast(L('Backup created ({n} projects)', {n:packages.length}), 'ok'); if (UI.view === 'settings') renderSettings();
  } catch (e) { toast(e.message, 'err'); } finally { busy(false); }
}
async function exportPackage() {
  const p = P(); if (!p) return; busy(L('Packaging project…'));
  try {
    const pkg = await buildPackage(p);
    await saveFile""")
R("""async function importPackage() {
  const [file] = await pickFiles('.json,application/json', false); if (!file) return;
  let pkg; try { pkg = JSON.parse(await file.text()); if (pkg.app !== 'SiteCore') throw 0; } catch (e) { return toast(L('Not a valid SiteCore package file'), 'err'); }
  if (!pkg.nodes) {""",
"""/** Imports a project package or a full backup (several packages). */
async function importAny() {
  const [file] = await pickFiles(IS_NATIVE ? '*/*' : '.json,application/json', false); if (!file) return;
  let data; try { data = JSON.parse(await file.text()); if (data.app !== 'SiteCore') throw 0; } catch (e) { return toast(L('Not a valid SiteCore package file'), 'err'); }
  if (data.format === 'backup') {
    if (!await confirmBox(L('Restore {n} project(s) from this backup? Projects that already exist will be replaced.', {n:data.packages.length}), L('Restore'), false)) return;
    for (const pkg of data.packages) await importPackage(pkg, S.projects.some(p => p.id === pkg.project.id) ? 'replace' : 'copy', true);
    save(); go('dashboard'); return toast(L('Backup restored'), 'ok');
  }
  return importPackage(data);
}
async function importPackage(pkg, forceMode, quiet) {
  if (!pkg || !pkg.project) return importAny();
  if (!pkg.nodes) {""")
R("""  const exists = S.projects.some(p => p.id === pkg.project.id); let mode = 'copy';
  if (exists) {""", """  const exists = S.projects.some(p => p.id === pkg.project.id); let mode = forceMode || 'copy';
  if (exists && !forceMode) {""")
R("""  busy(L('Importing package…'));
  try {
    const map = new Map();""", """  busy(L('Importing package…'));
  try {
    const copyName = mode === 'copy' && exists;
    const map = new Map();""")
R("if (mode === 'copy' && exists) p.name += ' (copy)';", "if (copyName) p.name += ' (copy)';")
R("""    save(); go('dashboard'); toast(L('Project imported'), 'ok');""", """    if (quiet) return; save(); go('dashboard'); toast(L('Project imported'), 'ok');""")
R("$('#pkgImport').onclick = importPackage;", "$('#pkgImport').onclick = importAny;")

# ---------------- settings: data card ----------------
R("""      <div class="card"><div class="card-h"><h3>${ic('save')} ${L('Storage')}</h3><span class="muted">SiteCore v${APP_VERSION}</span></div><div class="card-b"><div class="muted" id="storageInfo">…</div>
        <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap"><button class="btn" id="dupDemo">${L('Load sample project')}</button><button class="btn danger" id="delP">${ic('trash')} ${L('Delete this project')}</button></div></div></div>""",
"""      <div class="card"><div class="card-h"><h3>${ic('db')} ${L('Data & backup')}</h3><span class="muted">SiteCore v${APP_VERSION}</span></div><div class="card-b"><div class="muted" id="storageInfo">…</div>
        <p class="muted" style="margin:8px 0 0;font-size:12.5px">${L('Data is stored only on this device. Back up regularly — uninstalling the app or clearing browser data deletes it.')} ${S.lastBackup ? L('Last backup') + ': ' + fmtDT(S.lastBackup) : ''}</p>
        <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap"><button class="btn primary" id="bkAllBtn">${ic('download')} ${L('Back up all projects')}</button><button class="btn" id="rsBtn">${ic('upload')} ${L('Restore backup')}</button></div>
        <div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap"><button class="btn" id="dupDemo">${ic('layers')} ${L('Load sample project')}</button><button class="btn danger" id="delP">${ic('trash')} ${L('Delete this project')}</button></div></div></div>""")
R("  $('#dupDemo').onclick = loadDemo;", "  $('#dupDemo').onclick = loadDemo; $('#bkAllBtn').onclick = exportBackup; $('#rsBtn').onclick = importAny;")

# ---------------- boot: no auto sample, back button ----------------
R("if (LANGS[nl]) S.lang = nl; } catch (e) {} await seedDemo(); save(); } else save();", "if (LANGS[nl]) S.lang = nl; } catch (e) {} save(); } else save();")
R("""    const ov = modalStack[modalStack.length - 1]; if (ov) { const h = ov._onclose; ov._onclose = null; h && h(); return ov.close(); }
    if (UI.view !== 'dashboard') return go('dashboard'); AppP.exitApp();""",
"""    const pv = $('.pv'); if (pv && pv.close) return pv.close();
    const ov = modalStack[modalStack.length - 1]; if (ov) { const h = ov._onclose; ov._onclose = null; h && h(); return ov.close(); }
    const drw = $('#drw'); if (drw && (drw.classList.contains('show-tree') || drw.classList.contains('show-tags'))) return drw.classList.remove('show-tree', 'show-tags');
    if (UI.view === 'drawings' && UI.mode === 'add') return setMode('select');
    if (UI.view !== 'dashboard' && P()) return go('dashboard'); AppP.exitApp();""")
open('src.html', 'w', encoding='utf-8').write(s)

# ---------------- translations ----------------
tr = json.load(open('tr.json', encoding='utf-8'))
tr.update({
 "More": ["ເພີ່ມເຕີມ", "เพิ่มเติม"], "More actions": ["ການກະທຳເພີ່ມເຕີມ", "การทำงานเพิ่มเติม"], "About": ["ກ່ຽວກັບ", "เกี่ยวกับ"], "Version": ["ເວີຊັນ", "เวอร์ชัน"],
 "Field quality, punch lists and professional PDF reports for construction teams.": ["ຄຸນນະພາບໜ້າງານ, ລາຍການແກ້ໄຂ ແລະ ລາຍງານ PDF ມືອາຊີບ ສຳລັບທີມງານກໍ່ສ້າງ.", "คุณภาพหน้างาน รายการแก้ไข และรายงาน PDF ระดับมืออาชีพสำหรับทีมก่อสร้าง"],
 "Plans & tags": ["ແບບແປນ ແລະ ແທັກ", "แบบแปลนและแท็ก"], "Import PDF / JPG plans and pin issues exactly where they are.": ["ນຳເຂົ້າແບບ PDF / JPG ແລະ ປັກໝຸດບັນຫາຢູ່ຕຳແໜ່ງທີ່ແທ້ຈິງ.", "นำเข้าแบบ PDF / JPG และปักหมุดปัญหาตรงตำแหน่งจริง"],
 "Punch lists": ["ລາຍການແກ້ໄຂ", "รายการแก้ไข"], "Status, photos, markup, responsibility and due dates.": ["ສະຖານະ, ຮູບ, ການຂີດໝາຍ, ຜູ້ຮັບຜິດຊອບ ແລະ ວັນກຳນົດ.", "สถานะ รูป มาร์กอัป ผู้รับผิดชอบ และวันครบกำหนด"],
 "Pass / Fail checklists that turn failures into tags.": ["ລາຍການກວດ ຜ່ານ / ບໍ່ຜ່ານ ທີ່ປ່ຽນລາຍການບໍ່ຜ່ານເປັນແທັກ.", "รายการตรวจ ผ่าน / ไม่ผ่าน ที่แปลงรายการไม่ผ่านเป็นแท็ก"],
 "PDF reports": ["ລາຍງານ PDF", "รายงาน PDF"], "Branded reports with logos, plans and photos.": ["ລາຍງານພ້ອມໂລໂກ້, ແບບແປນ ແລະ ຮູບພາບ.", "รายงานพร้อมโลโก้ แบบแปลน และรูปภาพ"],
 "Create your first project": ["ສ້າງໂຄງການທຳອິດ", "สร้างโครงการแรก"], "Explore the sample project": ["ລອງໃຊ້ໂຄງການຕົວຢ່າງ", "ลองโครงการตัวอย่าง"],
 "Works offline": ["ໃຊ້ງານໄດ້ໂດຍບໍ່ມີອິນເຕີເນັດ", "ใช้งานได้แบบออฟไลน์"], "Your data stays on this device": ["ຂໍ້ມູນຂອງທ່ານຢູ່ໃນອຸປະກອນນີ້ເທົ່ານັ້ນ", "ข้อมูลของคุณอยู่ในอุปกรณ์นี้เท่านั้น"],
 "SiteCore helps construction and MEP teams manage drawings, punch lists, inspections and site diaries, and produce professional PDF reports — online or offline.": ["SiteCore ຊ່ວຍທີມງານກໍ່ສ້າງ ແລະ MEP ຈັດການແບບແປນ, ລາຍການແກ້ໄຂ, ການກວດກາ ແລະ ບັນທຶກໜ້າງານ ພ້ອມສ້າງລາຍງານ PDF ມືອາຊີບ — ທັງອອນລາຍ ແລະ ອອບລາຍ.", "SiteCore ช่วยทีมก่อสร้างและ MEP จัดการแบบแปลน รายการแก้ไข การตรวจสอบ และบันทึกหน้างาน พร้อมสร้างรายงาน PDF ระดับมืออาชีพ — ทั้งออนไลน์และออฟไลน์"],
 "Privacy policy": ["ນະໂຍບາຍຄວາມເປັນສ່ວນຕົວ", "นโยบายความเป็นส่วนตัว"], "Summary": ["ສະຫຼຸບ", "สรุป"],
 "SiteCore does not collect, transmit or sell any personal data. There are no accounts, no ads and no analytics.": ["SiteCore ບໍ່ເກັບ, ບໍ່ສົ່ງ ແລະ ບໍ່ຂາຍຂໍ້ມູນສ່ວນຕົວໃດໆ. ບໍ່ມີບັນຊີ, ບໍ່ມີໂຄສະນາ ແລະ ບໍ່ມີການວິເຄາະການນຳໃຊ້.", "SiteCore ไม่เก็บ ไม่ส่ง และไม่ขายข้อมูลส่วนบุคคลใดๆ ไม่มีบัญชีผู้ใช้ ไม่มีโฆษณา และไม่มีการวิเคราะห์การใช้งาน"],
 "Data you enter": ["ຂໍ້ມູນທີ່ທ່ານປ້ອນ", "ข้อมูลที่คุณป้อน"],
 "Projects, drawings, tags, photos, inspections and diary entries are stored only on this device (app storage / browser storage). They are not sent to us or to any third party.": ["ໂຄງການ, ແບບແປນ, ແທັກ, ຮູບ, ການກວດກາ ແລະ ບັນທຶກ ຖືກເກັບໄວ້ໃນອຸປະກອນນີ້ເທົ່ານັ້ນ. ບໍ່ຖືກສົ່ງໃຫ້ພວກເຮົາ ຫຼື ບຸກຄົນທີສາມ.", "โครงการ แบบแปลน แท็ก รูป การตรวจสอบ และบันทึก ถูกเก็บไว้ในอุปกรณ์นี้เท่านั้น ไม่ถูกส่งให้เราหรือบุคคลที่สาม"],
 "Camera and files": ["ກ້ອງ ແລະ ໄຟລ໌", "กล้องและไฟล์"],
 "The camera and file picker are used only when you choose to add a photo, drawing, logo or import file. Files are processed on the device.": ["ກ້ອງ ແລະ ຕົວເລືອກໄຟລ໌ ຖືກໃຊ້ເມື່ອທ່ານເລືອກເພີ່ມຮູບ, ແບບ, ໂລໂກ້ ຫຼື ນຳເຂົ້າໄຟລ໌ເທົ່ານັ້ນ. ໄຟລ໌ຖືກປະມວນຜົນໃນອຸປະກອນ.", "กล้องและตัวเลือกไฟล์ถูกใช้เมื่อคุณเลือกเพิ่มรูป แบบ โลโก้ หรือนำเข้าไฟล์เท่านั้น ไฟล์ถูกประมวลผลในอุปกรณ์"],
 "Sharing": ["ການແບ່ງປັນ", "การแชร์"],
 "Reports, CSV files and project packages leave the device only when you choose to share or save them, using the apps you select.": ["ລາຍງານ, ໄຟລ໌ CSV ແລະ ແພັກເກັດໂຄງການ ຈະອອກຈາກອຸປະກອນເມື່ອທ່ານເລືອກແບ່ງປັນ ຫຼື ບັນທຶກເທົ່ານັ້ນ.", "รายงาน ไฟล์ CSV และแพ็กเกจโครงการ จะออกจากอุปกรณ์เมื่อคุณเลือกแชร์หรือบันทึกเท่านั้น"],
 "Deleting data": ["ການລຶບຂໍ້ມູນ", "การลบข้อมูล"],
 "Delete a project in Project Settings, or uninstall the app / clear site data to remove everything. Create a backup first if you need one.": ["ລຶບໂຄງການໃນ ຕັ້ງຄ່າໂຄງການ, ຫຼື ຖອນການຕິດຕັ້ງແອັບ / ລ້າງຂໍ້ມູນເວັບ ເພື່ອລຶບທັງໝົດ. ສຳຮອງຂໍ້ມູນກ່ອນຖ້າຕ້ອງການ.", "ลบโครงการในตั้งค่าโครงการ หรือถอนการติดตั้งแอป / ล้างข้อมูลเว็บเพื่อลบทั้งหมด สำรองข้อมูลก่อนหากต้องการ"],
 "Children": ["ເດັກນ້ອຍ", "เด็ก"], "SiteCore is a professional tool and is not directed at children.": ["SiteCore ເປັນເຄື່ອງມືມືອາຊີບ ແລະ ບໍ່ໄດ້ມີຈຸດປະສົງສຳລັບເດັກນ້ອຍ.", "SiteCore เป็นเครื่องมือระดับมืออาชีพและไม่ได้มุ่งเป้าไปที่เด็ก"],
 "Open-source licences": ["ລິຂະສິດໂອເພນຊອດ", "สัญญาอนุญาตโอเพนซอร์ส"],
 "Report header logos and project data belong to their respective owners.": ["ໂລໂກ້ຫົວລາຍງານ ແລະ ຂໍ້ມູນໂຄງການ ເປັນຂອງເຈົ້າຂອງແຕ່ລະລາຍ.", "โลโก้หัวรายงานและข้อมูลโครงการเป็นของเจ้าของแต่ละราย"],
 "Backup created ({n} projects)": ["ສຳຮອງຂໍ້ມູນແລ້ວ ({n} ໂຄງການ)", "สำรองข้อมูลแล้ว ({n} โครงการ)"],
 "Restore {n} project(s) from this backup? Projects that already exist will be replaced.": ["ກູ້ຄືນ {n} ໂຄງການ ຈາກໄຟລ໌ສຳຮອງນີ້ບໍ? ໂຄງການທີ່ມີຢູ່ແລ້ວຈະຖືກແທນທີ່.", "กู้คืน {n} โครงการจากไฟล์สำรองนี้หรือไม่? โครงการที่มีอยู่แล้วจะถูกแทนที่"],
 "Restore": ["ກູ້ຄືນ", "กู้คืน"], "Backup restored": ["ກູ້ຄືນຂໍ້ມູນແລ້ວ", "กู้คืนข้อมูลแล้ว"], "Data & backup": ["ຂໍ້ມູນ ແລະ ການສຳຮອງ", "ข้อมูลและการสำรอง"],
 "Data is stored only on this device. Back up regularly — uninstalling the app or clearing browser data deletes it.": ["ຂໍ້ມູນຖືກເກັບໃນອຸປະກອນນີ້ເທົ່ານັ້ນ. ສຳຮອງຂໍ້ມູນເປັນປະຈຳ — ການຖອນແອັບ ຫຼື ລ້າງຂໍ້ມູນເວັບ ຈະລຶບຂໍ້ມູນ.", "ข้อมูลถูกเก็บในอุปกรณ์นี้เท่านั้น สำรองข้อมูลเป็นประจำ — การถอนแอปหรือล้างข้อมูลเว็บจะลบข้อมูล"],
 "Last backup": ["ສຳຮອງລ່າສຸດ", "สำรองล่าสุด"], "Back up all projects": ["ສຳຮອງທຸກໂຄງການ", "สำรองทุกโครงการ"], "Restore backup": ["ກູ້ຄືນຈາກໄຟລ໌ສຳຮອງ", "กู้คืนจากไฟล์สำรอง"],
})
json.dump(tr, open('tr.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
k = open('keys.py', encoding='utf-8').read()
extra = ['About', 'Plans & tags', 'Import PDF / JPG plans and pin issues exactly where they are.', 'Punch lists', 'Status, photos, markup, responsibility and due dates.',
         'Pass / Fail checklists that turn failures into tags.', 'PDF reports', 'Branded reports with logos, plans and photos.']
k = k.replace("'Small phone','Phone','Tablet','Computer']", "'Small phone','Phone','Tablet','Computer'," + ','.join(repr(x) for x in extra) + "]")
open('keys.py', 'w', encoding='utf-8').write(k)
print('patched')
