# Production methodology

Source: Higgsfield AI, "3-Step Workflow To Make Ultra-Realistic AI Ads"
(https://www.youtube.com/watch?v=3rDs6FhFoUQ). Their companion article with
every prompt from the tutorial is saved at `higgsfield/prompt-library.txt`;
their shotlist Claude skill is at `.claude/skills/marty-shotlist-director/`.
This document is the distilled workflow plus what we change for Marty.

## The three stages

### Stage 1 — Build and lock every asset before any motion

Everything that recurs on screen gets a locked reference image first: the
character, the product, each location, each prop. Consistency across scenes
comes from these references, not from prompt wording.

Techniques that carry the weight:

- **Character sheets**: split-frame layout, a facial close-up that locks the
  face plus full-body front and back that lock the build. Plain grey
  background so nothing competes with the character.
- **Face-lock edit**: a sheet with two faces makes video models drift. Erase
  the face from the full-body panel so exactly one face remains to lock onto.
- **State variants as separate locked sheets**: the tutorial builds a dry hero
  (`@s_hero`) and a sweat-soaked hero (`@s_hero_wet`) because a character who
  changes mid-scene drifts unless both states are themselves references.
- **Locations at a 3/4 angle**: gives the room depth for the camera to move
  through. Head-on flats collapse.
- **Prop sheets**: orthographic turnarounds on neutral grey, strictly
  unbranded unless the brand is ours.
- **Schematic layout maps**: text cannot pin positions; a top-down schematic
  can. Mark fixed landmarks and lock positions and relative sizes on it, then
  attach it to prompts as a location reference.

### Stage 2 — The prompting framework

A Claude skill turns the script into a connected shotlist. Assets get stable
names (`@hero`, `@bag`, `@kitchen`) used identically in the prompts and in the
generation platform, so references auto-attach.

Prompt anatomy, in fixed order:

1. **Style prefix** — one global block locking look, lens, lighting, color
   ratio (60:30:10), skin detail, acting style, physics, continuity, technical
   specs, and audio policy. Written once, prepended verbatim to every prompt.
   Per-scene lighting variations (morning kitchen vs midday stadium) edit the
   lighting lines only.
2. **Characters** — short vivid anchors for only the characters in this
   prompt, carrying state forward (wet, exhausted, same wardrobe).
3. **Scene** — one or two sentences, geo-spatial: where everyone and
   everything is, relative to the location and each other.
4. **CUT 1..n** — each cut names shot type, lens or FOV, camera position and
   movement, then the acting beat by beat. Choreography is spelled out move by
   move ("he dances" alone yields generic flailing). Diegetic sound noted.

Each prompt targets 15 seconds. Longer scenes split into 1a, 1b, 1c with full
prefix and character blocks each, continuity held across them. Music is not
generated; movement is locked to a supplied track (`@music_track`) and the real
track is added in the edit.

Recurring shot grammar worth reusing: match-cut ear-tap transitions between
scenes, jump-cut product montages, body-rig (snorricam) product locks,
broadcast super-telephoto coverage, worm's-eye passes, held single-take
packshots.

### Stage 3 — Generate, iterate, edit

Generate per prompt, many takes. Iterate the prompt when failure is
systematic; regenerate when it is luck. Keep seconds, not clips: the finished
ad is assembled from keeper moments across dozens of generations, cut to
music.

## What changes for Marty

The tutorial's style prefix demands "Photorealistic — no 3D render, no game
engine" because its hero is a human. Marty inverts the trick: the world, the
people, the lighting and the cinematography stay strictly photoreal, and
exactly one element is a stylized CG creature rendered to feature-film VFX
standard (the Ted / Detective Pikachu / Monsters Inc.-in-our-world recipe).

Consequences:

- The style prefix gains a **creature clause**: one CG character, Pixar-grade
  stylization, film-VFX integration (grounded contact shadows, fur responding
  to wind and touch, light and color spill from the environment onto the fur,
  reflections where due), and everything else in frame photoreal. No cartoon
  physics unless scripted.
- The character bible needs material studies a human hero does not: fur
  grooming and response, horn and paw surfacing, how the fur reads in real
  daylight vs interiors.
- A **scale + integration reference** (Marty next to a real human in a real
  location) becomes a Stage 1 asset in its own right, because the entire
  premise rides on that composite reading as believable.
- Voice is grunts and reactions only, so no lip-sync dependency anywhere in
  the pipeline.

## Platform mapping

The tutorial runs on Higgsfield (GPT Image 2 for sheets and schematics, Soul
Cinema for photoreal stills, Seedance 2.0 for video). We run on Kie.ai's REST
API with the same division of labor: an image model for sheets, edits and
schematics; Seedance-family video models for scenes. Verified model IDs and
costs live in `CLAUDE.md`. Format: master 16:9 with center-safe framing;
derive 9:16 per scene by crop or re-generation.
