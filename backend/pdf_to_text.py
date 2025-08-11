# backend/pdf_to_text.py

import fitz  # PyMuPDF
import os

def pdf_to_text(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file.
    
    Returns:
        str: Extracted text content.
    """
    text = ""
    try:
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                text += page.get_text()
    except Exception as e:
        print(f"[ERROR] Failed to process {pdf_path}: {e}")
    
    return text.strip()


def save_text_from_pdf(pdf_path: str, output_dir: str):
    """
    Converts PDF to text and saves it as a .txt file in output_dir.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    text = pdf_to_text(pdf_path)
    output_file = os.path.join(output_dir, os.path.basename(pdf_path).replace(".pdf", ".txt"))
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"[INFO] Saved text to {output_file}")


if __name__ == "__main__":
    # Example usage
    sample_pdf = "../data/papers/sample.pdf"  # change path
    output_folder = "../data/papers_text"
    save_text_from_pdf(sample_pdf, output_folder)
