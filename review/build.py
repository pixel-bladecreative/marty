#!/usr/bin/env python3
"""Build the Marty character bible review page.

Inlines the sheet images as data URIs so the page is self-contained and
publishable as an Artifact. Output goes to the path given as argv[1]
(default: review/index.html, which is gitignored; the page is rebuilt,
not committed).
"""
import base64, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def data_uri(relpath, width=1400, quality=82):
    from PIL import Image
    im = Image.open(os.path.join(ROOT, relpath)).convert("RGB")
    if im.size[0] > width:
        im = im.resize((width, int(im.size[1] * width / im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

IMG = {
    "integration": data_uri("character/sheets/05-integration.png"),
    "identity":    data_uri("character/sheets/01b-identity-sheet-v2.png"),
    "expressions": data_uri("character/sheets/02-expressions.png"),
    "poses":       data_uri("character/sheets/03-poses.png"),
    "fur":         data_uri("character/sheets/04-fur-macro.png"),
    "facelock":    data_uri("character/sheets/06-identity-facelock.png"),
    "source":      data_uri("character/reference/marty-climbing-detail.png", width=700, quality=85),
}

def plate(img, label, body, check=None, tag=None):
    tag_html = f'<span class="tag">{tag}</span>' if tag else ""
    check_html = f'<p class="check"><strong>Check this:</strong> {check}</p>' if check else ""
    return f'''
<figure class="plate">
  <img src="{IMG[img]}" alt="{label}">
  <figcaption>
    <div class="plate-head"><span class="plate-label">{label}</span>{tag_html}</div>
    <p>{body}</p>
    {check_html}
  </figcaption>
</figure>'''

HTML = f'''<title>The Marty Bible</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&family=Public+Sans:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
  :root {{
    --ground: #F7FAFC;
    --panel: #E9F3F8;
    --panel-edge: #C9DEE9;
    --ink: #16303E;
    --ink-soft: #4A6472;
    --teal: #0082B1;
    --teal-deep: #00658A;
    --warm: #C72A50;
    --chip-edge: rgba(22,48,62,.14);
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --ground: #0C1B24;
      --panel: #122833;
      --panel-edge: #1F3B4A;
      --ink: #DCEBF2;
      --ink-soft: #93AEBC;
      --teal: #3FB4DD;
      --teal-deep: #7FCDE8;
      --warm: #F06A8C;
      --chip-edge: rgba(220,235,242,.16);
    }}
  }}
  :root[data-theme="dark"] {{
    --ground: #0C1B24;
    --panel: #122833;
    --panel-edge: #1F3B4A;
    --ink: #DCEBF2;
    --ink-soft: #93AEBC;
    --teal: #3FB4DD;
    --teal-deep: #7FCDE8;
    --warm: #F06A8C;
    --chip-edge: rgba(220,235,242,.16);
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--ground);
    color: var(--ink);
    font-family: "Public Sans", system-ui, sans-serif;
    font-size: 16.5px;
    line-height: 1.6;
  }}
  .wrap {{ max-width: 960px; margin: 0 auto; padding: 48px 22px 90px; }}
  .eyebrow {{
    font-family: "IBM Plex Mono", monospace;
    font-size: 12.5px; letter-spacing: .14em; text-transform: uppercase;
    color: var(--teal);
  }}
  h1 {{
    font-family: "Fredoka", system-ui, sans-serif;
    font-weight: 600; font-size: clamp(40px, 7vw, 62px);
    line-height: 1.04; margin: 10px 0 14px; text-wrap: balance;
    letter-spacing: -0.01em;
  }}
  .standfirst {{ font-size: 19px; max-width: 620px; color: var(--ink-soft); margin: 0 0 40px; }}
  h2 {{
    font-family: "Fredoka", system-ui, sans-serif;
    font-weight: 500; font-size: 27px; margin: 64px 0 6px;
    text-wrap: balance;
  }}
  h2 + p {{ margin-top: 8px; }}
  p {{ max-width: 660px; }}
  .plate {{
    margin: 26px 0 34px;
    border: 1px solid var(--panel-edge);
    border-radius: 10px;
    overflow: hidden;
    background: var(--panel);
  }}
  .plate img {{ display: block; width: 100%; height: auto; }}
  .plate figcaption {{ padding: 14px 18px 16px; }}
  .plate-head {{ display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }}
  .plate-label {{
    font-family: "IBM Plex Mono", monospace;
    font-size: 13px; font-weight: 500; letter-spacing: .1em; text-transform: uppercase;
    color: var(--teal-deep);
  }}
  .tag {{
    font-family: "IBM Plex Mono", monospace;
    font-size: 11px; letter-spacing: .08em; text-transform: uppercase;
    border: 1px solid var(--chip-edge); border-radius: 99px;
    padding: 2px 10px; color: var(--ink-soft);
  }}
  .plate figcaption p {{ margin: 4px 0 0; color: var(--ink-soft); font-size: 15px; max-width: none; }}
  .plate .check {{ color: var(--ink); }}
  .check strong {{ color: var(--warm); font-weight: 600; }}
  .duo {{ display: grid; grid-template-columns: 1fr 1.15fr; gap: 18px; align-items: start; margin: 26px 0 10px; }}
  @media (max-width: 640px) {{ .duo {{ grid-template-columns: 1fr; }} }}
  .duo figure {{ margin: 0; border: 1px solid var(--panel-edge); border-radius: 10px; overflow: hidden; background: var(--panel); }}
  .duo img {{ display: block; width: 100%; height: auto; }}
  .duo figcaption {{ padding: 10px 14px; font-size: 14px; color: var(--ink-soft); }}
  .chips {{ display: flex; flex-wrap: wrap; gap: 12px; margin: 22px 0 8px; padding: 0; list-style: none; }}
  .chips li {{ display: flex; align-items: center; gap: 10px; border: 1px solid var(--chip-edge); border-radius: 10px; padding: 8px 14px 8px 8px; background: var(--panel); }}
  .swatch {{ width: 34px; height: 34px; border-radius: 8px; border: 1px solid var(--chip-edge); }}
  .chips b {{ display: block; font-size: 14px; font-weight: 600; }}
  .chips code {{ font-family: "IBM Plex Mono", monospace; font-size: 12.5px; color: var(--ink-soft); }}
  ol.decisions {{ max-width: 660px; padding-left: 22px; display: grid; gap: 12px; }}
  ol.decisions li strong {{ font-weight: 600; }}
  .next {{ border-left: 3px solid var(--teal); padding: 4px 0 4px 18px; margin: 22px 0; }}
  .next p {{ margin: 6px 0; }}
  .foot {{
    margin-top: 70px; padding-top: 18px; border-top: 1px solid var(--panel-edge);
    font-family: "IBM Plex Mono", monospace; font-size: 12.5px; color: var(--ink-soft);
  }}
</style>

<div class="wrap">
  <div class="eyebrow">Sticker Mountain · character development · round 1</div>
  <h1>The Marty Bible</h1>
  <p class="standfirst">Marty, rebuilt as a film-grade CG character who lives in the
  real world. This page is the review gate: nothing moves until the character is right.</p>

  <figure class="plate">
    <img src="{IMG["integration"]}" alt="CG Marty standing beside a real woman on a sunlit city sidewalk">
    <figcaption>
      <div class="plate-head"><span class="plate-label">Proof of premise</span></div>
      <p>CG Marty sharing a frame with a real person. Real sunlight, real contact shadow,
      rim light on the fur, everything else in frame photoreal. This is the look the whole
      video series is built on: the world stays live-action, and Marty is the one animated
      thing in it, rendered to feature-film standard.</p>
      <p class="check"><strong>Check this:</strong> does this feel like the Marty you want standing next to your customers?</p>
    </figcaption>
  </figure>

  <h2>From sticker to screen</h2>
  <p>The translation starts from Sticker Mountain's own artwork. Colors below are sampled
  directly from the site's mascot art, not invented: the teal of the horns and hands, the
  blue-ringed eyes, the raspberry mouth. What changes is the medium. Flat vector shapes
  become groomed fur, molded horn, and glass-wet eyes that hold up under a movie camera.</p>

  <div class="duo">
    <figure>
      <img src="{IMG["source"]}" alt="Original Sticker Mountain vector art of Marty climbing">
      <figcaption>Source: the site's vector Marty, color authority for the build.</figcaption>
    </figure>
    <figure>
      <img src="{IMG["identity"]}" alt="CG identity sheet: face close-up plus full-body front and back">
      <figcaption>The CG translation, master identity sheet.</figcaption>
    </figure>
  </div>

  <ul class="chips">
    <li><span class="swatch" style="background:#DFF4FA"></span><span><b>Snow fur</b><code>#DFF4FA</code></span></li>
    <li><span class="swatch" style="background:#0082B1"></span><span><b>Marty teal</b><code>#0082B1</code></span></li>
    <li><span class="swatch" style="background:#00699B"></span><span><b>Iris blue</b><code>#00699B</code></span></li>
    <li><span class="swatch" style="background:#DA345D"></span><span><b>Mouth raspberry</b><code>#DA345D</code></span></li>
  </ul>

  <h2>The identity sheet</h2>
  {plate("identity", "Sheet 01 · Identity",
    "The master reference. The close-up locks the face; the front and back views lock the build. Every future image and every second of video is generated against this sheet, so this is the one to get right.",
    check="horn shape and ridges, hand and foot color, mouth colors, overall body shape. The build came out rounder and more huggable than the slimmer vector Marty. Keep the round build, or slim him toward the source?")}

  <h2>The acting range</h2>
  {plate("expressions", "Sheet 02 · Expressions",
    "Six faces, one character. Left to right, top row: the default grin, amazed delight, a gentle smile. Bottom row: unimpressed deadpan, a content sly smile, a big laugh. The deadpan was not scripted but it is a gift for comedy timing and worth keeping.",
    check="does the personality read as Marty in every cell, even the quiet ones?")}
  {plate("poses", "Sheet 03 · Poses",
    "Full-body acting: run, jump, presenting to camera, double thumbs up, a playful tiptoe sneak, and a proud hero stance. Marty carries no dialogue in the videos, so body language like this does the talking.",
    check="anything here he would never do, or a signature pose that is missing?")}

  <h2>Up close, where believability lives</h2>
  {plate("fur", "Sheet 04 · Materials",
    "Fur, horn, and palm at film close-up distance. Individual strands, soft clumping, flyaway hairs at the edges, micro-texture on the horn. This is the level of detail that makes a CG character survive a real-world frame instead of looking pasted in.")}

  <h2>Pipeline asset</h2>
  {plate("facelock", "Sheet 05 · Face lock",
    "A production tool, not a portrait. Video models drift when a reference sheet contains more than one face, so this variant keeps exactly one: the close-up. The body views carry shape and color only. Included here for completeness; viewers can skip it.",
    tag="internal")}

  <h2>Decisions to confirm</h2>
  <ol class="decisions">
    <li><strong>Body build.</strong> The CG Marty is rounder than the vector art. It reads warm and huggable on screen. Confirm the round build or ask for a slimmer pass.</li>
    <li><strong>Scale.</strong> Proposed: chest height on an adult, about 4 ft 5. Big enough to be a yeti, small enough to be endearing next to customers.</li>
    <li><strong>Eyebrows.</strong> They came out frost-grey and subtle. The source art has thin dark brows. Either works on camera; pick one.</li>
    <li><strong>Colors.</strong> The palette is sampled from the website art. If brand guideline values exist, they replace the sampled ones.</li>
    <li><strong>Source art.</strong> Vector originals of Marty, if they exist, would sharpen every future sheet.</li>
    <li><strong>Usage.</strong> Any trademark or brand rules on how Marty may appear.</li>
  </ol>

  <h2>What happens after sign-off</h2>
  <div class="next">
    <p>1 · Story. Script and beat sheet for the first spot, from the arc and marketing message.</p>
    <p>2 · World. Location and prop reference sheets for that story, built the same way Marty was.</p>
    <p>3 · Shotlist. The script becomes a connected list of 15-second scene prompts.</p>
    <p>4 · Film. Scenes generated, iterated, and cut to music. Master in 16:9, verticals derived for social.</p>
  </div>
  <p>Nothing on this page is published anywhere. It is a private review link.</p>

  <div class="foot">marty · character bible · round 1 · 2026-08-28</div>
</div>
'''

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "review", "index.html")
with open(out, "w") as f:
    f.write(HTML)
print(out, f"{os.path.getsize(out)/1e6:.1f} MB")
