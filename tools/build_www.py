"""Builds the installable / offline web package in ../www from ../SiteCore.html.

  - CDN libraries -> local lib/ (works offline and inside the Android app)
  - PWA: manifest, icons, service worker (offline cache)
Run:  python tools/build_www.py
"""
import json, os, re
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WWW = os.path.join(ROOT, 'www')
VERSION = '1.09'
NAVY, ACCENT = (15, 31, 53), (245, 158, 11)

html = open(os.path.join(ROOT, 'SiteCore.html'), encoding='utf-8').read()
CDN = 'https://cdnjs.cloudflare.com/ajax/libs/'
for lib in ['pdf.js/3.11.174/pdf.min.js', 'pdf.js/3.11.174/pdf.worker.min.js', 'jspdf/2.5.1/jspdf.umd.min.js', 'jspdf-autotable/3.8.2/jspdf.plugin.autotable.min.js']:
    html = html.replace(CDN + lib, 'lib/' + lib.split('/')[-1])
assert CDN not in html, 'CDN reference left'
# Capacitor core (native plugin proxies for the Android app); harmless in a normal browser
cap_src = os.path.join(ROOT, 'android-app', 'node_modules', '@capacitor', 'core', 'dist', 'capacitor.js')
if os.path.exists(cap_src):
    import shutil; os.makedirs(os.path.join(WWW, 'lib'), exist_ok=True); shutil.copy(cap_src, os.path.join(WWW, 'lib', 'capacitor.js'))
html = html.replace('<script src="lib/pdf.min.js"></script>', '<script src="lib/capacitor.js"></script>\n<script src="lib/pdf.min.js"></script>', 1)
html = re.sub(r'<link rel="preconnect"[^>]*>\n?', '', html)
html = re.sub(r'<link href="https://fonts.googleapis.com[^>]*>\n?', '', html)  # offline: system Lao/Thai fonts are used
html = html.replace('<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
    '<meta name="theme-color" content="#0f1f35">\n<meta name="mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-title" content="SiteCore">\n'
    '<link rel="manifest" href="manifest.webmanifest">\n<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">\n'
    '<link rel="apple-touch-icon" href="icons/icon-192.png">')
os.makedirs(os.path.join(WWW, 'icons'), exist_ok=True)
open(os.path.join(WWW, 'index.html'), 'w', encoding='utf-8').write(html)

def font(sz):
    for f in ['C:/Windows/Fonts/segoeuib.ttf', 'C:/Windows/Fonts/arialbd.ttf']:
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()

def icon(size, maskable=False, fg_only=False, bg=True):
    """SiteCore mark: navy tile, amber rounded square, navy 'SC'."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if bg and not fg_only:
        if maskable: d.rectangle([0, 0, size, size], fill=NAVY)
        else: d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * .22), fill=NAVY)
    inset = size * (0.26 if (maskable or fg_only) else 0.16)
    d.rounded_rectangle([inset, inset, size - inset, size - inset], radius=int(size * .12), fill=ACCENT)
    f = font(int(size * (0.26 if (maskable or fg_only) else 0.33)))
    d.text((size / 2, size / 2 + size * .01), 'SC', font=f, fill=NAVY, anchor='mm')
    return im

for sz in (192, 512): icon(sz).save(os.path.join(WWW, 'icons', f'icon-{sz}.png'))
icon(512, maskable=True).save(os.path.join(WWW, 'icons', 'icon-maskable-512.png'))

json.dump({
    'name': 'SiteCore — Field Quality & Punch List', 'short_name': 'SiteCore', 'id': './', 'start_url': './', 'scope': './',
    'display': 'standalone', 'orientation': 'any', 'background_color': '#eef1f6', 'theme_color': '#0f1f35',
    'description': 'Construction drawings, punch lists, inspections and PDF reports.',
    'icons': [{'src': 'icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
              {'src': 'icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
              {'src': 'icons/icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}]
}, open(os.path.join(WWW, 'manifest.webmanifest'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

SHELL = ['./', 'index.html', 'manifest.webmanifest', 'icons/icon-192.png', 'icons/icon-512.png', 'icons/icon-maskable-512.png',
         'lib/capacitor.js', 'lib/pdf.min.js', 'lib/pdf.worker.min.js', 'lib/jspdf.umd.min.js', 'lib/jspdf.plugin.autotable.min.js']
open(os.path.join(WWW, 'sw.js'), 'w', encoding='utf-8').write(f"""/* SiteCore service worker: offline app shell (cache-first, refreshed in background). */
const CACHE = 'sitecore-{VERSION}';
const SHELL = {json.dumps(SHELL)};
self.addEventListener('install', e => {{ e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); }});
self.addEventListener('activate', e => {{ e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); }});
self.addEventListener('fetch', e => {{
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(caches.match(e.request, {{ignoreSearch: true}}).then(hit => {{
    const net = fetch(e.request).then(r => {{ if (r.ok) caches.open(CACHE).then(c => c.put(e.request, r.clone())); return r; }}).catch(() => hit);
    return hit || net;
  }}));
}});
""")
# Android launcher icons (used by tools/build_apk.ps1 after `npx cap add android`)
res = os.path.join(ROOT, 'android-app', 'android', 'app', 'src', 'main', 'res')
if os.path.isdir(res):
    for q, sz in {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}.items():
        d = os.path.join(res, f'mipmap-{q}'); os.makedirs(d, exist_ok=True)
        icon(sz).save(os.path.join(d, 'ic_launcher.png'))
        rnd = Image.new('RGBA', (sz, sz), (0, 0, 0, 0)); m = Image.new('L', (sz, sz), 0); ImageDraw.Draw(m).ellipse([0, 0, sz - 1, sz - 1], fill=255)
        full = icon(sz, maskable=True); rnd.paste(full, (0, 0), m); rnd.save(os.path.join(d, 'ic_launcher_round.png'))
        fg = round(sz * 108 / 48); icon(fg, fg_only=True).save(os.path.join(d, 'ic_launcher_foreground.png'))
    bgxml = os.path.join(res, 'values', 'ic_launcher_background.xml')
    if os.path.exists(bgxml): open(bgxml, 'w').write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#0F1F35</color>\n</resources>\n')
    # themed (monochrome) icon for Android 13+: alpha silhouette of the mark
    for q, sz in {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}.items():
        fg = round(sz * 108 / 48); m = Image.new('RGBA', (fg, fg), (0, 0, 0, 0)); d = ImageDraw.Draw(m); inset = fg * 0.26
        d.rounded_rectangle([inset, inset, fg - inset, fg - inset], radius=int(fg * .12), fill=(255, 255, 255, 255))
        d.text((fg / 2, fg / 2 + fg * .01), 'SC', font=font(int(fg * 0.26)), fill=(0, 0, 0, 0), anchor='mm')
        m.save(os.path.join(res, f'mipmap-{q}', 'ic_launcher_monochrome.png'))
    # splash screens: navy background with the SiteCore mark (replaces the Capacitor default)
    for dp, _, files in os.walk(res):
        for fn in files:
            if fn == 'splash.png':
                path = os.path.join(dp, fn); w, h = Image.open(path).size
                sp = Image.new('RGB', (w, h), NAVY); m = int(min(w, h) * 0.34)
                mark = icon(m, fg_only=True); sp.paste(mark, ((w - m) // 2, (h - m) // 2), mark); sp.save(path)
    print('android icons + splash updated')
print('www built:', WWW)
