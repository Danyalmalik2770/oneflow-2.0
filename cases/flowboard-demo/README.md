# flowboard-demo — feature demo film

**Concept (one sentence about the picture):** one tap is the whole
film — the pointer becomes the selection, the selection flies down
and becomes a chip in the input, and the chip grows into the result,
so the viewer watches a feature work instead of being told about it.

**Length:** 12.0s · 5 beats · vertical 1080×1920 · look:
`clean-light` · rendered with `--blur 2 --sound`

## Beat sheet

| # | Beat | What happens | Carries across |
|---|------|--------------|----------------|
| 1 | 2.2s | The Today card with three waiting rows; a small pointer dot rests on the first row | `hero` — the pointer |
| 2 | 2.4s | The pointer stretches into the highlight on the second row; the camera pushes in | `hero` — the pointer |
| 3 | 2.8s | The highlight flies down and becomes a chip inside the input bar; a hint line arrives | `hero` — the pointer |
| 4 | 2.6s | The chip grows into the Done card | `hero` — the pointer |
| 5 | 2.0s | Rest beat: the Done card settles; a single dot blinks beneath it (`"sound": "none"`) | — |

## Checker verdict

```
boundary 1 -> 2: jump 0.4   carry score 0.99 ✓
boundary 2 -> 3: jump 1.3   carry score 0.98 ✓
boundary 3 -> 4: jump 0.8   carry score 0.99 ✓
boundary 4 -> 5: jump 0.1   carry score 1.00 ✓
PASS: 5 beats, every boundary carried. Total length 12.0s.
```

## Render it

```bash
python3 ../../make_film.py sheet.json -o film.mp4 --blur 2 --sound
```

## Notes

- This sheet is also `templates/feature-demo.json` — the starting
  point for any "watch the feature work" demo: pick a row, carry the
  highlight into the input, grow the result.
- The menu rows are plain bars at low opacity, listed before the
  hero in each beat so the pointer always paints on top (the
  layering rule).
- Beat 3 is the longest camera move in the film, so its boundary
  whoosh is the strongest in the score — `make_sound.py` sizes
  whooshes by camera travel.
