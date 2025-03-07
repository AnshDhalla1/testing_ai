from docling.document_converter import DocumentConverter

def extract_text_and_tables(pdf_path):
    
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    parsed_data = result.document.export_to_markdown()
    #print(parsed_data)  
    return parsed_data
