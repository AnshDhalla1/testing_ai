import streamlit as st
import os
import json
import tempfile
import pandas as pd
from main_final import run_parse_and_infer

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
    st.title("Resume Parser Application")

    uploaded_file = st.file_uploader("Upload a resume file", type=["pdf", "doc", "docx", "xlsx"])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.getbuffer())
            temp_file_path = tmp.name

        output_file = "final_output1.json"
        with st.spinner("Processing..."):
            time_stats, parsed_data, llm_output = run_parse_and_infer(temp_file_path, output_file)

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

        except json.JSONDecodeError:
            st.error("Could not parse JSON. Displaying raw output below:")
            st.text_area("LLM Response (raw)", llm_output, height=300)

        st.subheader("Time Statistics")
        st.json(time_stats)

if __name__ == "__main__":
    run_app()
