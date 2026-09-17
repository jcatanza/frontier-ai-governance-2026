"""LinkedIn cover, built to their exact 1920x1080 so nothing is cropped."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
import io, os, re, subprocess
FONTS = io.open(paths.FONTS_CSS, encoding="utf-8").read()
rep = io.open(paths.HTML_REPORT, encoding="utf-8").read()
svg = re.search(r'<svg viewBox="0 0 820 260".*?</svg>', rep, re.S).group(0)

HTML = """<!doctype html><html data-theme="light"><head><meta charset="utf-8">
<style>@@FONTS@@</style>
<style>
  :root{ --ink:#14151d; --paper:#e9ebe3; --paper-raised:#f4f5ef;
         --signal:#b9721b; --petrol:#1d5c63; --redline:#a8402f; --muted:#5b5d6b; }
  *{box-sizing:border-box;margin:0;padding:0;}
  html,body{width:1920px;height:1080px;overflow:hidden;}
  body{background:var(--paper);color:var(--ink);font-family:'Newsreader',Georgia,serif;
       display:flex;flex-direction:column;}
  .sheet{flex:1;display:grid;grid-template-columns:1fr 1fr;align-items:center;
         gap:64px;padding:92px 96px 40px;}
  .kicker{font-family:'IBM Plex Mono',monospace;font-size:26px;letter-spacing:.18em;
          text-transform:uppercase;color:var(--muted);margin-bottom:44px;}
  .kicker span{color:var(--redline);}
  h1{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:112px;
     line-height:.98;letter-spacing:-.015em;margin-bottom:40px;}
  .hook{font-size:38px;line-height:1.42;color:var(--muted);max-width:24ch;
        border-left:5px solid var(--signal);padding-left:26px;}
  .art svg{width:100%;height:auto;max-width:none;}
  .label-sm{font-size:12px;} .label-md{font-size:15px;}
  .foot{border-top:5px solid var(--ink);padding:26px 96px 30px;display:flex;
        justify-content:space-between;align-items:baseline;}
  .byline{font-size:30px;} .byline b{font-weight:600;}
  .where{font-family:'IBM Plex Mono',monospace;font-size:24px;color:var(--muted);letter-spacing:.06em;}
</style></head><body>
<div class="sheet">
  <div>
    <p class="kicker">Frontier AI Governance <span>&middot;</span> September 2026</p>
    <h1>Everyone Is Arguing About the Wrong Thing</h1>
    <p class="hook">Two chief executives asked the industry to slow down. Both firms
    were weeks from the largest IPOs in American history.</p>
  </div>
  <div class="art">@@SVG@@</div>
</div>
<div class="foot">
  <p class="byline"><b>Joseph Catanzarite</b> &middot; with Claude as research and editorial partner</p>
  <p class="where">An essay, and a report</p>
</div>
</body></html>"""

p = os.path.join(paths.SCRATCH, "cover.html")
io.open(p, "w", encoding="utf-8").write(HTML.replace("@@FONTS@@", FONTS).replace("@@SVG@@", svg))
out = os.path.join(paths.FIG_DIR, "linkedin-cover-1920x1080.png")
if os.path.exists(out): os.remove(out)
subprocess.run(["google-chrome","--headless=new","--disable-gpu","--no-sandbox",
    f"--user-data-dir={paths.SCRATCH}/udc","--crash-dumps-dir="+paths.SCRATCH,"--virtual-time-budget=30000",
    "--force-device-scale-factor=1","--window-size=1920,1080",
    "--default-background-color=FFFFFFFF",f"--screenshot={out}","file://"+p],
    capture_output=True, timeout=200)
from PIL import Image
im = Image.open(out)
print(f"  cover: {im.width}x{im.height}, {os.path.getsize(out)//1024} KB")
