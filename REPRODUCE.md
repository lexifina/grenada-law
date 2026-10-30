# How this repository was made (Grenada)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Laws of Grenada, Cap. 128A Grenada Constitution Act | <https://laws.gov.gd/index.php/chapters/g-120-132/1201-cap128a-grenada-constitution-act/download> | 2026-10-29 | No licence stated on the site |
| Laws of Grenada, Cap. 72A Criminal Code | <https://laws.gov.gd/index.php/chapters/c-39a-75d/1107-cap72a-criminal-code/download> | 2026-10-30 | No licence stated on the site |
| Laws of Grenada, Cap. 58A Companies Act | <https://laws.gov.gd/index.php/chapters/c-39a-75d/1087-cap58a-companies-act/download> | 2026-10-30 | No licence stated on the site |
| Laws of Grenada, Criminal Procedure Code (Cap. 72B) | <https://laws.gov.gd/index.php/chapters/c-39a-75d/1108-cap72b-criminal-procedure-code/download> | 2026-10-30 | No licence stated on the site |
| Laws of Grenada, Evidence Act (Cap. 92) | <https://laws.gov.gd/index.php/chapters/e-85-98a/1151-cap92-evidence-act/download> | 2026-10-30 | No licence stated on the site |
| Laws of Grenada, Employment Act (Cap. 89) | <https://laws.gov.gd/index.php/chapters/e-85-98a/1146-cap89-employment-act/download> | 2026-10-30 | No licence stated on the site |
| Laws of Grenada, Interpretation and General Provisions Act (Cap. 153) | <https://laws.gov.gd/index.php/chapters/i-144-155/1250-cap153-interpretation-and-general-provisions-act/download> | 2026-10-30 | No licence stated on the site |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Constitution of Grenada (Grenada Constitution Act, Cap. 128A, Schedule) | 1 | 1974-02-07 to 1974-02-07 |
| `criminal-code` | Criminal Code (Cap. 72A) | 1 | 1987-01-20 to 1987-01-20 |
| `companies-act` | Companies Act (Cap. 58A) | 1 | 1994-11-18 to 1994-11-18 |
| `criminal-procedure-code` | Criminal Procedure Code (Cap. 72B) | 1 | 1897-01-20 to 1897-01-20 |
| `evidence-act` | Evidence Act (Cap. 92) | 1 | 1897-01-20 to 1897-01-20 |
| `employment-act` | Employment Act (Cap. 89) | 1 | 2000-04-17 to 2000-04-17 |
| `interpretation-act` | Interpretation and General Provisions Act (Cap. 153) | 1 | 1989-09-22 to 1989-09-22 |

The build made 7 commits:

| Commits | Kind |
| ---: | --- |
| 7 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-30.
- 2 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 1 laws in the record.
- 7 tags.

## Dates

Each commit is dated at noon (America/Grenada) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: A Grenada law takes effect on the day it names; the Constitution names 7 February 1974. https://laws.gov.gd

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `f9a07f8b4076a99bffa1a8724de78e49f5d90d657dd634eeccc8445cc8abc684` (1643161 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3d00541d258745461ab52b1b0cb4e1716a27a95d`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

7 versions of 7 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

A second build from the same corpus into an empty folder gave identical hashes for all 7 history commits and 7 tags (history tip `b205aca632a2aa466c3dc37445f922a4e13452b8`).

## Decisions made by hand

- Scope: the Constitution in the Schedule to Cap. 128A, with its Appendices 1 to 3 and the transitional provisions (Appendix 2 to the Schedule). The Act's own two sections, the Constituency Boundaries Order and the Public Service regulations in the same PDF are left out.
- No dated past versions are online, so there is one version, credited to the publisher as "oldest version available" and dated 7 February 1974, the commencement day printed in the Act.
- Line breaks inside a paragraph were joined using the PDF indentation; Part headings are not kept as separate files; typographic quotes and dashes were normalised.
- Criminal Code (Cap. 72A, Act No. 76 of 1958 as consolidated in the Revised Laws, amendments to Act No. 15 of 2007): one section file per section (1 to 446, with lettered sections), plus the Schedule form. Part, Title and sub-headings are not kept as files. The text is the current consolidation, one version credited to the publisher as "oldest version available" and dated 20 January 1987, the commencement date printed under the long title. The consolidation includes amendments up to 2007, which are not separate versions.
- Section 137 prints no heading in the PDF (its paragraphs start straight after the number); its file has the number only.
- Companies Act (Cap. 58A, Act No. 35 of 1994 as consolidated in the Revised Laws, amendments to Act No. 6 of 1997): the commercial-law statute, since Grenada has no commercial code. One file per section (1 to 550, with 516A and 516B). Part headings are not kept as files. The Companies Regulations (SRO 2 of 1995, as amended to SRO 5 of 2009) in the same PDF are left out. One version credited to the publisher as "oldest version available", dated 18 November 1994, the commencement date printed under the long title; the consolidation includes later amendments, which are not separate versions.
- No civil code: Grenada has none (private law is common law and statute), so no civil-code equivalent was built.
- Criminal Procedure Code (Cap. 72B, amended to Act No. 30 of 1989 and later Acts as consolidated): One file per section; Part, Title and centred sub-headings are not kept as files. The text is the current consolidation in the Revised Laws on laws.gov.gd: one version credited to the publisher as "oldest version available", dated from the date printed under the long title; later amendments included in the consolidation are not separate versions. Subsidiary legislation printed in the same PDF is left out. Tables are given row by row as the PDF text layer prints them. The date printed under the long title is 20 January 1897. Sections 47 to 50 (bail) are listed in the arrangement but the body prints no text for them, so they have no file. Sections 141 and 184 are printed without the full stop after the number. The Schedule of forms is one unit.
- Evidence Act (Cap. 92, amended to Act No. 26 of 2000): One file per section; Part, Title and centred sub-headings are not kept as files. The text is the current consolidation in the Revised Laws on laws.gov.gd: one version credited to the publisher as "oldest version available", dated from the date printed under the long title; later amendments included in the consolidation are not separate versions. Subsidiary legislation printed in the same PDF is left out. Tables are given row by row as the PDF text layer prints them. The date printed under the long title is 20 January 1897.
- Employment Act (Cap. 89, Act No. 14 of 1999 amended by Act No. 10 of 2000, SRO 10 of 2000 and Act No. 21 of 2000): the labour statute. One file per section; Part, Title and centred sub-headings are not kept as files. The text is the current consolidation in the Revised Laws on laws.gov.gd: one version credited to the publisher as "oldest version available", dated from the date printed under the long title; later amendments included in the consolidation are not separate versions. Subsidiary legislation printed in the same PDF is left out. Tables are given row by row as the PDF text layer prints them. The date printed under the long title is 17 April 2000. The Schedule (public contracts) is one unit.
- Interpretation and General Provisions Act (Cap. 153, Act No. 30 of 1989 amended by Act No. 3 of 1991, Act No. 21 of 1991 and Act No. 35 of 2000): One file per section; Part, Title and centred sub-headings are not kept as files. The text is the current consolidation in the Revised Laws on laws.gov.gd: one version credited to the publisher as "oldest version available", dated from the date printed under the long title; later amendments included in the consolidation are not separate versions. Subsidiary legislation printed in the same PDF is left out. Tables are given row by row as the PDF text layer prints them. The date printed under the long title is 22 September 1989.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none
