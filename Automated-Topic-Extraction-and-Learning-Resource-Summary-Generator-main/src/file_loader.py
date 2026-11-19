import os

import fitz
from pptx import Presentation


def extract_text_from_pdf(file_path):
    text_content = []
    try:
        doc = fitz.open(file_path)
        for page_num, page in enumerate(doc):
            page_text = page.get_text()
            if page_text:
                text_content.append(page_text)
        doc.close()
        return "\n".join(text_content)
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""

def extract_text_from_pptx(file_path):
    text_content = []
    try:
        prs = Presentation(file_path)
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text_frame"):
                    if shape.text_frame:
                        for paragraph in shape.text_frame.paragraphs:
                            text = ''.join(run.text for run in paragraph.runs)
                            if text.strip():
                                text_content.append(text)
        return "\n".join(text_content)
    except Exception as e:
        print(f"Error reading PPTX {file_path}: {e}")
        return ""

def load_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == '.pdf':
        print(f"Processing PDF: {file_path}")
        return extract_text_from_pdf(file_path)
    elif file_extension == '.pptx':
        print(f"Processing PPTX: {file_path}")
        return extract_text_from_pptx(file_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return None

if __name__ == "__main__":
    pass
