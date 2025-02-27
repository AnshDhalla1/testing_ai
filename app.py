# app.py

import streamlit as st
import os
import json
import tempfile
from main_final import run_parse_and_infer

def run_app():
    st.title("Resume Parser Application")

    uploaded_file = st.file_uploader("Upload a resume file", type=["pdf","doc","docx","xlsx"])
    if uploaded_file is not None:
        # 1) Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.getbuffer())
            temp_file_path = tmp.name

        # 2) Choose output file name
        output_file = "final_output.json"

        # 3) Call our run_parse_and_infer function
        with st.spinner("Processing..."):
            time_stats, parsed_data, llm_output = run_parse_and_infer(temp_file_path, output_file)

        # 4) Display results

        # A) Show the extracted text from the file
        # st.subheader("Extracted Text")
        # st.text_area("Parsed Data", parsed_data, height=500)

        # B) Show the raw JSON from LLM (if valid)
        st.subheader("LLM Output")

        try:
            loaded_json = json.loads(llm_output)  # parse the raw string
            # # Show the entire JSON
            # st.write("**Full JSON response:**")
            # st.json(loaded_json)

            # Optionally show only the 'parsed' field if you want
            if "parsed" in loaded_json:
                st.write("**Final 'parsed' content:**")
                st.json(loaded_json["parsed"])

        except json.JSONDecodeError:
            # If parsing fails, show the raw text
            st.error("Could not parse JSON. Displaying raw output below:")
            st.text_area("LLM Response (raw)", llm_output, height=300)

        # C) Show timing stats
        st.subheader("Time Statistics")
        st.json(time_stats)

if __name__ == "__main__":
    run_app()
