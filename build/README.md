# Build

Everything published from this repo — the two HTML editions, both PDFs, the
figure rasters and the LinkedIn cover — is regenerated from the two Markdown
files at the repo root by the scripts here. No path points outside the repo.
A fresh clone rebuilds everything.

## The reconstruction rule

The first version of this pipeline lived in a session scratchpad and was lost
when the machine cleaned `/tmp`. The illustrated editions were recovered only
because the published pages could be read back. So:

1. The generator ships beside the sources, never in a scratchpad.
2. Before a generator is trusted for edits, it must reproduce the *current*
   published output — visible text, tag sequence and every anchor identical.
   `build_report.py` prints that validation on every run.
3. Anything injected by anchor fails the build when its anchor is missing.
   A silent miss is how figures vanish.

## Order

```
python3 build/fonts.py          # once per machine: downloads and flattens the faces
python3 build/build_report.py   # markdown -> html/frontier-ai-governance-september-2026.html
python3 build/build_essay.py    # markdown -> html/everyone-is-arguing-about-the-wrong-thing.html
python3 build/render_figs.py    # figures/figure-N.png at 2400px
python3 build/render_pdf.py     # both PDFs at the repo root
python3 build/cover.py          # figures/linkedin-cover-1920x1080.png
```

The essay must build after the report: it lifts the stylesheet and two plates
from the built report so the editions cannot drift apart.

| File | What it does |
|---|---|
| `paths.py` | Every path, relative to the repo root. |
| `build_report.py` | Report markdown → HTML. Notes with backrefs, movement dividers, Part eyebrows. Injects the bespoke blocks from `report_blocks.json` after the paragraph each follows. |
| `report_blocks.json` | The figures, pull quotes, stat cards, policy grid, bar chart, eye row, cast grid and page head — everything that is not prose. Keyed by the last 80 characters of the anchor paragraph. |
| `anchor_overrides.json` | When an edit changes an anchor paragraph's tail, map the old tail to the new one here. The build reports which anchors it could not find, so a miss is never quiet. |
| `build_essay.py` | Essay markdown → HTML. |
| `plates_new.py` | The two data figures (policy inversion, verifiability ledger) and their CSS. |
| `fonts.py` | Fetches Fraunces and Newsreader, flattens them to static instances, writes `fonts.css` (gitignored; regenerate). |
| `render_pdf.py`, `render_figs.py`, `cover.py` | Headless-Chrome renders. |

## Two traps

**Chrome's print-to-PDF will not embed a variable font.** It falls back to a
system serif and reports nothing. Pinning `wght` alone leaves `fvar` in place
and still fails; every axis must be pinned (`opsz`, and `SOFT`/`WONK` for
Fraunces). `fonts.py` does this.

**Text inside SVG is where every legibility bug in this project came from.**
Labels overran their plates, white fills landed on pale ground, type that read
at article size vanished when enlarged. The two data figures are HTML for that
reason. Prefer HTML for anything carrying words.
