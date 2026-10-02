"""Builds SiteCoreSans (Latin + Lao + Thai) static fonts for jsPDF.
jsPDF has no OpenType shaping, so zero-advance Lao marks are shifted left to sit over the preceding base
(Thai marks in Noto already carry negative offsets)."""
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset, merge
import base64, os

uni = list(range(0x20, 0x7F)) + list(range(0xA0, 0x180)) + list(range(0x0E00, 0x0F00)) + \
      [0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026, 0x203A, 0x2039, 0x2192, 0x2190, 0x00B7, 0x20AC, 0x2122]

def shift_lao_marks(f):
    glyf, hmtx, cmap = f['glyf'], f['hmtx'], f.getBestCmap()
    base_adv = hmtx[cmap[0x0E81]][0]  # typical Lao consonant width
    done = set()
    for cp, g in cmap.items():
        if not (0x0E80 <= cp < 0x0F00) or g in done: continue
        adv, lsb = hmtx[g]; gl = glyf[g]
        if adv != 0 or gl.numberOfContours == 0: continue
        gl.recalcBounds(glyf)
        dx = round(-base_adv / 2 - (gl.xMin + gl.xMax) / 2)
        if gl.isComposite():
            for c in gl.components: c.x += dx
        else:
            coords = gl.coordinates; coords.translate((dx, 0))
        gl.recalcBounds(glyf); hmtx[g] = (0, gl.xMin); done.add(g)
    return len(done)

out = {}
for w, name in [(400, 'Regular'), (700, 'Bold')]:
    parts = []
    for src, tag in [('gLao.ttf', 'lao'), ('gThai.ttf', 'thai')]:
        f = instancer.instantiateVariableFont(TTFont(src), {'wght': w, 'wdth': 100})
        if tag == 'lao': print(name, 'lao marks shifted:', shift_lao_marks(f))
        o = subset.Options(); o.layout_features = []; o.hinting = False; o.drop_tables += ['GSUB', 'GPOS', 'GDEF', 'STAT', 'DSIG']; o.notdef_outline = True; o.name_IDs = ['*']
        s = subset.Subsetter(o)
        cps = [c for c in uni if (tag == 'lao' and not (0x0E00 <= c < 0x0E80)) or (tag == 'thai' and 0x0E00 <= c < 0x0E80)]
        s.populate(unicodes=cps); s.subset(f)
        p = f'{tag}_{name}.ttf'; f.save(p); parts.append(p)
    m = merge.Merger().merge(parts); fn = f'SiteCoreSans-{name}.ttf'; m.save(fn)
    out[name] = base64.b64encode(open(fn, 'rb').read()).decode()
    print(fn, os.path.getsize(fn))
open('fonts.js', 'w').write("const SC_FONTS={regular:'%s',bold:'%s'};" % (out['Regular'], out['Bold']))
