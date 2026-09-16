# Build

Regenerates the HTML editions, the PDFs, the figure rasters and the LinkedIn
cover. These scripts live here because an earlier copy lived in a session
scratchpad and was lost when the machine cleaned `/tmp`, taking the only
generator for the illustrated editions with it.

| Script | What it does |
|---|---|
| `plates_new.py` | The two data figures — the policy inversion and the verifiability ledger — and their CSS. |
| `swap_figs.py` | Puts those figures into the report's HTML. |
| `build_essay.py` | Rebuilds the essay's HTML from `../everyone-is-arguing-about-the-wrong-thing.md`. |
| `fonts.py` | Downloads Fraunces and Newsreader, flattens them to static instances, emits `fonts.css`. |
| `render_pdf.py` | Both PDFs, via headless Chrome with print CSS. |
| `render_figs.py` | The figure PNGs at 2400px. |
| `cover.py` | The 1920×1080 LinkedIn cover. |

Order: `fonts.py` → `swap_figs.py` → `build_essay.py` → `render_figs.py` →
`render_pdf.py` → `cover.py`.

## Two things that will waste your afternoon if you rediscover them

**Chrome's print-to-PDF will not embed a variable font.** It falls back to a
system serif and reports nothing. Pinning `wght` alone is not enough — the
instancer leaves `fvar` in place and the font is still variable. Every axis has
to be pinned (`opsz`, and `SOFT`/`WONK` for Fraunces). `fonts.py` does this.

**Text inside SVG is where every legibility bug in this project came from.**
Labels overran their plates, white fills landed on pale ground, type that read
fine at article size disappeared when enlarged. The two data figures are HTML
for exactly this reason. Prefer HTML for anything carrying words.
