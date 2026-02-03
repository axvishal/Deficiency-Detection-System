import pdfplumber
from app.utils.ocr import ocr_fallback
from app.services.llm_extractor import extract_all_fields_with_llm
from app.utils.chunker import chunk_text


def parse_pdf(pdf_path: str) -> dict:
    """
    Parse PDF → extract text → send to LLM to extract ALL fields dynamically
    """

    text = ""

    # -------- Step 1: Extract text using pdfplumber --------
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    # -------- Step 2: OCR fallback (scanned PDFs) --------
    if len(text.strip()) < 100:
        print("⚠️ Low text detected, using OCR fallback...")
        text = ocr_fallback(pdf_path)

    if not text or len(text.strip()) < 50:
        raise ValueError("No readable text could be extracted from PDF")

    # -------- Step 3: Chunk large documents --------
    chunks = chunk_text(text, max_chars=8000)

    all_fields = {}

    for idx, chunk in enumerate(chunks):
        print(f"📄 Processing chunk {idx + 1}/{len(chunks)}")

        chunk_fields = extract_all_fields_with_llm(chunk)

        if not isinstance(chunk_fields, dict):
            print("⚠️ LLM returned invalid format, skipping chunk")
            continue

        # Merge fields (LLM may repeat keys across chunks)
        for key, value in chunk_fields.items():
            if key not in all_fields:
                all_fields[key] = value

    # -------- Step 4: DEBUG VISIBILITY (CRITICAL) --------
    print("✅ TOTAL FIELDS EXTRACTED:", len(all_fields))
    print("✅ SAMPLE FIELD KEYS:", list(all_fields.keys())[:20])

    return all_fields
