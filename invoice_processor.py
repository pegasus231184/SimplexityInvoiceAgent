from typing import Dict, List
from openai import OpenAI
from config import Config
import json


class InvoiceProcessor:
    """Process invoices using OpenAI API and validate against rules"""

    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def parse_limitations(self, limitations_text: str) -> Dict:
        """Parse user-defined limitations using OpenAI"""
        prompt = f"""
        Parse the following invoice validation rules and extract:
        1. Allowed categories (e.g., food items only)
        2. Maximum amount limit
        3. Currency (CRC, USD, etc.)
        4. Any other restrictions

        Rules: {limitations_text}

        Respond in JSON format with keys: allowed_categories, max_amount, currency, other_restrictions
        """

        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that parses invoice validation rules. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            rules = json.loads(response.choices[0].message.content)
            return rules

        except Exception as e:
            print(f"Error parsing limitations: {e}")
            return {
                "allowed_categories": ["food"],
                "max_amount": 0,
                "currency": "CRC",
                "other_restrictions": []
            }

    def process_text_invoice(self, text: str, rules: Dict) -> Dict:
        """Process text-based invoice (PDF or XML) and validate against rules"""
        prompt = f"""
        Analyze the following invoice and extract:
        1. Supplier/vendor name
        2. Invoice number
        3. Invoice date
        4. All line items with descriptions and amounts
        5. Total amount
        6. Currency

        Then validate against these rules:
        - Allowed categories: {rules.get('allowed_categories', [])}
        - Maximum amount: {rules.get('max_amount', 0)} {rules.get('currency', 'CRC')}

        Invoice content:
        {text}

        Respond in JSON format with:
        {{
            "supplier_name": string,
            "invoice_number": string,
            "items": [list of items with name, amount, category],
            "total_amount": number,
            "currency": string,
            "date": string,
            "is_valid": boolean,
            "violations": [list of rule violations],
            "non_compliant_items": [items that don't match allowed categories],
            "exceeds_limit": boolean
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert invoice analyzer. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            print(f"Error processing text invoice: {e}")
            return {
                "supplier_name": "Desconocido",
                "invoice_number": "N/A",
                "items": [],
                "total_amount": 0,
                "currency": "Unknown",
                "date": "Unknown",
                "is_valid": False,
                "violations": [f"Processing error: {str(e)}"],
                "non_compliant_items": [],
                "exceeds_limit": False
            }

    def process_image_invoice(self, base64_image: str, file_extension: str, rules: Dict) -> Dict:
        """Process image-based invoice using OpenAI Vision API"""
        prompt = f"""
        Analyze this invoice image and extract:
        1. Supplier/vendor name
        2. Invoice number
        3. Invoice date
        4. All line items with descriptions and amounts
        5. Total amount
        6. Currency

        Then validate against these rules:
        - Allowed categories: {rules.get('allowed_categories', [])}
        - Maximum amount: {rules.get('max_amount', 0)} {rules.get('currency', 'CRC')}

        Respond in JSON format with:
        {{
            "supplier_name": string,
            "invoice_number": string,
            "items": [list of items with name, amount, category],
            "total_amount": number,
            "currency": string,
            "date": string,
            "is_valid": boolean,
            "violations": [list of rule violations],
            "non_compliant_items": [items that don't match allowed categories],
            "exceeds_limit": boolean
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_VISION_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{file_extension};base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )

            # Extract JSON from response
            content = response.choices[0].message.content
            # Try to parse as JSON directly, or extract JSON from markdown
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # Try to extract JSON from markdown code blocks
                if "```json" in content:
                    json_str = content.split("```json")[1].split("```")[0].strip()
                    result = json.loads(json_str)
                elif "```" in content:
                    json_str = content.split("```")[1].split("```")[0].strip()
                    result = json.loads(json_str)
                else:
                    raise ValueError("Could not parse JSON from response")

            return result

        except Exception as e:
            print(f"Error processing image invoice: {e}")
            return {
                "supplier_name": "Desconocido",
                "invoice_number": "N/A",
                "items": [],
                "total_amount": 0,
                "currency": "Unknown",
                "date": "Unknown",
                "is_valid": False,
                "violations": [f"Processing error: {str(e)}"],
                "non_compliant_items": [],
                "exceeds_limit": False
            }

    def calculate_accuracy(self, results: List[Dict]) -> float:
        """Calculate processing accuracy percentage"""
        if not results:
            return 0.0

        valid_count = sum(1 for r in results if r.get('is_valid', False))
        return (valid_count / len(results)) * 100

    def generate_report_data(self, results: List[Dict], rules: Dict) -> Dict:
        """Generate comprehensive report data"""
        total_processed = len(results)
        valid_invoices = sum(1 for r in results if r.get('is_valid', False))
        accuracy = self.calculate_accuracy(results)

        total_amount = sum(r.get('total_amount', 0) for r in results if r.get('is_valid', False))
        excluded_amount = sum(r.get('total_amount', 0) for r in results if not r.get('is_valid', False))

        all_violations = []
        for r in results:
            all_violations.extend(r.get('violations', []))

        return {
            'total_processed': total_processed,
            'valid_invoices': valid_invoices,
            'invalid_invoices': total_processed - valid_invoices,
            'accuracy_percentage': round(accuracy, 2),
            'total_approved_amount': total_amount,
            'total_excluded_amount': excluded_amount,
            'currency': rules.get('currency', 'CRC'),
            'max_limit': rules.get('max_amount', 0),
            'violations': all_violations,
            'detailed_results': results
        }
