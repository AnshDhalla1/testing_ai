# main.py

import os
import json
import time
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI
from utils.jp_schema import ResumeSchema
from knowledge.parse_pdf import extract_text_and_tables
from knowledge.parse_excel import extract_excel_to_markdown
from knowledge.parsedoc import extract_text_from_doc
from prompt_test.test2 import RESUME_EXTRACTION_PROMPT

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def log_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⏱️ {func.__name__} executed in {end_time - start_time:.2f} seconds.")
        return result
    return wrapper

@log_time
def call_openai(prompt):
    print("🔮 Calling OpenAI's API...")
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.beta.chat.completions.parse(
        temperature=0.1,
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format=ResumeSchema,
    )
    response = completion.choices[0].message.model_dump_json(exclude_none=True)

    print(
        f"Prompt Tokens: {completion.usage.prompt_tokens}, "
        f"Completion Tokens: {completion.usage.completion_tokens}, "
        f"Total Tokens: {completion.usage.total_tokens}"
    )
    return response

@log_time
def parse_file(file_path):
    """Given a path to a file on disk, parse it according to extension."""
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == ".pdf":
        return extract_text_and_tables(file_path)
    elif file_extension == ".doc":
        return extract_text_from_doc(file_path)
    elif file_extension == ".docx":
        # if needed, treat .docx same as .doc or adapt
        return extract_text_from_doc(file_path)
    elif file_extension == ".xlsx":
        return extract_excel_to_markdown(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

@log_time
def run_parse_and_infer(file_path: str, output_file: str):
    """
    Core function that:
      1) Parses the given file path.
      2) Calls the OpenAI API with the parsed text.
      3) Saves the JSON output to output_file.
    Returns a tuple: (time_stats, parsed_text, llm_output)
    """
    time_stats = {}
    total_start = time.time()

    # 1) Parse the file
    parse_start = time.time()
    parsed_data = parse_file(file_path)
    time_stats["pdf_parse_time"] = time.time() - parse_start
    print(f"📄 File Parsing Time: {time_stats['pdf_parse_time']:.2f}s")

    parsed_data_file = "./output_parsed/parsed_data_001.txt"
    with open(parsed_data_file, "w", encoding="utf-8") as f:
        f.write(str(parsed_data))  
        print(f"⛳️ Extraction saved to {parsed_data_file}")

    # 2) Create prompt
    prompt = f"{RESUME_EXTRACTION_PROMPT}\n\n{parsed_data}"

    # 3) Call OpenAI
    inference_start = time.time()
    llm_output = call_openai(prompt)
    time_stats["total_inference_time"] = time.time() - inference_start
    # 4) Save JSON output
    parsed_json = json.loads(llm_output)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parsed_json.get("parsed"), f, ensure_ascii=False, indent=4)
    print(f"✅ Final output saved to {output_file}")


    time_stats["total_time"] = time.time() - total_start
    print(f"⏱️ Total Inference Time: {time_stats['total_inference_time']:.2f}s")
    print(f"⏱️ Total Execution Time: {time_stats['total_time']:.2f}s")

    return time_stats, parsed_data, llm_output

def main():
    """
    This is the CLI entry point. 
    Hard-coded example usage for local debugging.
    """
    file_path = "/Users/Apple/Documents/Givery/data/JP resume format 001.pdf"
    output_file = "output_pdf/final_output000011.json"

    run_parse_and_infer(file_path, output_file)

if __name__ == "__main__":
    main()
