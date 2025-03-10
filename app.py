import streamlit as st
import os
import json
import tempfile
import pandas as pd
from main_final import process_resume

def convert_to_dataframe(parsed_json):
    """
    Converts parsed JSON into a pandas dataframe for display.
    """
    if isinstance(parsed_json, list):
        df = pd.DataFrame(parsed_json)
    elif isinstance(parsed_json, dict):
        df = pd.json_normalize(parsed_json)
    else:
        df = pd.DataFrame([parsed_json])
    return df

def run_app():
    st.title("Resume Parser Application (Multi-file)")

    uploaded_files = st.file_uploader(
        "Upload resume files",
        type=["pdf", "doc", "docx", "xlsx"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.markdown(f"### Processing: **{uploaded_file.name}**")
            
            # Temporary file creation
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                tmp.write(uploaded_file.getbuffer())
                temp_file_path = tmp.name

            with st.spinner(f"Running pipeline for {uploaded_file.name}..."):
                result_dict = process_resume(temp_file_path, uploaded_file.name)

            # Extract relevant fields from the result
            llm_output = result_dict["llm_output"]
            time_stats = result_dict["time_stats"]
            unique_id = result_dict["unique_id"]
            inserted_id = result_dict["inserted_id"]

            st.subheader("LLM Output")

            try:
                loaded_json = json.loads(llm_output)
                if "parsed" in loaded_json:
                    parsed_json = loaded_json["parsed"]

                    st.subheader("Personal Information")
                    personal_info = convert_to_dataframe(parsed_json.get('個人的', {}))
                    st.dataframe(personal_info)
                    
                    st.subheader("Desired Preferences")
                    desired_prefs = convert_to_dataframe(parsed_json.get('希望条件', {}))
                    st.dataframe(desired_prefs)

                    st.subheader("Qualifications")
                    qualifications = convert_to_dataframe(parsed_json.get('資格_', []))
                    if '年' in qualifications.columns:
                        qualifications['年'] = qualifications['年'].astype(str).str.replace(',', '')
                    if '月' in qualifications.columns:
                        qualifications['月'] = qualifications['月'].astype(str).str.replace(',', '')
                    st.dataframe(qualifications)

                    st.subheader("Skills Summary")
                    skills_summary = parsed_json.get('スキルサマリー', {})
                    self_pr = skills_summary.get('自己PR', '')
                    st.text_area("Self PR", self_pr if isinstance(self_pr, str) else "", height=200)

                    st.subheader("Work History")
                    work_history = convert_to_dataframe(parsed_json.get('職歴', []))
                    st.dataframe(work_history)

                    st.subheader("Skill Evaluation")
                    skill_eval = parsed_json.get('スキル評価', {})

                    for category, skills in skill_eval.items():
                        st.markdown(f"**Category:** {category}")
                        skills_df = pd.DataFrame.from_dict(skills, orient='index')
                        st.dataframe(skills_df)

                    st.subheader("Time Statistics")
                    st.json(time_stats)

                    # MongoDB Document ID
                    st.write(f"**Stored in DB with ID:** `{inserted_id}`")
                    st.write(f"**Unique ID:** `{unique_id}`")
                    st.markdown("---")

            except json.JSONDecodeError:
                st.error("Could not parse JSON. Displaying raw output below:")
                st.text_area("LLM Response (raw)", llm_output, height=300)

            
if __name__ == "__main__":
    run_app()
