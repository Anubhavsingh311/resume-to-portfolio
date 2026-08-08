# AI Usage Log

This log documents the AI tools used during development of the AI-Assisted Resume Portfolio Generator. All AI-generated output was reviewed, tested, and where necessary corrected or rewritten by the team before inclusion in the project.

---

## Entry 1

**Tool:** Claude (Anthropic)
**Stage:** Week 1 — Frontend Design & HTML Generation
**Team member responsible:** Anubhav Singh

**What we did:**
The team designed the complete frontend layout in Figma before writing any code. This covered the section hierarchy (hero, skills, experience, projects, contact), the earthy warm color palette (`#f1e0c5` background, `#71816d` accent, `#c9b79c` cards), and the typography pairing of Lato for body text and Playfair Display for headings. Once the design was finalized and approved internally, we handed it off to Claude to speed up the translation from Figma to HTML/CSS.

**Prompt given to AI:**
> This is the Figma design of the frontend that I made: https://www.figma.com/design/c7F2zUQg06VXAjTySmQnKs/Resume_to_Portfolio?node-id=0-1&t=M9c4BottWIjQQ1YO-1 — Use this to make an HTML file that will be the frontend of our project.

**What the AI generated:**
Claude produced a complete `index.html` with embedded CSS, matching the Figma layout including the section structure, font imports from Google Fonts, color variables, and responsive card styling.

**What we changed before using it:**
- Adjusted spacing and padding values that did not match the Figma spec precisely.
- Replaced placeholder section headings with our actual copy.
- Restructured the skills section from a list to pill badges, which was in our Figma but not correctly reflected in the AI output.
- Added the Google Fonts `<link>` tag that was missing from the initial `<head>`.
- Verified cross-browser rendering manually in Chrome and Safari before committing.

---

## Entry 2

**Tool:** ChatGPT 5.6 LUNA
**Stage:** Week 2 — Ai_parser Module Debugging
**Team member responsible:** Shivanshu Rajput

**What we did:**
One team member built the `Ai_parser` package from scratch — covering `parser.py`, `schema.py`, `validator.py`, `normalizer.py`, `exceptions.py`, `logger.py`, `cleaner.py`, and `__init__.py`. After internal code review, the team identified two files that were producing import and runtime errors during integration testing and passed them to ChatGPT for a second-opinion review.

**Prompt given to AI:**
> These are the AI parser files that one of my teammates made. Check if there is any error.

The files `__init__.py` and `cleaner.py` were shared.

**What the AI found:**
ChatGPT identified two bugs:
1. `__init__.py` — `ValidationError` was listed in `__all__` but was not imported from `exceptions.py`, causing an `ImportError` at runtime.
2. `cleaner.py` — The `rfind("}")` call was returning `-1` on some edge-case Gemini responses that returned a trailing newline after the closing brace, causing the extractor to silently return an empty string instead of the JSON object.

**What we changed before using it:**
- The `__init__.py` fix (adding `ValidationError` to the import line) was applied directly as the diagnosis was correct.
- For `cleaner.py`, ChatGPT suggested a regex-only approach. We reviewed this and kept our own two-step logic (markdown fence extraction first, then brace-boundary fallback), adding only a `.strip()` call before the `rfind` to handle the trailing newline case. This was cleaner and preserved the original author's intent.
- Both files were re-tested against valid JSON, JSON wrapped in markdown fences, and malformed responses before merging.

---

## Entry 3

**Tool:** Claude (Anthropic)
**Stage:** Week 3 — Documentation
**Team member responsible:** Shivam Sharma

**What we did:**
With the project functionally complete and tested, the team drafted the README content collaboratively — covering the workflow, setup steps, prompt design rationale, known limitations, and testing results. The full project was then packaged and given to Claude to produce a formatted `README.md` that matched our content and structure.

**Prompt given to AI:**
> This is the final project in the .zip file format. Make a proper README.md file for me. GitHub repo link — https://github.com/Anubhavsingh311/resume-to-portfolio and deployed link — https://anubhavsingh311.github.io/resume-to-portfolio/

**What the AI generated:**
Claude produced a complete `README.md` with sections for project overview, live demo link, browser-based usage, local Python CLI usage, project structure, workflow diagram, responsible use notes, and setup instructions.

**What we changed before using it:**
- Rewrote the "How it works" section to more accurately describe our `Ai_parser` pipeline, which the AI had described too generically.
- Added the mandatory testing results table and the hallucination/limitations section, which Claude had omitted.
- Corrected the Python version requirement (Claude assumed 3.8; our code requires 3.10+ due to `match` statement usage in `normalizer.py`).
- Added the AI usage log reference and the `.env.example` instructions, which were missing from the generated output.

---

## Summary

| Entry | Tool | Task | Lines of AI output used as-is | Lines modified or rewritten |
|-------|------|------|-------------------------------|----------------------------|
| 1 | Claude | HTML/CSS from Figma design | ~70% structural HTML | Spacing, pills section, font tag, copy |
| 2 | ChatGPT 5.6 LUNA | Bug review of `__init__.py` and `cleaner.py` | Fix for `__init__.py` import | `cleaner.py` fix adapted, not copied |
| 3 | Claude | README.md generation | ~60% formatting and structure | Limitations, testing table, version info, AI log ref |

All AI tools were used as accelerators. Core logic (`main.py`, full `Ai_parser` package, prompt engineering, testing suite) was written entirely by the team.
