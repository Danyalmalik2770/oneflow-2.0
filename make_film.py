#!/usr/bin/env python3
"""
OneFlow — motion films that never cut.

OneFlow makes short motion films the way a single camera shot works:
there are no scenes that replace each other. Instead, a film is a list
of BEATS, and at every beat boundary one element — the CARRY — survives
and visibly morphs into the next beat (a dot stretches into a bar, the
bar becomes a headline plate, the plate folds into the logo). One
virtual camera moves continuously the whole time: it pans and zooms
without ever cutting.

You describe the film in a small JSON "film sheet", then:

    python3 make_film.py templates/launch-cashcow.json -o film.mp4
    python3 check_film.py templates/launch-cashcow.json   # continuity check

Rendering is deterministic: the film is one HTML page whose every
element is a pure function of time. The renderer seeks to each frame
time with Playwright/Chromium and screenshots it into ffmpeg.
--blur 2 renders at double frame rate and averages frame pairs with
ffmpeg's tmix filter for real temporal motion blur.

Film sheet format:

    {
      "title": "My film",
      "width": 1080, "height": 1920, "fps": 30,
      "background": "#0d0f12",
      "morph": 0.5,               // seconds a carry morphs across a boundary
      "beats": [
        {"dur": 2.4,
         "camera": {"x": 540, "y": 960, "zoom": 1.0},
         "elements": [
            {"id": "hero", "kind": "dot", "x": 540, "y": 960,
             "size": 36, "color": "#ffd23f"}
         ],
         "carry": "hero"},
        ...
      ]
    }

Element kinds: dot (circle, "size" = diameter), bar (rounded rect,
"w"/"h"/"radius"), text ("text", "size" = font size, "color",
"weight"), card ("w"/"h" plus "title"/"sub"), ring (circle outline,
"size", "width"). Every element has a centre "x"/"y" in world
coordinates (the canvas is width x height). An element id that appears
in two neighbouring beats MORPHS between its two definitions across
the boundary; an id that appears only in the new beat enters (fade +
grow); an id that disappears exits (fade out at the beat's end).
Layering: within a beat, elements listed later paint above elements
listed earlier — list backgrounds first, heroes and labels last.

Free for everyone, forever — MIT licensed. See LICENSE.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

HTML_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:#000; overflow:hidden; font-family: Arial, 'DejaVu Sans', sans-serif; }
  #stage { position:absolute; left:0; top:0; overflow:hidden; }
  #world { position:absolute; left:0; top:0; transform-origin: 0 0; }
  .el { position:absolute; transform: translate(-50%,-50%); }
  .card { border-radius: 28px; padding: 34px 40px; }
  .card .t { font-weight: 800; line-height: 1.15; }
  .card .s { font-weight: 400; opacity: .62; margin-top: 10px; line-height: 1.25; }
  .text { font-weight: 800; white-space: nowrap; line-height: 1.1; }
</style></head>
<body>
<div id="stage"><div id="world"></div></div>
<script>
const SHEET = __SHEET_JSON__;
const W = SHEET.width, H = SHEET.height;
const stage = document.getElementById('stage');
stage.style.width = W + 'px'; stage.style.height = H + 'px';
stage.style.background = SHEET.background || '#0d0f12';
const world = document.getElementById('world');
world.style.width = W + 'px'; world.style.height = H + 'px';

// beat start times
const starts = []; let acc = 0;
for (const b of SHEET.beats) { starts.push(acc); acc += b.dur; }
const TOTAL = acc;
const MORPH = SHEET.morph != null ? SHEET.morph : 0.5;

const clamp01 = x => Math.max(0, Math.min(1, x));
const smooth = x => { x = clamp01(x); return x*x*(3-2*x); };
const lerp = (a,b,p) => a + (b-a)*p;
function hexRgb(h){ h = String(h||'#000000').replace('#','');
  if (h.length===3) h = h.split('').map(c=>c+c).join('');
  return [parseInt(h.substr(0,2),16), parseInt(h.substr(2,2),16), parseInt(h.substr(4,2),16)]; }
function lerpColor(a,b,p){ const A=hexRgb(a), B=hexRgb(b);
  return 'rgb(' + A.map((v,i)=>Math.round(lerp(v,B[i],p))).join(',') + ')'; }

// build DOM for every element id that ever appears; an element that
// is a card in ANY beat gets the card's inner structure from the start,
// because a carried element may morph into a card mid-film
const els = {};
const anyCard = {};
for (const b of SHEET.beats) for (const e of b.elements)
  if (e.kind === 'card') anyCard[e.id] = true;
for (const b of SHEET.beats) for (const e of b.elements) {
  if (els[e.id]) continue;
  const d = document.createElement('div');
  d.className = 'el';
  if (anyCard[e.id]) d.innerHTML = '<div class="t"></div><div class="s"></div>';
  world.appendChild(d); els[e.id] = d;
}

function beatAt(t) {
  for (let i = SHEET.beats.length - 1; i >= 0; i--)
    if (t >= starts[i]) return i;
  return 0;
}

function camAt(t) {
  const i = beatAt(t), b = SHEET.beats[i];
  const c0 = b.camera || {x: W/2, y: H/2, zoom: 1};
  const nb = SHEET.beats[i+1];
  const c1 = nb && nb.camera ? nb.camera : c0;
  const p = smooth((t - starts[i]) / b.dur);
  return { x: lerp(c0.x ?? W/2, c1.x ?? W/2, p),
           y: lerp(c0.y ?? H/2, c1.y ?? H/2, p),
           zoom: lerp(c0.zoom ?? 1, c1.zoom ?? 1, p) };
}

const NUM = ['x','y','w','h','size','radius','width','opacity','rotate','tsize','ssize'];
function styleFor(e, d, opacityScale) {
  const kind = e.kind;
  d.classList.toggle('card', kind === 'card');
  d.classList.toggle('text', kind === 'text');
  d.style.left = e.x + 'px'; d.style.top = e.y + 'px';
  d.style.opacity = (e.opacity != null ? e.opacity : 1) * opacityScale;
  let tr = 'translate(-50%,-50%)';
  if (e.rotate) tr += ' rotate(' + e.rotate + 'deg)';
  if (e._grow != null) tr += ' scale(' + e._grow + ')';
  d.style.transform = tr;
  if (kind === 'dot') {
    d.style.width = e.size + 'px'; d.style.height = e.size + 'px';
    d.style.borderRadius = '50%'; d.style.background = e.color || '#fff';
  } else if (kind === 'ring') {
    d.style.width = e.size + 'px'; d.style.height = e.size + 'px';
    d.style.borderRadius = '50%'; d.style.background = 'transparent';
    d.style.border = (e.width || 10) + 'px solid ' + (e.color || '#fff');
  } else if (kind === 'bar') {
    d.style.width = e.w + 'px'; d.style.height = e.h + 'px';
    d.style.borderRadius = (e.radius != null ? e.radius : 24) + 'px';
    d.style.background = e.color || '#fff';
  } else if (kind === 'text') {
    d.style.fontSize = e.size + 'px'; d.style.color = e.color || '#fff';
    if (e.weight) d.style.fontWeight = e.weight;
    d.textContent = e.text || '';
  } else if (kind === 'card') {
    d.style.width = e.w + 'px'; d.style.height = e.h + 'px';
    d.style.background = e.color || '#1d2126';
    if (!d.querySelector('.t')) d.innerHTML = '<div class="t"></div><div class="s"></div>';
    const t = d.querySelector('.t'), s = d.querySelector('.s');
    t.textContent = e.title || ''; t.style.fontSize = (e.tsize || 54) + 'px';
    t.style.color = e.tcolor || '#f5f6f8';
    s.textContent = e.sub || ''; s.style.fontSize = (e.ssize || 36) + 'px';
    s.style.color = e.tcolor || '#f5f6f8';
  }
}

function morphProps(a, b, p) {
  // normalise circle kinds to boxes so a dot can stretch into a bar
  const asBox = e => {
    if (e.kind === 'dot' || e.kind === 'ring') {
      const c = Object.assign({}, e);
      c.w = e.size; c.h = e.size; c.radius = e.size / 2;
      return c;
    }
    return e;
  };
  a = asBox(a); b = asBox(b);
  const out = Object.assign({}, b);
  for (const k of NUM) {
    if (a[k] != null && b[k] != null) out[k] = lerp(a[k], b[k], p);
    else if (b[k] == null && a[k] != null) out[k] = a[k];
  }
  if (a.color && b.color) out.color = lerpColor(a.color, b.color, p);
  if (a.tcolor && b.tcolor) out.tcolor = lerpColor(a.tcolor, b.tcolor, p);
  if (a.kind !== b.kind && p < 0.5) { out.kind = a.kind; }
  return out;
}

window.seek = function(t) {
  const cam = camAt(t);
  world.style.transform =
    'translate(' + (W/2 - cam.x*cam.zoom) + 'px,' + (H/2 - cam.y*cam.zoom) + 'px)' +
    ' scale(' + cam.zoom + ')';
  const i = beatAt(t), beat = SHEET.beats[i], lt = t - starts[i];
  // layering rule: within a beat, later elements paint above earlier ones
  const zmap = {}; beat.elements.forEach((e, idx) => { zmap[e.id] = idx + 1; });
  const prev = SHEET.beats[i-1], next = SHEET.beats[i+1];
  const cur = {}; for (const e of beat.elements) cur[e.id] = e;
  const prv = {}; if (prev) for (const e of prev.elements) prv[e.id] = e;
  const nxt = {}; if (next) for (const e of next.elements) nxt[e.id] = e;
  const ids = new Set([...Object.keys(cur), ...Object.keys(prv)]);
  for (const id of ids) {
    const d = els[id]; if (!d) continue;
    if (cur[id]) {
      let e = cur[id], os = 1;
      if (prv[id] && lt < MORPH) {
        e = morphProps(prv[id], cur[id], smooth(lt / MORPH));
      } else if (!prv[id]) {
        const p = smooth(lt / 0.35); os = p; e = Object.assign({}, e, {_grow: 0.6 + 0.4*p});
      }
      if (!nxt[id] && next) {
        const remain = beat.dur - lt;
        if (remain < 0.3) os *= clamp01(remain / 0.3);
      }
      d.style.display = 'block';
      d.style.zIndex = zmap[id] || 0;
      styleFor(e, d, os);
    } else {
      d.style.display = 'none';
    }
  }
};
window.TOTAL = TOTAL;
</script></body></html>
"""


def build_html(sheet):
    return HTML_TEMPLATE.replace("__SHEET_JSON__", json.dumps(sheet))


def total_duration(sheet):
    return sum(float(b.get("dur", 0)) for b in sheet.get("beats", []))


def render(sheet, out_path, blur=1, scale=1.0):
    """Render the film sheet to an MP4. blur=2 renders at double rate
    and averages frame pairs (real temporal motion blur)."""
    from playwright.sync_api import sync_playwright

    fps = int(sheet.get("fps", 30))
    width, height = int(sheet["width"]), int(sheet["height"])
    total = total_duration(sheet)
    render_fps = fps * blur
    frames = int(total * render_fps)
    html = build_html(sheet)

    ffmpeg_cmd = ["ffmpeg", "-y", "-v", "error",
                  "-f", "image2pipe", "-framerate", str(render_fps), "-i", "-",
                  "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]
    vf = []
    if blur > 1:
        vf.append(f"tmix=frames={blur}")
        vf.append("select='not(mod(n\\," + str(blur) + "))'")
    if scale != 1.0:
        vf.append(f"scale={int(width*scale)}:{int(height*scale)}")
    if vf:
        ffmpeg_cmd += ["-vf", ",".join(vf)]
    ffmpeg_cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "19",
                   "-pix_fmt", "yuv420p", "-r", str(fps), "-shortest",
                   str(out_path)]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.set_content(html)
        page.wait_for_timeout(150)
        for f in range(frames):
            page.evaluate(f"window.seek({f / render_fps:.4f})")
            png = page.screenshot()
            proc.stdin.write(png)
            if f % 60 == 0:
                print(f"frame {f}/{frames}", flush=True)
        browser.close()
    proc.stdin.close()
    proc.wait()
    if proc.returncode != 0:
        raise SystemExit("ffmpeg failed while rendering")
    print(f"DONE: {out_path} ({total:.1f}s, {frames} frames rendered)")


def main():
    ap = argparse.ArgumentParser(description="OneFlow — motion films that never cut.")
    ap.add_argument("sheet", help="film sheet JSON")
    ap.add_argument("-o", "--output", default="film.mp4", help="output MP4")
    ap.add_argument("--blur", type=int, default=1,
                    help="temporal motion-blur factor (2 = average frame pairs)")
    args = ap.parse_args()
    sheet = json.loads(Path(args.sheet).read_text(encoding="utf-8"))
    if not sheet.get("beats"):
        raise SystemExit("the film sheet needs a non-empty 'beats' list")
    render(sheet, args.output, blur=args.blur)


if __name__ == "__main__":
    main()
