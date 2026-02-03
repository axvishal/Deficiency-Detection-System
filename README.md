# Deficiency Detection System

Compare **Application Form** (CAF/Form 1/Form 1A) with **Project Proposal/EIA Report** to identify discrepancies and inconsistencies for environmental clearance.

## Tech Stack

- **FastAPI** – REST API
- **PyMuPDF / PDFPlumber** – PDF parsing
- **Tesseract** – OCR fallback for scanned documents
- **AWS Bedrock (Claude 3.0 Sonnet)** – Semantic text comparison
- **PostgreSQL** – Comparison rules storage
- **Redis** – Rules cache (TTL: 2 hours)
- **Difflib** – Text comparison

## Project Structure

```
Deficiency Detection System/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models/              # Pydantic models
│   │   ├── document.py      # ExtractedDocument, BasicInfo, TechnicalData, etc.
│   │   └── comparison.py    # DiscrepancyReport, ComparisonRule, etc.
│   ├── services/
│   │   ├── document_parser.py   # PDF parsing + extraction
│   │   ├── comparison_rules.py  # Rules loading (Redis/DB/default)
│   │   ├── field_comparator.py  # Field-by-field comparison
│   │   ├── bedrock_semantic.py  # AWS Bedrock semantic comparison
│   │   └── deficiency_detector.py  # Main orchestrator
│   └── db/
│       ├── models.py        # SQLAlchemy models
│       └── session.py       # DB & Redis connections
├── scripts/
│   ├── init_db.py           # Initialize DB and seed rules
│   └── run_server.py        # Run uvicorn server
├── config.py
├── requirements.txt
└── .env.example
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key variables:

- `DATABASE_URL` – PostgreSQL connection string
- `REDIS_URL` – Redis connection (optional; falls back to default rules)
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` – For Bedrock semantic comparison (optional)

### 3. Initialize Database

```bash
python scripts/init_db.py
```

### 4. Run Server

```bash
python scripts/run_server.py
# Or: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

## API Endpoints

### `POST /compare`

Compare two PDFs: Application Form and Project Proposal.

**Request:** `multipart/form-data` with:

- `application_form` – PDF file
- `project_proposal` – PDF file

**Response:** `DiscrepancyReport` JSON

### `POST /compare/from-extracted`

Compare two pre-extracted documents (JSON body).

### `GET /health`

Health check (API + Redis).

## Output Format

```json
{
  "comparison_status": "discrepancies_found",
  "total_fields_compared": 20,
  "matched_fields": 15,
  "discrepancies": 5,
  "critical": 1,
  "high": 2,
  "medium": 1,
  "low": 1,
  "details": [
    {
      "field": "technical_data.capacity",
      "form_value": "100 MW",
      "proposal_value": "150 MW",
      "variance": "+50.0%",
      "severity": "CRITICAL",
      "category": "Technical"
    }
  ],
  "clarification_deadline": "2026-02-16",
  "discrepancy_score": 42,
  "processing_time_seconds": 2.5
}
```

## Comparison Rules (per 2_Deficiency_Detection_Flow.pdf)

- **185 fields** total: 85 critical (exact match), 100 flexible (tolerance allowed)
- **Exact match**: Project name, proponent name, company, address, state, district
- **Tolerance ±5%**: Capacity, production, raw materials (Technical)
- **Tolerance ±10%**: Investment, land cost, equipment (Financial)
- **Tolerance ±15%**: Plot area (Location)
- **Semantic**: Activity type (e.g., "Iron & Steel" vs "Steel Manufacturing" → Same)
- **Conditional**: If Form says X, Proposal must include X details

**Severity**: CRITICAL (capacity/location), HIGH (>20% financial), MEDIUM (5-20%), LOW (employment, semantic)

Rules cached in Redis (key: comparison_rules_v2024, TTL: 2 hours). Fallback: PostgreSQL → built-in defaults.

## Running Without PostgreSQL/Redis

The app can run without PostgreSQL and Redis. In that case it uses built-in default comparison rules.
