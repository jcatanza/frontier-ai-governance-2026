"""Rebuild the essay's illustrated edition from its markdown.

The previous generator lived in a session scratchpad and was lost when /tmp was
cleaned. This one lives in the repo. Shared assets (stylesheet, the lorries and
timeline plates) are lifted from the report's published HTML so the two editions
cannot drift apart.
"""
import io, re, sys
sys.path.insert(0, '/home/jcatanz/build-ai-gov')
from plates_new import PLATE_INVERSION, PLATE_LEDGER, CHART_CSS

MD = "/home/jcatanz/projects/ai-governance/.claude/worktrees/frontier-ai-governance-rev3-edits-161705/frontier-ai-governance-essay.md"
REPORT_HTML = "/home/jcatanz/build-ai-gov/illustrated-rev4.html"
OUT = "/home/jcatanz/build-ai-gov/essay.html"

rep = io.open(REPORT_HTML, encoding="utf-8").read()
base_css = next(b for b in re.findall(r"<style>.*?</style>", rep, re.S) if "--ink:" in b)

def plate(aria):
    m = re.search(r'<figure class="plate">\s*<svg viewBox="[^"]*" role="img" aria-label="'
                  + re.escape(aria) + r'.*?</figure>', rep, re.S)
    return m.group(0)

CARS = plate("Two cars racing at full speed")
TIMELINE = plate("Timeline of the September 2026 cascade")

def inline(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", t)
    return t

title = sub = byline = standfirst = ""
body = []
for b in [x.strip() for x in io.open(MD, encoding="utf-8").read().split("\n\n") if x.strip()]:
    if b.startswith("# "):        title = b[2:].strip(); continue
    if b.startswith("### "):      sub = b[4:].strip(); continue
    if b.startswith("**Joseph"):  byline = inline(b); continue
    if b.startswith("*The full report"): standfirst = inline(b.strip("*")); continue
    if b.startswith("## "):       body.append(f"<h2>{inline(b[3:].strip())}</h2>"); continue
    if b.startswith("---"):       continue
    body.append(f"<p>{inline(b)}</p>")

# figures sit after the paragraph whose closing words name them
AFTER = [("an argument already under way.", TIMELINE),
         ("nobody in power is debating.", PLATE_INVERSION),
         ("is a Fable number.", PLATE_LEDGER)]
out, placed = [], []
for blk in body:
    out.append(blk)
    for anchor, fig in AFTER:
        if anchor in blk and anchor not in placed:
            out.append(fig); placed.append(anchor)

missing = [a for a, _ in AFTER if a not in placed]
if missing:
    print("  !! anchors not found:", missing)

html = f"""<title>Arguing About the Wrong Thing</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500;1,9..144,600&family=Newsreader:ital,wght@0,400;0,500;0,600;1,400;1,500&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
{base_css}
<style>{CHART_CSS}</style>
<style>
  article p:first-of-type{{ font-size:1.22rem; line-height:1.6; }}
  .masthead + figure.plate{{ border-top:none; margin-top:0; }}
  .standfirst{{ font-size:.9rem; color:var(--muted); line-height:1.6; border-left:3px solid var(--signal); padding-left:14px; margin-top:18px; }}
  h1.title{{ font-size:clamp(2.3rem,7vw,3.6rem); }}
</style>
<div class="wrap">
<div class="masthead">
<p class="kicker mono cap">Frontier AI Governance <span class="dot">·</span> Essay <span class="dot">·</span> September 2026</p>
<h1 class="title">{title}</h1>
<p class="subtitle">{sub}</p>
<p class="byline">{byline}</p>
<p class="standfirst">{standfirst}</p>
</div>
{CARS}
<article>
{chr(10).join(out)}
</article>
</div>
"""
io.open(OUT, "w", encoding="utf-8").write(html)
print(f"  essay: {len(body)} blocks, {len(placed)+1} figures, {len(html)//1024} KB")
