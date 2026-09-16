import io, re, sys
sys.path.insert(0, '/home/jcatanz/build-ai-gov')
from plates_new import PLATE_INVERSION, PLATE_LEDGER, CHART_CSS

def swap(path, out):
    s = io.open(path, encoding="utf-8").read()
    for aria, new in (("A tug-of-war between a locked vault", PLATE_INVERSION),
                      ("An iceberg diagram", PLATE_LEDGER)):
        pat = re.compile(r'<figure class="plate">\s*<svg viewBox="[^"]*" role="img" aria-label="'
                         + re.escape(aria) + r'.*?</figure>', re.S)
        s, k = pat.subn(lambda m: new, s)
        print(f"   {aria[:34]:36} replaced {k}")
    if "--c-amodei" not in s:
        # after the HOUSE stylesheet (the one defining --ink), never after the
        # publish skeleton's own reset block
        i = s.find("--ink:")
        j = s.find("</style>", i)
        s = s[:j+8] + "\n<style>" + CHART_CSS + "</style>" + s[j+8:]
        print("   chart palette block inserted after the house stylesheet")
    io.open(out, "w", encoding="utf-8").write(s)

R = "/home/jcatanz/.claude/projects/-home-jcatanz-projects-ai-governance--claude-worktrees-frontier-ai-governance-rev3-edits-161705/4f031dce-fd86-4ac8-9da3-5d5e6d2a0c23/tool-results/artifact-0239e89f-1789560619-6ca9.html"
print("report:")
swap(R, "/home/jcatanz/build-ai-gov/illustrated-rev4.html")
