# v1.05 dark mode: theme setting (Auto / Light / Dark), dark palette + overrides, early theme script, Android bars.
import json
s = open('src.html', encoding='utf-8').read()
def R(a, b, n=1):
    global s
    c = s.count(a); assert c == n, f'({c}) ' + a[:100]; s = s.replace(a, b)

# --- early theme (no white flash) ---
R('<meta name="theme-color" content="#0f1f35">', '<meta name="theme-color" content="#0f1f35">', 0) if '<meta name="theme-color"' not in s else None
R("<style>\n:root{", """<script>/* theme before first paint */try{var t=localStorage.getItem('sitecore.theme')||'auto';document.documentElement.dataset.theme=(t==='auto'?(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'):t);}catch(e){document.documentElement.dataset.theme='light';}</script>
<style>
:root{""")
R("  --r:10px;\n  /* Safe areas:", "  --soft:#475569;--hl:#fff4dc;--hl2:#fff7e8;--hlt:#9a5b00;--field:#fff;--bar:#fff;\n  color-scheme:light;\n  --r:10px;\n  /* Safe areas:")

DARK = r"""
/* ================= DARK MODE ================= */
html[data-theme=dark]{
  color-scheme:dark;
  --bg:#0a111c;--panel:#121b29;--panel2:#172233;--line:#243247;--line2:#33435b;
  --text:#e6ecf4;--muted:#93a3b8;--soft:#b3c0d1;--blue:#60a5fa;--red:#f87171;--green:#22c55e;
  --hl:rgba(245,158,11,.16);--hl2:rgba(245,158,11,.12);--hlt:#fbbf24;--field:#0e1624;--bar:#121b29;
  --shadow:0 1px 2px rgba(0,0,0,.35),0 6px 18px rgba(0,0,0,.28);
}
html[data-theme=dark] .top{background:#0b1626}
html[data-theme=dark] nav,html[data-theme=dark] .tree-panel,html[data-theme=dark] .tag-panel,html[data-theme=dark] .viewer-bar{background:var(--bar)}
html[data-theme=dark] .nav-i{color:#c3cede}
html[data-theme=dark] .nav-i.on,html[data-theme=dark] .sheet-i.on{background:var(--hl);color:var(--hlt)}
html[data-theme=dark] .btn{background:var(--panel2);color:var(--text)}
html[data-theme=dark] .btn:hover{background:#1f2c41}
html[data-theme=dark] .btn.primary{background:var(--accent);color:#1c1300}
html[data-theme=dark] .btn.primary:hover{background:#fbbf24}
html[data-theme=dark] .btn.ghost{background:transparent;color:#e2e8f0}
html[data-theme=dark] .btn.danger{color:var(--red);border-color:#5b2330}
html[data-theme=dark] .btn.danger:hover{background:rgba(248,113,113,.12)}
html[data-theme=dark] .input,html[data-theme=dark] .fl input,html[data-theme=dark] .fl select,html[data-theme=dark] .fl textarea,html[data-theme=dark] .cm-add input{background:var(--field);color:var(--text)}
html[data-theme=dark] .fl,html[data-theme=dark] .field-l,html[data-theme=dark] .tbl th,html[data-theme=dark] .logo-slot h4,html[data-theme=dark] .cm.sys,html[data-theme=dark] .vp-empty,html[data-theme=dark] .welcome .lead,html[data-theme=dark] .icard-f,html[data-theme=dark] .tmore,html[data-theme=dark] .res button{color:var(--soft)}
html[data-theme=dark] .chip,html[data-theme=dark] .seg button,html[data-theme=dark] .res button,html[data-theme=dark] .lang-chips button{background:var(--panel2);color:var(--text)}
html[data-theme=dark] .seg button.on{background:#2b4a78;color:#fff}
html[data-theme=dark] .seg button.on.add{background:var(--accent);color:#1c1300}
html[data-theme=dark] .lang-chips button.on{background:var(--accent);color:#1c1300;border-color:var(--accent)}
html[data-theme=dark] .tbl tr.click:hover td{background:rgba(245,158,11,.07)}
html[data-theme=dark] .trow.on,html[data-theme=dark] .tag-item.on{background:var(--hl)}
html[data-theme=dark] .trow.lvs .tlabel{color:#bcd0ea}
html[data-theme=dark] .tact button{color:#93a3b8}html[data-theme=dark] .tact button:hover{background:#24334b;color:var(--text)}
html[data-theme=dark] .tchildren{border-left-color:var(--line)}
html[data-theme=dark] .cnt{color:#cbd5e1}html[data-theme=dark] .cnt.open{background:rgba(248,113,113,.18);color:#fca5a5}
html[data-theme=dark] .viewport{background-color:#0c1420;background-image:linear-gradient(45deg,#101a2a 25%,transparent 25%,transparent 75%,#101a2a 75%),linear-gradient(45deg,#101a2a 25%,transparent 25%,transparent 75%,#101a2a 75%)}
html[data-theme=dark] .modal{background:var(--panel)}
html[data-theme=dark] .status-seg button{background:var(--panel2)}
html[data-theme=dark] .status-seg button.on{background:var(--c);color:#fff}
html[data-theme=dark] .ph{background:#1a2536}
html[data-theme=dark] .col{background:#0f1826}
html[data-theme=dark] .kcard,html[data-theme=dark] .icard,html[data-theme=dark] .feat{background:var(--panel)}
html[data-theme=dark] .rtree .rrow.lay{background:#101a28}
html[data-theme=dark] .selbar,html[data-theme=dark] .bulkbar{background:rgba(245,158,11,.10);border-color:rgba(245,158,11,.35)}
html[data-theme=dark] .feat .fi{background:var(--hl);color:var(--hlt)}
html[data-theme=dark] .legal{color:#c9d4e2}
html[data-theme=dark] .empty-sm a{color:var(--hlt)}
html[data-theme=dark] .m-head::before{background:#475569}
html[data-theme=dark] .spin.dark{border-color:rgba(255,255,255,.15);border-top-color:var(--accent)}
html[data-theme=dark] .slot-pos{background:#33435b}
html[data-theme=dark] .credit{color:#7d8ca1}
html[data-theme=dark] .mk-wrap{background:#05090f}
html[data-theme=dark] .lightbox{background:rgba(0,0,0,.94)}
html[data-theme=dark] .ov{background:rgba(0,0,0,.6)}
html[data-theme=dark] .logo-strip img,html[data-theme=dark] .logo-prev{background:#fff}
html[data-theme=dark] ::-webkit-scrollbar{width:10px;height:10px}html[data-theme=dark] ::-webkit-scrollbar-thumb{background:#2a384e;border-radius:6px}html[data-theme=dark] ::-webkit-scrollbar-track{background:transparent}
"""
R("</style>\n</head>", DARK + "</style>\n</head>")

# --- icons ---
R("  more:'<circle", """  moon:'<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
  sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  contrast:'<circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/>',
  more:'<circle""")

# --- theme logic (next to display size) ---
R("applyDisplayScale();\naddEventListener('orientationchange'", r"""applyDisplayScale();
/* ---------- theme: Auto (system) / Light / Dark, stored per device ---------- */
const THEMES = [['auto', 'contrast', 'Auto (system)'], ['light', 'sun', 'Light'], ['dark', 'moon', 'Dark']];
function getThemePref() { try { return localStorage.getItem('sitecore.theme') || 'auto'; } catch (e) { return 'auto'; } }
const themeNow = () => { const t = getThemePref(); return t === 'auto' ? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light') : t; };
function applyTheme() { document.documentElement.dataset.theme = themeNow(); if (typeof styleSystemBars === 'function') styleSystemBars(); const b = document.getElementById('themeBtn'); if (b) b.innerHTML = ic(themeNow() === 'dark' ? 'moon' : 'sun'); }
function setThemePref(v) { try { localStorage.setItem('sitecore.theme', v); } catch (e) {} applyTheme(); }
try { matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => { if (getThemePref() === 'auto') applyTheme(); }); } catch (e) {}
applyTheme();
addEventListener('orientationchange'""")

# --- Android system bars follow the theme ---
R("""    const SB = capPlugin('SystemBars');
    const styleBars = () => { if (!SB) return;
      const edge = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--safe-area-inset-top')) > 0; // page drawn behind the bars
      SB.setStyle({style:'DARK', bar:'StatusBar'}).catch(() => {}); SB.setStyle({style:edge ? 'LIGHT' : 'DARK', bar:'NavigationBar'}).catch(() => {}); };
    styleBars(); setTimeout(styleBars, 800); addEventListener('resize', () => setTimeout(styleBars, 300));""",
"""    const SB = capPlugin('SystemBars');
    window.styleSystemBars = () => { if (!SB) return;
      const edge = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--safe-area-inset-top')) > 0; // page drawn behind the bars
      SB.setStyle({style:'DARK', bar:'StatusBar'}).catch(() => {}); SB.setStyle({style:edge && themeNow() === 'light' ? 'LIGHT' : 'DARK', bar:'NavigationBar'}).catch(() => {}); };
    styleSystemBars(); setTimeout(styleSystemBars, 800); addEventListener('resize', () => setTimeout(styleSystemBars, 300));""")

# --- top bar quick toggle (desktop / tablet) ---
R("""    <button class="user-chip" id="userChip">""", """    <button class="btn ghost sm" id="themeBtn" title="Theme"></button>
    <button class="user-chip" id="userChip">""")
R("  $('#newProj').onclick = newProject;", "  $('#themeBtn').onclick = () => setThemePref(themeNow() === 'dark' ? 'light' : 'dark'); applyTheme();\n  $('#newProj').onclick = newProject;")
R("  $('#pkgImport').title = L('Import a SiteCore project package');", "  $('#pkgImport').title = L('Import a SiteCore project package'); $('#themeBtn').title = L('Theme'); $('#themeBtn').setAttribute('aria-label', L('Theme'));")
R("  #langSel{display:none}", "  #langSel,#themeBtn{display:none}")

# --- More sheet + Settings ---
R("['_lang', 'globe', L('Language') + ': ' + LANGS[LANG]]);", "['_lang', 'globe', L('Language') + ': ' + LANGS[LANG]], ['_theme', themeNow() === 'dark' ? 'moon' : 'sun', L('Theme') + ': ' + L(THEMES.find(t => t[0] === getThemePref())[2])]);")
R("  if (k === '_lang') {", "  if (k === '_theme') { const t = await actionSheet(L('Theme'), THEMES.map(([v, icon, lab]) => [v, icon, L(lab), false, v === getThemePref()])); if (t) setThemePref(t); return; }\n  if (k === '_lang') {")
R("""        <label class="fl">${L('Display size (this device)')}""", """        <label class="fl">${L('Theme')}<select id="uTheme">${opt(THEMES.map(([v, , lab]) => [v, L(lab)]), getThemePref())}</select></label>
        <label class="fl">${L('Display size (this device)')}""")
R("  $('#uScale').onchange = e =>", "  $('#uTheme').onchange = e => setThemePref(e.target.value);\n  $('#uScale').onchange = e =>")
open('src.html', 'w', encoding='utf-8').write(s)

tr = json.load(open('tr.json', encoding='utf-8'))
tr.update({"Theme": ["ຮູບແບບສີ", "ธีม"], "Auto (system)": ["ອັດຕະໂນມັດ (ຕາມລະບົບ)", "อัตโนมัติ (ตามระบบ)"], "Light": ["ສະຫວ່າງ", "สว่าง"], "Dark": ["ມືດ", "มืด"]})
json.dump(tr, open('tr.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
k = open('keys.py', encoding='utf-8').read()
k = k.replace("'Small phone','Phone','Tablet','Computer',", "'Small phone','Phone','Tablet','Computer','Auto (system)','Light','Dark',")
open('keys.py', 'w', encoding='utf-8').write(k)
print('patched')
