from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from math import ceil
import textwrap
from datetime import datetime
import os

OUTPUT_DIR = Path('static') / 'outputs'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def _render_panel(prompt, size=(512,512), bg=(240,240,255)):
    img = Image.new('RGB', size, color=bg)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('arial.ttf', 18)
    except Exception:
        font = ImageFont.load_default()

    margin = 16
    max_width = size[0] - margin*2
    lines = textwrap.wrap(prompt, width=40)
    y = margin
    for line in lines:
        w, h = draw.textsize(line, font=font)
        draw.text(((size[0]-w)/2, y), line, fill=(10,10,10), font=font)
        y += h + 6

    # simple caption area at bottom
    caption = "— " + (prompt if len(prompt) < 40 else prompt[:37] + '...')
    w, h = draw.textsize(caption, font=font)
    draw.rectangle([0, size[1]-h-24, size[0], size[1]], fill=(255,255,255))
    draw.text(((size[0]-w)/2, size[1]-h-12), caption, fill=(50,50,50), font=font)
    return img

def generate_comic(prompts, title='Comic', panel_size=(512,512), columns=2):
    panels = []
    for p in prompts:
        panels.append(_render_panel(p, size=panel_size))

    cols = max(1, columns)
    rows = ceil(len(panels) / cols)

    header_h = 72
    W, H = panel_size
    out_w = cols * W
    out_h = header_h + rows * H
    out_img = Image.new('RGB', (out_w, out_h), color=(255,255,255))
    draw = ImageDraw.Draw(out_img)
    try:
        title_font = ImageFont.truetype('arial.ttf', 36)
    except Exception:
        title_font = ImageFont.load_default()

    tw, th = draw.textsize(title, font=title_font)
    draw.text(((out_w-tw)/2, (header_h-th)/2), title, fill=(0,0,0), font=title_font)

    for idx, panel in enumerate(panels):
        r = idx // cols
        c = idx % cols
        x = c * W
        y = header_h + r * H
        out_img.paste(panel, (x, y))

    fname = f"comic_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.png"
    out_path = OUTPUT_DIR / fname
    out_img.save(out_path)
    return str(out_path)
