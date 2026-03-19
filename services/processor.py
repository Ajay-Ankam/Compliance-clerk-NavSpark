import fitz  # PyMuPDF
import os

class PDFProcessor:
    @staticmethod
    def extract_text(file_path_or_bytes):
        """
        Extracts raw text from a PDF file.
        Works with both file paths and byte streams (from Streamlit).
        """
        text = ""
        try:
            # Open the document
            if isinstance(file_path_or_bytes, str):
                doc = fitz.open(file_path_or_bytes)
            else:
                doc = fitz.open(stream=file_path_or_bytes, filetype="pdf")

            # Iterate through pages and extract text
            for page in doc:
                text += page.get_text("text")
            
            doc.close()
            
            # Basic cleaning: remove excessive newlines and trailing spaces
            cleaned_text = " ".join(text.split())
            
            return cleaned_text
            
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None

    @staticmethod
    def get_preview_image(file_bytes, page_num=0):
        """
        Optional: Generates an image of the first page for the UI.
        Useful for visually confirming the document type.
        """
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            doc.close()
            return pix.tobytes()
        except:
            return None