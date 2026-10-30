"""Grenada: add one Cap. statute (from a laws.gov.gd PDF text layer) to corpus.json as one act, one version.
usage: add_statute.py <pdf> <slug> <short> <title> <url> <from-date>   (existing acts are left unchanged)"""
import hashlib, json, re, subprocess, sys
from pathlib import Path

pdf, slug, short, title, url, frm = sys.argv[1:7]
PDF = Path(pdf)
CORPUS = Path(__file__).with_name('corpus.json')
raw = subprocess.run(['pdftotext', '-enc', 'UTF-8', '-layout', str(PDF), '-'], capture_output=True, check=True).stdout.decode('utf8')
lines = raw.replace('\f', '\n').replace(' ', ' ').split('\n')
sha = hashlib.sha256(PDF.read_bytes()).hexdigest()

# body starts at the "1. Short title" heading that is followed by the sentence "may be cited"
start = next(i for i, l in enumerate(lines) if re.match(r'^1\. Short title\s*$', l)
             and any('may be cited' in x for x in lines[i + 1:i + 4]))
end = next(i for i in range(len(lines) - 1, start, -1) if 'SUBSIDIARY LEGISLATION' in lines[i])
# cut the trailing "CHAPTER n / TITLE" page header and anything from the final Schedule block of forms is kept as it is
sched = [i for i in range(start, end) if re.match(r'^\s*Schedules?\s*$', lines[i])]
sched_at = sched[-1] if sched and sched[-1] > start + (end - start) * 0.9 else None
body = lines[start:sched_at or end]
STRUCT = re.compile(r'^\s*(BOOK|PART|TITLE|DIVISION|CHAPTER|SCHEDULE)', re.I)
HEAD = re.compile(r'^(\d+)([A-Z]{0,2})\.(?: (\S.*))?\s*$')
TOC = {}  # section heading from the arrangement of sections, used when the body prints only the number
_k = None
for l in lines[:start]:
    m = re.match(r'^\s*(\d+)([A-Z]{0,2})\.\s+(\S.*)$', l)
    if m:
        _k = (int(m.group(1)), m.group(2)); TOC[_k] = m.group(3).strip()
    elif _k and l.strip() and not STRUCT.match(l) and len(l) - len(l.lstrip()) > 3 and len(l) - len(l.lstrip()) < 12:
        TOC[_k] += ' ' + l.strip()
    elif not l.strip():
        pass
    else:
        _k = None
STRUCT = re.compile(r'^\s*(BOOK|PART|TITLE|DIVISION|CHAPTER|SCHEDULE)\b', re.I)


def clean(t):
    for a, b in (('’', "'"), ('‘', "'"), ('“', '"'), ('”', '"'), ('–', '-'), ('—', '-')):
        t = t.replace(a, b)
    return re.sub(r' {2,}', ' ', t).strip()


def split(ls):
    paras = []
    for l in ls:
        if not l.strip():
            continue
        ind = len(l) - len(l.lstrip())
        t = l.strip()
        marker = re.match(r'^\(\w{1,5}\)\s', t) or t.startswith('Provided') or t[:1] in '“"'
        if paras and not marker and not (1 <= ind <= 5 and paras[-1][-1] in '.;:—-'):
            prev = paras[-1]
            paras[-1] = prev + t if (prev.endswith('-') and len(prev) > 1 and prev[-2].isalpha() and t[:1].islower()) else prev + ' ' + t
        else:
            paras.append(t)
    return [clean(p) for p in paras]


blocks = []
lastn, lastsuf = 0, ''
for l in body:
    m = HEAD.match(l) if l[:1].isdigit() else None
    if m:
        n, suf = int(m.group(1)), m.group(2)
        ok = (n == lastn + 1 and not suf) or (n == lastn and suf > lastsuf and (lastsuf == '' or len(suf) == len(lastsuf)))
        if ok:
            lastn, lastsuf = n, suf
            blocks.append({'n': n, 'suf': suf, 'head': clean(m.group(3) or TOC.get((n, suf), '').rstrip('.')), 'lines': []})
            continue
    if blocks:
        s = l.strip()
        if STRUCT.match(l) and (len(l) - len(l.lstrip())) >= 8:
            continue  # centred Part / Title headings are not kept as units
        if s and (len(l) - len(l.lstrip())) >= 20 and not re.match(r'^\(\w{1,5}\)', s) and len(s) < 70 and not s.endswith(('.', ';', ':', ',', '-')):
            continue  # centred sub-headings
        blocks[-1]['lines'].append(l)

units = {}
for b in blocks:
    key = 'sec-%03d%s' % (b['n'], ('-' + b['suf'].lower()) if b['suf'] else '')
    label = 'Section %d%s' % (b['n'], b['suf'])
    paras = split(b['lines'])
    text = ('# %d%s. %s' % (b['n'], b['suf'], b['head'])).rstrip() + '\n' + ''.join(p + '\n' for p in paras)
    assert key not in units, key
    units[key] = {'label': label, 'kind': 'section', 'text': text}
if sched_at:
    sl = [clean(x) for x in lines[sched_at + 1:end] if x.strip()]
    units['schedule'] = {'label': 'Schedule', 'kind': 'schedule', 'text': '# Schedule\n' + ''.join(x + '\n' for x in sl)}
print(slug, len(units), 'sections; last', lastn, lastsuf)

d = json.loads(CORPUS.read_text(encoding='utf8'))
assert not any(a['slug'] == slug for a in d['acts'])
d['acts'].append({'slug': slug, 'short': short, 'title': title, 'url': url, 'first_law': None, 'earlier_laws': [],
                  'versions': [{'from': frm, 'source_url': url, 'sha256': sha, 'units': units}]})
CORPUS.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf8', newline='\n')
