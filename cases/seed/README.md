# seed — concept ad

**Concept (one sentence about the picture):** one seed is the whole
film — it grows into a plant, opens into a ring of light, and folds
back into a seed, because starting small is the whole story.

**Length:** 12.2s · 5 beats · vertical 1080×1920

## Beat sheet

| # | Beat | What happens | Carries across |
|---|------|--------------|----------------|
| 1 | 2.2s | A single yellow seed rests on a ground line | `hero` — the seed |
| 2 | 2.6s | The seed stretches into a green stem; two leaves enter; a bud appears on top | `bud` — the bud |
| 3 | 2.8s | The bud opens into a ring of light above the stem | `hero` — the stem |
| 4 | 2.4s | The camera pushes in; the ring grows; the word "grow" arrives | `hero` — the stem |
| 5 | 2.2s | Everything folds back into the seed; "start small" | — |

## Checker verdict

```
boundary 1 -> 2: jump 0.0   carry score 1.00 ✓
boundary 2 -> 3: jump 0.0   carry score 1.00 ✓
boundary 3 -> 4: jump 0.2   carry score 1.00 ✓
boundary 4 -> 5: jump 0.6   carry score 0.99 ✓
PASS: 5 beats, every boundary carried.
```

## Render it

```bash
python3 ../../make_film.py sheet.json -o film.mp4
```

## Notes

- The film loops by construction: the last frame is the first frame's
  subject, back at rest.
- The stem is the carry for three of the four boundaries; the bud
  carries the one boundary where the picture changes most.
