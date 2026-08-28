# Spot 1 music brief

Target vibe: Izzy Bizu, "White Tiger" — sunny UK neo-soul pop, piano-led,
bouncy swung groove, handclaps, playful energy, roughly 100-105 BPM.

Structure must mirror the story: cheery groove, hard stop at the DORK slap
(needle skip), a silent/SFX hole, pizzicato strings for the coworker's
decision, then the groove returns bigger at the LEGEND press.

Production rule: the needle skip, clattering, and tire screech are layered
as separate SFX in the edit for frame-accurate sync, even if the generated
track carries its own stop. Ask Suno for the hard stop and the pizzicato
bridge; do not rely on it for the foley.

The Suno prompts live in this file so they can be iterated; current version
below (v1, 2026-08-28). Backing track is wordless (oohs/scat only) so the
end VO sits clean.

## Suno prompt v1

Style (paste into the style/description field):

Upbeat British neo-soul pop, sunny and playful, in the spirit of 2016 UK
soul-pop. Bright bouncy piano riff leads the track. Swung feel-good groove
at 103 BPM, handclaps, warm round bassline, crisp live drums, subtle
tambourine. Female wordless vocals only: light oohs and playful scat, no
lyrics. Clean modern production, cheerful morning energy.

Structure (paste into the custom lyrics field):

[Intro: bright piano riff with handclaps, groove locks in immediately]
[Verse: bouncy full-band groove, playful wordless oohs riding the piano]
[Break: the music stops DEAD mid-bar, abrupt hard cut, two bars of near
silence with only a faint room tone]
[Bridge: curious pizzicato strings alone, light tiptoeing plucks, no drums,
gently building anticipation step by step]
[Chorus: the full band bursts back in, bigger and brighter than before,
joyful piano-led groove, claps, soaring oohs, triumphant and warm]
[Outro: groove settles low and soft, room left for a spoken voiceover, ends
clean on a piano chord]

Usage notes:
- Generate several takes; keep the one whose hard stop lands cleanly on a
  bar line, since the edit syncs the DORK slap to that stop.
- The pizzicato bridge maps to 0:13-0:18 (her decision and walk); the chorus
  re-entry maps to the LEGEND press at ~0:18-0:22.
- Trim the full song down to the 30s map in SPOT1-BEATSHEET.md; the intro
  groove needs only ~8 usable seconds before the stop.
- Needle skip, clatter, tire screech: layered in the edit, not from Suno.

## Delivered track v1 (spot1-backing-v1.wav)

Spencer-produced, received 2026-08-28 via Drive. 44.8s, 48kHz stereo WAV,
measured ~102 BPM. Structure from energy/band analysis (not by ear):

| Track time | Content |
|---|---|
| 0:00-0:10 | Intro/verse groove, piano-led, drums light |
| 0:11, 0:14, 0:16 | Three hard bass/drum dropouts (~1s each), mids continue |
| 0:17.5-0:28 | Full-band chorus, loudest section |
| 0:28.5 | Brief transition dip |
| 0:29-0:38 | Second full section |
| 0:39-0:40.5 | ~2s breakdown, drums out, sparse mids |
| 0:41-0:44.8 | Final full-band push, quick out |

Edit map to the 30s beat sheet (cut the music to picture):
- Picture 0:00-0:08 = track 0:00-0:08 intro groove.
- Picture 0:08 slap: hard-mute the track in the edit (do not rely on an
  in-track stop; the dead hole is built at the cut with needle-skip SFX).
- Picture 0:13-0:18 her decision = the sparse 0:14-0:17.5 stretch, or the
  0:39-0:40.5 breakdown looped, whichever reads plucky by ear.
- Picture 0:18 press = jump into the 0:17.5 chorus downbeat, the bloom.
- Picture 0:27-0:30 = duck under VO, end on the track's closing push.
