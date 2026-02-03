import json
import boto3
from app.utils.chunker import chunk_text
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


def extract_all_fields_with_llm(text: str) -> dict:
    """
    Extract ALL possible fields dynamically from document text.
    No predefined schema. No validation here.
    """

    chunks = chunk_text(text, max_chars=8000)
    all_fields = {}

    for idx, chunk in enumerate(chunks):
        print(f"🔹 LLM extracting fields from chunk {idx + 1}/{len(chunks)}")

        prompt = f"""
You are given a project-related document text.

Your task:
- Extract ALL project parameters as key–value pairs
- Include numeric, categorical, and boolean parameters
- Ignore narrative paragraphs
- Do NOT invent values
- Do NOT normalize names
- Preserve original field wording as much as possible

Return STRICT JSON only in this format:

{{
  "Field Name": {{
    "value": <number | string>,
    "unit": "<unit or null>"
  }}
}}

Document text:
----------------
{chunk}
----------------
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
        extracted_text = raw["content"][0]["text"]

        try:
            partial_fields = json.loads(extracted_text)
        except json.JSONDecodeError:
            print("⚠️ Invalid JSON from LLM, skipping chunk")
            continue

        # Merge fields without overwriting existing keys
        for key, value in partial_fields.items():
            if key not in all_fields:
                all_fields[key] = value

    print("✅ TOTAL FIELDS DISCOVERED:", len(all_fields))
    print("✅ SAMPLE FIELD KEYS:", list(all_fields.keys())[:20])

    return all_fields
