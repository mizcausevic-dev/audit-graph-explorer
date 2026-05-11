from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.audit_graph_report import build_report


WIDTH = 1600
OUT_DIR = ROOT / "screenshots"
BG = "#071220"
CARD = "#0f1e33"
CARD_ALT = "#12243b"
TEXT = "#f4efe4"
MUTED = "#a9b7cc"
ACCENT = "#82c8ff"
GREEN = "#8ce5b0"
YELLOW = "#f4d27b"
RED = "#ff9e8f"
EDGE = "#29486e"


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def rounded(draw: ImageDraw.ImageDraw, box, fill, outline=None, width=1, radius=24):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def write(draw, xy, text, fill, size, bold=False, spacing=8):
    draw.multiline_text(xy, text, fill=fill, font=font(size, bold), spacing=spacing)


def scene_hero(report: dict):
    img = Image.new("RGB", (WIDTH, 900), BG)
    draw = ImageDraw.Draw(img)
    rounded(draw, (50, 40, WIDTH - 50, 860), CARD, outline=EDGE, width=2, radius=32)
    write(draw, (95, 95), "AUDIT GRAPH EXPLORER", ACCENT, 24)
    write(draw, (95, 155), "Trace how policy debt,\nexceptions, and ownership intersect.", TEXT, 56, bold=True)
    write(draw, (95, 330), report["headline"], MUTED, 28)

    stats = [
        ("Nodes", str(report["summary"]["node_count"])),
        ("Edges", str(report["summary"]["edge_count"])),
        ("Open exceptions", str(report["summary"]["open_exceptions"])),
        ("Active incidents", str(report["summary"]["active_incidents"])),
    ]
    x = 95
    for label, value in stats:
        rounded(draw, (x, 430, x + 300, 610), CARD_ALT, outline=EDGE, width=2, radius=22)
        write(draw, (x + 24, 462), label.upper(), MUTED, 16)
        write(draw, (x + 24, 510), value, TEXT, 42, bold=True)
        x += 320

    rounded(draw, (95, 660, WIDTH - 95, 800), CARD_ALT, outline=EDGE, width=2, radius=22)
    write(draw, (125, 695), "CURRENT PRIORITY", "#f6bfd8", 18)
    write(draw, (125, 730), report["priority_note"], TEXT, 26, bold=True)
    return img


def scene_path(report: dict):
    img = Image.new("RGB", (WIDTH, 900), BG)
    draw = ImageDraw.Draw(img)
    rounded(draw, (50, 40, WIDTH - 50, 860), CARD, outline=EDGE, width=2, radius=32)
    write(draw, (95, 95), "EXPLANATION PATH", ACCENT, 24)
    write(draw, (95, 155), "The shortest path from exception to\ntier-0 exposure.", TEXT, 54, bold=True)

    path = report["path"]
    card_w = 250
    gap = 34
    y = 430
    x = 95
    for index, step in enumerate(path):
        rounded(draw, (x, y, x + card_w, y + 190), CARD_ALT, outline=EDGE, width=2, radius=24)
        write(draw, (x + 20, y + 24), step["type"].upper(), MUTED, 15)
        write(draw, (x + 20, y + 70), step["label"], TEXT, 28, bold=True)
        if index > 0:
            write(draw, (x + 20, y + 138), f"via {step['via']}", YELLOW, 20)
        if index < len(path) - 1:
            draw.line((x + card_w, y + 95, x + card_w + gap - 10, y + 95), fill=ACCENT, width=6)
            draw.polygon([(x + card_w + gap - 10, y + 95), (x + card_w + gap - 26, y + 84), (x + card_w + gap - 26, y + 106)], fill=ACCENT)
        x += card_w + gap
    return img


def scene_blast(report: dict):
    img = Image.new("RGB", (WIDTH, 980), BG)
    draw = ImageDraw.Draw(img)
    rounded(draw, (50, 40, WIDTH - 50, 940), CARD, outline=EDGE, width=2, radius=32)
    write(draw, (95, 95), "BLAST RADIUS", ACCENT, 24)
    write(draw, (95, 155), "What the vendor touches downstream.", TEXT, 54, bold=True)

    items = report["blast_radius"][:6]
    cols = 3
    card_w = 440
    card_h = 170
    start_x = 95
    start_y = 330
    gap_x = 30
    gap_y = 24
    for i, item in enumerate(items):
        row, col = divmod(i, cols)
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)
        rounded(draw, (x, y, x + card_w, y + card_h), CARD_ALT, outline=EDGE, width=2, radius=22)
        color = GREEN if item["type"] == "Asset" else RED if item["type"] == "Incident" else YELLOW
        write(draw, (x + 22, y + 22), item["type"].upper(), color, 16)
        write(draw, (x + 22, y + 58), item["label"], TEXT, 28, bold=True)
        write(draw, (x + 22, y + 112), f"depth {item['depth']} via {item['via'].lower()}", MUTED, 20)
    return img


def scene_owners(report: dict):
    img = Image.new("RGB", (WIDTH, 900), BG)
    draw = ImageDraw.Draw(img)
    rounded(draw, (50, 40, WIDTH - 50, 860), CARD, outline=EDGE, width=2, radius=32)
    write(draw, (95, 95), "OWNER PRESSURE", ACCENT, 24)
    write(draw, (95, 155), "Who is carrying unresolved exception load.", TEXT, 54, bold=True)

    y = 320
    for row in report["owner_pressure"]:
        rounded(draw, (95, y, WIDTH - 95, y + 140), CARD_ALT, outline=EDGE, width=2, radius=22)
        write(draw, (125, y + 28), row["owner"], TEXT, 30, bold=True)
        write(draw, (125, y + 78), row["role"], MUTED, 22)
        write(draw, (720, y + 28), "OPEN ITEMS", MUTED, 16)
        write(draw, (720, y + 62), str(row["exceptions"]), TEXT, 34, bold=True)
        write(draw, (900, y + 52), ", ".join(row["items"]), YELLOW, 22)
        y += 165
    return img


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()
    scenes = [
        ("01-hero.png", scene_hero(report)),
        ("02-explanation-path.png", scene_path(report)),
        ("03-blast-radius.png", scene_blast(report)),
        ("04-owner-pressure.png", scene_owners(report)),
    ]
    for name, image in scenes:
        image.save(OUT_DIR / name)


if __name__ == "__main__":
    main()
