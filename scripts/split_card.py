#!/usr/bin/env python3
"""Draw Groupie's fair split card (or progress card) as a PNG.

Usage:
  split_card.py --input split.json --out split_card.png [--progress]
  split_card.py --sample --out sample_card.png [--progress]

Exit codes: 0 card drawn, 1 bad or missing input, 2 Pillow not installed.
"""
import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow is not installed; run the Setup commands in SKILL.md.")
    sys.exit(2)

HERE = Path(__file__).resolve().parent
SAMPLE = HERE.parent / "assets" / "sample_split.json"

S = 2  # render scale for crisp text on phones
W = 540 * S
PAD = 28 * S
BG = (30, 30, 30)
CARD = (38, 38, 38)
DASH = (95, 95, 95)
TEXT = (245, 245, 245)
MUTED = (160, 160, 160)
TRACK = (60, 60, 60)
AMBER = (239, 159, 39)
COLORS = [(155, 135, 245), (240, 120, 100), (64, 196, 170), (245, 190, 70),
          (95, 160, 240), (236, 110, 160), (140, 200, 90), (200, 150, 250)]


def font(size):
    try:
        return ImageFont.load_default(size=size * S)
    except TypeError:  # very old Pillow
        return ImageFont.load_default()


F_LABEL, F_TITLE, F_SUB = font(11), font(22), font(12)
F_NAME, F_TASK, F_SMALL = font(15), font(12), font(11)


def load(args):
    path = SAMPLE if args.sample else (Path(args.input) if args.input else None)
    if path is None:
        print("Give --input <file.json> or --sample.")
        sys.exit(1)
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        print(f"Input file not found: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Input is not valid JSON: {e}")
        sys.exit(1)
    members = data.get("members")
    if not isinstance(members, list) or not members:
        print("Input needs a non-empty 'members' list.")
        sys.exit(1)
    for m in members:
        if not m.get("name") or not isinstance(m.get("tasks"), list):
            print("Each member needs a 'name' and a 'tasks' list.")
            sys.exit(1)
        for t in m["tasks"]:
            if not t.get("title") or not isinstance(t.get("points"), (int, float)):
                print(f"Every task for {m['name']} needs a 'title' and numeric 'points'.")
                sys.exit(1)
    return data


def dashed_round_rect(d, box, r, color, width=S, dash=6 * S, gap=5 * S):
    x0, y0, x1, y1 = box

    def dline(a, b, horizontal):
        start, end = a, b
        pos = start
        while pos < end:
            seg_end = min(pos + dash, end)
            if horizontal[0]:
                d.line([(pos, horizontal[1]), (seg_end, horizontal[1])], fill=color, width=width)
            else:
                d.line([(horizontal[1], pos), (horizontal[1], seg_end)], fill=color, width=width)
            pos = seg_end + gap

    dline(x0 + r, x1 - r, (True, y0))
    dline(x0 + r, x1 - r, (True, y1))
    dline(y0 + r, y1 - r, (False, x0))
    dline(y0 + r, y1 - r, (False, x1))
    d.arc([x0, y0, x0 + 2 * r, y0 + 2 * r], 180, 270, fill=color, width=width)
    d.arc([x1 - 2 * r, y0, x1, y0 + 2 * r], 270, 360, fill=color, width=width)
    d.arc([x0, y1 - 2 * r, x0 + 2 * r, y1], 90, 180, fill=color, width=width)
    d.arc([x1 - 2 * r, y1 - 2 * r, x1, y1], 0, 90, fill=color, width=width)


def tw(d, text, f):
    return d.textlength(text, font=f)


def fit(d, text, f, max_w):
    if tw(d, text, f) <= max_w:
        return text
    while text and tw(d, text + "...", f) > max_w:
        text = text[:-1]
    return text + "..."


def fmt(n):
    return str(int(n)) if float(n).is_integer() else f"{n:.1f}"


def draw(data, progress):
    members = data["members"]
    totals = [sum(t["points"] for t in m["tasks"]) for m in members]
    done = [sum(min(t.get("done", 0) or 0, t["points"]) for t in m["tasks"]) for m in members]
    grand = sum(totals)
    max_total = max(totals) or 1
    spread = max(totals) - min(totals)

    row_h, task_h = 64 * S, 22 * S
    blocks = [row_h + len(m["tasks"]) * task_h + 14 * S for m in members]
    header_h = 104 * S
    footer_h = 44 * S
    gap = 12 * S
    H = PAD + header_h + sum(blocks) + gap * (len(members) - 1) + footer_h + PAD

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    y = PAD
    label = "PROGRESS" if progress else "FAIR SPLIT"
    d.text((PAD, y), label, font=F_LABEL, fill=COLORS[0])
    y += 20 * S
    title = data.get("project") or "Group project"
    d.text((PAD, y), fit(d, title, F_TITLE, W - 2 * PAD), font=F_TITLE, fill=TEXT,
           stroke_width=1, stroke_fill=TEXT)
    y += 34 * S
    parts = [p for p in [data.get("course"), f"Due {data['due']}" if data.get("due") else None,
                         f"{len(members)} members", f"{fmt(grand)} pts total"] if p]
    if progress and grand:
        parts.append(f"{round(100 * sum(done) / grand)}% done")
    d.text((PAD, y), "  ·  ".join(parts), font=F_SUB, fill=MUTED)
    y = PAD + header_h

    for i, m in enumerate(members):
        color = COLORS[i % len(COLORS)]
        x0, x1 = PAD, W - PAD
        y1 = y + blocks[i]
        d.rounded_rectangle([x0, y, x1, y1], radius=16 * S, fill=CARD)
        dashed_round_rect(d, (x0, y, x1, y1), 16 * S, DASH)

        cx, cy = x0 + 22 * S, y + 22 * S
        d.ellipse([cx - 7 * S, cy - 7 * S, cx + 7 * S, cy + 7 * S], fill=color)
        d.text((cx + 16 * S, cy), m["name"], font=F_NAME, fill=TEXT, anchor="lm",
               stroke_width=1, stroke_fill=TEXT)
        if progress:
            pct = round(100 * done[i] / totals[i]) if totals[i] else 0
            right = f"{fmt(done[i])}/{fmt(totals[i])} pts · {pct}%"
        else:
            right = f"{fmt(totals[i])} pts"
        d.text((x1 - 20 * S, cy), right, font=F_NAME, fill=TEXT, anchor="rm")

        bx0, bx1, by = x0 + 22 * S, x1 - 20 * S, y + 44 * S
        d.rounded_rectangle([bx0, by, bx1, by + 6 * S], radius=3 * S, fill=TRACK)
        frac = (done[i] / totals[i] if totals[i] else 0) if progress else totals[i] / max_total
        if frac > 0:
            d.rounded_rectangle([bx0, by, bx0 + max(6 * S, (bx1 - bx0) * frac), by + 6 * S],
                                radius=3 * S, fill=color)

        ty = y + row_h
        for t in m["tasks"]:
            pts = f"{fmt(t['points'])} pts"
            due = t.get("due")
            meta = f"{pts}  ·  {due}" if due else pts
            bx, byc, br = x0 + 25 * S, ty + 8 * S, 3 * S
            if progress:
                tdone = min(t.get("done", 0) or 0, t["points"])
                br = 4 * S
                if tdone >= t["points"]:
                    d.ellipse([bx - br, byc - br, bx + br, byc + br], fill=color)
                elif tdone > 0:
                    d.ellipse([bx - br, byc - br, bx + br, byc + br], outline=color, width=S)
                    d.pieslice([bx - br, byc - br, bx + br, byc + br], 90, 270, fill=color)
                else:
                    d.ellipse([bx - br, byc - br, bx + br, byc + br], outline=MUTED, width=S)
            else:
                d.ellipse([bx - br, byc - br, bx + br, byc + br], fill=MUTED)
            meta_w = tw(d, meta, F_TASK)
            d.text((x0 + 36 * S, ty), fit(d, t["title"], F_TASK, x1 - x0 - 70 * S - meta_w),
                   font=F_TASK, fill=TEXT)
            d.text((x1 - 20 * S, ty), meta, font=F_TASK, fill=MUTED, anchor="ra")
            ty += task_h
        y = y1 + gap

    y = y - gap + 18 * S
    if progress:
        note = "Points done out of points assigned"
    else:
        note = f"Balanced within {fmt(spread)} pts" if spread <= 3 else f"Spread {fmt(spread)} pts - rebalance"
    d.text((PAD, y), note, font=F_SMALL, fill=AMBER if (not progress and spread > 3) else MUTED)
    d.text((W - PAD, y), "Groupie", font=F_SMALL, fill=COLORS[0], anchor="ra")
    return img, totals, done, spread


def main():
    p = argparse.ArgumentParser(description="Draw Groupie's split or progress card.")
    p.add_argument("--input", help="JSON file with the split")
    p.add_argument("--sample", action="store_true", help="use assets/sample_split.json")
    p.add_argument("--out", default="split_card.png", help="PNG file to write")
    p.add_argument("--progress", action="store_true", help="draw the progress card")
    args = p.parse_args()

    data = load(args)
    img, totals, done, spread = draw(data, args.progress)
    img.save(args.out)
    for m, t, dn in zip(data["members"], totals, done):
        line = f"{m['name']}: {fmt(t)} pts"
        if args.progress:
            line += f", {fmt(dn)} done"
        print(line)
    print(f"spread: {fmt(spread)} pts")
    print(f"card: {args.out}")


if __name__ == "__main__":
    main()
