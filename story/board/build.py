#!/usr/bin/env python3
"""Build the Spot 1 storyboard review page. Same conventions as review/build.py."""
import base64, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def data_uri(relpath, width=1400, quality=82):
    from PIL import Image
    im = Image.open(os.path.join(ROOT, relpath)).convert("RGB")
    if im.size[0] > width:
        im = im.resize((width, int(im.size[1] * width / im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

FRAMES = [
    ("f0-street",      "0:00–0:04", "The street",
     "Marty solo on the sunlit sidewalk, buoyant, almost dance-stepping along, coffee in hand.",
     "Bright piano-led groove from frame one."),
    ("f1-great-day",   "0:04–0:06", "The entry",
     "Through the glass doors of the inner entrance, still bouncing.",
     "Groove keeps rolling."),
    ("f2-slap",        "0:06–0:08", "The slap",
     "The office bully smirks and presses the crooked DORK sticker onto Marty's chest.",
     "The groove runs right up to the hit."),
    ("f3-skip",        "0:08", "The skip",
     "Close on Marty. The grin dies as he looks down at the label.",
     "Needle skips off the record. Music dead."),
    ("f4-coffee-down", "0:08–0:12", "The deflation",
     "Shoulders slump. The quiet gut-punch: he sets the coffee down and does not sip it.",
     "No music. Office clatter, a dropped tray, a distant tire screech."),
    ("f5-her-decision","0:12–0:17", "Her decision",
     "Across the floor she sees it happen. A beat of thought, and she makes up her mind.",
     "Pizzicato strings, curious and light, building with her."),
    ("f6-peel",        "0:17–0:20", "The peel",
     "One slow, satisfying pull. The cheap label comes off his fur.",
     "Pizzicato resolves, holding its breath."),
    ("f7-press",       "0:20–0:23", "The press",
     "Macro: her thumb seats the gold-foil LEGEND label into his chest fur, the foil catching light.",
     "On the press, the piano groove blooms back in, bigger than before."),
    ("f8-return",      "0:23–0:25", "The return",
     "Marty lights up, chest out, wearing LEGEND. She laughs with him.",
     "Full cheery groove."),
    ("f8b-pat",        "0:25–0:27", "The send-off",
     "A pat on the shoulder and she walks off, glancing back smiling as he waves after her.",
     "Groove riding high, multi-angle pops."),
    ("f9-packshot",    "0:27–0:30", "The packshot",
     "The LEGEND label, beauty macro on deep teal, foil gleaming.",
     "Music ducks. VO: “Don’t let labels control you. Take control. Call Sticker Mountain.”"),
]

cards = ""
for i, (f, tc, name, action, audio) in enumerate(FRAMES, 1):
    img = data_uri(f"story/board/{f}.png")
    cards += f'''
<figure class="plate">
  <img src="{img}" alt="Frame {i}: {name}">
  <figcaption>
    <div class="plate-head"><span class="tc">{tc}</span><span class="plate-label">{i} · {name}</span></div>
    <p>{action}</p>
    <p class="audio">♪ {audio}</p>
  </figcaption>
</figure>'''

HTML = f'''<title>The Labels Board</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&family=Public+Sans:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
  :root {{
    --ground: #F7FAFC; --panel: #E9F3F8; --panel-edge: #C9DEE9;
    --ink: #16303E; --ink-soft: #4A6472;
    --teal: #0082B1; --teal-deep: #00658A; --warm: #C72A50;
    --gold: #8A6A1F;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --ground: #0C1B24; --panel: #122833; --panel-edge: #1F3B4A;
      --ink: #DCEBF2; --ink-soft: #93AEBC;
      --teal: #3FB4DD; --teal-deep: #7FCDE8; --warm: #F06A8C; --gold: #D9B75B;
    }}
  }}
  :root[data-theme="dark"] {{
    --ground: #0C1B24; --panel: #122833; --panel-edge: #1F3B4A;
    --ink: #DCEBF2; --ink-soft: #93AEBC;
    --teal: #3FB4DD; --teal-deep: #7FCDE8; --warm: #F06A8C; --gold: #D9B75B;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--ground); color: var(--ink);
    font-family: "Public Sans", system-ui, sans-serif; font-size: 16.5px; line-height: 1.6; }}
  .wrap {{ max-width: 960px; margin: 0 auto; padding: 48px 22px 90px; }}
  .eyebrow {{ font-family: "IBM Plex Mono", monospace; font-size: 12.5px;
    letter-spacing: .14em; text-transform: uppercase; color: var(--teal); }}
  h1 {{ font-family: "Fredoka", system-ui, sans-serif; font-weight: 600;
    font-size: clamp(40px, 7vw, 62px); line-height: 1.04; margin: 10px 0 14px;
    text-wrap: balance; letter-spacing: -0.01em; }}
  .standfirst {{ font-size: 19px; max-width: 640px; color: var(--ink-soft); margin: 0 0 14px; }}
  .meta {{ font-family: "IBM Plex Mono", monospace; font-size: 13px; color: var(--ink-soft); margin-bottom: 36px; }}
  .plate {{ margin: 26px 0 34px; border: 1px solid var(--panel-edge);
    border-radius: 10px; overflow: hidden; background: var(--panel); }}
  .plate img {{ display: block; width: 100%; height: auto; }}
  .plate figcaption {{ padding: 14px 18px 16px; }}
  .plate-head {{ display: flex; align-items: center; gap: 12px; margin-bottom: 4px; }}
  .tc {{ font-family: "IBM Plex Mono", monospace; font-size: 12.5px; font-weight: 500;
    color: var(--ground); background: var(--teal); border-radius: 6px; padding: 2px 9px; }}
  .plate-label {{ font-family: "IBM Plex Mono", monospace; font-size: 13px; font-weight: 500;
    letter-spacing: .1em; text-transform: uppercase; color: var(--teal-deep); }}
  .plate p {{ margin: 4px 0 0; color: var(--ink); font-size: 15.5px; }}
  .plate .audio {{ color: var(--gold); font-size: 14px; }}
  .note {{ border-left: 3px solid var(--teal); padding: 4px 0 4px 18px; margin: 40px 0; max-width: 660px; }}
  .note p {{ margin: 6px 0; color: var(--ink-soft); }}
  .foot {{ margin-top: 70px; padding-top: 18px; border-top: 1px solid var(--panel-edge);
    font-family: "IBM Plex Mono", monospace; font-size: 12.5px; color: var(--ink-soft); }}
</style>
<div class="wrap">
  <div class="eyebrow">Sticker Mountain · Marty · spot 1</div>
  <h1>The Labels Board</h1>
  <p class="standfirst">Round 2. Eleven frames, thirty seconds. A bully sticks a cheap label on
  Marty's great day; someone kinder replaces it with a better one. Every frame below
  was generated from the locked character, cast, location, and product references,
  so what you approve here is what the film will look like. This round: crisp air everywhere (no more mist), Marty height-locked above the coworker, the new solo street open, and the new pat-and-walk send-off.</p>
  <p class="meta">30s master · 16:9 center-safe · cutdowns 15s / 6s · music: Spencer's
  102 BPM track, needle-skip and SFX layered in the edit · VO closes: "Don't let
  labels control you. Take control. Call Sticker Mountain."</p>
  {cards}
  <div class="note">
    <p>What happens after sign-off: the board becomes the shotlist (15-second scene
    prompts with these frames as first-frame references), scenes generate on
    Seedance, keepers get cut to the track, then SFX, VO, and end card.</p>
    <p>Frames are storyboard stills, not final renders. Faces, fur, and label
    details sharpen at the video stage; the bully's smug close-up and Marty's
    full expression range live in the casting sheets.</p>
  </div>
  <div class="foot">marty · spot 1 storyboard · round 2 · 2026-08-28</div>
</div>
'''

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "story", "board", "index.html")
with open(out, "w") as f:
    f.write(HTML)
print(out, f"{os.path.getsize(out)/1e6:.1f} MB")
