# Marty — project instructions

CG mascot video production for Sticker Mountain (client roster: see the
`agency-clients` skill). Read `character/MARTY.md` before writing any
generation prompt; it is the single source of truth for the character.
`docs/METHODOLOGY.md` is the production workflow.

## Current state

- Milestone 1 (character bible) in progress. Review gate: Spencer and Marcus
  approve the character before any video generation.
- Story arc and marketing message: Spencer has one, not yet shared. Do not
  invent campaign story.
- Format: master 16:9, center-safe framing so 9:16 crops can be derived.
- Voice: grunts and reactions only. No dialogue, no lip-sync.

## Generation

All generation goes through Kie.ai's REST API directly. Composio's hosted MCP
blocks every generation tool under a marketplace policy; do not retry it.
`KIE_API_KEY` is injected at container start.

- `tools/kie/kie.sh "prompt" [model] [out]` — text-to-image, polls and downloads.
- `tools/kie/kie-img.sh` — same, with reference image inputs (see its header).
- Record verified model IDs and observed credit costs in this file as they are
  confirmed.

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
