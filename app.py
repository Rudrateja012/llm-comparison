from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from utils.parallel import run_parallel
from utils.report import generate_report

st.set_page_config(
    page_title="LLM Comparison Tool",
    page_icon="🤖👾👽",
    layout="wide",
)
st.title("🤖👾👽 LLM Comparison Tool")
st.markdown(
    """
    compare **chatGPT**, **GPT-4**, **Claude**, **Gemini** and more models side by side.
    """
)
prompt = st.text_area(
    "Enter your prompt here:", 
    height=200
    placeholder="e.g., Write a poem about the sea in the style of Shakespeare."
)