# Spot 1 rebuild on the v4 pipeline

Started 2026-11-17. Same story as `../SPOT1-BEATSHEET.md`, all-new scene assets.
Engine: Higgsfield through the Composio CLI (`composio execute HIGGSFIELD_MCP_*`).
Pipeline reference: `higgsfield-master-pipeline-v4.md` in Spencer's Drive.

## Decisions

- Marty's identity is kept as approved in the bible (`character/sheets/v2`).
- City scene is kept. The office is rebuilt.
- Office direction: **E3** (`office/concepts/E3-sticker-company.png`), an ordinary
  corporate open-plan office dressed as a sticker company. Chosen for flat even
  ceiling light, carpet (no floor reflections), a 9 ft tile ceiling as a height
  ruler, and about 10 ft of clear floor.
- Location plates are three-quarter views.
- No blue on set or in wardrobe: Marty's fur and the brand palette are blue/teal.

## Why the rebuild

Marty clipped into office objects and did not sit in the space, for lighting and
sometimes for scale.

## Shot list direction (Spencer)

A mix of camera compositions that make sense, not only full-body shots: some
close, some wider. Scale and lighting must hold in every frame. Let the engine do
it with light prompting where it can; take explicit control where it cannot.

## Model notes

- `gpt_image_2_5` (quality high, 2k) follows long layout briefs. Use it for
  plates and sheets.
- `soul_cinematic` gives the most natural faces. Use it for casting portraits.
- `cinematic_studio_2_5` ignored the brief (returned a sci-fi corridor). Avoid.
- Seedance 2.5, 12 s: 36 credits as a 480p draft, 84 at 720p, 192 at 1080p.
