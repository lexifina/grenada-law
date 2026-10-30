"""Grenada: parse the Constitution (Cap. 128A, Schedule) from the laws.gov.gd PDF text layer into corpus.json.
Input: the PDF (path in argv[1]); text comes from pdftotext -layout."""
import hashlib, json, re, subprocess, sys
from pathlib import Path

PDF = Path(sys.argv[1])
URL = 'https://laws.gov.gd/index.php/chapters/g-120-132/1201-cap128a-grenada-constitution-act/download'
RETRIEVED = '2026-10-29'
raw = subprocess.run(['pdftotext', '-enc', 'UTF-8', '-layout', str(PDF), '-'], capture_output=True, check=True).stdout.decode('utf8')
lines = raw.replace('\f', '').replace(' ', ' ').split('\n')
sha = hashlib.sha256(PDF.read_bytes()).hexdigest()

start = next(i for i, l in enumerate(lines) if l.strip().startswith('Whereas the people of Grenada'))
end = next(i for i, l in enumerate(lines) if 'SUBSIDIARY LEGISLATION' in l and i > start) - 3
body = lines[start:end]

HEAD = re.compile(r'^(\d+)\. (\S.*)$')
PART = re.compile(r'^\s*PART [IVX]+\s*$')
PARTS = ['Protection of Fundamental Rights and Freedoms', 'The Governor-General', 'Parliament', 'The Executive',
         'Finance', 'The Public Service', 'Citizenship', 'Judicial Provisions', 'Miscellaneous']


def clean(t):
    t = re.sub(r'\.{5,}', '.......', t)
    for a, b in (('’', "'"), ('‘', "'"), ('“', '"'), ('”', '"'), ('–', '-')):
        t = t.replace(a, b)
    return re.sub(r' {2,}', ' ', t).strip()


def paragraphs(ls):
    paras = []  # [indent, text, closed]
    for l in ls:
        if not l.strip():
            continue
        ind = len(l) - len(l.lstrip())
        t = l.strip()
        marker = re.match(r'^\(\w{1,5}\)\s', t) or t.startswith('Provided')
        centred = ind >= 18
        cont = False
        if paras and not marker and not centred and not paras[-1][2]:
            pind, ptxt = paras[-1][0], paras[-1][1]
            if ind == 0 or ind >= 11:
                cont = True
            elif ind < 7 and pind >= 7 and ptxt[-1] not in '.;:-,"—':
                cont = True
        if cont:
            prev = paras[-1][1]
            if prev.endswith('-') and len(prev) > 1 and prev[-2].isalpha() and t[:1].isalpha():
                paras[-1][1] = prev + t
            else:
                paras[-1][1] = prev + ' ' + t
        else:
            paras.append([ind, t, centred])
    return [clean(p[1]) for p in paras]


blocks = []
cur = None


def new(key, label, heading, kind):
    global cur
    cur = {'key': key, 'label': label, 'heading': heading, 'kind': kind, 'lines': [], 'n': 0}
    blocks.append(cur)


new('preamble', 'Preamble', 'Preamble', 'preamble')
mode = 'sections'
nextn = 1
for l in body:
    s = l.strip()
    ind = len(l) - len(l.lstrip())
    if mode == 'sections':
        m = HEAD.match(s) if ind == 0 else None
        if m and int(m.group(1)) == nextn:
            new('sec-%03d' % nextn, 'Section %d' % nextn, '%d. %s' % (nextn, clean(m.group(2))), 'section')
            nextn += 1
            continue
        if re.match(r'^\s*Appendix 1\s*$', l):
            mode = 'appendix'
            new('appendix-1', 'Appendix 1', 'Appendix 1: provisions referred to in section 39(5)', 'schedule')
            continue
    elif mode == 'appendix':
        if re.match(r'^\s*Appendix 2\s*$', l):
            new('appendix-2', 'Appendix 2', 'Appendix 2: rules relating to constituencies', 'schedule')
            continue
        if re.match(r'^\s*Appendix 3\s*$', l):
            new('appendix-3', 'Appendix 3', 'Appendix 3: forms of oath', 'schedule')
            continue
        if re.match(r'^\s*APPENDIX 2 TO THE SCHEDULE\s*$', l):
            mode = 'transitional'
            new('drop', '', '', 'drop')
            continue
        if s in ('GRENADA CONSTITUTION ACT', 'GRENADA CONSTITUTION'):
            continue
    elif mode == 'transitional':
        m = HEAD.match(s) if ind == 0 else None
        if m:
            n = int(m.group(1))
            new('transitional-%d' % n, 'Transitional provision %d' % n,
                'Transitional provision %d. %s' % (n, clean(m.group(2))), 'transitional')
            continue
    if PART.match(l):
        continue
    cur['lines'].append(l)

units = {}
for b in blocks:
    if b['kind'] == 'drop':
        continue
    ps = paragraphs(b['lines'])
    while ps and ps[-1] in PARTS:
        ps.pop()
    ps = [p for p in ps if p not in PARTS or b['kind'] != 'section']
    units[b['key']] = {'label': b['label'], 'kind': b['kind'], 'text': '# ' + b['heading'] + '\n' + '\n'.join(ps) + '\n'}

credits = {k: ['publisher-oldest'] for k in units}

corpus = {
    'country': {
        'code': 'GD', 'name': 'Grenada', 'slug': 'grenada', 'lang': 'en', 'tz': 'America/Grenada', 'future_branch': 'future',
        'publisher': {'name': 'Laws of Grenada (laws.gov.gd)', 'email': 'laws@laws-gov-gd.invalid'},
        'default_in_force_rule': {'text': 'A Grenada law takes effect on the day it names; the Constitution names 7 February 1974.',
                                  'source': 'https://laws.gov.gd'},
        'licence_note': 'Text of the Grenada Constitution Act (Cap. 128A) as published on laws.gov.gd, the official Laws of Grenada site. The site states no licence; legislation is reproduced as published.'},
    'sources': [{'name': 'Laws of Grenada, Cap. 128A Grenada Constitution Act', 'url': URL, 'retrieved': RETRIEVED,
                 'licence': 'No licence stated on the site; robots.txt allows all agents',
                 'notes': 'PDF sha256 %s; born-digital PDF with a text layer, read with pdftotext.' % sha}],
    'laws': {'publisher-oldest': {'label': 'Laws of Grenada', 'title': 'Laws of Grenada (laws.gov.gd), oldest version available',
                                  'kind': 'publisher', 'enacted': '1974-02-07', 'published': '1974-02-07', 'url': URL,
                                  'temporary_until': None, 'restores': None, 'note': None}},
    'acts': [{'slug': 'constitution', 'short': 'Const.', 'title': 'Constitution of Grenada (Grenada Constitution Act, Cap. 128A, Schedule)',
              'url': URL, 'first_law': None, 'earlier_laws': [],
              'versions': [{'from': '1974-02-07', 'source_url': URL, 'sha256': sha, 'units': units, 'credits': credits,
                            'note': 'The Constitution as printed on laws.gov.gd in the Laws of Grenada (Cap. 128A, S.I. 2155 of 1973), in force 7 February 1974. This is the current consolidated text, dated from the commencement day the Act gives; the as-enacted 1974 text and later amendments are not online.'}]}],
    'applies': [],
    'decisions': [
        "Scope: the Constitution in the Schedule to Cap. 128A, with its Appendices 1 to 3 and the transitional provisions (Appendix 2 to the Schedule). The Act's own two sections, the Constituency Boundaries Order and the Public Service regulations in the same PDF are left out.",
        'No dated past versions are online, so there is one version, credited to the publisher as "oldest version available" and dated 7 February 1974, the commencement day printed in the Act.',
        'Line breaks inside a paragraph were joined using the PDF indentation; Part headings are not kept as separate files; typographic quotes and dashes were normalised.'],
    'ai_use': ['none']}
Path(__file__).with_name('corpus.json').write_text(json.dumps(corpus, indent=1, ensure_ascii=False) + '\n', encoding='utf8', newline='\n')
print(len(units), 'units')
