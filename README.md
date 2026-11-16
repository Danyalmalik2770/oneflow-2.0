# OneFlow — motion films that never cut

**One continuous take. Every beat grows out of the one before it.**

Most AI-made motion videos are slideshows in disguise: title card,
fade, feature card, fade, logo. Each shot looks fine and the whole
still falls apart, because nothing connects one beat to the next —
scenes *replace* each other.

OneFlow builds films the other way. A film is a list of **beats**, and
at every boundary one element — the **carry** — survives and visibly
morphs into the next beat:

- a dot **stretches into** a bar;
- the bar **becomes** a logo plate;
- cards **grow out of** the plate;
- at the end, everything **folds back** into the lockup.

One virtual camera holds it all together. It never cuts: it pushes
in, pulls back, drifts — and rests, because rests are what make the
moves land.

And continuity is **measured, not hoped for**: the included checker
renders the frames around every boundary and fails the film if the
picture jumps. If it jumps, it was a cut.

## Free — really free

OneFlow is **MIT licensed**: free for personal *and* commercial use,
no paid tier, no licence to buy, no attribution required (though it
is appreciated). It exists so anyone can make a launch film that
feels finished, without paying for the privilege.

## Quick start

```bash
pip install playwright pillow
playwright install chromium
# plus ffmpeg on your PATH

python3 check_film.py templates/launch-cashcow.json   # continuity check
python3 make_film.py templates/launch-cashcow.json -o film.mp4
python3 make_film.py templates/launch-cashcow.json -o film.mp4 --blur 2
```

`--blur 2` renders at double frame rate and averages frame pairs —
real temporal motion blur, so fast morphs smear instead of strobing.

The demo film (the Cashcow launch sheet above, rendered) is in
[`demo/`](demo/).

## Write your own film

A film is one JSON file — beats, elements, a camera. The full format
is documented in the docstring of [`make_film.py`](make_film.py);
the working template is
[`templates/launch-cashcow.json`](templates/launch-cashcow.json).
The method — concept, beat sheet, carries, camera, rests — is written
up for humans and AI agents alike in [`SKILL.md`](SKILL.md).

Five element kinds: `dot`, `bar`, `text`, `card`, `ring`. An element
id that appears in two neighbouring beats morphs between its two
definitions; a new id enters (fade + grow); a dropped id exits (fade
out). That one mechanism is the whole trick — everything else is
taste.

## Use it with an AI agent

OneFlow is an agent skill: point Claude, or any agent that reads
skills, at this repo and say *"make me a 15-second launch film, one
take, no cuts"*. The protocol in `SKILL.md` is the same one a human
would follow.

## Honest limits

- Films are HTML/CSS elements on one plane — product shots are
  rebuilt as elements, not filmed footage. That is the style, and it
  is why the camera can move through them at any zoom.
- No sound design yet: render silent, add music/voice in your editor
  (or with a sister tool like Cashcow). Sound is on the roadmap.
- Text that changes on a carried element swaps at the boundary;
  geometry, colour and position are what morph.

## License

MIT — see [`LICENSE`](LICENSE). © 2026 Danyal Malik.
