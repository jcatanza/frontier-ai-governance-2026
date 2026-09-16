import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
import io, os, re, subprocess
H = paths.HTML_ESSAY
OUT = paths.FIG_DIR + "/"
os.makedirs(OUT, exist_ok=True)
s = io.open(H, encoding="utf-8").read()
css = "\n".join(re.findall(r"<style>.*?</style>", s, re.S))
figs = re.findall(r'<figure class="plate">.*?</figure>', s, re.S)
print("figures:", len(figs))
SHELL = """<!doctype html><html data-theme="light"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500;1,9..144,600&family=Newsreader:ital,wght@0,400;0,500;0,600;1,400;1,500&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
@@CSS@@
<style>
html,body{background:#fff;margin:0;padding:0;}
:root{padding:0 !important;}
body{padding:0 !important;width:1200px;}
figure.plate{margin:0;padding:34px 30px 26px;border-top:3px solid var(--ink);
  border-bottom:1px solid var(--rule);background:var(--paper-raised);}
figure.plate svg{max-width:1080px;}
figure.plate figcaption{font-size:21px;max-width:64ch;line-height:1.55;}
.label-sm{font-size:14px !important;} .label-md{font-size:18px !important;}
/* the HTML figures need their type scaled for a 1200px raster too */
.inv-pol{font-size:19px !important;} .inv-key{font-size:15px !important;}
.inv-scale{font-size:14px !important;} .inv-note{font-size:15px !important;}
.inv-row{padding:15px 0 !important;}
.inv-dot{width:22px !important;height:22px !important;top:0 !important;}
.inv-rail{top:11px !important;}
.inv-track{height:24px !important;}
.led-open{font-size:17px !important;} .led-open b{font-size:14px !important;}
.led-row > span{font-size:18px !important;} .led-head > span{font-size:14px !important;}
.led-when{font-size:16px !important;}
</style></head><body>@@FIG@@</body></html>"""
for i, fig in enumerate(figs, 1):
    p = OUT + f"fig{i}.html"
    io.open(p, "w", encoding="utf-8").write(SHELL.replace("@@CSS@@", css).replace("@@FIG@@", fig))
    png = OUT + f"figure-{i}.png"
    if os.path.exists(png): os.remove(png)
    subprocess.run(["google-chrome","--headless=new","--disable-gpu","--no-sandbox",
        f"--user-data-dir={paths.SCRATCH}/udf","--crash-dumps-dir="+paths.SCRATCH,"--virtual-time-budget=25000",
        "--force-device-scale-factor=2","--window-size=1200,1000",
        "--default-background-color=FFFFFFFF",f"--screenshot={png}","file://"+p],
        capture_output=True, timeout=180)
    try:
        from PIL import Image, ImageChops
        im = Image.open(png).convert("RGB")
        bg = Image.new("RGB", im.size, im.getpixel((im.width-2, im.height-2)))
        bb = ImageChops.difference(im, bg).getbbox()
        if bb: im.crop((0,0,im.width,min(im.height,bb[3]+24))).save(png)
    except Exception as e: print("   crop skipped:", e)
    cap = re.search(r"<figcaption>(.*?)</figcaption>", fig, re.S)
    cap = re.sub(r"<[^>]+>","",cap.group(1)).strip() if cap else "-"
    im = __import__("PIL.Image", fromlist=["Image"]).open(png)
    print(f"  figure-{i}.png {im.width}x{im.height} — {' '.join(cap.split())[:70]}")
