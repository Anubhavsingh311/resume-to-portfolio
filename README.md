# Resume-to-Portfolio Generator

Turn your plain-text resume into a polished portfolio webpage in seconds — no coding required.

**Live site:** [View](https://anubhavsingh311.github.io/resume-to-portfolio/)

---

## Use it in the browser (no setup)

1. Open the [live site](https://anubhavsingh311.github.io/resume-to-portfolio/).
2. Enter your free [Gemini API key](https://aistudio.google.com/app/apikey).
3. Paste your resume text.
4. Click **Generate** — preview appears instantly.
5. Click **Download** to save your `portfolio.html`.

Your resume and API key go directly to Google. Nothing is stored or proxied through any server.

---

## Use it locally (Python CLI)

If you prefer to run it on your machine and get a file written to disk:

```bash
# 1. Clone
git clone https://github.com/Anubhavsingh311/resume-to-portfolio.git
cd resume-to-portfolio

# 2. Virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
echo "GEMINI_API_KEY=your_key_here" > .env

# 5. Add your resume
# Paste your resume content into resume.txt

# 6. Run
python main.py
# Output: portfolio.html
```

Get a free Gemini API key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).

---

## How it works

```
resume.txt → Gemini API → {html, css, js} → Ai_parser → portfolio.html
```

The `Ai_parser` package cleans, validates, and normalizes Gemini's response before the HTML is assembled. The browser UI (`index.html`) does the same thing client-side with JavaScript — no Python required.

---

## Responsible use

- Do not include passwords, ID numbers, or financial details in your resume text.
- Never commit your `.env` file — it's already in `.gitignore`.
- Verify every generated section against your actual resume before sharing publicly.
