import json
import boto3
import re
from app.models.document_model import DocumentModel
from app.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION
)

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


def _extract_json(text: str) -> dict:
    """
    Safely extract first JSON object from LLM output
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in LLM response")

    json_text = match.group(0)
    return json.loads(json_text)


def compare_documents_with_llm(
    form_doc: DocumentModel,
    proposal_doc: DocumentModel
) -> dict:

    prompt = f"""
You are an expert government compliance auditor.

You are given TWO JSON documents extracted from PDFs.

APPLICATION FORM:
{json.dumps(form_doc.model_dump(), indent=2)}

PROJECT PROPOSAL:
{json.dumps(proposal_doc.model_dump(), indent=2)}

TASK:
1. Match semantically similar fields (even if names differ)
2. Compare values
3. Identify discrepancies
4. Identify missing fields
5. Assign severity:
   - CRITICAL (legal / clearance / capacity mismatch)
   - HIGH
   - MEDIUM
   - LOW

⚠️ OUTPUT RULES (MANDATORY):
- Output STRICT JSON ONLY
- No explanations
- No comments
- No markdown
- Keys MUST be in double quotes
- Values must be valid JSON

Return JSON in EXACT format:

{{
  "matched": [
    {{
      "field_form": "",
      "field_proposal": "",
      "value_form": "",
      "value_proposal": "",
      "reason": ""
    }}
  ],
  "discrepancies": [
    {{
      "field_form": "",
      "field_proposal": "",
      "value_form": "",
      "value_proposal": "",
      "severity": "",
      "reason": ""
    }}
  ],
  "missing_in_application": [],
  "missing_in_proposal": []
}}
"""

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ],
            "max_tokens": 4096,
            "temperature": 0
        })
    )

    raw = json.loads(response["body"].read())
    llm_text = raw["content"][0]["text"]

    try:
        return _extract_json(llm_text)
    except Exception as e:
        print("❌ RAW LLM OUTPUT (for debugging):")
        print(llm_text)
        raise RuntimeError(f"LLM returned invalid JSON: {e}")
