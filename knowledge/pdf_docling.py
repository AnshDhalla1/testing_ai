from docling.document_converter import DocumentConverter

def extract_text_and_tables(pdf_path):
    
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    parsed_data = result.document.export_to_markdown()
    # print(parsed_data)  
    return parsed_data


# path = "/Users/Apple/Desktop/Givery/testing_ai/knowledge/Copy of 14893_20240722120940-37357ed226651667.pdf"
# text = extract_text_and_tables(path)