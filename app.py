import streamlit as st
import os
import json
import tempfile
import pandas as pd
from main_final import process_resume
from retrieve_doc import get_all_documents, get_document_by_object_id

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

def display_llm_output(parsed_json, time_stats, inserted_id, unique_id):
    st.subheader("個人情報")
    personal_info = convert_to_dataframe(parsed_json.get('個人的', {}))
    st.dataframe(personal_info)

    st.subheader("希望条件")
    desired_prefs = convert_to_dataframe(parsed_json.get('望ましい', {}))
    st.dataframe(desired_prefs)

    st.subheader("資格")
    qualifications = convert_to_dataframe(parsed_json.get('資格_', []))
    if '年' in qualifications.columns:
        qualifications['年'] = qualifications['年'].astype(str).str.replace(',', '')
    if '月' in qualifications.columns:
        qualifications['月'] = qualifications['月'].astype(str).str.replace(',', '')
    st.dataframe(qualifications)

    st.subheader("スキルサマリー")
    skills_summary = parsed_json.get('スキルサマリー', {})
    self_pr = skills_summary.get('自己PR', '')
    st.text_area("自己PR", self_pr if isinstance(self_pr, str) else "", height=200)

    st.subheader("職歴")
    work_history = convert_to_dataframe(parsed_json.get('職歴', []))
    st.dataframe(work_history)

    st.subheader("スキル評価")
    skill_eval = parsed_json.get('スキル評価', {})
    for category, skills in skill_eval.items():
        st.markdown(f"**カテゴリ:** {category}")
        skills_df = pd.DataFrame.from_dict(skills, orient='index')
        st.dataframe(skills_df)

    st.subheader("時間統計")
    st.json(time_stats)

    st.write(f"**MongoDBに保存されたID:** `{inserted_id}`")
    st.write(f"**Unique ID:** `{unique_id}`")

def run_app():
    st.title("Resume Parser Application (Multi-file)")

    # Create two tabs: one for upload and one for retrieving stored results
    tab1, tab2 = st.tabs(["アップロード", "保存済み結果"])

    with tab1:
        uploaded_files = st.file_uploader(
            "Please upload the resume files",
            type=["pdf", "doc", "docx", "xlsx"],
            accept_multiple_files=True
        )

        if uploaded_files:
            for uploaded_file in uploaded_files:
                with st.expander(f"### 処理中: **{uploaded_file.name}**"):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                        tmp.write(uploaded_file.getbuffer())
                        temp_file_path = tmp.name

                    with st.spinner(f"{uploaded_file.name} の処理中..."):
                        result_dict = process_resume(temp_file_path, uploaded_file.name)

                    llm_output = result_dict["llm_output"]
                    time_stats = result_dict["time_stats"]
                    unique_id = result_dict["unique_id"]
                    inserted_id = result_dict["inserted_id"]

                    st.subheader(f"### LLM 出力: **{uploaded_file.name}**")

                    try:
                        loaded_json = json.loads(llm_output)
                        if "parsed" in loaded_json:
                            parsed_json = loaded_json["parsed"]
                            display_llm_output(parsed_json, time_stats, inserted_id, unique_id)
                            st.markdown("---")
                        else:
                            st.error("期待される 'parsed' キーがLLM出力に見つかりませんでした。")
                    except json.JSONDecodeError:
                        st.error("JSONの解析に失敗しました。下記に生データを表示します:")
                        st.text_area("LLM 出力 (生データ)", llm_output, height=300)

    with tab2:
        st.header("保存済み結果の一覧")

        documents = get_all_documents()

        if documents:

            documents.sort(key=lambda x: x.get("timestamp", 0), reverse=True)

            for doc in documents:
                _id = str(doc.get("_id"))
                unique_id = doc.get("unique_id", "N/A")
                file_name = doc.get("file_name", "N/A")
                timestamp = doc.get("timestamp", "N/A")
                total_time = doc.get("time_stats", {}).get("total_time", "N/A")

                with st.expander(f"View {file_name} | Doc ID: {_id}"):
                    st.markdown(f"""
                    <div style="border: 2px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                        <p><strong>Unique ID:</strong> {unique_id}</p>
                        <p><strong>Timestamp:</strong> {timestamp}</p>
                        <p><strong>Parse Time:</strong> {total_time} seconds</p>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"View Parsed Data for Unique ID: {unique_id}"):
                        st.subheader(f"パース結果: {_id}")
                        stored_llm_output = doc.get("llm_output", {})
                        time_stats = doc.get("time_stats", {})
                        display_llm_output(stored_llm_output, time_stats, _id, unique_id)
                        st.markdown("---")

        else:
            st.write("保存済みの結果がありません。")

if __name__ == "__main__":
    run_app()