from pydantic import BaseModel
from typing import Optional

class ExtractedField(BaseModel):
    key: str                    # Raw field name from document
    value: str | float | int    # Raw value
    unit: Optional[str] = None
    page: Optional[int] = None
    section: Optional[str] = None
