# Replacement figures for the tug-of-war and iceberg plates.
#
# Both are HTML rather than SVG. Every legibility fault in this project came
# from text inside SVG: labels overrunning their plates, white fills landing on
# pale ground, type too small to read once enlarged. HTML text wraps, scales
# with the reader's settings, and inherits the theme tokens, so none of those
# failure modes are reachable.
#
# Chart colours are the dataviz-validated categorical pair, not the house
# accents: the house petrol fails the OKLCH chroma floor (0.063) and reads as
# grey. Light #0891b2/#b9721b and dark #1093ae/#c2812f both pass every check.

CHART_CSS = """
  :root{ --c-amodei:#0891b2; --c-liu:#b9721b; }
  @media (prefers-color-scheme: dark){
    :root:not([data-theme="light"]){ --c-amodei:#1093ae; --c-liu:#c2812f; }
  }
  :root[data-theme="dark"]{ --c-amodei:#1093ae; --c-liu:#c2812f; }

  .inv{ margin:.5em 0 .2em; }
  .inv-key{ display:flex; gap:20px; justify-content:flex-end; font-size:.66rem;
            letter-spacing:.09em; color:var(--muted); margin-bottom:12px; }
  .inv-key i{ display:inline-block; width:11px; height:11px; border-radius:50%;
              margin-right:7px; vertical-align:-1px; }
  .inv-key .sw-a{ background:var(--c-amodei); }
  .inv-key .sw-b{ background:var(--c-liu); }
  .inv-scale, .inv-row{ display:grid; grid-template-columns:47% 1fr; gap:18px; align-items:center; }
  .inv-scale{ font-size:.62rem; letter-spacing:.11em; color:var(--muted); margin-bottom:6px; }
  .inv-ends{ display:flex; justify-content:space-between; }
  .inv-row{ padding:10px 0; border-top:1px solid var(--rule); }
  .inv-pol{ font-size:.87rem; line-height:1.34; }
  .inv-track{ position:relative; height:18px; }
  .inv-rail{ position:absolute; top:8px; left:8px; right:8px; height:2px;
             background:repeating-linear-gradient(90deg, color-mix(in srgb, var(--ink) 34%, transparent) 0 7px, transparent 7px 14px); }
  .inv-mid{ position:absolute; top:0; left:50%; width:1px; height:18px;
            background:color-mix(in srgb, var(--ink) 22%, transparent); }
  .inv-dot{ position:absolute; top:1px; width:16px; height:16px; border-radius:50%;
            box-shadow:0 0 0 2px var(--paper-raised); }
  .inv-dot.a{ background:var(--c-amodei); } .inv-dot.b{ background:var(--c-liu); }
  .inv-note{ font-size:.7rem; color:var(--muted); margin-top:10px; font-style:italic; }

  .ledger{ margin:.5em 0 .2em; border:1px solid var(--rule-strong); }
  .led-open{ padding:10px 13px; background:color-mix(in srgb, var(--petrol) 12%, transparent);
             font-size:.78rem; line-height:1.45; border-bottom:1px solid var(--rule-strong); }
  .led-open b{ color:var(--petrol); letter-spacing:.09em; font-size:.66rem; margin-right:9px; }
  .led-row{ display:grid; grid-template-columns:1fr 1.5fr .52fr; border-top:1px solid var(--rule); }
  .led-row > span{ padding:11px 13px; font-size:.82rem; line-height:1.42; border-left:1px solid var(--rule); }
  .led-row > span:first-child{ border-left:none; font-weight:600; }
  .led-head{ border-top:none; background:var(--ink); }
  .led-head > span{ color:var(--paper-raised); font-size:.64rem; letter-spacing:.09em; padding-block:8px; font-weight:600; }
  .led-when{ font-family:'IBM Plex Mono',monospace; font-size:.72rem !important; color:var(--redline); font-weight:600; }
  @media (max-width:520px){
    .led-row{ grid-template-columns:1fr; }
    .led-row > span{ border-left:none; border-top:1px solid var(--rule); }
    .led-head{ display:none; }
    .inv-scale, .inv-row{ grid-template-columns:1fr; gap:6px; }
  }
"""

def _row(policy, amodei_supports):
    """One policy. The dot on the right is whoever supports it."""
    left, right = ("b", "a") if amodei_supports else ("a", "b")
    return (f'<div class="inv-row"><span class="inv-pol">{policy}</span>'
            f'<span class="inv-track"><i class="inv-rail"></i><i class="inv-mid"></i>'
            f'<i class="inv-dot {left}" style="left:0"></i>'
            f'<i class="inv-dot {right}" style="right:0"></i></span></div>')

# Every row is sourced in Part VIII of the report.
POLICIES = [
    ("Outside evaluators embedded in every frontier lab", True),
    ("Chip export controls on China, sustained", True),
    ("A crackdown on distillation", True),
    ("An antitrust waiver so firms can pace together", True),
    ("Open-weight release of frontier models", False),
]

PLATE_INVERSION = (
    '<figure class="plate">\n<div class="inv">\n'
    '<div class="inv-key mono cap"><span><i class="sw-a"></i>Amodei</span>'
    '<span><i class="sw-b"></i>Liu</span></div>\n'
    '<div class="inv-scale mono cap"><span></span>'
    '<span class="inv-ends"><span>Opposes</span><span>Supports</span></span></div>\n'
    + "\n".join(_row(p, s) for p, s in POLICIES) +
    '\n<p class="inv-note">Liu has never stated a position on SB 53\'s compute threshold, '
    'so it is left off rather than inferred.</p>\n'
    '</div>\n<figcaption>Two men, both arguing from safety, split on five policies: on four of them '
    'Amodei supports what Liu opposes, and on open weights the poles simply swap. '
    '<b>The middle of this chart is empty.</b></figcaption>\n</figure>'
)

LEDGER = [
    ("How the strongest model behaves",
     "Claude Mythos 5.1 was withheld from Britain's AI Security Institute — the first exclusion of an allied government's safety body on record",
     "no date set"),
    ("What the frontier actually scores",
     "Every public benchmark measures Fable, the deliberately safeguarded twin of the same underlying model",
     "no date set"),
    ("Which models are legally &ldquo;frontier&rdquo;",
     "SB 53 leaves the 10<sup>26</sup>-operation determination to the developer, and no register exists or can be built",
     "indefinite"),
    ("What went wrong inside a lab",
     "SB 53 exempts incident reports from public-records requests; anonymized summaries are not due before January 2027",
     "Jan 2027"),
]

PLATE_LEDGER = (
    '<figure class="plate">\n<div class="ledger">\n'
    '<div class="led-open"><b class="mono cap">Still public</b>Safety frameworks, model cards, '
    'and a transparency report at each deployment — the half of SB 53 the labs already satisfied.</div>\n'
    '<div class="led-row led-head mono cap"><span>What outsiders cannot see</span>'
    '<span>What closes it</span><span>Open again</span></div>\n'
    + "\n".join(
        f'<div class="led-row"><span>{a}</span><span>{b}</span>'
        f'<span class="led-when">{c}</span></div>' for a, b, c in LEDGER) +
    '\n</div>\n<figcaption>Four mechanisms, each arriving for its own reasons, compound into one '
    'result: <b>less about the frontier can be checked from outside each year, while the claims '
    'made about it grow louder.</b></figcaption>\n</figure>'
)
