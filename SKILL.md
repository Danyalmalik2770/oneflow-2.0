# OneFlow — motion films that never cut

An agent skill for making short motion films (product launches,
feature demos, promos) that play as **one continuous take**: no scene
ever replaces another. Every beat grows out of the beat before it,
carried across the boundary by an element that survives and morphs,
while one virtual camera pans and zooms without cutting.

Free for everyone, for any purpose, forever — MIT licensed.

## The idea in one paragraph

Slideshows fail because beats *replace* each other. OneFlow films are
built the opposite way: you write a list of **beats**, and every beat
names a **carry** — the element that lives through the boundary and
visibly becomes the next beat (a dot stretches into a bar, the bar
becomes a logo plate, the plate folds into the lockup). The camera
never cuts; it drifts, pushes in, and settles. A checker then measures
the boundary: if the picture jumps, it was a cut, and the film fails.

## How a film is made

1. **Concept first, in one sentence about the picture** — "one dot
   becomes everything", "a bar becomes the product". Not three stories
   told with the same cards; one visual thread.
2. **Write the film sheet** (JSON, format in `make_film.py`'s
   docstring and in `templates/launch-cashcow.json`):
   - Vary beat lengths — rhythm dies when every beat is the same
     length. A short beat next to a long one is what pace feels like.
   - Every beat except the last names a `carry`, and that element id
     must exist in both beats around the boundary.
   - Give the camera a reason to move: push in on the important beat,
     pull back to reveal, then let it rest. Stillness is part of the
     language — a camera that never rests makes moves meaningless.
3. **Check continuity**: `python3 check_film.py <sheet.json>` — the
   carry check plus a rendered jump measurement at every boundary.
   Fix failures by strengthening the carry (same element, closer
   start/end geometry), never by adding a fade. Fades are cuts wearing
   a costume.
4. **Render**: `python3 make_film.py <sheet.json> -o film.mp4`
   (`--blur 2` for real temporal motion blur on fast moves).
5. **Show the human the film**, with the checker's verdict.

## Hard rules (each one cost a rejected film somewhere)

- **No cuts, no fades between beats.** The only allowed boundary is a
  morph of the carried element.
- **One hero thread.** The carry chain should be traceable from the
  first frame to the last; if a viewer can't say what the film's one
  thing was, the concept is wrong.
- **The camera is one camera.** Its position is a continuous path —
  never teleport it. Zoom and pan are interpolated across the whole
  film by construction; do not fight that with per-beat jumps in the
  camera values.
- **Rest beats are real beats.** Hold at least one moment nearly
  still. Constant motion reads as noise.
- **Text enters as an element, not a title card.** Words ride on the
  things that carry (a bar, a plate, a card), they do not get their
  own replacing screens.

## Files

- `make_film.py` — the renderer (film sheet JSON → MP4). The full
  format is documented in its docstring.
- `check_film.py` — the continuity checker (carry check + boundary
  jump measurement with a printed carry score per boundary).
- `templates/launch-cashcow.json` — a complete working film sheet:
  a launch film for Cashcow, an open-source video maker.
- `cases/` — finished films (concept ad, launch film, app promo,
  feature demo), each with its sheet and a breakdown carrying the
  checker's verdict. Study these before writing a new sheet.

## Requirements

Python 3.10+, `playwright` with Chromium, `Pillow`, and `ffmpeg`.
Rendering is deterministic: seek to any time, get the same frame.

## Asks that fit this skill

- "Make a 15-second launch film for my app — one take, no cuts."
- "Turn these three features into a demo where each one grows out of
  the last."
- "My motion video feels like a slideshow — rebuild it so every beat
  is carried."
