from pydantic import BaseModel
from typing import Dict
from app.models.extracted_field import ExtractedField

class DocumentModel(BaseModel):
    document_type: str          # "application_form" / "proposal"
    fields: Dict[str, ExtractedField]
