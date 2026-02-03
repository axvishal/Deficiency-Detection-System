# Deficiency Detection Agent

An intelligent document comparison system that analyzes environmental compliance documents using AI-powered semantic analysis. It compares Application Forms (CAF, Form 1, Form 1A) with Project Proposals/EIA Reports to identify discrepancies, inconsistencies, and compliance issues.

## 🎯 Features

- **AI-Powered Comparison**: Uses AWS Bedrock (Claude 3.0 Sonnet) for semantic text analysis and field matching
- **Multi-format PDF Support**: Handles both digital and scanned PDFs with OCR fallback
- **Dynamic Field Extraction**: Automatically extracts and normalizes fields from unstructured documents
- **Intelligent Matching**: Matches semantically similar fields even when names differ (e.g., "capacity" vs "installed capacity")
- **Discrepancy Detection**: Identifies mismatches with severity levels (CRITICAL, HIGH, MEDIUM, LOW)
- **Flexible Tolerance Rules**: Supports tolerance-based comparisons for numeric fields
- **Production-Ready**: FastAPI-based REST API with comprehensive error handling

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   FastAPI Server                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐        ┌──────────────┐          │
│  │  PDF Upload  │        │ Pre-extracted│          │
│  │   Endpoint   │        │  JSON Input  │          │
│  └──────┬───────┘        └──────┬───────┘          │
│         │                       │                   │
│         └───────────┬───────────┘                   │
│                     ▼                               │
│         ┌─────────────────────────┐                │
│         │   PDF Parser Service    │                │
│         │  ┌──────────────────┐   │                │
│         │  │ PDFPlumber       │   │                │
│         │  │ + OCR Fallback   │   │                │
│         │  │ + Chunking       │   │                │
│         │  └──────────────────┘   │                │
│         └────────────┬─────────────┘                │
│                      ▼                              │
│         ┌─────────────────────────┐                │
│         │   LLM Extractor         │                │
│         │   (AWS Bedrock)         │                │
│         │  Extract all fields     │                │
│         │  dynamically            │                │
│         └────────────┬─────────────┘                │
│                      ▼                              │
│         ┌─────────────────────────┐                │
│         │ Document Model Builder  │                │
│         │ Normalize & Structure   │                │
│         │ Create Dict of Fields   │                │
│         └────────────┬─────────────┘                │
│                      ▼                              │
│         ┌─────────────────────────┐                │
│         │   LLM Comparator        │                │
│         │   (AWS Bedrock)         │                │
│         │  • Match fields         │                │
│         │  • Detect discrepancies │                │
│         │  • Assign severity      │                │
│         │  • Return structured    │                │
│         │    JSON report          │                │
│         └────────────┬─────────────┘                │
│                      ▼                              │
│         ┌─────────────────────────┐                │
│         │    Response API         │                │
│         │  JSON Discrepancy       │                │
│         │  Report                 │                │
│         └─────────────────────────┘                │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
deficiency-detection-agent/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry point
│   ├── config.py                    # Environment configuration (ignored in git)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── compare.py               # Comparison endpoints
│   │       ├── POST /compare/       # Upload PDFs and compare
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── document_model.py        # DocumentModel, ExtractedField
│   │   ├── extracted_field.py       # Field data structure
│   │   └── project_fields.py        # Field definitions
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py            # PDF extraction + text normalization
│   │   ├── llm_extractor.py         # AWS Bedrock field extraction
│   │   ├── document_builder.py      # Structure extracted data
│   │   ├── llm_comparator.py        # AWS Bedrock comparison logic
│   │   ├── llm_prompts.py           # LLM prompt templates
│   │   ├── discrepancy_analyzer.py  # Severity & categorization
│   │   └── rule_loader.py           # Load comparison rules
│   │
│   └── utils/
│       ├── __init__.py
│       ├── chunker.py               # Text chunking for LLM processing
│       └── ocr.py                   # Tesseract OCR fallback
│
├── rules/                           # Comparison rules (git ignored)
├── uploads/                         # PDF uploads (git ignored)
├── config.py                        # Credentials & env vars
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules (protects credentials)
└── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Tesseract-OCR (for scanned document support)
- AWS Account with Bedrock access (Claude 3.0 Sonnet)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/axvishal/Deficiency-Detection-System.git
   cd deficiency-detection-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your AWS credentials
   ```

5. **Install Tesseract (Optional, for scanned PDFs)**
   
   **Windows:**
   ```bash
   # Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
   # Or use: choco install tesseract
   ```
   
   **macOS:**
   ```bash
   brew install tesseract
   ```
   
   **Linux:**
   ```bash
   sudo apt-get install tesseract-ocr
   ```

6. **Run the server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access API**
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health: http://localhost:8000/

## 📊 API Usage

### Endpoint: POST /compare/

Compare two PDF documents (Application Form and Project Proposal).

**Request:**
```bash
curl -X POST http://localhost:8000/compare/ \
  -F "application_form=@form.pdf" \
  -F "project_proposal=@proposal.pdf"
```

**Response:**
```json
{
  "comparison_status": "completed",
  "form_fields": 45,
  "proposal_fields": 38,
  "comparison": {
    "matched": [
      {
        "field_form": "project_name",
        "field_proposal": "Project Title",
        "value_form": "Solar Farm Alpha",
        "value_proposal": "Solar Farm Alpha",
        "reason": "Exact match"
      }
    ],
    "discrepancies": [
      {
        "field_form": "capacity_mw",
        "field_proposal": "installed_capacity",
        "value_form": "100 MW",
        "value_proposal": "150 MW",
        "severity": "CRITICAL",
        "reason": "50% variance exceeds tolerance"
      }
    ],
    "missing_in_application": [],
    "missing_in_proposal": ["environmental_clearance_number"]
  }
}
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# AWS Credentials (Required for LLM features)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-south-1

# Optional: Database & Caching
DATABASE_URL=postgresql://user:password@localhost/deficiency_db
REDIS_URL=redis://localhost:6379
```

**Security Note:** The `.env` file is git-ignored to protect your credentials. Never commit it!

## 🧠 How It Works

### Step 1: PDF Processing
- **PDFPlumber** extracts text from digital PDFs
- **Tesseract OCR** handles scanned documents (fallback)
- **Text Chunking** breaks large documents for LLM processing

### Step 2: Field Extraction
- **LLM Extractor** (AWS Bedrock) dynamically identifies and extracts fields
- No hardcoded field mappings - works with any document structure
- Handles both structured and unstructured text

### Step 3: Document Structuring
- **Document Builder** normalizes extracted data
- Creates searchable field dictionary
- Preserves context and metadata

### Step 4: Intelligent Comparison
- **LLM Comparator** (AWS Bedrock) performs semantic analysis
- Matches semantically similar field names
- Compares values with business logic
- Identifies missing fields
- Assigns severity levels

### Step 5: Report Generation
- Structures results into:
  - **Matched fields** - fields that align
  - **Discrepancies** - conflicting values with severity
  - **Missing fields** - fields in one document but not the other

## 📋 Comparison Rules

### Matching Criteria
- **Exact Match**: Project name, proponent, company, address, state, district
- **Semantic Match**: Activity type, location description, facility type
- **Tolerance-Based Match** (numeric):
  - ±5%: Capacity, production, raw materials
  - ±10%: Investment, land cost, equipment
  - ±15%: Plot area

### Severity Levels
- **CRITICAL**: Legal/clearance/capacity mismatch (>20% variance)
- **HIGH**: Financial discrepancies >20%
- **MEDIUM**: 5-20% variance
- **LOW**: Minor discrepancies or semantic differences

## 🛡️ Security

✅ **Credentials Protected**
- AWS credentials stored in `.env` (git-ignored)
- No hardcoded secrets in source code
- Environment variables used for all sensitive data

✅ **File Handling**
- Temporary file cleanup after processing
- PDF uploads not persisted (unless explicitly configured)
- No sensitive data logged

## 🔍 Troubleshooting

### Common Issues

**"No readable text could be extracted from PDF"**
- Ensure Tesseract is installed
- Check PDF is not corrupted
- Verify image quality for scanned documents

**"AWS Bedrock API Error"**
- Verify AWS credentials in `.env`
- Check AWS region has Bedrock enabled
- Ensure IAM permissions for bedrock:InvokeModel

**"Temporary file not found"**
- Check disk space for temp files
- Verify file permissions in /tmp or Windows temp folder

## 🤝 Contributing

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make changes and test
3. Commit with clear messages: `git commit -m "Add new feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Create Pull Request to `main`

## 📝 Git Workflow

- **main** - Production-ready code
- **develop/vishal** - Development and testing branch
- **feature/** - Feature branches for new developments

## 📚 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| API | FastAPI | ≥0.109.0 |
| PDF Processing | PyMuPDF, PDFPlumber | ≥1.24.0, ≥0.10.0 |
| OCR | Tesseract | - |
| LLM | AWS Bedrock (Claude 3.0) | Sonnet |
| Web Server | Uvicorn | ≥0.27.0 |
| Data Validation | Pydantic | ≥2.6.0 |
| Async | httpx | ≥0.26.0 |
| Testing | pytest, pytest-asyncio | ≥8.0.0 |

## 📄 License

This project is proprietary and confidential.

## 👤 Author

**Vishal** - Project Lead & Developer

---

**Last Updated:** February 3, 2026

For issues, feature requests, or contributions, please create an issue or pull request on GitHub.
