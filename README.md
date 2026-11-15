# Grenada: law history in git


The law of Grenada as a git history: one file per section, one commit per version on the day it took effect, and the law that made each change as the commit's author. `git blame` names who is credited with every line; `git log` lists every change to a section; picking a date gives the text in force that day. Each act here has one version so far, credited to the publisher.

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is Grenada's national law, which global-law reads at `grenada/national/acts/`.

**What is in it now:** seven acts of the Laws of Grenada, each in one version, the current consolidated text, with 1,677 provisions: the Constitution (Cap. 128A, Schedule), the Criminal Code (Cap. 72A), the Criminal Procedure Code (Cap. 72B), the Evidence Act (Cap. 92), the Companies Act (Cap. 58A), the Employment Act (Cap. 89) and the Interpretation and General Provisions Act (Cap. 153). [`REPRODUCE.md`](REPRODUCE.md) lists each act with its version and the choices made for it.

Each act is a folder named after it, with one file per section and one per schedule or appendix, and a `README.md` listing its provisions (`employment-act/sec-056.md` is section 56 of the Employment Act, annual leave). The Constitution is in `constitution/`, with its preamble, Appendices 1 to 3 and the transitional provisions.

The text is in English, as the Laws of Grenada PDFs print it.

## Questions as git commands

| Question | Command |
| --- | --- |
| Every change to section 56 of the Employment Act | `git log -p --word-diff -- employment-act/sec-056.md` |
| Who is credited with each line of section 56? | `git blame employment-act/sec-056.md` |
| Every version of the Employment Act, with the day each took effect | `git log --format="%h %(trailers:key=In-force,valueonly,separator=) %an" -- employment-act ':!*/README.md'` |
| Section 56 as in force on 1 January 2026 | `python tools/on.py 2026-01-01 employment-act 56` |

**Outside git**, we also host this record publicly, for free:

- **[Ask Claude about Grenadian law](https://global-law.lexifina.com/v1/try_claude?country=grenada)**: opens Claude with a first question ready.
- **[Ask ChatGPT](https://global-law.lexifina.com/v1/try_chatgpt?country=grenada)**: the same question in ChatGPT.
- **[Call the API in your browser](https://global-law.lexifina.com/v1/search_law?query=annual+leave&jurisdictions=grenada)**: a search of Grenadian law for "annual leave", returned as JSON. See the [documentation here](https://lexifina.com/api/global-law).

Both assistants read the record through the free Global law connector (MCP, `https://global-law.lexifina.com/mcp`); the first time, the chat gives you the link that adds it. Ask in English.

**Host it yourself easily.** All it takes is git and Python, and the tools run on your machine:

```sh
git clone --depth 1 https://github.com/lexifina/global-law && cd global-law
python3 tools/countries.py add grenada/national/acts
python3 tools/law.py show 2026-01-01 grenada/national/acts/employment-act/sec-056.md
```

Opened in Claude Code, Cursor, VS Code or Codex, the clone also starts a local MCP server with the same tools ([MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md)).

## Dates

Each commit is dated at noon, America/Grenada, on the day the version took effect, and carries it in its `In-force:` trailer:

- each act's one version is dated from the date the act prints under its long title (7 February 1974 for the Constitution, 17 April 2000 for the Employment Act); since the text is the current consolidation, this is the day the act began, not the day its latest amendment took effect;
- git cannot store dates before 1970, so the Criminal Procedure Code and the Evidence Act (both 20 January 1897) are dated from 1970-01-01, one second apart, with the real day in `In-force:`. Ask for a date with `tools/on.py`, not `git log --before`.

Every version is credited to the publisher, `Laws of Grenada (laws.gov.gd)`, as the "oldest version available"; no commit is credited to a law yet, because the site publishes no past versions.

## How it is checked

- `tools/check_repo.py` reads every version back from git on the day it took effect and on the day before and compares it with the corpus: 7 versions of 7 acts, 0 mismatches.
- Every commit's trailers parse; there are no merge commits, no dates that go backwards and none after the build.
- A second build from the same corpus gave the same hashes for all 7 commits and 7 tags; `data/versions.json` gives each source PDF's sha256. The results are in [`REPRODUCE.md`](REPRODUCE.md).
- History is append-only: later versions are appended, never forced.

## What it does not show

- **Most Grenadian law.** Only these seven acts: no other chapter of the Revised Laws, no later annual Acts, no statutory rules and orders and no case law.
- **Past versions.** The site gives each act only as currently consolidated; amendments already in it (to Act No. 15 of 2007 for the Criminal Code) are not separate commits, so an earlier date gives today's text.
- **The rest of each PDF.** Subsidiary legislation printed with an act (the Companies Regulations, for one) and the two sections of the Grenada Constitution Act itself are left out; sections 47 to 50 of the Criminal Procedure Code print no text, so they have no file.
- **Layout.** Part and Title headings are not kept, and tables are given row by row.

## Sources

| Source | Kind | Past versions | Notes |
| --- | --- | --- | --- |
| [Laws of Grenada](https://laws.gov.gd) (Government of Grenada) | Official legislation site | no, the current consolidation only, as PDF | Each act's text and the commencement date it prints |

## Licence

See [`LICENSE`](LICENSE). The Laws of Grenada site states no licence; Lexifina's own contributions (the arrangement of the history, the commit messages and the tools) are dedicated to the public domain under CC0 1.0.

No AI model wrote, translated or corrected legal text, and no model runs when the history is built; the scripts were written by an AI model (see [`REPRODUCE.md`](REPRODUCE.md)).

## More

From [lexifina/global-law](https://github.com/lexifina/global-law):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): every feature, and what every corpus must support (`git blame`, `law.py`, the MCP tools)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): questions and answers · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): proposing changes · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): the MCP server · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): how it was built · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): how current each corpus is · [Monitoring](https://github.com/lexifina/global-law/tree/main/monitoring): whether updates are running · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): how each official source is watched for changes
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): how fast the tools are, measured
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): charts and bridges across the world's law
- [Vulnerabilities](https://github.com/lexifina/global-law/tree/main/vulnerabilities): mistakes in legislation as published
