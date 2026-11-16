# chip — feature demo

**Concept (one sentence about the picture):** the pointer is the
thread — follow one dot and you have followed the whole feature.

**Length:** 12.6s · 5 beats · vertical 1080×1920

## Beat sheet

| # | Beat | What happens | Carries across |
|---|------|--------------|----------------|
| 1 | 2.6s | A menu card with three rows; a yellow dot rests on the first row | `hero` — the dot |
| 2 | 2.4s | The dot becomes the selection highlight on row two | `hero` — the highlight |
| 3 | 2.8s | The highlight flies down and becomes a chip inside the input bar | `hero` — the chip |
| 4 | 2.6s | The chip grows into the result card: "Done" | `hero` — the card |
| 5 | 2.2s | The camera settles: "ship it" | — |

## Checker verdict

```
boundary 1 -> 2: jump 0.1   carry score 1.00 ✓
boundary 2 -> 3: jump 2.6   carry score 0.96 ✓
boundary 3 -> 4: jump 1.3   carry score 0.98 ✓
boundary 4 -> 5: jump 0.0   carry score 1.00 ✓
PASS: 5 beats, every boundary carried.
```

## Render it

```bash
python3 ../../make_film.py sheet.json -o film.mp4
```

## What was rejected, and why

- **The first build of this film crashed the renderer.** The hero
  starts life as a dot and only becomes a card in beat 4; the engine
  built the card's inner structure only for elements that *start* as
  cards, so the morph arrived at a card with nothing inside it. The
  engine now prepares the card structure for any element that is a
  card in *any* beat — a carried element can become anything, and the
  renderer has to be ready for that. Fixed in the engine, verified by
  this film and by `tidy`, which morphs a dot into a window the same
  way.
