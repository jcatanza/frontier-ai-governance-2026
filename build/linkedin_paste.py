"""LinkedIn paste edition of the essay: bare HTML with only paragraphs, the section
headings, italics and one link. Open it in a browser, select all, copy, and paste
into LinkedIn's article editor -- a rich-text paste keeps paragraphs and maps <h2>
to Heading 2, which a plain-text paste of the Markdown does not (it runs the
paragraphs together and drops the ## markers).

The title is not included: it goes in LinkedIn's title field. The byline is the
short feed-facing form; the repo editions keep the full credit. Images are placed
by hand afterwards (see the posting kit for where each goes).

    python3 build/linkedin_paste.py [out.html]      # default: build/.scratch/linkedin-paste.html
"""
import io, os, re, sys
import paths

REPO_URL = "https://github.com/jcatanza/frontier-ai-governance-2026"
BYLINE = "<strong>Joseph Catanzarite</strong>, with Claude as research and editorial partner."
DATE_LINE = "Written to the state of the record on 16 September 2026."

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def inline(t):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
    return t

def build(md):
    out, n_p, n_h = [], 0, 0
    for para in re.split(r"\n\s*\n", md.strip()):
        p = para.strip().replace("\n", " ")
        if p.startswith("# "):            # title -> LinkedIn's title field
            continue
        if p.startswith("### "):          # standfirst -> italic first line
            out.append(f"<p><em>{esc(p[4:])}</em></p>"); n_p += 1; continue
        if p.startswith("**Joseph"):      # byline -> short feed-facing form
            out.append(f"<p>{BYLINE}</p>"); n_p += 1; continue
        if p.startswith("*The full report"):   # pointer -> link the first words
            body = esc(p.strip("*"))
            body = body.replace("The full report", f'<a href="{REPO_URL}">The full report</a>', 1)
            out.append(f"<p><em>{body}</em></p>"); n_p += 1; continue
        if p == "---":
            continue
        if p.startswith("## "):
            out.append(f"<h2>{esc(p[3:])}</h2>"); n_h += 1; continue
        out.append(f"<p>{inline(p)}</p>"); n_p += 1
    out.append("<hr>")
    out.append(f'<p>The full report — 16,400 words, 100 endnotes, including the contested readings and the claims that remain unverified — is at <a href="{REPO_URL}">github.com/jcatanza/frontier-ai-governance-2026</a></p>')
    out.append(f"<p>{DATE_LINE}</p>")
    n_p += 2
    return "\n".join(out), n_p, n_h

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(paths.SCRATCH, "linkedin-paste.html")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    md = io.open(paths.MD_ESSAY, encoding="utf-8").read()
    body, n_p, n_h = build(md)
    html = ("<!doctype html><html><head><meta charset=\"utf-8\"><title>LinkedIn paste edition</title>"
            "<style>body{max-width:42em;margin:2em auto;font:17px/1.5 Georgia,serif}h2{font-size:1.25em}</style>"
            "</head><body>\n" + body + "\n</body></html>\n")
    io.open(out_path, "w", encoding="utf-8").write(html)
    print(f"  linkedin paste edition: {n_p} paragraphs, {n_h} headings -> {out_path}")
