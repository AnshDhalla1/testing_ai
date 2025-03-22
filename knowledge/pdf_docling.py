from docling.document_converter import DocumentConverter

def extract_text_and_tables(pdf_path):
    
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    parsed_data = result.document.export_to_markdown()
    return parsed_data


# path = "/Users/Apple/Desktop/Givery BP/Givery-Resume-Parsing/data/JP resume format 002.pdf"
# text = extract_text_and_tables(path)

# parsed_data_file = "/Users/Apple/Desktop/Givery BP/Givery-Resume-Parsing/output_parsed/parsed_data_001.txt"
# with open(parsed_data_file, "w", encoding="utf-8") as f:
#     f.write(str(text))  
#     print(f"⛳️ Extraction saved to {parsed_data_file}")