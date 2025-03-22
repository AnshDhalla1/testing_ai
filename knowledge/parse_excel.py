import pandas as pd
from tabulate import tabulate

def extract_excel_to_markdown(file_path):
    df = pd.read_excel(file_path, header=None, dtype=str, engine='openpyxl')
    

    df_cleaned = df.dropna(how='all').dropna(axis=1, how='all')
    df_filled = df_cleaned.ffill(axis=0)
    markdown_text = tabulate(df_filled, headers='firstrow', tablefmt="github")
    return markdown_text
 

# file_path = '/Users/Apple/Desktop/Givery BP/Givery-Resume-Parsing/data/JP resume format 012.xlsx'  # Replace with your file path

# # Call the function and print the output
# markdown_output = extract_excel_to_markdown(file_path)

# parsed_data_file = "/Users/Apple/Desktop/Givery BP/Givery-Resume-Parsing/output_parsed/parsed_data2.txt"
# with open(parsed_data_file, "w", encoding="utf-8") as f:
#     f.write(str(markdown_output))  
#     print(f"⛳️ Extraction saved to {parsed_data_file}")