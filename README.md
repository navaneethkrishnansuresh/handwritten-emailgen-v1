# ✍️ Vertical Handwriting Generator

Convert any block of text—emails, letters, journal entries—into **realistic, vertically-written, hand-inked images**.  
This tool adds warmth, texture, and personal expression to your digital words.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bookish-space-dollop-q7x7pg64gj6639pqj-8501.app.github.dev/)

## 💌 About This Project

This app simulates how a letter or journal might look if handwritten on real paper.  
You paste your message, pick your style, and it renders natural-looking handwriting on a textured background.

No fancy AI. No cloud. Just pure visual storytelling.

## 🖼️ Sample Output

Here’s an example of a handwritten image generated using the default font and background with the following advanced settings

<img src="assets/sample_output.png" alt="Sample Output" width="400"/>

| Setting               | Value                     |
|-----------------------|---------------------------|
| ✒️ Ink Colour          | Default (Navy Blue `#00008A`) |
| 🎚️ Tilt Range         | 0.4°                      |
| 🔀 Jitter             | 5px                       |
| 🖋️ Font Override      | None                      |
| 📄 Background Override| None                      |

## 🎯 Use Cases

- **Emails as images** – Make personal messages feel handwritten
- **Journaling** – Create diary-style text visuals
- **Social media** – Add handwritten notes to Reels or carousels
- **Posters / cards** – Print notes or use them in digital gifts
- **Storytelling mockups** – Use handwriting in app prototypes

## 🛠️ Features

| Feature                   | Description |
|--------------------------|-------------|
| ✅ Vertical layout        | Top-to-bottom handwriting flow |
| ✅ Realistic strokes      | Ink fading, bold strokes, overlap, jitter |
| ✅ Custom fonts           | Upload your own `.ttf` handwriting font |
| ✅ Paper backgrounds      | Use any JPG/PNG image as textured paper |
| ✅ Ink customization      | Pick ink color via color picker |
| ✅ Tilt + Jitter control  | Adjust realism with sliders |
| ✅ PNG export             | One-click download of the result |
| ✅ Fully local            | No server, no API, no uploads |

## 🖼️ Interface Preview

**✍️ Vertical Handwriting Generator**

**🖊️ Your handwritten message**  
[ large multi-line text box ]

**🛠️ Advanced Settings**  
🎨 Ink color [color picker]  
🔄 Tilt range [0.0 to 5.0 slider]  
🔀 Jitter [0 to 6 slider]  
📁 Upload font (.ttf)  
🖼️ Upload background (.jpg/.png)  

[🖋️ Generate] → [📥 Download PNG]

## 🚀 Getting Started

### 1. Clone & install

```bash
git clone https://github.com/your-username/handwriting-generator.git
cd handwriting-generator
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project Structure

```
📁 handwriting-generator
├── app.py                # Streamlit app
├── QEDavidReidCAP.ttf    # Default handwriting font
├── bkg1.jpg              # Default paper background
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Customize

| What                    | How                                                    |
|-------------------------|---------------------------------------------------------|
| 🖋️ Use a different font  | Replace `QEDavidReidCAP.ttf` or upload via the UI       |
| 📄 Change background     | Replace `bkg1.jpg` or upload via the UI                 |
| 🎨 Ink color             | Use the color picker in the sidebar                     |
| 🌀 Tilt / Jitter control | Adjust realism using sliders in *Advanced Settings*     |

---

## 📋 License

**License: Non-Commercial Use Only**

This software is provided free for **personal, academic, and non-commercial** use.

You **may not**:
- Sell it  
- Offer it as part of a paid product or SaaS  
- Use it in any commercial offering  

If you want to use it commercially, contact the author at: [navaneeth@vantablan.com](mailto:navaneeth@vantablan.com)

