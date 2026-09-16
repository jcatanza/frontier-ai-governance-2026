"""Render both editions to PDF, and the LinkedIn cover, via headless Chrome."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
import io, os, re, subprocess
FONTS = io.open(paths.FONTS_CSS, encoding="utf-8").read()
os.makedirs(paths.SCRATCH, exist_ok=True)

PRINT_CSS = """<style>
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
html,body{background:#fff !important;}
:root{padding:0 !important;}
body{padding-inline:0 !important;padding-block:0 !important;font-size:10.5pt;}
.wrap{max-width:none !important;}
figure.plate,.statcards,.statcard,.polgrid,.barchart,.eyerow,blockquote.pull,
table,.ledger,.inv{break-inside:avoid;page-break-inside:avoid;}
figure.plate svg{max-width:460px !important;}
h1,h2,h3{break-after:avoid;page-break-after:avoid;}
h2{margin-top:1.6em !important;}
article p,ol.notes li{orphans:3;widows:3;}
.notes-wrap{break-before:page;page-break-before:always;}
ol.notes li{font-size:8.6pt;line-height:1.45;margin-bottom:.5em;}
a{color:inherit;text-decoration:none;}
</style>"""

def chrome(html, out, extra=()):
    if os.path.exists(out): os.remove(out)
    subprocess.run(["google-chrome","--headless=new","--disable-gpu","--no-sandbox",
        f"--user-data-dir={paths.SCRATCH}/ud","--crash-dumps-dir="+paths.SCRATCH,
        "--virtual-time-budget=40000", *extra, "file://"+html],
        capture_output=True, timeout=300)
    return os.path.exists(out)

def pdf(src, out_pdf):
    frag = io.open(src, encoding="utf-8").read()
    frag = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>',
                  "<style>"+FONTS+"</style>", frag)
    doc = ('<!doctype html>\n<html lang="en" data-theme="light">\n<head>\n<meta charset="utf-8">\n'
           + PRINT_CSS + "</head>\n<body>\n" + frag + "\n</body>\n</html>\n")
    p = os.path.join(paths.SCRATCH, os.path.basename(out_pdf).replace(".pdf", ".print.html"))
    io.open(p, "w", encoding="utf-8").write(doc)
    ok = chrome(p, out_pdf, ["--no-pdf-header-footer", f"--print-to-pdf={out_pdf}"])
    if ok:
        d = open(out_pdf,"rb").read()
        fonts = sorted({m.decode('latin1').split('+')[-1]
                        for m in re.findall(rb'/BaseFont\s*/([^\s/\]>]+)', d)})
        print(f"  {out_pdf}: {len(re.findall(rb'/Type\s*/Page[^s]', d))} pages, "
              f"{len(d)//1024} KB, fonts: {', '.join(fonts)[:70]}")
    else:
        print(f"  {out_pdf}: FAILED")

pdf(paths.HTML_REPORT, paths.PDF_REPORT)
pdf(paths.HTML_ESSAY, paths.PDF_ESSAY)
