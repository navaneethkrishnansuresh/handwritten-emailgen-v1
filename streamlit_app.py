"""
app.py • Vertical Handwriting Generator
--------------------------------------
A Streamlit app that converts any text block into a realistic
vertical handwritten image.

Features
========
✓ Uses default QEDavidReidCAP.ttf + bkg1.jpg in repo root
✓ Optional uploads to override font / background
✓ Adjustable ink colour, tilt range, jitter
✓ Live preview and PNG download
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageColor
import numpy as np
import textwrap
import random
import io
import os

# ───────────────────────────────────────────────────────
# Core Draft-5 Functions (unaltered behaviour)
# ───────────────────────────────────────────────────────
def detect_white_space(image):
    img = image.convert("L")
    arr = np.array(img)
    ys, xs = np.where(arr > 200)
    if xs.size == 0 or ys.size == 0:
        return (0, 0, arr.shape[1], arr.shape[0])
    return (xs.min(), ys.min(), xs.max(), ys.max())


def calculate_font_and_wrap(draw, text, font_path, max_width, max_height):
    for size in range(70, 20, -2):
        font = ImageFont.truetype(font_path, size)
        lines = []
        for para in text.split("\n"):
            if para.strip() == "":
                lines.append("")
            else:
                line_width = int(max_width / (size * 0.55))
                lines.extend(textwrap.wrap(para, width=line_width))
        dummy = "\n".join(lines)
        w, h = draw.multiline_textbbox((0, 0), dummy, font=font, spacing=20)[2:]
        if w <= max_width and h <= max_height:
            return font, lines
    return ImageFont.truetype(font_path, 20), text.split("\n")


def add_jitter(x, y, jitter=2):
    return x + random.randint(-jitter, jitter), y + random.randint(-jitter, jitter)


def draw_text_with_effects(
    draw, line, position, font, color, overlap=False, fade=False
):
    x, y = position
    for idx, char in enumerate(line):
        char_width = font.getbbox(char)[2] - font.getbbox(char)[0]
        cy = y - 0.5 if overlap and char.lower() in {"y", "g", "j"} else y
        fill = (*color[:3], 180) if fade and 4 < idx < len(line) - 4 else color
        draw.text((x, cy), char, font=font, fill=fill)
        if random.random() < random.uniform(0.08, 0.4):
            draw.text((x + 0.5, cy), char, font=font, fill=fill)
        x += char_width - 1


def handwriting_vertical(
    text: str,
    font_path: str = "QEDavidReidCAP.ttf",
    background_path: str = "bkg1.jpg",
    ink_hex: str = "#00008a",
    tilt_range: float = 2.0,
    jitter: int = 2,
):
    # Load and rotate paper
    img = Image.open(background_path).convert("RGBA").rotate(270, expand=True)
    draw = ImageDraw.Draw(img)

    # Safe writing box
    l, t, r, b = detect_white_space(img)
    pad = 40
    safe_left, safe_top = l + pad + 200, t + pad + 100
    safe_right, safe_bottom = r + 600 - pad, b - pad
    max_w, max_h = safe_right - safe_left, safe_bottom - safe_top

    # Wrap + font size search
    font, lines = calculate_font_and_wrap(
        draw, text, font_path, max_w, max_h
    )

    # Draw each line
    y = safe_top
    ink_rgba = (*ImageColor.getrgb(ink_hex), 255)
    for i, line in enumerate(lines):
        indent = 25 if i % 5 == 0 else 0
        x = safe_left + indent
        jx, jy = add_jitter(x, y, jitter)
        last_blank = (i + 1 < len(lines)) and (lines[i + 1].strip() == "")
        draw_text_with_effects(
            draw,
            line,
            (jx, jy),
            font,
            color=ink_rgba,
            overlap=random.random() < 0.85,
            fade=random.random() < 0.3,
        )
        if last_blank:
            jx += random.randint(20, 60)
            jy += random.randint(3, 10)
        y += font.size + (25 if line.strip() == "" else 12)

    # Final tilt + flatten
    img = img.rotate(
        random.uniform(-tilt_range, tilt_range),
        expand=True,
        resample=Image.BICUBIC,
        fillcolor="white",
    )
    return img.convert("RGB")


# ───────────────────────────────────────────────────────
# Streamlit UI
# ───────────────────────────────────────────────────────
st.set_page_config(page_title="Vertical Handwriting Generator", layout="centered")
st.title("✍️ Vertical Handwriting Generator")

# 1️⃣ Text input
default_text = """Hey Mia,

Just wanted to say thanks again for last weekend—it was honestly one of the best trips I’ve had in a while. The hike, the food, the absolutely chaotic game of Uno—10/10 would recommend.

Also, I might’ve stolen your playlist. Too good to ignore.

Hope the week isn’t too brutal. Let’s plan something soon!

Take care,
Jason
"""
text = st.text_area("Your handwritten message", value=default_text, height=250)

# 2️⃣ Advanced options (accordion)
with st.expander("🛠️ Advanced Settings", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        ink_hex = st.color_picker("Ink colour", value="#00008a")
    with col2:
        tilt_range = st.slider("Tilt range (°)", 0.0, 5.0, 2.0, 0.1)
    with col3:
        jitter = st.slider("Jitter (px)", 0, 6, 2, 1)

    # Optional overrides
    font_file = st.file_uploader("Override font (.ttf)", type=["ttf"])
    bg_file = st.file_uploader("Override background (.jpg/.png)", type=["jpg", "jpeg", "png"])

# 3️⃣ Generate button
if st.button("🖋️ Generate"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        # Paths: default or temp override
        font_path = "QEDavidReidCAP.ttf"
        bg_path = "bkg1.jpg"

        if font_file:
            font_path = "/tmp/font.ttf"
            with open(font_path, "wb") as f:
                f.write(font_file.read())

        if bg_file:
            bg_path = "/tmp/bg"
            ext = ".png" if bg_file.type == "image/png" else ".jpg"
            bg_path += ext
            with open(bg_path, "wb") as f:
                f.write(bg_file.read())

        with st.spinner("Rendering handwriting..."):
            img = handwriting_vertical(
                text,
                font_path=font_path,
                background_path=bg_path,
                ink_hex=ink_hex,
                tilt_range=tilt_range,
                jitter=jitter,
            )
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.image(img, caption="Preview", use_column_width=True)
            st.download_button(
                "📥 Download PNG",
                buf.getvalue(),
                file_name="handwritten.png",
                mime="image/png",
            )
