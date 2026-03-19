import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from schemas.document_schemas import EChallanData, NAPermissionData
from database.db_manager import log_audit

load_dotenv()

class DocumentExtractor:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-3-flash-preview"

    def _get_system_prompt(self, doc_type: str):
        # We fetch the JSON schema from Pydantic to tell Gemini exactly what to return
        schema = EChallanData.model_json_schema() if doc_type == "eChallan" else NAPermissionData.model_json_schema()
        
        return f"""
        Act as a professional Compliance Clerk. Your task is to extract structured data from the provided {doc_type} text.
        
        STRICT RULES:
        1. Output MUST be a valid JSON object.
        2. Follow this JSON Schema exactly: {json.dumps(schema)}
        3. If a value is missing, use "N/A" for strings or 0 for numbers.
        4. Do not include any conversational text, markdown formatting like ```json, or explanations. Only the raw JSON.
        """

    def extract(self, text: str, doc_type: str, filename: str):
        system_prompt = self._get_system_prompt(doc_type)
        user_prompt = f"Extract details from this document text:\n\n{text}"

        try:
            # 1. Call Gemini
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.1,
                    response_mime_type="application/json" # Ensures JSON output
                )
            )

            raw_response = response.text
            
            # 2. Audit Logging (Requirement #3)
            log_audit(
                filename=filename,
                doc_type=doc_type,
                prompt=system_prompt + "\n" + user_prompt,
                response=raw_response,
                status="Success"
            )

            # 3. Parse and Validate with Pydantic (Schema Enforcement)
            data_dict = json.loads(raw_response)
            if doc_type == "eChallan":
                return EChallanData(**data_dict)
            else:
                return NAPermissionData(**data_dict)

        except Exception as e:
            # Log failure to audit trail
            log_audit(filename, doc_type, user_prompt, str(e), status="Failure")
            print(f"Extraction Error: {e}")
            return None