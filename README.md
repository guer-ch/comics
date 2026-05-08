AI Comics Generator
===================

Quick local AI-like comics generator that composes comic panels from text prompts.

Features
- Simple Flask web UI to enter a title and one prompt per panel.
- Local "synth" mode that renders panel artwork by drawing prompt text onto panels using Pillow (no external API required).
- Option to wire an external image API (stubbed) using an env var later.

Getting started

1. Create a virtual environment and install deps:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the app:

```bash
python app.py
```

3. Open http://127.0.0.1:5000 in your browser.

Notes
- The default generator is a local renderer (Pillow) that creates simple illustrative panels from text.
- To integrate a real AI image API, update `comics/generator.py` and set an API key via `.env`.
