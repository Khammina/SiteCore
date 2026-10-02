"""Builds Google Play store listing graphics in ../store/
   - icon-512.png             (app icon, 512x512)
   - feature-graphic.png      (1024x500)
   - phone/NN_*.png           (1080x1920 framed screenshots with captions)
   - tablet/NN_*.png          (1600x2560 framed screenshots)
Input: raw screenshots (store_ph_*.png, store_tb_*.png) captured from the app.
Usage: python tools/make_store_assets.py <raw-screenshot-folder>
"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = sys.argv[1] if len(sys.argv) > 1 else '.'
OUT = os.path.join(ROOT, 'store'); os.makedirs(os.path.join(OUT, 'phone'), exist_ok=True); os.makedirs(os.path.join(OUT, 'tablet'), exist_ok=True)
NAVY, NAVY2, ACCENT = (15, 31, 53), (35, 64, 107), (245, 158, 11)

def font(sz, bold=True):
    for f in (['C:/Windows/Fonts/segoeuib.ttf', 'C:/Windows/Fonts/arialbd.ttf'] if bold else ['C:/Windows/Fonts/segoeui.ttf', 'C:/Windows/Fonts/arial.ttf']):
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()

def gradient(w, h):
    im = Image.new('RGB', (w, h), NAVY); d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h; d.line([(0, y), (w, y)], fill=tuple(int(NAVY[i] + (NAVY2[i] - NAVY[i]) * t * .9) for i in range(3)))
    return im

def mark(size):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * .24), fill=ACCENT)
    d.text((size / 2, size / 2 + size * .02), 'SC', font=font(int(size * .44)), fill=NAVY, anchor='mm')
    return im

def rounded(img, r):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=r, fill=255)
    out = Image.new('RGBA', img.size); out.paste(img, (0, 0), m); return out

def framed(raw, size, title, sub):
    W, H = size; bg = gradient(W, H).convert('RGBA'); d = ImageDraw.Draw(bg)
    pad = int(W * .07); ty = int(H * .055)
    d.text((W / 2, ty), title, font=font(int(W * .062)), fill='white', anchor='ma')
    d.text((W / 2, ty + int(W * .085)), sub, font=font(int(W * .033), False), fill=(203, 213, 225), anchor='ma')
    shot = Image.open(raw).convert('RGB'); top = ty + int(W * .16)
    sw = W - pad * 2; sh = int(shot.height * sw / shot.width); shot = shot.resize((sw, sh), Image.LANCZOS)
    avail = H - top; shot = rounded(shot.crop((0, 0, sw, min(sh, avail + 40))), int(W * .035))
    shadow = Image.new('RGBA', (shot.width + 80, shot.height + 80), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([40, 40, 40 + shot.width, 40 + shot.height], radius=int(W * .035), fill=(0, 0, 0, 120))
    bg.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(22)), (pad - 40, top - 30))
    bg.alpha_composite(shot, (pad, top))
    d.rectangle([0, H - 10, W, H], fill=ACCENT)
    return bg.convert('RGB')

PHONE = [('1_dashboard', 'Your whole site at a glance', 'Open items, overdue work and progress by discipline'),
         ('2_plan', 'Tag issues on the plan', 'Import PDF / JPG drawings and pin defects exactly'),
         ('3_tag', 'Photos, status and owners', 'Before / After photos, markup, due dates'),
         ('4_punchlist', 'Punch list that works in the field', 'Filter, bulk update and export to Excel / PDF'),
         ('5_reports', 'Reports from any level', 'Discipline, floor or sub-system in one tap'),
         ('6_preview', 'Professional PDF reports', 'Your logos, plans, tag details and photos')]
TABLET = [('1_dashboard', 'Built for site and office', 'Dashboard, drawings and reports on tablet'),
          ('2_plan', 'Drawing register', 'Discipline > Floor > Sub-system > Layout'),
          ('3_preview', 'Preview before you share', 'Branded PDF reports in English, Lao and Thai')]
for k, (n, t, s) in enumerate(PHONE, 1):
    framed(os.path.join(RAW, f'store_ph_{n}.png'), (1080, 1920), t, s).save(os.path.join(OUT, 'phone', f'{k:02d}_{n[2:]}.png'))
for k, (n, t, s) in enumerate(TABLET, 1):
    framed(os.path.join(RAW, f'store_tb_{n}.png'), (1600, 2560), t, s).save(os.path.join(OUT, 'tablet', f'{k:02d}_{n[2:]}.png'))

# app icon 512 (Play: 512x512, 32-bit PNG) - full-bleed square; Play applies its own rounding
ic = Image.new('RGBA', (512, 512), NAVY + (255,)); m = mark(300); ic.alpha_composite(m, (106, 106)); ic.save(os.path.join(OUT, 'icon-512.png'))

# feature graphic 1024x500
fg = gradient(1024, 500).convert('RGBA'); d = ImageDraw.Draw(fg)
fg.alpha_composite(mark(96), (64, 120))
d.text((180, 128), 'SiteCore', font=font(64), fill='white')
d.text((66, 248), 'Punch lists, inspections and', font=font(30, False), fill=(226, 232, 240))
d.text((66, 288), 'professional PDF reports', font=font(30, False), fill=(226, 232, 240))
d.text((66, 328), 'for construction & MEP teams.', font=font(30, False), fill=(226, 232, 240))
d.rectangle([66, 392, 186, 398], fill=ACCENT)
d.text((66, 414), 'Works offline  ·  English / Lao / Thai', font=font(20, False), fill=(148, 163, 184))
shot = Image.open(os.path.join(RAW, 'store_ph_2_plan.png')).convert('RGB'); sw = 300; shot = shot.resize((sw, int(shot.height * sw / shot.width)), Image.LANCZOS).crop((0, 0, sw, 560))
shot = rounded(shot, 26); sh = Image.new('RGBA', (sw + 60, 600), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([30, 30, 30 + sw, 590], radius=26, fill=(0, 0, 0, 140))
fg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), (640, 20)); fg.alpha_composite(shot, (670, 46))
fg.convert('RGB').save(os.path.join(OUT, 'feature-graphic.png'))
print('store assets written to', OUT)
