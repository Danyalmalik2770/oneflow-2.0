#!/usr/bin/env python3
"""
OneFlow continuity checker — a film is only a one-take film if its
beats are CARRIED, not replaced.

    python3 check_film.py templates/launch-cashcow.json

Two checks, both must pass:

1. Carry check (the sheet): every beat except the last must name a
   "carry" element, and that element id must exist in BOTH that beat
   and the next one — that is what morphs across the boundary.

2. Jump check (the picture): the checker renders the frame just
   before each boundary and the frame just after it and measures the
   mean pixel difference. A hard cut produces a large jump; a carried
   boundary stays small. It also samples a mid-beat frame pair as a
   baseline, so the number means something: the boundary jump should
   be in the same league as ordinary mid-beat motion.

Prints a carry score per boundary (1.00 = perfectly continuous) and a
final verdict. Exit code 0 = PASS, 1 = FAIL.
"""

import argparse
import io
import json
import sys
from pathlib import Path

from PIL import Image

from make_film import build_html, resolve_sheet, total_duration

JUMP_LIMIT = 30.0  # mean absolute pixel difference (0-255) at a boundary


def grab_frames(sheet, times):
    from playwright.sync_api import sync_playwright
    width, height = int(sheet["width"]), int(sheet["height"])
    html = build_html(sheet)
    out = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.set_content(html)
        page.wait_for_timeout(150)
        for t in times:
            page.evaluate(f"window.seek({t:.4f})")
            png = page.screenshot()
            out[t] = Image.open(io.BytesIO(png)).convert("RGB")
        browser.close()
    return out


def mean_diff(a, b):
    if a.size != b.size:
        b = b.resize(a.size)
    pa, pb = a.tobytes(), b.tobytes()
    n = len(pa)
    step = 997  # sample ~1/333 of pixels — plenty for a jump measure
    total, count = 0, 0
    for i in range(0, n, step):
        total += abs(pa[i] - pb[i])
        count += 1
    return total / max(count, 1)


def main():
    ap = argparse.ArgumentParser(description="OneFlow continuity checker.")
    ap.add_argument("sheet", help="film sheet JSON")
    ap.add_argument("--no-visual", action="store_true",
                    help="only run the carry check on the sheet, skip rendering")
    args = ap.parse_args()
    sheet = resolve_sheet(json.loads(Path(args.sheet).read_text(encoding="utf-8")))
    beats = sheet.get("beats", [])
    if len(beats) < 2:
        print("FAIL: a one-take film needs at least 2 beats")
        return 1

    failures = []
    # ---- check 1: carries in the sheet
    print("carry check:")
    for i, beat in enumerate(beats[:-1]):
        carry = beat.get("carry")
        here = {e.get("id") for e in beat.get("elements", [])}
        there = {e.get("id") for e in beats[i + 1].get("elements", [])}
        if not carry:
            failures.append(f"beat {i + 1}: no 'carry' named — the boundary would be a cut")
            print(f"  beat {i + 1} -> {i + 2}: NO CARRY  ✗")
        elif carry not in here or carry not in there:
            failures.append(
                f"beat {i + 1}: carry {carry!r} must exist in beats {i + 1} and {i + 2}")
            print(f"  beat {i + 1} -> {i + 2}: carry {carry!r} missing on one side  ✗")
        else:
            print(f"  beat {i + 1} -> {i + 2}: {carry!r} carries across  ✓")

    # ---- check 2: the visual jump at each boundary
    if not args.no_visual:
        starts, acc = [], 0.0
        for b in beats:
            starts.append(acc)
            acc += float(b.get("dur", 0))
        times = []
        for i in range(1, len(beats)):
            times += [starts[i] - 0.05, starts[i] + 0.05]
        mid = starts[0] + beats[0]["dur"] / 2
        times += [mid, mid + 0.1]
        frames = grab_frames(sheet, sorted(set(times)))
        base = mean_diff(frames[mid], frames[mid + 0.1])
        print(f"jump check (baseline mid-beat motion: {base:.1f}):")
        for i in range(1, len(beats)):
            jump = mean_diff(frames[starts[i] - 0.05], frames[starts[i] + 0.05])
            score = max(0.0, min(1.0, 1 - jump / 64.0))
            ok = jump <= JUMP_LIMIT
            if not ok:
                failures.append(
                    f"boundary {i} -> {i + 1}: visual jump {jump:.1f} over the limit "
                    f"{JUMP_LIMIT:.0f} — that boundary reads as a cut")
            print(f"  boundary {i} -> {i + 1}: jump {jump:5.1f}   "
                  f"carry score {score:.2f}  {'✓' if ok else '✗'}")

    if failures:
        print("FAIL:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"PASS: {len(beats)} beats, every boundary carried. "
          f"Total length {total_duration(sheet):.1f}s.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
