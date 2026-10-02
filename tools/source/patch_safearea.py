# v1.02 patch: safe areas (notch / Dynamic Island / system bars), per-device auto scale, Android bar styling.
import json
s = open('src.html', encoding='utf-8').read()
def R(a, b):
    global s
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b)

# ---- safe-area variables ----
R("  --r:10px;\n}", """  --r:10px;
  /* Safe areas: Capacitor injects --safe-area-inset-* (Android); browsers / iOS provide env(). Divided by the page scale. */
  --ps:1;
  --it:calc(var(--safe-area-inset-top, env(safe-area-inset-top, 0px)) / var(--ps));
  --ib:calc(var(--safe-area-inset-bottom, env(safe-area-inset-bottom, 0px)) / var(--ps));
  --il:calc(var(--safe-area-inset-left, env(safe-area-inset-left, 0px)) / var(--ps));
  --ir:calc(var(--safe-area-inset-right, env(safe-area-inset-right, 0px)) / var(--ps));
}""")
R(".top{height:56px;background:var(--navy);color:#fff;display:flex;align-items:center;gap:14px;padding:0 14px;border-bottom:3px solid var(--accent)}",
  ".top{height:calc(56px + var(--it));background:var(--navy);color:#fff;display:flex;align-items:center;gap:14px;padding:var(--it) calc(14px + var(--ir)) 0 calc(14px + var(--il));border-bottom:3px solid var(--accent)}")
R(".shell{display:grid;grid-template-columns:220px 1fr;height:calc(100vh / var(--z, 1) - 56px)}",
  ".shell{display:grid;grid-template-columns:220px 1fr;height:calc(100vh / var(--z, 1) - 56px - var(--it));height:calc(100dvh / var(--z, 1) - 56px - var(--it));padding:0 var(--ir) var(--ib) var(--il)}")
R(".ov{position:fixed;inset:0;background:rgba(10,20,35,.55);display:flex;align-items:center;justify-content:center;z-index:100;padding:16px}",
  ".ov{position:fixed;inset:0;background:rgba(10,20,35,.55);display:flex;align-items:center;justify-content:center;z-index:100;padding:calc(16px + var(--it)) calc(16px + var(--ir)) calc(16px + var(--ib)) calc(16px + var(--il))}")
R("max-height:calc(100vh / var(--z, 1) - 32px);display:flex;flex-direction:column;box-shadow",
  "max-height:calc(100dvh / var(--z, 1) - 32px - var(--it) - var(--ib));display:flex;flex-direction:column;box-shadow")
R(".lightbox{position:fixed;inset:0;background:rgba(0,0,0,.9);z-index:200;display:flex;align-items:center;justify-content:center;cursor:zoom-out}",
  ".lightbox{position:fixed;inset:0;background:rgba(0,0,0,.9);z-index:200;display:flex;align-items:center;justify-content:center;cursor:zoom-out;padding:var(--it) var(--ir) var(--ib) var(--il)}")
R(".pv{position:fixed;inset:0;z-index:150;background:#3a4250;display:flex;flex-direction:column}",
  ".pv{position:fixed;inset:0;z-index:150;background:#3a4250;display:flex;flex-direction:column;padding:0 var(--ir) var(--ib) var(--il);border-top:var(--it) solid var(--navy)}")
R("#toasts{position:fixed;right:16px;bottom:16px;", "#toasts{position:fixed;right:calc(16px + var(--ir));bottom:calc(16px + var(--ib));")
R("  .shell{grid-template-columns:1fr;grid-template-rows:1fr auto}\n  nav{flex-direction:row;order:2;border-right:0;border-top:1px solid var(--line);padding:4px;overflow-x:auto}",
  "  .shell{grid-template-columns:1fr;grid-template-rows:1fr auto;padding:0 var(--ir) 0 var(--il)}\n  nav{flex-direction:row;order:2;border-right:0;border-top:1px solid var(--line);padding:4px 4px calc(4px + var(--ib));overflow-x:auto}")

# ---- auto scale per device class ----
R("""/* ---------- display size (auto resolution) ----------
   Auto = 90% on every device. Phones / tablets / Android app: page scale via <meta viewport> (native browser zoom).
   Desktop browsers ignore that, so they use CSS zoom; layout heights use --z to stay full-screen. Stored per device. */
const SCALES = [['auto', 'Auto (90%)'], ['80', '80%'], ['85', '85%'], ['90', '90%'], ['100', '100%'], ['110', '110%'], ['120', '120%']];""",
"""/* ---------- display size (auto resolution) ----------
   Auto picks a scale per device class (short screen side in CSS px):
     small phone < 360 -> 85% | phone < 700 -> 90% | tablet 700-1100 -> fits the full desktop layout (85-90%) | PC -> 90%.
   Phones / tablets / Android app: page scale via <meta viewport> (native browser zoom).
   Desktop browsers ignore that, so they use CSS zoom; layout heights use --z to stay full-screen. Stored per device. */
const SCALES = [['auto', 'Auto'], ['80', '80%'], ['85', '85%'], ['90', '90%'], ['100', '100%'], ['110', '110%'], ['120', '120%']];
const isTouchDevice = () => (window.Capacitor && Capacitor.isNativePlatform && Capacitor.isNativePlatform()) || (matchMedia('(pointer:coarse)').matches && Math.min(screen.width, screen.height) < 1100);
function deviceClass() { const s = Math.min(screen.width, screen.height); return !isTouchDevice() ? 'pc' : s < 360 ? 'small-phone' : s < 700 ? 'phone' : 'tablet'; }
function autoScale() {
  const s = Math.min(screen.width, screen.height), c = deviceClass();
  if (c === 'small-phone') return 0.85;
  if (c === 'phone' || c === 'pc') return 0.9;
  return Math.round(Math.max(0.85, Math.min(0.9, s / 900)) * 100) / 100; // tablet: portrait width >= ~900 css px -> side-menu layout
}""")
R("const scaleValue = () => { const v = getScalePref(); return v === 'auto' ? 0.9 : (+v || 100) / 100; };",
  "const scaleValue = () => { const v = getScalePref(); return v === 'auto' ? autoScale() : (+v || 100) / 100; };")
R("  const k = scaleValue(), touch = (window.Capacitor && Capacitor.isNativePlatform && Capacitor.isNativePlatform()) || (matchMedia('(pointer:coarse)').matches && Math.min(screen.width, screen.height) < 1100);",
  "  const k = scaleValue(), touch = isTouchDevice();")
R("root.style.zoom = ''; root.style.setProperty('--z', 1); }", "root.style.zoom = ''; root.style.setProperty('--z', 1); root.style.setProperty('--ps', k); }")
R("root.style.zoom = k === 1 ? '' : k; root.style.setProperty('--z', k); }", "root.style.zoom = k === 1 ? '' : k; root.style.setProperty('--z', k); root.style.setProperty('--ps', 1); }")
R("applyDisplayScale();\n/* ---------- platform layer", "applyDisplayScale();\naddEventListener('orientationchange', () => setTimeout(applyDisplayScale, 250));\n/* ---------- platform layer")
R("opt(SCALES.map(([v, t]) => [v, v === 'auto' ? L('Auto') + ' (90%)' : t]), getScalePref())",
  "opt(SCALES.map(([v, t]) => [v, v === 'auto' ? `${L('Auto')} (${Math.round(autoScale() * 100)}% · ${L({'small-phone':'Small phone', phone:'Phone', tablet:'Tablet', pc:'Computer'}[deviceClass()])})` : t]), getScalePref())")
R("L('Auto fits the screen resolution at 90%. Choose a size if text looks too small or too large.')",
  "L('Auto fits this screen: 85% small phone, 90% phone, 85–90% tablet, 90% computer. Choose a size if text looks too small or too large.')")

# ---- Android system bars ----
R("  const AppP = IS_NATIVE && capPlugin('App');", """  if (IS_NATIVE) { // navy status bar with light icons; gesture-bar icons matched to what is behind them
    const SB = capPlugin('SystemBars');
    const styleBars = () => { if (!SB) return;
      const edge = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--safe-area-inset-top')) > 0; // page drawn behind the bars
      SB.setStyle({style:'DARK', bar:'StatusBar'}).catch(() => {}); SB.setStyle({style:edge ? 'LIGHT' : 'DARK', bar:'NavigationBar'}).catch(() => {}); };
    styleBars(); setTimeout(styleBars, 800); addEventListener('resize', () => setTimeout(styleBars, 300));
  }
  const AppP = IS_NATIVE && capPlugin('App');""")
open('src.html', 'w', encoding='utf-8').write(s)

tr = json.load(open('tr.json', encoding='utf-8'))
tr.pop("Auto fits the screen resolution at 90%. Choose a size if text looks too small or too large.", None)
tr.update({
 "Auto fits this screen: 85% small phone, 90% phone, 85–90% tablet, 90% computer. Choose a size if text looks too small or too large.":
   ["ອັດຕະໂນມັດ ປັບໃຫ້ພໍດີກັບໜ້າຈໍ: 85% ໂທລະສັບນ້ອຍ, 90% ໂທລະສັບ, 85–90% ແທັບເລັດ, 90% ຄອມພິວເຕີ. ເລືອກຂະໜາດອື່ນຖ້າຕົວອັກສອນນ້ອຍ ຫຼື ໃຫຍ່ເກີນໄປ.",
    "อัตโนมัติปรับให้พอดีกับหน้าจอ: 85% โทรศัพท์เล็ก, 90% โทรศัพท์, 85–90% แท็บเล็ต, 90% คอมพิวเตอร์ เลือกขนาดอื่นหากตัวอักษรเล็กหรือใหญ่เกินไป"],
 "Small phone": ["ໂທລະສັບນ້ອຍ", "โทรศัพท์เล็ก"], "Phone": ["ໂທລະສັບ", "โทรศัพท์"], "Tablet": ["ແທັບເລັດ", "แท็บเล็ต"], "Computer": ["ຄອມພິວເຕີ", "คอมพิวเตอร์"]})
json.dump(tr, open('tr.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
k = open('keys.py', encoding='utf-8').read()
k = k.replace("'Left','Centre','Right']", "'Left','Centre','Right','Small phone','Phone','Tablet','Computer']")
open('keys.py', 'w', encoding='utf-8').write(k)
print('patched')
