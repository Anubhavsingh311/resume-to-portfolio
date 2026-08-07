"""
Resume to Portfolio Generator - Backend
========================================
FastAPI backend that accepts resume uploads (PDF/DOCX),
extracts text, sends to Gemini API, and returns structured JSON.
"""

import os
import uuid
import logging
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from utils.pdf_parser import extract_text_from_pdf
from utils.docx_parser import extract_text_from_docx
from utils.prompt_builder import build_portfolio_prompt
from utils.gemini_client import call_gemini
from utils.json_validator import validate_portfolio_json

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

load_dotenv()

# Ensure upload / log directories exist at startup
Path("uploads").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/app.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("main")

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Resume to Portfolio Generator API",
    description="Converts PDF/DOCX resumes into structured portfolio JSON via Gemini.",
    version="1.0.0",
)

# Allow requests from the frontend served locally or from any origin during
# development. Tighten this to the real frontend origin in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Supported MIME / extension mapping
# ---------------------------------------------------------------------------

ALLOWED_CONTENT_TYPES = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    # Browsers sometimes send these for .docx
    "application/octet-stream": None,  # resolved by extension below
}

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def _resolve_file_type(filename: str, content_type: str) -> str:
    """
    Returns 'pdf' or 'docx', or raises HTTPException on unsupported type.
    """
    ext = Path(filename).suffix.lower()

    if ext in ALLOWED_EXTENSIONS:
        return ext.lstrip(".")

    mapped = ALLOWED_CONTENT_TYPES.get(content_type)
    if mapped:
        return mapped

    raise HTTPException(
        status_code=415,
        detail=(
            f"Unsupported file type '{ext}' (content-type: {content_type}). "
            "Please upload a PDF or DOCX file."
        ),
    )


# ---------------------------------------------------------------------------
# Health-check endpoint
# ---------------------------------------------------------------------------


@app.get("/health", tags=["meta"])
async def health_check():
    """Quick liveness probe."""
    return {"status": "ok", "version": "1.0.0"}


# ---------------------------------------------------------------------------
# Main endpoint
# ---------------------------------------------------------------------------


@app.post("/api/parse-resume", tags=["resume"])
async def parse_resume(file: UploadFile = File(...)):
    """
    Accept a resume file (PDF or DOCX), extract its text, send to Gemini,
    and return a structured portfolio JSON object.

    Returns
    -------
    JSON object matching the PortfolioSchema (see utils/json_validator.py).
    """
    request_id = str(uuid.uuid4())[:8]
    logger.info("[%s] Received file: name=%s  content_type=%s", request_id, file.filename, file.content_type)

    # ── 1. Validate file type ────────────────────────────────────────────────
    file_type = _resolve_file_type(file.filename or "", file.content_type or "")

    # ── 2. Read file bytes ───────────────────────────────────────────────────
    raw_bytes = await file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    file_size_kb = len(raw_bytes) / 1024
    logger.info("[%s] File size: %.1f KB  type: %s", request_id, file_size_kb, file_type)

    if file_size_kb > 10_240:  # 10 MB guard
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10 MB.")

    # ── 3. Optionally persist upload for debugging (disable in prod) ─────────
    if os.getenv("SAVE_UPLOADS", "false").lower() == "true":
        save_path = Path("uploads") / f"{request_id}_{file.filename}"
        save_path.write_bytes(raw_bytes)
        logger.debug("[%s] Saved upload to %s", request_id, save_path)

    # ── 4. Extract text ──────────────────────────────────────────────────────
    try:
        if file_type == "pdf":
            resume_text = extract_text_from_pdf(raw_bytes)
        else:
            resume_text = extract_text_from_docx(raw_bytes)
    except Exception as exc:
        logger.exception("[%s] Text extraction failed", request_id)
        raise HTTPException(
            status_code=422,
            detail=f"Could not extract text from the uploaded {file_type.upper()} file: {exc}",
        ) from exc

    if not resume_text or len(resume_text.strip()) < 50:
        raise HTTPException(
            status_code=422,
            detail=(
                "The extracted text is too short or empty. "
                "Ensure the file is not scanned/image-only and contains selectable text."
            ),
        )

    logger.info("[%s] Extracted %d characters of resume text.", request_id, len(resume_text))

    # ── 5. Build prompt ──────────────────────────────────────────────────────
    prompt = build_portfolio_prompt(resume_text)

    # ── 6. Call Gemini ───────────────────────────────────────────────────────
    try:
        raw_json_str = await call_gemini(prompt, request_id=request_id)
    except Exception as exc:
        logger.exception("[%s] Gemini API call failed", request_id)
        raise HTTPException(
            status_code=502,
            detail=f"Gemini API error: {exc}",
        ) from exc

    # ── 7. Validate JSON ─────────────────────────────────────────────────────
    try:
        portfolio_data = validate_portfolio_json(raw_json_str)
    except ValueError as exc:
        logger.error("[%s] JSON validation failed: %s", request_id, exc)
        raise HTTPException(
            status_code=502,
            detail=f"Gemini returned invalid JSON: {exc}",
        ) from exc

    logger.info("[%s] Successfully parsed resume. Returning portfolio JSON.", request_id)
    return JSONResponse(content=portfolio_data)
