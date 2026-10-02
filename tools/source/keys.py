import re, json
s = open('src.html', encoding='utf-8').read()
keys = set(re.findall(r"\bL\('([^']*)'", s)) | set(re.findall(r'\bL\("([^"]*)"', s))
extra = ['Dashboard','Drawings & Tags','Punch List','Task Board','Inspections','Site Diary & Log','Reports','Project Settings',
 'Open','In Progress','Defect','Not Pass','Pass','Closed','Observation','Snag','Safety','NCR','Low','Medium','High','Critical',
 'Sunny','Cloudy','Light rain','Heavy rain','Windy','Hot','Owner','Consultant','Contractor','NOT PASS','IN PROGRESS','PASS','Fail',
 'Project','Share / Export','Import','Project name','Project No. / code','Owner / Client','Location','Project manager','Start date',
 'Report title (default: PUNCH LIST REPORT)','Report footer note','Pen','Arrow','Box','Ellipse','Before','After','Left','Centre','Right','Small phone','Phone','Tablet','Computer','Auto (system)','Light','Dark','About','Plans & tags','Import PDF / JPG plans and pin issues exactly where they are.','Punch lists','Status, photos, markup, responsibility and due dates.','Pass / Fail checklists that turn failures into tags.','PDF reports','Branded reports with logos, plans and photos.']
keys |= set(extra)
keys = sorted(keys)
json.dump(keys, open('keys.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(keys))
print('\n'.join(keys))
