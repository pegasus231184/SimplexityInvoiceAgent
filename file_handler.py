import os
import base64
from typing import Dict, List, Optional
from werkzeug.utils import secure_filename
import PyPDF2
import pdfplumber
import xmltodict
from PIL import Image
from config import Config


class FileHandler:
    """Handle file uploads and text extraction from various formats"""

    @staticmethod
    def allowed_file(filename: str) -> bool:
        """Check if file extension is allowed"""
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @staticmethod
    def save_uploaded_file(file) -> Optional[str]:
        """Save uploaded file and return the file path"""
        if file and FileHandler.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)
            return filepath
        return None

    @staticmethod
    def extract_text_from_pdf(filepath: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            # Try with pdfplumber first (better for complex PDFs)
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            # Fallback to PyPDF2
            try:
                with open(filepath, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as fallback_error:
                print(f"Error extracting PDF text: {fallback_error}")
                return ""

        return text.strip()

    @staticmethod
    def extract_text_from_xml(filepath: str) -> Dict:
        """Parse XML file and return structured data"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                xml_content = file.read()
                data = xmltodict.parse(xml_content)
                return data
        except Exception as e:
            print(f"Error parsing XML: {e}")
            return {}

    @staticmethod
    def encode_image_to_base64(filepath: str) -> Optional[str]:
        """Encode image to base64 for OpenAI Vision API"""
        try:
            with open(filepath, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error encoding image: {e}")
            return None

    @staticmethod
    def get_file_extension(filepath: str) -> str:
        """Get file extension"""
        return filepath.rsplit('.', 1)[1].lower() if '.' in filepath else ''

    @staticmethod
    def process_file(filepath: str) -> Dict[str, any]:
        """Process file based on its type and return extracted data"""
        ext = FileHandler.get_file_extension(filepath)

        result = {
            'filepath': filepath,
            'extension': ext,
            'text': '',
            'data': None,
            'base64': None
        }

        if ext == 'pdf':
            result['text'] = FileHandler.extract_text_from_pdf(filepath)
        elif ext == 'xml':
            result['data'] = FileHandler.extract_text_from_xml(filepath)
            # Convert XML data to string for processing
            result['text'] = str(result['data'])
        elif ext in ['png', 'jpg', 'jpeg']:
            result['base64'] = FileHandler.encode_image_to_base64(filepath)

        return result

    @staticmethod
    def cleanup_file(filepath: str):
        """Delete uploaded file after processing"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Error deleting file {filepath}: {e}")
