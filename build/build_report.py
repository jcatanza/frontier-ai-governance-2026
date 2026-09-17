"""Build the report's illustrated HTML from its markdown.

The markdown is the source of truth for every word. The bespoke blocks -- the
figures, pull quotes, stat cards, policy grid, bar chart, eye row, cast grid --
are not in the markdown; they live in report_blocks.json, keyed by the tail of
the paragraph each one follows, and are injected after that paragraph. A block
whose anchor is not found fails the build loudly, because a silent miss is how
figures vanish.
"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
import io, json, re, sys

MD = paths.MD_REPORT
BLOCKS = paths.BLOCKS
OUT = paths.HTML_REPORT
ROMAN = {"I":1,"II":2,"III":3,"IV":4,"V":5,"VI":6,"VII":7,"VIII":8,"IX":9,"X":10,"XI":11,"XII":12}

def inline(t):
    # escape first, so markup we then generate is not itself escaped
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\[\^(\d+)\]", lambda m: f'<sup class="fn"><a id="r{m.group(1)}" href="#n{m.group(1)}">{m.group(1)}</a></sup>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", t)
    return t

def strip_tags(h):
    return " ".join(re.sub(r"<[^>]+>", "", h).split())

def build(md_path=MD, out_path=OUT, anchor_overrides=None):
    B = json.load(io.open(BLOCKS, encoding="utf-8"))
    src = io.open(md_path, encoding="utf-8").read()
    body_md, notes_md = src.split("\n## Notes", 1)

    title = sub = byline = revnote = ""
    body = []
    for p in [x.strip() for x in body_md.split("\n\n") if x.strip()]:
        if p.strip() == "---": continue          # horizontal rule: masthead/body divider, not a paragraph
        if p.startswith("# "):     title = p[2:].strip(); continue
        if p.startswith("### "):   sub = p[4:].strip(); continue
        if p.startswith("**Joseph"): byline = inline(p).replace("<strong>", "<b>").replace("</strong>", "</b>"); continue
        if not revnote and p.startswith("*") and not p.startswith("**"):   # the italic reading note under the byline
            revnote = inline(p.strip("*")); body.append(f"<p><em>{revnote}</em></p>"); continue
        m = re.match(r"^\*\*(PART [A-Z]+ — [^*]+)\*\*$", p)
        if m: body.append(f'<p class="movement mono cap">{m.group(1)}</p>'); continue
        m = re.match(r"^## ([IVX]+)\. (.+)$", p)
        if m: body.append(f'<span class="eyebrow mono cap">Part {m.group(1)}</span><h2>{inline(m.group(2))}</h2>'); continue
        m = re.match(r"^## Coda: (.+)$", p)
        if m: body.append(f'<span class="eyebrow mono cap">Coda</span><h2>{inline(m.group(1))}</h2>'); continue
        body.append(f"<p>{inline(p)}</p>")

    # inject bespoke blocks after their anchor paragraphs, preserving order
    inj = B["injections"]
    if anchor_overrides:
        for old, new in anchor_overrides.items():
            for j in inj:
                if j["anchor_tail"] == old: j["anchor_tail"] = new
    pending = list(inj); out = []
    for blk in body:
        out.append(blk)
        if blk.startswith("<p>"):
            tail = strip_tags(blk)[-80:]
            while pending and pending[0]["anchor_tail"] == tail:
                out.append(pending.pop(0)["html"])
    if pending:
        sys.exit("BUILD FAILED -- anchors not found for %d block(s):\n  " % len(pending)
                 + "\n  ".join(repr(p["anchor_tail"]) for p in pending))

    # notes from markdown, in the published li format
    lis = []
    for m in re.finditer(r"(?ms)^\[\^(\d+)\]:\s*(.*?)(?=^\[\^\d+\]:|\Z)", notes_md):
        n, txt = m.group(1), " ".join(m.group(2).split())
        lis.append(f'<li id="n{n}">{inline(txt)} <a class="backref" href="#r{n}" aria-label="back to text">↩</a></li>')
    ns = B["notes_section"]
    shell_before = ns.split('<ol class="notes">', 1)[0]
    shell_after = ns.split("</ol>", 1)[1]
    notes_html = shell_before + '<ol class="notes">\n' + "\n".join(lis) + "\n</ol>" + shell_after

    masthead = ('<div class="masthead">\n'
                '<p class="kicker mono cap">Frontier AI Governance <span class="dot">·</span> Illustrated Edition <span class="dot">·</span> September 2026</p>\n'
                f'<h1 class="title">{title}</h1>\n<p class="subtitle">{sub}</p>\n'
                f'<p class="byline">{byline}</p>\n<p class="revnote">{revnote}</p>\n</div>\n')
    html = (B["head"] + '<div class="wrap">\n' + masthead + B["cast"] + B["cars"] + "\n<article>\n"
            + "\n".join(out) + "\n</article>" + notes_html)
    io.open(out_path, "w", encoding="utf-8").write(html)
    return html, len(out), len(lis), len(inj)

if __name__ == "__main__":
    ov = json.load(io.open(paths.OVERRIDES, encoding="utf-8")) if os.path.exists(paths.OVERRIDES) else None
    # Capture the previously published HTML BEFORE building: build() overwrites OUT,
    # so reading it afterwards compares the new file with itself and always passes.
    ref = io.open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else None
    html, nblocks, nnotes, ninj = build(anchor_overrides=ov)
    print(f"built: {nblocks} blocks, {nnotes} notes, {ninj} injections")
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    a, b = (norm(ref) if ref is not None else None), norm(html)
    if ref is None:
        print("VALIDATION: no previously published HTML to compare against")
    elif a == b:
        print("VALIDATION: rebuilt HTML is identical to the previously published HTML")
    else:
        import difflib
        sa, sb = re.split(r"(?<=>)", a), re.split(r"(?<=>)", b)
        d = [l for l in difflib.unified_diff(sa, sb, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++","---")]
        print(f"VALIDATION: {len(d)} differing fragments (showing up to 12):")
        for l in d[:12]: print("   ", l[:170])
