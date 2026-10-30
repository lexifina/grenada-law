"""Grenada: write one Cap. statute (from a laws.gov.gd PDF text layer) as its own corpus.d part, one act, one version,
and verify every unit against the PDF text (all characters of the body, whitespace aside, in order).
usage: add_part.py <pdf> <part> <slug> <short> <title> <url> <from-date> <decision>
Existing corpus.json and parts are left unchanged."""
import hashlib, json, os, re, subprocess, sys
from pathlib import Path

pdf, part, slug, short, title, url, frm, decision = sys.argv[1:9]
PDF = Path(pdf)
OUT = Path(__file__).with_name('corpus.d') / f'{part}.json'
raw = subprocess.run(['pdftotext', '-enc', 'UTF-8', '-layout', str(PDF), '-'], capture_output=True, check=True).stdout.decode('utf8')
lines = raw.replace('\f', '\n').replace('\u00a0', ' ').split('\n')
sha = hashlib.sha256(PDF.read_bytes()).hexdigest()

start = next(i for i, l in enumerate(lines) if re.match(r'^1\. Short title\.?\s*$', l)
             and any('may be cited' in x for x in lines[i + 1:i + 4]))
end = next((i for i in range(start, len(lines)) if re.match(r'^\s*SUBSIDIARY LEGISLATION\s*$', lines[i])), len(lines))
while end > start and (not lines[end - 1].strip() or (lines[end - 1].strip().isupper() and len(lines[end - 1].strip()) < 70
                                                       and not lines[end - 1].strip().endswith('.'))):
    end -= 1  # the running title printed above SUBSIDIARY LEGISLATION
sched = [i for i in range(start, end) if re.match(r'^\s*(First |Second )?Schedules?\s*$', lines[i])]
sched_at = sched[0] if sched and sched[0] > start + (end - start) * 0.6 else None
body = lines[start:sched_at or end]
STRUCT = re.compile(r'^\s*(BOOK|PART|TITLE|DIVISION|CHAPTER|SCHEDULE)\b', re.I)
HEAD = re.compile(r'^(\d+)([A-Z]{0,2})\.(?: (\S.*))?\s*$')
HEAD_NODOT = re.compile(r'^(\d+) (\S.*?)\s*$')
TOC = {}
_k = None
for l in lines[:start]:
    m = re.match(r'^\s*(\d+)([A-Z]{0,2})\.\s+(\S.*)$', l)
    if m:
        _k = (int(m.group(1)), m.group(2)); TOC[_k] = m.group(3).strip()
    elif _k and l.strip() and not STRUCT.match(l) and 3 < len(l) - len(l.lstrip()) < 12:
        TOC[_k] += ' ' + l.strip()
    else:
        _k = None if l.strip() else _k


def norm_h(t):
    return re.sub(r'[^a-z0-9]', '', clean(t).lower())


def clean(t):
    for a, b in (('’', "'"), ('‘', "'"), ('“', '"'), ('”', '"'), ('–', '-'), ('—', '-')):
        t = t.replace(a, b)
    return re.sub(r' {2,}', ' ', t).strip()


def arr_mode(b, s):
    """An 'Arrangement' section lists the Books, Parts and Titles: keep those lines (one per paragraph) until a
    heading repeats, which is where the body's own headings start again."""
    if b['head'] != 'Arrangement' or b.get('arr_done'):
        return False
    seen = b.setdefault('seen', set())
    if s in seen and s.isupper():
        b['arr_done'] = True; b['arr'] = False
        return False
    seen.add(s); b['arr'] = True
    return True


def split(ls):
    paras, last_row = [], False
    for l in ls:
        own = l.startswith('\x00')
        l = l.lstrip('\x00')
        if not l.strip():
            continue
        ind = len(l) - len(l.lstrip())
        t = l.strip()
        row = bool(re.search(r'\S {3,}\S', t))
        marker = re.match(r'^\(\w{1,5}\)\s', t) or t.startswith('Provided') or t[:1] in '“"' or row or last_row or own
        last_row = row
        if paras and not marker and not (1 <= ind <= 5 and paras[-1][-1] in '.;:—-'):
            prev = paras[-1]
            paras[-1] = prev + t if (prev.endswith('-') and len(prev) > 1 and prev[-2].isalpha() and t[:1].islower()) else prev + ' ' + t
        else:
            paras.append(t)
    return [clean(p) for p in paras]


blocks, skipped, filled, gaps, nodot = [], [], [], [], []
skipped_at = set()
lastn, lastsuf = 0, ''
prev, prev_skipped = '', False
for bi, l in enumerate(body):
    m = HEAD.match(l) if l[:1].isdigit() else None
    if not m and l[:1].isdigit():
        m2 = HEAD_NODOT.match(l)
        if m2 and int(m2.group(1)) == lastn + 1 and (lastn + 1, '') in TOC \
                and norm_h(TOC[(lastn + 1, '')]).rstrip('.') == norm_h(m2.group(2)):
            nodot.append(lastn + 1)
            l = m2.group(1) + '. ' + m2.group(2)
            m = HEAD.match(l)
    if m:
        n, suf = int(m.group(1)), m.group(2)
        ok = (n == lastn + 1 and not suf) or (n == lastn and suf > lastsuf and (lastsuf == '' or len(suf) == len(lastsuf)))
        if not ok and m.group(3) and (n, suf) in TOC and (n > lastn + 1 or (n == lastn and suf > lastsuf))                 and norm_h(TOC[(n, suf)])[:20] == norm_h(m.group(3))[:20]:
            ok = True
            gaps.append('%d%s after %d%s' % (n, suf, lastn, lastsuf))
        if ok:
            lastn, lastsuf = n, suf
            head = m.group(3)
            if not head and TOC.get((n, suf)):
                filled.append('%d%s' % (n, suf))
            blocks.append({'n': n, 'suf': suf, 'src': l, 'head': clean(head or TOC.get((n, suf), '').rstrip('.')), 'lines': [],
                           'more': bool(head) and norm_h(TOC.get((n, suf), '')).startswith(norm_h(head)) and norm_h(TOC.get((n, suf), '')) != norm_h(head)})
            continue
    if blocks and blocks[-1]['more'] and l.strip():
        b = blocks[-1]
        full = norm_h(TOC[(b['n'], b['suf'])])
        cand = norm_h(b['head'] + ' ' + l.strip())
        if full.startswith(cand):
            b['head'] = clean(b['head'] + ' ' + l.strip()); b['hl'] = b.get('hl', []) + [l]
            b['more'] = full != cand
            continue
        b['more'] = False
    if blocks:
        s = l.strip()
        am = arr_mode(blocks[-1], s) if s else False
        after_gap = (not prev.strip() or prev_skipped) and not re.search(r'\S {3,}\S', s) and not am
        if s and after_gap and s.isupper() and len(s) < 60 and (len(l) - len(l.lstrip())) >= 8:
            skipped.append(s); skipped_at.add(start + bi); prev, prev_skipped = l, True; continue
        if s and after_gap and s[0].isupper() and (len(l) - len(l.lstrip())) >= 20 and not re.match(r'^\(\w{1,5}\)', s) and len(s) < 70 and not s.endswith(('.', ';', ':', ',', '-')):
            skipped.append(s); skipped_at.add(start + bi); prev, prev_skipped = l, True; continue
        if s:
            prev_skipped = False
        blocks[-1]['lines'].append(('\x00' + l) if blocks[-1].get('arr') else l)
    prev = l

units = {}
for b in blocks:
    key = 'sec-%03d%s' % (b['n'], ('-' + b['suf'].lower()) if b['suf'] else '')
    paras = split(b['lines'])
    text = ('# %d%s. %s' % (b['n'], b['suf'], b['head'])).rstrip() + '\n' + ''.join(p + '\n' for p in paras)
    assert key not in units, key
    units[key] = {'label': 'Section %d%s' % (b['n'], b['suf']), 'kind': 'section', 'text': text}
if sched_at:
    # in the Schedule, centred lines (headings, form titles), numbered paragraphs and [Section n.] notes start a paragraph
    pre = [('\x00' + x) if x.strip() and ((len(x) - len(x.lstrip())) >= 12 and len(x.strip()) < 60 and not x.strip()[0].islower() or re.match(r'^\s*(\d+\.|FORM\b|\[)', x)) else x
           for x in lines[sched_at + 1:end]]
    sl = split(pre)
    units['schedule'] = {'label': 'Schedule', 'kind': 'schedule', 'text': '# Schedule\n' + ''.join(x + '\n' for x in sl)}

# verification: every non-space character of the PDF body (minus the skipped headings) appears in the units, in order
def norm(t):
    return re.sub(r'\s+', '', clean(t))
src = []
for i in range(start, end):
    if i not in skipped_at:
        src.append(lines[i].strip())
sk = []
src_s = norm(''.join(src))
uni = []
for b, (k, u) in zip(blocks + [None], units.items()):
    t = u['text'][2:]
    if b is not None and not HEAD.match(b['src']).group(3):
        t = t.split('\n', 1)[0].split(' ', 1)[0] + '\n' + t.split('\n', 1)[1]  # TOC-filled heading is not in the body
    if b is not None and b['n'] in nodot and not b['suf']:
        t = t.replace('%d.' % b['n'], str(b['n']), 1)  # the PDF prints this section number without its full stop
    uni.append(t)
uni_s = norm(''.join(uni))
assert not sk, ('skipped lines not found in order', sk[:3])
if src_s != uni_s:
    i = next(i for i, (a, b) in enumerate(zip(src_s, uni_s)) if a != b) if any(a != b for a, b in zip(src_s, uni_s)) else min(len(src_s), len(uni_s))
    sys.exit(f'VERIFY FAILED at {i}: src ...{src_s[i-80:i+80]}\n uni ...{uni_s[i-80:i+80]}')
toc_keys = {'sec-%03d%s' % (n, ('-' + s.lower()) if s else '') for n, s in TOC}
print('TOC not in units:', sorted(toc_keys - set(units))[:20], ' units not in TOC:', sorted(set(units) - toc_keys - {'schedule'})[:20])
print("SKIPPED:", skipped)
print("GAPS:", gaps, "NODOT:", nodot)
print(f'{slug}: {len(units)} units, last section {lastn}{lastsuf}; verified {len(src_s)} chars; '
      f'{len(skipped)} headings skipped; TOC-filled headings: {filled}')

d = {'acts': [{'slug': slug, 'short': short, 'title': title, 'url': url, 'first_law': None, 'earlier_laws': [],
               'versions': [{'from': frm, 'source_url': url, 'sha256': sha, 'units': units}]}],
     'sources': [{'name': f'Laws of Grenada, {title}', 'url': url, 'retrieved': '2026-10-30',
                  'licence': 'No licence stated on the site; robots.txt allows all agents',
                  'notes': f'PDF sha256 {sha}; born-digital PDF with a text layer, read with pdftotext.'}],
     'decisions': [decision]}
OUT.parent.mkdir(exist_ok=True)
tmp = OUT.with_suffix('.tmp')
tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf8', newline='\n')
os.replace(tmp, OUT)
