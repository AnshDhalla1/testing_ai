import os
import json
import time
import certifi
from dotenv import load_dotenv
from openai import OpenAI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone

from utils.jp_schema import ResumeSchema
from knowledge.pdf_docling import extract_text_and_tables
from knowledge.parse_excel import extract_excel_to_markdown
from knowledge.parsedoc import extract_text_docx_file, extract_text_from_doc
from prompt.test1 import RESUME_EXTRACTION_PROMPT

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")

# MongoDB Connection
client = MongoClient(
        MONGODB_URI, 
        tlsCAFile=certifi.where(),  
        serverSelectionTimeoutMS=5000
    )
db = client["resume_db"]
collection = db["resumes"]

#Helper/Decorator
def log_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⏱️ {func.__name__} executed in {end_time - start_time:.2f} seconds.")
        return result
    return wrapper

#Parsing Resume Files
@log_time
def parse_file(file_path):
    """Given a path to a file on disk, parse it according to extension."""
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == ".pdf":
        return extract_text_and_tables(file_path)
    elif file_extension in [".doc"]:
        return extract_text_from_doc(file_path)
    elif file_extension in [".docx"]:
        return extract_text_docx_file(file_path)
    elif file_extension == ".xlsx":
        return extract_excel_to_markdown(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

#Calling OpenAI API (ChatCompletions)
@log_time
def call_openai(prompt, parsed_data):
    print("🔮 Calling OpenAI's API...")
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.beta.chat.completions.parse(
        temperature=0.65,
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": str(prompt)},
            {"role": "user", "content": str(parsed_data)}
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

#Core Pipeline
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

    parse_start = time.time()
    parsed_data = parse_file(file_path)
    time_stats["pdf_parse_time"] = time.time() - parse_start
    print(f"📄 File Parsing Time: {time_stats['pdf_parse_time']:.2f}s")

    prompt = RESUME_EXTRACTION_PROMPT
    #print(f"🔍 Parsed data {parsed_data}")

    inference_start = time.time()
    llm_output = call_openai(prompt, parsed_data)
    time_stats["total_inference_time"] = time.time() - inference_start

    parsed_json = json.loads(llm_output)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parsed_json.get("parsed"), f, ensure_ascii=False, indent=4)
    print(f"✅ Final output saved to {output_file}")

    time_stats["total_time"] = time.time() - total_start
    print(f"⏱️ Total Inference Time: {time_stats['total_inference_time']:.2f}s")
    print(f"⏱️ Total Execution Time: {time_stats['total_time']:.2f}s")

    return time_stats, parsed_data, llm_output

#Generate Unique ID
def generate_unique_id(file_name):
    """
    Creates a unique ID based on file name + timestamp.
    """
    import time
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    sanitized_name = base_name.replace(" ", "_")
    timestamp = int(time.time())
    return f"{sanitized_name}_{timestamp}"

#Store in MongoDB
def store_in_mongo(unique_id, file_name, parsed_data, llm_output, time_stats):
    """
    Insert a record in the MongoDB collection.
    """
    doc = {
        "unique_id": unique_id,
        "file_name": file_name,
        # "parsed_data": parsed_data,
        "llm_output": json.loads(llm_output).get("parsed", {}),
        "timestamp": datetime.now(timezone.utc),
        "time_stats": time_stats
    }
    result = collection.insert_one(doc)
    print(f"Inserted document with _id: {result.inserted_id}")
    return result.inserted_id

#Main Function
def process_resume(file_path, original_filename):
    """
    Orchestrates:
      1) Parsing
      2) OpenAI inference
      3) Unique ID generation
      4) Saving output to local file
      5) Storing in Mongo
    """
    unique_id = generate_unique_id(file_path)
    output_file = f"final_output_{unique_id}.json"

    time_stats, parsed_data, llm_output = run_parse_and_infer(file_path, output_file)

    inserted_id = store_in_mongo(unique_id, original_filename, parsed_data, llm_output, time_stats)

    return {
        "inserted_id": inserted_id,
        "unique_id": unique_id,
        "time_stats": time_stats,
        "parsed_data": parsed_data,
        "llm_output": llm_output
    }


def main():
    """
    This is the CLI entry point. 
    Hard-coded example usage for local debugging.
    """
    file_path = "/Users/Apple/Desktop/Givery BP/Givery-Resume-Parsing/data/JP resume format 021.docx"
    result_info = process_resume(file_path, "JP resume format 001.pdf")

    print (result_info)

if __name__ == "__main__":
    main()