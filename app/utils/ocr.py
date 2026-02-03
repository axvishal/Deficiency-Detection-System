import pytesseract
from PIL import Image
import fitz  # PyMuPDF

def ocr_fallback(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        full_text += pytesseract.image_to_string(img)

    return full_text
