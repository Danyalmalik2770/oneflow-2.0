# tidy — app promo

**Concept (one sentence about the picture):** a mess is swept into
order by one bar — and the bar turns out to be the app itself.

**Length:** 12.4s · 5 beats · vertical 1080×1920

## Beat sheet

| # | Beat | What happens | Carries across |
|---|------|--------------|----------------|
| 1 | 2.4s | Clutter: dots and blocks scattered at random | `hero` — one yellow dot |
| 2 | 2.6s | The dot becomes a sweep bar; the surviving dots line up in a row | `hero` — the bar |
| 3 | 2.8s | The bar becomes the app window; the dots move inside as list bullets, rows beside them | `hero` — the window |
| 4 | 2.4s | The name "Tidy" arrives; a green ring marks the first row done | `hero` — the window |
| 5 | 2.2s | The camera settles: "done — in one take" | — |

## Checker verdict

```
boundary 1 -> 2: jump 0.4   carry score 0.99 ✓
boundary 2 -> 3: jump 2.5   carry score 0.96 ✓
boundary 3 -> 4: jump 0.0   carry score 1.00 ✓
boundary 4 -> 5: jump 0.0   carry score 1.00 ✓
PASS: 5 beats, every boundary carried.
```

## Render it

```bash
python3 ../../make_film.py sheet.json -o film.mp4
```

## What was rejected, and why

- **The first render.** The four list bullets were invisible: they
  sat *behind* the app window, because the engine painted elements in
  creation order and the window was created after them. A promo whose
  list has no bullets is a broken promo. The fix went into the engine,
  not the sheet: within a beat, elements now paint in sheet order
  (later = on top), and the film was re-rendered. The sheet lists the
  window first and the bullets after it — backgrounds first, labels
  last.
