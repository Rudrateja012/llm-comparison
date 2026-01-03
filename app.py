from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from utils.parallel import run_parallel
from utils.report import generate_report

st.set_page_config(
    page_title="LLM Comparison Tool",
    page_icon="🤖",
    