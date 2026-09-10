#!/usr/bin/env python3
"""Build the client-facing Marty character bible page.

The client edition of review/build.py: same visual system, but written for
Sticker Mountain rather than for review. No sign-off prompts, no next-steps
messaging, no internal pipeline sheets. Adds the standard character-reference
material: overview, specifications, palette, on-screen rules, and a short
section on why the asset matters.

Inlines the sheet images as data URIs so the page is self-contained and
publishable as an Artifact. Output goes to argv[1] (default:
review/client.html, which is gitignored; the page is rebuilt, not committed).
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
    "integration": data_uri("character/sheets/v2/05b-integration-v1-look.png"),
    "identity":    data_uri("character/sheets/v2/01-identity.png"),
    "exp_up":      data_uri("character/sheets/v2/02-expressions-up.png"),
    "exp_down":    data_uri("character/sheets/v2/03-expressions-down.png"),
    "poses":       data_uri("character/sheets/v2/04-poses.png"),
    "fur":         data_uri("character/sheets/04-fur-macro.png"),
    "source":      data_uri("character/reference/marty-climbing-detail.png", width=700, quality=85),
}

def plate(img, label, body):
    return f'''
<figure class="plate">
  <img src="{IMG[img]}" alt="{label}">
  <figcaption>
    <div class="plate-head"><span class="plate-label">{label}</span></div>
    <p>{body}</p>
  </figcaption>
</figure>'''

SPECS = [
    ("Species", "Yeti. Friendly, not fearsome."),
    ("Height", "6&prime;0&Prime; (183 cm), horns excluded. Beside a 5&prime;7&Prime; adult his eye line sits just above theirs."),
    ("Build", "Athletic. Broad shoulders, deep chest, tapered waist, long arms."),
    ("Horns", "Two, one each side, curving up and out, with soft segment ridges."),
    ("Hands and feet", "Four fingers, three toes. Soft rounded tips, never claws."),
    ("Tail", "None."),
    ("Eyes", "Large and round, white sclera, teal irises. Thin dark eyebrows carry most of the acting."),
    ("Voice", "Grunts, gasps, chuckles, happy little roars. He never speaks words."),
    ("Render", "Feature-film CG creature placed in photoreal live-action footage."),
]

specs_html = "".join(
    f'<div class="spec"><span class="spec-label">{k}</span><span>{v}</span></div>'
    for k, v in SPECS)

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
  .plate figcaption p {{ margin: 4px 0 0; color: var(--ink-soft); font-size: 15px; max-width: none; }}
  .specs {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 14px; margin: 24px 0 10px;
  }}
  .spec {{
    border: 1px solid var(--panel-edge); border-radius: 10px;
    background: var(--panel); padding: 12px 16px 14px;
    display: grid; gap: 3px; font-size: 15px;
  }}
  .spec-label {{
    font-family: "IBM Plex Mono", monospace;
    font-size: 11.5px; font-weight: 500; letter-spacing: .1em; text-transform: uppercase;
    color: var(--teal-deep);
  }}
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
  .rules {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin: 24px 0 10px; }}
  @media (max-width: 640px) {{ .rules {{ grid-template-columns: 1fr; }} }}
  .rules > div {{ border: 1px solid var(--panel-edge); border-radius: 10px; background: var(--panel); padding: 16px 20px 18px; }}
  .rules h3 {{
    font-family: "IBM Plex Mono", monospace; font-size: 13px; font-weight: 500;
    letter-spacing: .1em; text-transform: uppercase; margin: 0 0 10px;
  }}
  .rules .yes h3 {{ color: var(--teal-deep); }}
  .rules .no h3 {{ color: var(--warm); }}
  .rules ul {{ margin: 0; padding-left: 18px; display: grid; gap: 9px; font-size: 15px; }}
  .why {{ border-left: 3px solid var(--teal); padding: 4px 0 4px 18px; margin: 22px 0; }}
  .why p {{ margin: 10px 0; }}
  .foot {{
    margin-top: 70px; padding-top: 18px; border-top: 1px solid var(--panel-edge);
    font-family: "IBM Plex Mono", monospace; font-size: 12.5px; color: var(--ink-soft);
  }}
  @media print {{
    :root, :root:not([data-theme="light"]), :root[data-theme="dark"] {{
      --ground: #FFFFFF;
      --panel: #EFF6FA;
      --panel-edge: #C9DEE9;
      --ink: #16303E;
      --ink-soft: #4A6472;
      --teal: #0082B1;
      --teal-deep: #00658A;
      --warm: #C72A50;
      --chip-edge: rgba(22,48,62,.14);
    }}
    body {{ font-size: 14px; }}
    .wrap {{ max-width: none; padding: 0 0 20px; }}
    .standfirst {{ font-size: 16px; }}
    h2 {{ margin-top: 36px; break-after: avoid; }}
    .plate, .spec, .rules > div, .duo figure, .chips li, .why {{ break-inside: avoid; }}
    .plate {{ margin: 18px 0 22px; }}
    .foot {{ margin-top: 40px; }}
  }}
</style>

<div class="wrap">
  <div class="eyebrow">Sticker Mountain · character reference · version 2</div>
  <h1>The Marty Bible</h1>
  <p class="standfirst">The master reference for Marty as a film-grade CG character.
  Every image and video of him starts from this document: the sheets below define
  how he looks, how he acts, and the rules he lives by on screen.</p>

  <figure class="plate">
    <img src="{IMG["integration"]}" alt="CG Marty standing beside a real woman on a sunlit city sidewalk">
    <figcaption>
      <div class="plate-head"><span class="plate-label">The premise</span></div>
      <p>Marty on a real street, beside a real person, in real light. He renders as a
      feature-film CG character with real contact shadows and sunlight in his fur, while
      everything else in frame stays photoreal. Every video in the series is built on
      this idea: one impossible thing, and a world that treats him as ordinary.</p>
    </figcaption>
  </figure>

  <h2>Who Marty is</h2>
  <p>Marty is Sticker Mountain's yeti: the big, strong, guileless best friend.
  He is enthusiastic, easily delighted, and quick to help, with the power in
  his body and the warmth in his face. He plays the full range, from triumphant
  to genuinely sad, but he never stays down long and he is never scary. He
  carries no dialogue; his grunts, gasps, and eyebrows do the talking, and the
  humans around him carry the words.</p>

  <h2>Specifications</h2>
  <div class="specs">{specs_html}</div>

  <h2>From sticker to screen</h2>
  <p>The translation starts from Sticker Mountain's own artwork. The colors below are
  sampled directly from the brand's mascot art, not invented: the teal of the horns and
  hands, the blue-ringed eyes, the raspberry mouth. What changes is the medium. Flat
  vector shapes become groomed fur, molded horn, and glass-wet eyes that hold up under
  a movie camera.</p>

  <div class="duo">
    <figure>
      <img src="{IMG["source"]}" alt="Original Sticker Mountain vector art of Marty climbing">
      <figcaption>Source: the brand's vector Marty, the color authority for the build.</figcaption>
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
  <p>The palette rule: white beast, teal trim, one warm accent. Blue appears only at
  the horns, hands, feet, lips, and irises. Nothing else on him is blue.</p>

  <h2>The identity sheet</h2>
  {plate("identity", "Sheet 01 · Identity",
    "The master reference: face close-up plus full-body front and back views. Every generated image and video is checked against this sheet. Broad shoulders, deep chest, tapered waist, a wild animal's frame under the fur, all warmth above the neck.")}

  <h2>The acting range, up</h2>
  {plate("exp_up", "Sheet 02 · Expressions · up range",
    "Six faces, one character. The default grin, amazed delight, a gentle smile, the deadpan, a bashful hands-clasped moment, and a big laugh. This is the register Marty lives in by default.")}

  <h2>He can lose, too</h2>
  <p>Marty carries no dialogue, so when a story needs a setback, his face and
  shoulders have to play it. This range keeps him sympathetic the whole way
  down, and the recovery cell matters most: for Marty, sadness is a visit, not
  a residence.</p>
  {plate("exp_down", "Sheet 03 · Expressions · down range",
    "Disappointed, a frustrated pout, hangdog self-pity, real sadness, big pleading eyes, and the smile starting to come back. Never scary, never bitter, always the big guy you want to cheer up.")}

  <h2>Body language</h2>
  {plate("poses", "Sheet 04 · Poses",
    "Full-body acting: run, jump, presenting to camera, double thumbs up, a playful tiptoe sneak, and a proud hero stance. With no dialogue in the videos, body language like this does the talking.")}

  <h2>Up close, where believability lives</h2>
  {plate("fur", "Sheet 05 · Materials",
    "Fur, horn, and palm at film close-up distance. Individual strands, soft clumping, flyaway hairs at the silhouette, micro-texture on the horn. This is the level of finish the camera can move in on.")}

  <h2>On-screen rules</h2>
  <p>These keep Marty the same character in every appearance, whoever is producing him.</p>
  <div class="rules">
    <div class="yes">
      <h3>Always</h3>
      <ul>
        <li>He is the only stylized element in frame. The world around him stays strictly photoreal.</li>
        <li>He is lit by the scene he stands in. The white coat takes the environment's light and color.</li>
        <li>He moves with real weight. Floors thud softly, held objects obey gravity, fur settles a half beat after he stops.</li>
        <li>He recovers fast. Setbacks are played fully, then let go.</li>
      </ul>
    </div>
    <div class="no">
      <h3>Never</h3>
      <ul>
        <li>Never speaks words. No lip-sync, anywhere. Humans in scene carry the dialogue.</li>
        <li>Never menacing. Upset means deflated or frustrated, and his size never becomes scary.</li>
        <li>Never off-model color. No blue body fur, no extra blue elements, no invented markings.</li>
        <li>Never a costume, a plush toy, or a photoreal animal. He is a living CG creature with big cartoon eyes.</li>
      </ul>
    </div>
  </div>

  <h2>Why a character bible</h2>
  <div class="why">
    <p>Marty is now produced by AI generation tools, and those tools drift: run the
    same request twice and the proportions, colors, and face shift a little each
    time. This document is the fixed measure that keeps him one character. Every
    frame is generated against these sheets and checked against them, so the Marty
    in a video, a social post, and a print piece is the same Marty.</p>
    <p>It also makes the character portable. Anyone producing Marty work, now or
    years from now, starts from this page instead of from memory, and questions of
    what he would or would not do settle against the sheets instead of opinion.
    A logo has brand guidelines for the same reason. This is that document for a
    character.</p>
  </div>

  <div class="foot">the marty bible · character reference, version 2 · sticker mountain · prepared by pixel blade creative · 2026</div>
</div>
'''

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "review", "client.html")
with open(out, "w") as f:
    f.write(HTML)
print(out, f"{os.path.getsize(out)/1e6:.1f} MB")
