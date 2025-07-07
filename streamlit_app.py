# app.py
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap
import random
import io
import os

# ──────────────────────────
# Original helper functions
# ──────────────────────────
def detect_white_space(image):
    img = image.convert("L")
    arr = np.array(img)
    ys, xs = np.where(arr > 200)
    if xs.size == 0 or ys.size == 0:
        return (0, 0, arr.shape[1], arr.shape[0])
    return (xs.min(), ys.min(), xs.max(), ys.max())

def calculate_font_and_wrap(draw, text, font_path, max_w, max_h):
    for size in range(70, 20, -2):
        font = ImageFont.truetype(font_path, size)
        lines = []
        for para in text.split("\n"):
            if para.strip() == "":
                lines.append("")
            else:
                line_w = int(max_w / (size * 0.55))
                lines += textwrap.wrap(para, width=line_w)
        bbox = draw.multiline_textbbox((0, 0), "\n".join(lines), font=font, spacing=20)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if w <= max_w and h <= max_h:
            return font, lines
    return ImageFont.truetype(font_path, 20), text.split("\n")

def add_jitter(x, y, jitter=2):
    return x + random.randint(-jitter, jitter), y + random.randint(-jitter, jitter)

def draw_text_with_effects(draw, line, pos, font, color, overlap=False, fade=False):
    x, y = pos
    for idx, ch in enumerate(line):
        w = font.getbbox(ch)[2] - font.getbbox(ch)[0]
        cy = y - 0.5 if overlap and ch.lower() in {"y", "g", "j"} else y
        fill = (*color[:3], 180) if fade and 4 < idx < len(line) - 4 else color
        draw.text((x, cy), ch, font=font, fill=fill)
        if random.random() < random.uniform(0.08, 0.4):
            draw.text((x + 0.5, cy), ch, font=font, fill=fill)
        x += w - 1

def handwriting_vertical(text, font_path, bg_path):
    img = Image.open(bg_path).convert("RGBA").rotate(270, expand=True)
    draw = ImageDraw.Draw(img)

    l, t, r, b = detect_white_space(img)
    pad = 40
    safe_left   = l + pad + 200
    safe_right  = r + 600 - pad
    safe_top    = t + pad + 100
    safe_bottom = b - pad

    font, lines = calculate_font_and_wrap(
        draw, text, font_path,
        safe_right - safe_left,
        safe_bottom - safe_top
    )

    y = safe_top
    for i, line in enumerate(lines):
        x = safe_left + (25 if i % 5 == 0 else 0)
        jx, jy = add_jitter(x, y)
        draw_text_with_effects(
            draw, line, (jx, jy), font,
            color=(0, 0, 138, 255),
            overlap=random.random() < 0.85,
            fade=random.random() < 0.3
        )
        if (i + 1 < len(lines)) and (lines[i + 1].strip() == ""):
            jx += random.randint(20, 60)
            jy += random.randint(3, 10)
        y += font.size + (25 if line.strip() == "" else 12)

    img = img.rotate(random.uniform(-2.0, 2.0), expand=True,
                     resample=Image.BICUBIC, fillcolor="white")
    return img.convert("RGB")

# ──────────────────────────
# Streamlit UI
# ──────────────────────────
st.set_page_config(page_title="Handwriting Generator", layout="centered")
st.title("🖋️ Vertical Handwriting Generator")

text_input = st.text_area("Enter text", height=250)

if st.button("Generate"):
    if not text_input.strip():
        st.warning("Please enter some text first.")
    elif not os.path.exists("bkg1.jpg") or not os.path.exists("QEDavidReidCAP.ttf"):
        st.error("Missing `bkg1.jpg` or `QEDavidReidCAP.ttf` in project root.")
    else:
        with st.spinner("Rendering…"):
            final_img = handwriting_vertical(
                text_input,
                font_path="QEDavidReidCAP.ttf",
                bg_path="bkg1.jpg"
            )
            buf = io.BytesIO()
            final_img.save(buf, format="PNG")
            st.image(final_img, use_column_width=True)
            st.download_button(
                "📥 Download PNG",
                data=buf.getvalue(),
                file_name="handwriting.png",
                mime="image/png"
            )

