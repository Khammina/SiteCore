"""Assembles the public website in ../website (upload this folder to any static HTTPS host):
   website/index.html      landing page          (from website-src/)
   website/privacy.html    privacy policy        (URL needed for Google Play)
   website/app/            the web app (PWA)     (copy of www/)
   website/download/       SiteCore.apk
   website/assets/         images
"""
import os, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, OUT, STORE = os.path.join(ROOT, 'website-src'), os.path.join(ROOT, 'website'), os.path.join(ROOT, 'store')
if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, 'assets')); os.makedirs(os.path.join(OUT, 'download'))
for f in ('index.html', 'privacy.html'): shutil.copy(os.path.join(SRC, f), OUT)
shutil.copytree(os.path.join(ROOT, 'www'), os.path.join(OUT, 'app'))
A = os.path.join(OUT, 'assets')
shutil.copy(os.path.join(ROOT, 'www', 'icons', 'icon-192.png'), A)
shutil.copy(os.path.join(STORE, 'feature-graphic.png'), A)
raw = os.path.join(STORE, 'raw')
for src, dst in (('store_ph_1_dashboard.png', 'shot-dashboard.png'), ('store_ph_2_plan.png', 'shot-plan.png'), ('store_tb_3_preview.png', 'shot-preview.png')):
    shutil.copy(os.path.join(raw, src), os.path.join(A, dst))
for k, f in enumerate(sorted(os.listdir(os.path.join(STORE, 'phone'))), 1):
    shutil.copy(os.path.join(STORE, 'phone', f), os.path.join(A, f's{k}.png'))
apk = os.path.join(ROOT, 'SiteCore.apk')
if os.path.exists(apk): shutil.copy(apk, os.path.join(OUT, 'download', 'SiteCore.apk'))
# report preview image: crop the tall tablet capture to a 4:5 area
from PIL import Image
pv = os.path.join(A, 'shot-preview.png'); im = Image.open(pv); im.crop((0, 0, im.width, int(im.width * 1.25))).save(pv)
# optimise images for the web
for f in os.listdir(A):
    p = os.path.join(A, f)
    if f.endswith('.png') and f not in ('icon-192.png',):
        im = Image.open(p); im.thumbnail((1200, 2200)); im.save(p, optimize=True)
print('website built:', OUT)
