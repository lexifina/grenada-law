# Grenada: law history in git

The law of Grenada (GD) as a git history: one file per provision, one commit per law on the day it took effect, and the law that made the change as the commit author. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `gd/`.

**Small build.** Language: English (the official language).

| Folder | Text | Versions | History |
| --- | --- | ---: | --- |
| `constitution/` | Constitution of Grenada (Grenada Constitution Act, Cap. 128A, Schedule): preamble, sections 1 to 111, Appendices 1 to 3 and the transitional provisions | 1 | Oldest version available: the current consolidated text, dated 7 February 1974, the commencement day the Act prints |
| `criminal-code/` | Criminal Code (Cap. 72A): sections 1 to 446 and the Schedule form | 1 | Oldest version available: the current consolidated text (amendments to Act No. 15 of 2007), dated 20 January 1987, the commencement date the Code prints |
| `companies-act/` | Companies Act (Cap. 58A): sections 1 to 550; the commercial-law statute (the Companies Regulations are not included) | 1 | Oldest version available: the current consolidated text (amendments to Act No. 6 of 1997), dated 18 November 1994, the commencement date the Act prints |
| `criminal-procedure-code/` | Criminal Procedure Code (Cap. 72B): sections 1 to 200 and the Schedule of forms (sections 47 to 50 print no text) | 1 | Oldest version available: the current consolidated text, dated 20 January 1897, the date the Code prints |
| `evidence-act/` | Evidence Act (Cap. 92): sections 1 to 168 | 1 | Oldest version available: the current consolidated text (amendments to Act No. 26 of 2000), dated 20 January 1897, the date the Act prints |
| `employment-act/` | Employment Act (Cap. 89): sections 1 to 92 and the Schedule; the labour statute | 1 | Oldest version available: the current consolidated text, dated 17 April 2000, the commencement date the Act prints |
| `interpretation-act/` | Interpretation and General Provisions Act (Cap. 153): sections 1 to 69 | 1 | Oldest version available: the current consolidated text (amendments to Act No. 35 of 2000), dated 22 September 1989, the date the Act prints |

**Why only these.** [laws.gov.gd](https://laws.gov.gd) publishes the Revised Laws of Grenada (2010 edition) and later Acts as separate PDFs, with no dated past versions and no per-section amendment notes. The Constitution has not been amended since 1974, and its PDF has a clean text layer, so it can be recorded without guessing. The Criminal Code, Criminal Procedure Code, Evidence Act, Companies Act, Employment Act and Interpretation and General Provisions Act are consolidations whose PDFs also have clean text layers. Grenada has no civil code (private law is common law and statute), so no civil code is built. The as-enacted 1974 text is not online, so the history starts at this version.

**Source:** [Laws of Grenada](https://laws.gov.gd), official, retrieved 29 October 2026. See `LICENSE` and `REPRODUCE.md`.

Dates are the day the change took effect. This repository is not legal advice; for anything that matters, read the original.
