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

python3 check_film.py templates/product-launch.json   # continuity check
python3 make_film.py templates/product-launch.json -o film.mp4 --blur 2 --sound
```

`--blur 2` renders at double frame rate and averages frame pairs —
real temporal motion blur, so fast morphs smear instead of strobing.
`--sound` scores the film from its own events and muxes the score in
(see **Sound** below).

## Looks

A film sheet can name a **look** — a small JSON file in
[`looks/`](looks/) with a background and a colour palette:

```json
{ "title": "Orbit", "look": "midnight-launch", "beats": [ ... ] }
```

Elements then use palette tokens instead of raw hex — `"$hero"`,
`"$ink"`, `"$card"`, `"$accent"`, `"$muted"`, `"$onhero"` — and the
whole film can be re-skinned by changing one word. Four presets ship
with the repo: `midnight-launch` (dark stage, hot yellow hero),
`clean-light` (warm paper white, friendly), `neon-pop` (violet-black,
electric), `paper-craft` (craft paper, calm). Copy one and tweak it
to make your own.

## Sound

OneFlow scores its own films. `make_sound.py` reads the film sheet
and synthesises the score from what actually happens on screen:

- a soft pad chord under every beat;
- a **whoosh at every carried boundary**, sized by how far the
  camera travelled;
- a **pluck for every element that enters**, pitched from a scale
  by the element's id;
- a **low hit on the final beat** — the landing.

A beat can set `"sound": "none"` (rest beats stay quiet) or
`"sound": "hit"` (force a hit). No audio files, no samples, no
library music — and because the sound is derived from the beats, it
always fits the action. Run it standalone
(`python3 make_sound.py <sheet.json> -o sound.wav`) or let
`make_film.py --sound` mux it straight into the render.

## Films made with it

Every case ships its **film sheet** (the source — render the film
yourself with one command) and a **breakdown**: the concept, the beat
sheet, and the continuity checker's measured verdict. Nothing here is
a black box.

### Concept ad

- **seed** — one seed is the whole film: a dot becomes a stem, the
  stem's bud opens into a ring of light, and everything folds back
  into a seed. [Breakdown](cases/seed/README.md)

### Launch film

- **cashcow-launch** — a dot stretches into the prompt bar, the bar
  becomes the logo plate, and the feature cards grow out of the
  plate. [Breakdown](cases/cashcow-launch/README.md)
- **orbit-launch** — a smart lamp wakes up: a dot of light opens
  into the lamp's ring, the ring floats up as its three features
  arrive, then folds back into a single point of light over the
  name. Rendered in the `midnight-launch` look, with sound scored
  from its beats. [Breakdown](cases/orbit-launch/README.md)

### App promo

- **tidy** — a scatter of clutter is swept into order by one bar,
  which then becomes the app window itself.
  [Breakdown](cases/tidy/README.md)

### Feature demo

- **chip** — the pointer is the thread: a dot becomes the selection,
  the selection flies down and becomes a chip in the input, and the
  chip grows into the result card. [Breakdown](cases/chip/README.md)
- **flowboard-demo** — a tap becomes a highlight, the highlight
  flies down and becomes a chip in the input bar, and the chip grows
  into the Done card. Rendered in the `clean-light` look, with sound
  scored from its beats. [Breakdown](cases/flowboard-demo/README.md)

## How a film is made

1. **One sentence about the picture** — the single visual thread
   ("one dot becomes everything"). If the concept needs a paragraph,
   it is not a concept yet.
2. **The beat sheet** — beats of *varied* lengths; every beat names
   the element that carries across its boundary.
3. **The carry check** — `check_film.py` proves each carry exists on
   both sides of its boundary and measures the visual jump there.
4. **The render** — deterministic: the same sheet always produces
   the same film.
5. **The verdict** — the film is shown with its checker numbers,
   not just its best frame.

The full protocol, written for humans and AI agents, is in
[`SKILL.md`](SKILL.md).

## Write your own film

A film is one JSON file — beats, elements, a camera, and a named
look. The full format is documented in the docstring of
[`make_film.py`](make_film.py); start from a template and rewrite
its beats: [`templates/product-launch.json`](templates/product-launch.json)
for a launch, [`templates/feature-demo.json`](templates/feature-demo.json)
for a feature walk-through,
[`templates/launch-cashcow.json`](templates/launch-cashcow.json) for
the original hand-coloured style. The method — concept, beat sheet,
carries, camera, rests, sound — is written up for humans and AI
agents alike in [`SKILL.md`](SKILL.md).

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
- The built-in sound is a synthesised score grown from the film's
  beats — fitted, but instrumental only. For voice-over or a licensed
  music track, mux your own audio over the render in an editor.
- Text that changes on a carried element swaps at the boundary;
  geometry, colour and position are what morph.

## License

MIT — see [`LICENSE`](LICENSE). © 2026 Danyal Malik.
