# Marty — project instructions

CG mascot video production for Sticker Mountain (client roster: see the
`agency-clients` skill). Read `character/MARTY.md` before writing any
generation prompt; it is the single source of truth for the character.
`docs/METHODOLOGY.md` is the production workflow.

## Current state

- Milestone 1 complete: the character bible is APPROVED (round 2, 2026-08-28).
  Canon is `character/MARTY.md` + the `character/sheets/v2/` sheets. Round 1
  sheets are archived in `character/sheets/`. Usage: unrestricted per client.
- Story arc and marketing message: Spencer has one, not yet shared. Do not
  invent campaign story.
- Format: master 16:9, center-safe framing so 9:16 crops can be derived.
- Voice: grunts and reactions only. No dialogue, no lip-sync.

## Generation

All generation goes through Kie.ai's REST API directly. Composio's hosted MCP
blocks every generation tool under a marketplace policy; do not retry it.
`KIE_API_KEY` is injected at container start.

- `tools/kie/kie.sh "prompt" [model] [out]` — text-to-image, polls and downloads.
- `tools/kie/kie-img.sh "prompt" model out ref...` — with reference image
  inputs; local refs are auto-uploaded (see its header).

Verified 2026-08-28, by successful generation unless noted:

| Model | Use | Observed cost |
|---|---|---|
| `google/nano-banana-edit` | image edit / multi-reference, input key `image_urls` | ~4 credits/image |
| `gpt-image-2-image-to-image` | same, input key `input_urls`; slightly different render look | ~4 credits/image |
| `google/nano-banana` | text-to-image | (from corpsitetest) |
| `bytedance/seedance-2-5` | video; `prompt`, `first_frame_url`, `last_frame_url`, `reference_image_urls`, `reference_video_urls` | schema verified, not yet run |

The whole 8-generation character bible cost ~30 credits total.

Hard-won API notes:
- File uploads go to `https://kieai.redpandaai.co/api/file-base64-upload`, NOT
  api.kie.ai (docs' servers line is wrong). Files expire after ~3 days.
- The egress proxy 403s python-urllib's default User-Agent; send any curl or
  browser UA and it passes. kie-img.sh already does.
- Google's output-side safety filter intermittently eats harmless creature
  images (`failCode` 400/422 "unsafe" / "Prohibited Use policy"). Studio names
  ("Pixar", "Monsters Inc.") in the prompt reliably trigger it; multi-figure
  full-body grids trigger it stochastically. Fixes that worked: drop brand
  names, rephrase from "generate a study sheet of the character" to "a
  character chart for an animated film", or switch that one sheet to
  `gpt-image-2-image-to-image` (different filter).

## Environment gotchas (inherited from corpsitetest, verified there)

- Headless Chromium needs `--proxy-server` and `--ssl-version-max=tls1.2` to
  reach the internet. Import `tools/browser/launch.mjs`, never
  `chromium.launch()` directly.
- Environment variables are injected at container start; mid-session additions
  do not appear until a new session.
- YouTube bot-walls this egress IP. Fetch YouTube data via description/metadata
  scraping or mirrors, not the player API.

## Conventions

- Every generated asset in `character/sheets/` gets a sidecar `.prompt.txt`
  with the exact prompt and model that produced it. Outputs are rebuilt from
  prompts, not hand edited.
- Review pages are flat HTML, no build step, publishable as Artifacts.
- Client-facing prose: plain and direct, no em-dashes, describe what something
  does rather than asserting that it is good.
