from app.models.extracted_field import ExtractedField
from app.models.document_model import DocumentModel


def build_document_model(raw_json: dict, doc_type: str) -> DocumentModel:
    """
    Convert raw LLM-extracted JSON into a structured DocumentModel
    """

    fields = {}

    for key, data in raw_json.items():
        fields[key] = ExtractedField(
            key=key,
            value=data.get("value"),
            unit=data.get("unit"),
            page=data.get("page"),
            section=data.get("section")
        )

    return DocumentModel(
        document_type=doc_type,
        fields=fields
    )
