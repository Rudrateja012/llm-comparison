from dotenv import load_dotenv
import streamlit as st
from utils.parallel import run_parallel
from utils.report import generate_report

load_dotenv()

st.set_page_config(
    page_title="LLM Model Comparision",
    page_icon="🤖",
    layout="wide"
)

st.title("LLM Model Comparision")
st.markdown(
    """
    Compare **ChatGPT**, **LLaMA**, and **Gemini** models using a single prompt.
    """
)

prompt = st.text_area(
    "Enter your prompt here:",
    height=150,
    placeholder="Type your prompt to compare model responses..."
)

if st.button("Compare Models"):
    if not prompt.strip():
        st.warning("Please enter a valid prompt.")
    else:
        with st.spinner("Running models in parallel..."):
            responses = run_parallel(prompt)
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("ChatGPT")
                st.write(responses.get("ChatGPT", ""))

                st.subheader("Gemini")
                st.write(responses.get("Gemini", ""))

            with col2:
                st.subheader("LLaMA")
                st.write(responses.get("LLaMA", ""))

            report_path = generate_report(prompt, responses)

            with open(report_path, "rb") as file:
                st.download_button(
                    label="Download Comparison Report",
                    data=file,
                    file_name="model_comparison_report.csv",
                    mime="text/csv"
                )
            
            st.success("Model comparison completed!")