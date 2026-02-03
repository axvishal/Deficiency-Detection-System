EXTRACTION_PROMPT = """
You are an expert environmental clearance scrutiny officer.

Extract the following 185 project fields from the provided document text.

Rules:
- Return ONLY valid JSON
- Use null if a field is missing
- Do NOT invent values
- Numeric values must be numbers (no units)
- Capacity in MW, Investment in Crores, Area in Hectares

Fields to extract:
{field_list}

Document text:
----------------
{text}
----------------
"""
