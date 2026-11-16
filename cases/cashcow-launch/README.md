# cashcow-launch — launch film

**Concept (one sentence about the picture):** one dot becomes
everything the product is — the prompt, the logo, the features —
without the camera ever cutting.

**Length:** 12.8s · 5 beats · vertical 1080×1920

Cashcow is an open-source tool that turns a written script into a
video. The film tells that story as a single thread: the dot is the
idea, the bar is the script, the plate is the finished video.

## Beat sheet

| # | Beat | What happens | Carries across |
|---|------|--------------|----------------|
| 1 | 2.4s | One yellow dot, alone | `hero` — the dot |
| 2 | 2.6s | The dot stretches into the prompt bar: "make me a video" | `hero` — the bar |
| 3 | 3.0s | The bar squares into the logo plate; three feature cards grow below it | `hero` — the plate |
| 4 | 2.6s | The cards leave; the name arrives under the plate | `hero` — the plate |
| 5 | 2.2s | The plate settles to centre; the lockup rests | — |

## Checker verdict

```
boundary 1 -> 2: jump 0.0   carry score 1.00 ✓
boundary 2 -> 3: jump 1.0   carry score 0.98 ✓
boundary 3 -> 4: jump 1.4   carry score 0.98 ✓
boundary 4 -> 5: jump 1.8   carry score 0.97 ✓
PASS: 5 beats, every boundary carried.
```

## Render it

```bash
python3 ../../make_film.py sheet.json -o film.mp4
```

## Notes

- This sheet is also the repo's starter template
  (`templates/launch-cashcow.json`) — copy it and change the words.
- The hero element never leaves the film: it is on screen, in one
  form or another, for all 12.8 seconds.
