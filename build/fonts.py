"""Fetch the display faces and flatten them to static instances.

Chrome's print-to-PDF silently refuses variable fonts and falls back to a system
serif, so Fraunces and Newsreader have to be instanced with EVERY axis pinned
(wght alone leaves fvar in place and still fails). Google's css2 endpoint is not
reachable from Chrome in this sandbox either, so the faces are embedded as data
URIs rather than linked.
"""
import base64, io, os, re, subprocess

W = os.path.expanduser("~/build-ai-gov/fontwork/")
os.makedirs(W, exist_ok=True)
B = "https://raw.githubusercontent.com/google/fonts/main/ofl"
SRC = {
    "Fraunces":          f"{B}/fraunces/Fraunces%5BSOFT%2CWONK%2Copsz%2Cwght%5D.ttf",
    "Fraunces-Italic":   f"{B}/fraunces/Fraunces-Italic%5BSOFT%2CWONK%2Copsz%2Cwght%5D.ttf",
    "Newsreader":        f"{B}/newsreader/Newsreader%5Bopsz%2Cwght%5D.ttf",
    "Newsreader-Italic": f"{B}/newsreader/Newsreader-Italic%5Bopsz%2Cwght%5D.ttf",
}
WANT = [("Fraunces", "Fraunces", "normal", [400, 500, 600, 700]),
        ("Fraunces-Italic", "Fraunces", "italic", [500, 600]),
        ("Newsreader", "Newsreader", "normal", [400, 500, 600]),
        ("Newsreader-Italic", "Newsreader", "italic", [400, 500])]
PLEX = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/140.0.0.0 Safari/537.36")


def build():
    for name, url in SRC.items():
        p = W + name + ".ttf"
        if not os.path.exists(p):
            subprocess.run(["curl", "-sL", "-o", p, url], timeout=240)
    faces = []
    for src, fam, style, ws in WANT:
        for wt in ws:
            out = f"{W}{src}-{wt}.ttf"
            if not os.path.exists(out):
                ax = ["wght=%d" % wt] + (["opsz=14", "SOFT=0", "WONK=0"]
                                         if src.startswith("Fraunces") else ["opsz=16"])
                subprocess.run(["uvx", "--quiet", "--from", "fonttools", "fonttools",
                                "varLib.instancer", f"{W}{src}.ttf", *ax, "-o", out],
                               capture_output=True, timeout=300)
            if os.path.exists(out):
                b64 = base64.b64encode(open(out, "rb").read()).decode()
                faces.append("@font-face{font-family:'%s';font-style:%s;font-weight:%d;"
                             "font-display:block;src:url(data:font/ttf;base64,%s) "
                             "format('truetype');}" % (fam, style, wt, b64))
    # IBM Plex Mono is shipped static already, so Google's own woff2 works
    css = subprocess.run(["curl", "-s", "-A", UA, PLEX],
                         capture_output=True, text=True, timeout=60).stdout
    for u in sorted(set(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css))):
        f = W + "plex_" + u.rsplit("/", 1)[-1]
        if not os.path.exists(f):
            subprocess.run(["curl", "-s", "-A", UA, "-o", f, u], timeout=120)
        if os.path.exists(f):
            b64 = base64.b64encode(open(f, "rb").read()).decode()
            css = css.replace(u, f"data:font/woff2;base64,{b64}")
    out = "\n".join(faces) + "\n" + css
    io.open(os.path.expanduser("~/build-ai-gov/fonts.css"), "w", encoding="utf-8").write(out)
    print(f"  fonts.css: {len(out)/1024:.0f} KB, {out.count('@font-face')} faces")
    return out


if __name__ == "__main__":
    build()
