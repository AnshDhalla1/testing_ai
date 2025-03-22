import subprocess
import os
from docling.document_converter import DocumentConverter

def extract_text_docx_file(path):
    
    converter = DocumentConverter()
    result = converter.convert(path)
    parsed_data = result.document.export_to_markdown()
    return parsed_data

def extract_text_from_doc(doc_path): 
    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"Input file not found: {doc_path}")
    if not doc_path.endswith(".doc"):
        raise ValueError(f"Unsupported file type: {doc_path}. Expected .doc")

    try:
        result = subprocess.run(
            ["antiword", doc_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise FileNotFoundError(f"Antiword failed: {e.stderr}")
    except FileNotFoundError:
        raise FileNotFoundError("antiword is not installed. Install it via 'brew install antiword' on macOS or 'apt-get install antiword' on Linux.")
    
