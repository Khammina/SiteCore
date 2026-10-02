# v1.03 phone UX: compact plan toolbar with a "More" sheet, punch list as cards on phones.
import json
s = open('src.html', encoding='utf-8').read()
def R(a, b):
    global s
    assert s.count(a) == 1, a[:100]
    s = s.replace(a, b)

R("""      <div class="seg"><button id="zOut">${ic('minus')}</button><button id="zFit">${L('Fit')}</button><button id="zIn">${ic('plus')}</button></div>
      <button class="btn sm" id="lockBtn">""", """      <div class="seg ph-hide"><button id="zOut" title="${L('Zoom out')}">${ic('minus')}</button><button id="zFit">${L('Fit')}</button><button id="zIn" title="${L('Zoom in')}">${ic('plus')}</button></div>
      <button class="btn sm ph-only" id="zFit2">${ic('fit')} ${L('Fit')}</button>
      <button class="btn sm ph-hide" id="lockBtn">""")
R("""      ${STATUSES.map(s => `<span class="chip ${UI.statusFilter.has(s) ? '' : 'off'}" data-sf="${s}\"""",
  """      ${STATUSES.map(s => `<span class="chip ph-hide ${UI.statusFilter.has(s) ? '' : 'off'}" data-sf="${s}\"""")
R("""      <button class="btn sm" id="lyInfo">${ic('edit')} ${L('Info')}</button><button class="btn sm" id="renum">${ic('hash')} ${L('Renumber')}</button>
      <button class="btn sm panel-toggle tags" onclick="$('#drw').classList.toggle('show-tags')">${ic('tag')} ${L('Tags')}</button>
      <button class="btn sm primary" id="lyPdf">${ic('file')} ${L('Export PDF report')}</button>""",
  """      <button class="btn sm ph-hide" id="lyInfo">${ic('edit')} ${L('Info')}</button><button class="btn sm ph-hide" id="renum">${ic('hash')} ${L('Renumber')}</button>
      <button class="btn sm panel-toggle tags ph-hide" onclick="$('#drw').classList.toggle('show-tags')">${ic('tag')} ${L('Tags')}</button>
      <button class="btn sm ph-only" id="vMore" aria-label="${esc(L('More'))}">${ic('dots')} ${L('More')}</button>
      <button class="btn sm primary" id="lyPdf" title="${L('Export PDF report')}">${ic('file')} <span class="ph-hide">${L('Export PDF report')}</span><span class="ph-only">PDF</span></button>""")
R("""  $('#lyInfo').onclick = () => editLayout(l); $('#renum').onclick = () => renumberLayout(l); $('#lyPdf').onclick = () => generateReport('layout', l.id);
}""", """  $('#lyInfo').onclick = () => editLayout(l); $('#renum').onclick = () => renumberLayout(l); $('#lyPdf').onclick = () => generateReport('layout', l.id);
  $('#zFit2').onclick = fitView;
  $('#vMore').onclick = async () => {
    const shown = STATUSES.filter(s => UI.statusFilter.has(s)).length;
    const k = await actionSheet(l.name, [['tags', 'tag', `${L('Tags on this layout')} (${iss.length})`], ['filter', 'sliders', `${L('Status')}: ${shown === STATUSES.length ? L('All statuses') : shown + '/' + STATUSES.length}`],
      ['zin', 'plus', L('Zoom in')], ['zout', 'minus', L('Zoom out')], ['lock', UI.lockPins ? 'unlock' : 'lock', UI.lockPins ? L('Tags movable') : L('Tags locked')],
      ['info', 'edit', L('Layout information')], ['renum', 'hash', L('Renumber')]]);
    if (k === 'tags') $('#drw').classList.add('show-tags'); if (k === 'zin') zoomCenter(1.3); if (k === 'zout') zoomCenter(1 / 1.3);
    if (k === 'lock') { UI.lockPins = !UI.lockPins; renderVBar(); } if (k === 'info') editLayout(l); if (k === 'renum') renumberLayout(l);
    if (k === 'filter') { const f = await actionSheet(L('Status'), [['all', 'checks', L('All statuses'), false, shown === STATUSES.length], ['open', 'alert', L('All open (not Pass/Closed)')],
        ...STATUSES.map(st => [st, 'flag', `${L(st)} (${iss.filter(i => i.status === st).length})`, false, shown === 1 && UI.statusFilter.has(st)])]);
      if (!f) return; UI.statusFilter = new Set(f === 'all' ? STATUSES : f === 'open' ? STATUSES.filter(x => !DONE.has(x)) : [f]); renderVBar(); renderPins(); renderTagList(); }
  };
}""")
# tag panel on phones: a close button
R("""    <aside class="tag-panel"><div class="panel-head"><b>${ic('tag')} ${L('Tags on this layout')}</b><span id="tagCount" class="muted"></span></div>""",
  """    <aside class="tag-panel"><div class="panel-head"><b>${ic('tag')} ${L('Tags on this layout')}</b><span id="tagCount" class="muted"></span><button class="btn sm ph-only" onclick="$('#drw').classList.remove('show-tags')" aria-label="${esc(L('Close'))}">${ic('x')}</button></div>""")
R("""    <aside class="tree-panel"><div class="panel-head"><b>${ic('folder')} ${L('Drawing register')}</b><button class="btn sm primary" id="addDisc">${ic('plus')} ${L('Discipline')}</button></div>""",
  """    <aside class="tree-panel"><div class="panel-head"><b>${ic('folder')} ${L('Drawing register')}</b><button class="btn sm primary" id="addDisc">${ic('plus')} ${L('Discipline')}</button><button class="btn sm ph-only" onclick="$('#drw').classList.remove('show-tree')" aria-label="${esc(L('Close'))}">${ic('x')}</button></div>""")

# ---- punch list as cards on phones ----
R("""    bar(list);
  };""", """    if (matchMedia('(max-width:600px)').matches) $('#itb').innerHTML = `<tr><td colspan="13" style="padding:0;border:0"><div class="icards">${list.map(i => { const c = ctxOf(i.layoutId);
      return `<div class="icard" data-id="${i.id}" style="--c:${STATUS[i.status]}"><div class="icard-h"><input type="checkbox" data-bk="${i.id}" ${UI.bulk.has(i.id) ? 'checked' : ''} aria-label="${esc(L('Select'))} ${esc(i.number)}"><span class="badge tag" style="--c:${STATUS[i.status]}">${esc(i.number)}</span>${stBadge(i.status)}<span class="sp"></span><span class="badge" style="--c:${PRI_COLOR[i.priority]}">${esc(L(i.priority))}</span></div>
        <b>${esc(i.title || L('(untitled)'))}</b><small>${esc(pathOf(i.layoutId))}</small>
        <div class="icard-f"><span>${ic('users', 13)} ${esc(i.assignee || i.trade || L('Unassigned'))}</span>${i.dueDate ? `<span class="${isOverdue(i) ? 'overdue' : ''}">${ic('calendar', 13)} ${fmtDate(i.dueDate)}</span>` : ''}${i.photoIds.length ? `<span>${ic('camera', 13)} ${i.photoIds.length}</span>` : ''}<span class="sp"></span><button class="btn sm" data-plan="${i.id}" aria-label="${esc(L('Show on plan'))}">${ic('map')}</button></div></div>`; }).join('') || `<div class="empty">${L('No items match the filters')}</div>`}</div></td></tr>`;
    bar(list);
  };""")
R("""const tr = e.target.closest('tr[data-id]'); if (tr) openIssueEditor(tr.dataset.id); };""",
  """const tr = e.target.closest('tr[data-id],.icard[data-id]'); if (tr) openIssueEditor(tr.dataset.id); };""")
R("  $('#fq').oninput = e => { F.q = e.target.value; draw(); };", "  $('#fq').oninput = e => { F.q = e.target.value; draw(); };\n  window.addEventListener('resize', function rz() { if (!$('#itb')) return removeEventListener('resize', rz); clearTimeout(rz.t); rz.t = setTimeout(draw, 200); });")

# ---- CSS ----
R(".nav-more{display:none}", """.nav-more{display:none}
.ph-only{display:none !important}
.icards{display:flex;flex-direction:column;gap:10px;padding:10px}
.icard{background:#fff;border:1px solid var(--line);border-left:4px solid var(--c);border-radius:10px;padding:10px 12px;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.icard-h{display:flex;gap:6px;align-items:center;margin-bottom:6px}.icard b{display:block;font-size:14px;line-height:1.35}.icard small{color:var(--muted);display:block;margin-top:2px}
.icard-f{display:flex;gap:12px;align-items:center;margin-top:8px;font-size:12.5px;color:#475569;flex-wrap:wrap}.icard-f span{display:inline-flex;gap:4px;align-items:center}""")
R("@media (max-width:600px){\n  .ov{align-items:flex-end;", """@media (max-width:600px){
  .ph-hide{display:none !important}.ph-only{display:inline-flex !important}
  .tbl:has(.icards) thead{display:none}.tbl td:has(.icards){background:transparent !important}
  .card:has(.icards){background:transparent;border:0;box-shadow:none;max-height:none !important}
  .crumbs{font-size:12px}.crumbs .muted{display:none}
  .tag-panel{width:100% !important;max-width:none}
  .ov{align-items:flex-end;""")
open('src.html', 'w', encoding='utf-8').write(s)

tr = json.load(open('tr.json', encoding='utf-8'))
tr.update({"Zoom in": ["ຂະຫຍາຍ", "ซูมเข้า"], "Zoom out": ["ຫຍໍ້", "ซูมออก"], "Select": ["ເລືອກ", "เลือก"]})
json.dump(tr, open('tr.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('patched')
