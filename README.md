# Marty

Sticker Mountain's yeti mascot, rebuilt as a film-grade CG character that lives
in real-world footage, for a series of short marketing videos.

The production method follows Higgsfield's "3-Step Workflow To Make
Ultra-Realistic AI Ads" (https://www.youtube.com/watch?v=3rDs6FhFoUQ), adapted
for a stylized CG creature instead of a photoreal human. See
`docs/METHODOLOGY.md` for the workflow and `character/MARTY.md` for the
character canon.

## Layout

| Path | What it holds |
|---|---|
| `character/MARTY.md` | The character canon. Every prompt derives from this. |
| `character/reference/` | Source mascot art from the client |
| `character/sheets/` | Generated reference sheets, each with the prompt that made it |
| `docs/METHODOLOGY.md` | The production workflow |
| `docs/higgsfield/` | The source prompt library from the tutorial |
| `.claude/skills/marty-shotlist-director/` | Shotlist skill (Stage 2) |
| `tools/kie/` | Kie.ai generation scripts |
| `tools/browser/` | Headless Chromium launcher for this environment |

## Status

Milestone 1: character bible, in progress. No video generation until the
character is approved and the story arc is set.
