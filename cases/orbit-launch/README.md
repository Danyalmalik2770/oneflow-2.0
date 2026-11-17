# orbit-launch — product launch film

**Concept (one sentence about the picture):** one point of light is
the whole film — it wakes into the lamp's ring, the ring rises as
its features arrive, and at the end it folds back into a single
point of light above the name.

**Length:** 12.6s · 5 beats · vertical 1080×1920 · look:
`midnight-launch` · rendered with `--blur 2 --sound`

## Beat sheet

| # | Beat | What happens | Carries across |
|---|------|--------------|----------------|
| 1 | 2.2s | A single dot of light rests in the dark | `hero` — the light |
| 2 | 2.6s | The dot opens into the lamp's glowing ring; the name fades in at its centre; the camera pushes in | `hero` — the light |
| 3 | 3.2s | The ring floats up; three feature cards arrive beneath it, one by one | `hero` — the light |
| 4 | 2.6s | The cards leave; the ring folds back into a point of light; the ORBIT lockup lands under it | `hero` — the light |
| 5 | 2.0s | Rest beat: the point of light breathes once and settles (`"sound": "none"` — the score rests too) | — |

## Checker verdict

```
boundary 1 -> 2: jump 0.0   carry score 1.00 ✓
boundary 2 -> 3: jump 1.2   carry score 0.98 ✓
boundary 3 -> 4: jump 1.6   carry score 0.97 ✓
boundary 4 -> 5: jump 0.2   carry score 1.00 ✓
PASS: 5 beats, every boundary carried. Total length 12.6s.
```

## Render it

```bash
python3 ../../make_film.py sheet.json -o film.mp4 --blur 2 --sound
```

## Notes

- This sheet is also `templates/product-launch.json` — copy it and
  rewrite the beats for your own product.
- Every colour in the sheet is a palette token (`$hero`, `$ink`,
  `$card`) from the `midnight-launch` look. Change `"look"` to
  `clean-light` and the same film renders on warm paper white.
- The sound was not added afterwards: `make_sound.py` scored it
  from this sheet — a whoosh where the camera pushes in, plucks as
  the three cards enter, a low hit under the lockup, silence in the
  rest beat.
