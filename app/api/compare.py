from fastapi import APIRouter, UploadFile, File
import tempfile
import os

from app.services.pdf_parser import parse_pdf
from app.services.document_builder import build_document_model
from app.services.llm_comparator import compare_documents_with_llm

router = APIRouter()


@router.post("/compare/")
async def compare_documents(
    application_form: UploadFile = File(...),
    project_proposal: UploadFile = File(...)
):
    # -------- Save uploaded files --------
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f1:
        f1.write(await application_form.read())
        form_path = f1.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f2:
        f2.write(await project_proposal.read())
        proposal_path = f2.name

    try:
        # -------- Extract ALL fields dynamically --------
        form_raw_fields = parse_pdf(form_path)
        proposal_raw_fields = parse_pdf(proposal_path)

        print("📄 FORM FIELD COUNT:", len(form_raw_fields))
        print("📄 PROPOSAL FIELD COUNT:", len(proposal_raw_fields))

        # -------- Build structured document models --------
        form_doc = build_document_model(form_raw_fields, "application_form")
        proposal_doc = build_document_model(proposal_raw_fields, "project_proposal")

        # -------- LLM-based semantic comparison --------
        comparison_result = compare_documents_with_llm(form_doc, proposal_doc)

        return {
            "comparison_status": "completed",
            "form_fields": len(form_doc.fields),
            "proposal_fields": len(proposal_doc.fields),
            "comparison": comparison_result
        }

    finally:
        os.unlink(form_path)
        os.unlink(proposal_path)
