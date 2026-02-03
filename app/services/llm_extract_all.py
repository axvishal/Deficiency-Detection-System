You are given a project document.

Extract ALL project-related parameters as key–value pairs.

Rules:
- Extract ALL numeric and categorical parameters
- Ignore narrative paragraphs
- Return JSON only
- Each key must be a human-readable field name
- Each value must be a number or short string
- Include unit if present

Output format:
{
  "Field Name": {
     "value": <value>,
     "unit": "<unit or null>"
  }
}
