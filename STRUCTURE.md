# Structure

| Folder | What it holds |
| --- | --- |
| `constitution/`, `criminal-code/`, `companies-act/`, ... | The seven acts first built here (one file per section) |
| `chapters/cap-<n>-<slug>/` | A chapter of the Revised Laws of Grenada (`cap-1-abatement-of-litter-act/`), as the Ministry of Legal Affairs site publishes it |
| `acts/<year>/<NNN>-<slug>/` | An Act as enacted, by year and number (`acts/2018/002-consumer-protection-act/`) |
| `sro/<year>/<NNN>-<slug>/` | A Statutory Rule and Order, by year and number |

Each folder holds `sec-NNN.md` per section (`sec-005a.md` is section 5A), `sch*.md` per schedule, `front.md` (long title),
`subsidiary.md` where the chapter prints subsidiary legislation, and a `README.md` with the source address and the
PDF's sha256. Where the sections cannot be split reliably (and for every S.R.&O.) the whole text is one `text.md`.
No folder holds more than 1,000 entries.

## Dates

One commit per instrument, at noon America/Grenada on the day it took effect (`In-force:`); `In-force-basis:` says why:

- `date-printed-under-long-title`: a chapter of the Revised Laws, dated by the day printed in square brackets under its
  long title (the Act's commencement). The text is the current consolidation, so this is the day the Act began;
- `commencement-clause`: an Act or S.R.&O. whose own text gives the day;
- `gazette-publication`: an Act or S.R.&O. that names no day but prints the Gazette day, on which it comes into operation
  (Interpretation and General Provisions Act, Cap. 153, ss. 6 and 21).

Before 1970 git cannot store a date: those commits are dated 1970-01-01, a second apart, with the real day in
`In-force:`. An instrument whose commencement is left to an order or notice, or that prints no day, is held out.
No date is the day we downloaded anything.
