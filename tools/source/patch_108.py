# v1.08: auto-fit bottom tab labels; punch list detail pages: portrait / landscape + 1-4 tags per page (responsive tag block).
import json, re
s = open('src.html', encoding='utf-8').read()
def R(a, b):
    global s
    assert s.count(a) == 1, a[:100]
    s = s.replace(a, b)

# ---------- bottom tab bar: equal widths, labels scale with the screen ----------
R("  nav{flex-direction:row;order:2;border-right:0;border-top:1px solid var(--line);padding:4px 4px calc(4px + var(--ib));overflow-x:auto}\n  .nav-i{flex-direction:column;gap:0;padding:6px 8px;font-size:10.5px;min-width:64px;text-align:center}",
  "  nav{flex-direction:row;order:2;border-right:0;border-top:1px solid var(--line);padding:4px 2px calc(4px + var(--ib));overflow:hidden;gap:0}\n"
  "  .nav-i{flex:1 1 0;min-width:0;flex-direction:column;gap:2px;padding:6px 2px;font-size:clamp(9px, 2.7vw, 12px);line-height:1.15;text-align:center;justify-content:flex-start}\n"
  "  .nav-i .nt{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;overflow-wrap:anywhere;max-width:100%}\n"
  "  .nav-i .ic{width:auto}")

# ---------- report options ----------
R("perPage:2, maxPhotos:3,", "perPage:2, detailOrient:'portrait', maxPhotos:3,")
R("""        <label class="fl">${L('Tags per detail page')}<select data-o="perPage">${opt([[1, '1 — ' + L('large photos')], [2, '2 — ' + L('compact')]], o.perPage)}</select></label></div>""",
  """        <label class="fl">${L('Tags per detail page')}<select data-o="perPage">${opt([[1, '1 — ' + L('large photos')], [2, '2'], [3, '3'], [4, '4 — ' + L('compact')]], o.perPage)}</select></label></div>
        <label class="fl">${L('Detail page orientation')}<select data-o="detailOrient">${opt([['portrait', L('Portrait')], ['landscape', L('Landscape')]], o.detailOrient)}</select></label>""")
R("k === 'perPage' ? 'Tags per detail page' : 'Max photos per tag'", "k === 'perPage' ? 'Tags per detail page' : k === 'detailOrient' ? 'Detail page orientation' : 'Max photos per tag'")
R("${sel('perPage', [[1, '1'], [2, '2']])}", "${sel('perPage', [[1, '1'], [2, '2'], [3, '3'], [4, '4']])}${sel('detailOrient', [['portrait', L('Portrait')], ['landscape', L('Landscape')]])}")

# ---------- detail pages ----------
a = s.index("async function drawDetails(doc, C, iss, o, meta, im) {"); b = s.index("function drawCover(")
NEW = r'''/** Detail page grid [columns, rows] per orientation and tags per page. */
const DETAIL_GRID = {portrait:{1:[1, 1], 2:[1, 2], 3:[1, 3], 4:[2, 2]}, landscape:{1:[1, 1], 2:[2, 1], 3:[3, 1], 4:[2, 2]}};
async function drawDetails(doc, C, iss, o, meta, im) {
  const per = Math.max(1, Math.min(4, +o.perPage || 2)), orient = o.detailOrient === 'landscape' ? 'landscape' : 'portrait', [cols, rows] = DETAIL_GRID[orient][per];
  for (let k = 0; k < iss.length; k++) {
    const slot = k % per;
    if (slot === 0) { doc.addPage(o.size, orient); pdfHeader(doc, `${rTitle()} — ${L('PUNCH LIST DETAILS')}`, pathOf(C.l.id), hdrRight(meta, `${L('Tags')} ${k + 1}–${Math.min(k + per, iss.length)} / ${iss.length}`), meta); }
    const W = pw(doc), H = ph(doc), top = PDF_TOP, bottom = H - 12, gap = 4;
    const bw = (W - 20 - (cols - 1) * gap) / cols, bh = (bottom - top - (rows - 1) * gap) / rows;
    await drawTagBlock(doc, 10 + (slot % cols) * (bw + gap), top + Math.floor(slot / cols) * (bh + gap), bw, bh, iss[k], C, o, im);
  }
}
/** One tag block; the layout adapts to the block size (1-4 tags per page, portrait or landscape). */
async function drawTagBlock(doc, x, y, w, h, i, C, o, im) {
  const {l, f, d} = C, col = STATUS[i.status];
  const big = h > 180 && w > 160, tiny = h < 100 || w < 110, narrow = w < 120;
  const hs = tiny ? 9 : 10.5, nf = tiny ? 9.5 : 11, tf = tiny ? 8.5 : 10, sf = tiny ? 6.5 : 7.5;
  doc.setDrawColor(200, 207, 218); doc.setLineWidth(0.3); doc.roundedRect(x, y, w, h, 1.5, 1.5, 'S');
  doc.setFillColor(243, 246, 250); doc.roundedRect(x + 0.2, y + 0.2, w - 0.4, hs, 1.4, 1.4, 'F'); doc.setFillColor(...rgb(col)); doc.rect(x + 0.2, y + 0.2, 1.6, hs, 'F');
  doc.setFont(FONT, 'bold'); doc.setFontSize(nf); const nw = Math.max(tiny ? 16 : 20, doc.getTextWidth(i.number) + 6), bhh = hs - 3.7;
  doc.setFillColor(...rgb(col)); doc.roundedRect(x + 4, y + 2, nw, bhh, 1.2, 1.2, 'F'); doc.setTextColor(255); doc.text(i.number, x + 4 + nw / 2, y + 2 + bhh / 2 + nf * 0.3528 * 0.36, {align:'center'});
  const stT = L(i.status).toUpperCase(); doc.setFontSize(sf); const sw = doc.getTextWidth(stT) + 6;
  doc.setTextColor(20, 30, 45); doc.setFontSize(tf); doc.text(doc.splitTextToSize(i.title || L('(untitled)'), Math.max(10, w - nw - sw - 16))[0], x + nw + 7, y + 2 + bhh / 2 + tf * 0.3528 * 0.36);
  statusBadge(doc, x + w - 3, y + (hs - (sf * 0.3528 + 2.6)) / 2, stT, col, sf, 'right');
  let yy = y + hs + 3;
  const last = i.comments.filter(c => !c.sys).slice(-1)[0];
  const due = i.dueDate ? fmtDate(i.dueDate) + (isOverdue(i) ? `  (${L('OVERDUE')})` : '') : '—';
  const rows = tiny || h < 120
    ? [[`${L('Type')} / ${L('Priority')}`, `${L(i.type)}  /  ${L(i.priority)}`], [L('Location detail'), i.location || '—'], [L('System'), sysLabel(C)],
       [L('Responsible'), [i.trade, i.assignee].filter(Boolean).join('  —  ') || '—'], [L('Due date'), due + (i.closedAt ? `  |  ${L('Closed date')} ${fmtDate(i.closedAt)}` : '')]]
    : [[`${L('Type')} / ${L('Priority')}`, `${L(i.type)}  /  ${L(i.priority)}`], [L('Location detail'), i.location || '—'], [L('Discipline'), nodeLabel(d)], [`${L('Floor')} / ${L('Layout')}`, `${f ? f.name : '—'}  /  ${l.name}`], [L('System'), sysLabel(C)],
       [L('Responsible'), [i.trade, i.assignee].filter(Boolean).join('  —  ') || '—'], [L('Due date'), due], [L('Raised'), `${fmtDate(i.createdAt)} · ${i.createdBy || '—'}   |   ${i.closedAt ? L('Closed date') + ' ' + fmtDate(i.closedAt) : L('Updated') + ' ' + fmtDate(i.updatedAt)}`]];
  const kpSide = o.keyplan && im && !narrow, kpStrip = o.keyplan && im && narrow;
  const infoW = kpSide ? w * 0.58 : w - 6, rh = big ? 5.8 : tiny ? 4.5 : 5.1, kfs = big ? 7.8 : tiny ? 6.5 : 7.1;
  const yEnd = kvTable(doc, x + 3, yy, infoW, rows, {lw:narrow ? 22 : 28, rh, fs:kfs});
  const keyPlan = (kx, ky, kw, kh) => { doc.addImage(keyPlanCrop(im, i, kw, kh), 'JPEG', kx, ky, kw, kh); doc.setDrawColor(190, 198, 210); doc.rect(kx, ky, kw, kh);
    doc.setFont(FONT, 'bold'); doc.setFontSize(tiny ? 5 : 6); const kt = L('KEY PLAN'), ktw = doc.getTextWidth(kt) + 4; doc.setFillColor(...rgb(NAVY)); doc.rect(kx, ky, ktw, tiny ? 3.6 : 4.4, 'F'); doc.setTextColor(255); doc.text(kt, kx + ktw / 2, ky + (tiny ? 2.5 : 3), {align:'center'}); };
  if (kpSide) keyPlan(x + 3 + infoW + 3, yy, w - 6 - infoW - 3, yEnd - yy);
  yy = yEnd + (tiny ? 2 : 3);
  // photo strip cells: (key plan when narrow) + photos
  const photos = i.photoIds.slice(0, o.maxPhotos), cells = [...(kpStrip ? ['__kp'] : []), ...photos];
  const lfs = tiny ? 6.5 : 7.3, fs = big ? 8.5 : tiny ? 6.8 : 7.8, lh = fs * 0.3528 * 1.35;
  const rem = y + h - 3 - yy, photoMin = cells.length ? Math.max(tiny ? 16 : 22, rem * (big ? 0.55 : 0.45)) + 4 : 6;
  doc.setFont(FONT, 'bold'); doc.setFontSize(lfs); doc.setTextColor(84, 96, 114); doc.text(L('DESCRIPTION / ISSUE'), x + 3, yy + 2.4); yy += 3.6;
  doc.setFont(FONT, 'normal'); doc.setFontSize(fs);
  let lines = doc.splitTextToSize(i.description || '—', w - 10); if (last) lines = lines.concat(doc.splitTextToSize(`${L('Latest remark')} (${last.by}, ${fmtDate(last.t)}): ${last.text}`, w - 10));
  const maxL = Math.max(1, Math.min(big ? 14 : 8, Math.floor((rem - 3.6 - photoMin - 5) / lh)));
  if (lines.length > maxL) { lines = lines.slice(0, maxL); lines[maxL - 1] += ' …'; }
  const boxH = Math.max(lines.length, big ? 3 : 1) * lh + 3;
  doc.setFillColor(250, 251, 253); doc.setDrawColor(214, 220, 229); doc.rect(x + 3, yy, w - 6, boxH, 'FD'); doc.setTextColor(25, 35, 50); doc.text(lines, x + 5, yy + 2 + lh * 0.75, {lineHeightFactor:1.35});
  yy += boxH + (tiny ? 2 : 3);
  const avail = y + h - 3 - yy - 4;
  doc.setFont(FONT, 'bold'); doc.setFontSize(lfs); doc.setTextColor(84, 96, 114); doc.text(`${L('PHOTOS')} (${i.photoIds.length})`, x + 3, yy + 2.4); yy += 4;
  if (!cells.length || avail < 10) { doc.setFont(FONT, 'normal'); doc.setFontSize(tiny ? 6.5 : 7.5); doc.setTextColor(150); doc.text(cells.length ? L('(photos omitted — not enough space)') : L('No photos attached.'), x + 3, yy + 3); return; }
  const g = tiny ? 2 : 3, maxCols = Math.max(1, Math.floor((w - 6 + g) / ((tiny ? 24 : 30) + g)));
  const use = cells.slice(0, big ? cells.length : Math.min(cells.length, maxCols * (avail > 70 ? 2 : 1)));
  const n = use.length, cols = big && n > 2 ? 2 : Math.min(n, maxCols), rowsN = Math.ceil(n / cols);
  const cw = (w - 6 - (cols - 1) * g) / cols, chh = Math.min((avail - (rowsN - 1) * g) / rowsN, cw * 0.78);
  let pn = 0;
  for (let k = 0; k < n; k++) {
    const cx = x + 3 + (k % cols) * (cw + g), cy = yy + Math.floor(k / cols) * (chh + g);
    if (use[k] === '__kp') { keyPlan(cx, cy, cw, chh); continue; }
    const src = await getFile(use[k]); if (!src) continue; const pim = await loadImage(src); pn++;
    doc.setFillColor(240, 243, 247); doc.rect(cx, cy, cw, chh, 'F'); const ft = fit(pim.naturalWidth, pim.naturalHeight, cw - 1, chh - 1);
    doc.addImage(src, 'JPEG', cx + 0.5 + ft.dx, cy + 0.5 + ft.dy, ft.w, ft.h, 'ph_' + use[k], 'FAST'); doc.setDrawColor(200, 207, 218); doc.rect(cx, cy, cw, chh);
    const kind = (i.photoTags || {})[use[k]] || '', pt = `${L('PHOTO')} ${pn}${kind ? ' · ' + L(kind).toUpperCase() : ''}`;
    doc.setFont(FONT, 'bold'); doc.setFontSize(tiny ? 5 : 5.8); const ptw = doc.getTextWidth(pt) + 4; doc.setFillColor(...rgb(kind === 'Before' ? '#d97706' : kind === 'After' ? '#16a34a' : NAVY)); doc.rect(cx, cy, ptw, tiny ? 3.4 : 4, 'F'); doc.setTextColor(255); doc.text(pt, cx + ptw / 2, cy + (tiny ? 2.4 : 2.8), {align:'center'});
  }
}
'''
s = s[:a] + NEW + s[b:]
open('src.html', 'w', encoding='utf-8').write(s)

tr = json.load(open('tr.json', encoding='utf-8'))
tr.update({"Detail page orientation": ["ທິດທາງໜ້າລາຍລະອຽດ", "แนวหน้ารายละเอียด"], "Portrait": ["ແນວຕັ້ງ", "แนวตั้ง"], "Landscape": ["ແນວນອນ", "แนวนอน"]})
json.dump(tr, open('tr.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('patched')
