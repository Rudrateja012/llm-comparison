import streamlit as st
import pandas as pd
import time
import os

from dotenv import load_dotenv

load_dotenv()

try:
    from auth import login
    from utils.router import choose_models
    from utils.parallel import run_parallel
    from utils.rate_limiter import check_limit
    from utils.report import generate_report
except Exception as e:
    st.error(e)
    st.stop()

st.set_page_config(
    page_title="LLM Nexus | Enterprise Comparison",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;0,700;1,400&family=Montserrat:wght@200;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        background-color: #050505 !important; /* Pure Black */
    }

    .stApp {
        background: linear-gradient(180deg, #0a0a0a 0%, #000000 100%);
    }

    /* --- Luxury Header Style --- */
    .main-header {
        font-family: 'Bodoni Moda', serif !important;
        font-size: 4rem !important;
        font-weight: 400 !important;
        font-style: italic;
        letter-spacing: -2px !important;
        background: linear-gradient(to bottom, #ffffff 30%, #a1a1a1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-top: 2rem;
    }

    .sub-header {
        font-family: 'Montserrat', sans-serif;
        font-weight: 200;
        text-transform: uppercase;
        letter-spacing: 8px !important;
        color: #d4af37 !important; /* Classic Gold */
        text-align: center;
        font-size: 0.8rem !important;
        margin-bottom: 4rem !important;
    }

    /* --- Floating Glass Inputs --- */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 0.5px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 0px !important; /* Sharp edges = Luxury */
        color: #ffffff !important;
        padding: 20px !important;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    .stTextArea textarea:focus {
        border-color: #d4af37 !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }

    /* --- The "Signature" Button --- */
    div.stButton > button {
        background: transparent !important;
        color: #d4af37 !important;
        border: 1px solid #d4af37 !important;
        padding: 1rem 3rem !important;
        border-radius: 0px !important;
        text-transform: uppercase !important;
        letter-spacing: 4px !important;
        font-weight: 400 !important;
        transition: all 0.6s cubic-bezier(0.19, 1, 0.22, 1) !important;
    }

    div.stButton > button:hover {
        background: #d4af37 !important;
        color: #000 !important;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.3);
    }

    /* --- Card Aesthetics (The "Boutique" Look) --- */
    .model-card {
        background: rgba(255, 255, 255, 0.01);
        border-top: 1px solid rgba(212, 175, 55, 0.3); /* Gold accent top line */
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding: 40px !important;
        text-align: center;
    }

    .model-name {
        font-family: 'Bodoni Moda', serif !important;
        font-size: 1.5rem !important;
        font-style: italic;
        color: #ffffff !important;
        margin-bottom: 20px !important;
    }

    /* --- Metric Refinement --- */
    div[data-testid="metric-container"] {
        background: transparent !important;
        border: none !important;
        border-left: 1px solid rgba(212, 175, 55, 0.5) !important;
        padding-left: 20px !important;
    }

    label[data-testid="stMetricLabel"] {
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        font-size: 0.7rem !important;
        color: #888 !important;
    }

    /* Scrollbar for luxury feel */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #d4af37; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ Controls")
    
    if "user" in st.session_state:
        st.info(f"👤 Logged in as: **{st.session_state.user}**")
    
    st.markdown("---")
    
    st.subheader("Configuration")
    model_temp = st.slider("Temperature (Creativity)", 0.0, 1.0, 0.7)
    max_tokens = st.number_input("Max Tokens", value=1024, step=256)
    
    st.markdown("---")
    st.caption("v2.1.0 | Enterprise Edition")


def main():
    
    login()
    if "user" not in st.session_state:
        st.stop()

   
    st.markdown('<div class="main-header">LLM Nexus</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Intelligent routing & cost-analysis engine for Generative AI.</div>', unsafe_allow_html=True)

    
    col1, col2 = st.columns([1, 3])

    with col1:
        task = st.selectbox(
            "Target Objective",
            ["General", "Coding", "Fast Response", "Cost Saving"],
            help="This determines which models are selected via the router."
        )
        
       
        st.metric(label="Active Models", value="3 Online", delta="All Systems Go")

    with col2:
        prompt = st.text_area(
            "Input Prompt",
            height=140,
            placeholder="E.g., Write a secure Python function to connect to AWS S3...",
            label_visibility="visible"
        )

   
    col_submit, col_spacer = st.columns([1, 4])
    with col_submit:
        run_btn = st.button("⚡ Execute Query")

    if run_btn:
        if not check_limit(st.session_state.user):
            st.error("🚫 Rate limit reached. Please upgrade your plan or wait.")
            st.stop()
            
        if not prompt.strip():
            st.warning("⚠️ Please provide a prompt to analyze.")
            st.stop()

     
        with st.status("🔄 Orchestrating Model Requests...", expanded=True) as status:
            st.write("🔍 Analyzing intent...")
            models = choose_models(task)
            st.write(f"✅ Selected optimized models: **{', '.join(models)}**")
            
            st.write("🚀 Dispatching parallel requests...")
            start_time = time.time()
            
            responses = run_parallel(prompt, models)
            
            elapsed = round(time.time() - start_time, 2)
            status.update(label=f"✅ Complete! Processed in {elapsed}s", state="complete", expanded=False)

     
        st.markdown("### 📊 Analysis Results")
        
       
        tab1, tab2, tab3, tab4 = st.tabs([
            "👁️ Visual Comparison",
            "📝 Raw Data",
            "📉 Cost Report",
            "📊 Performance Dashboard"
        ])



        with tab1:
           
            cols = st.columns(len(responses))
            
         
            for idx, (model_name, response_text) in enumerate(responses.items()):
                with cols[idx]:
                    st.markdown(f"""
                    <div class="model-card">
                        <div class="model-name">{model_name}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("---")
                    st.markdown(response_text) 

        with tab2:
            st.json(responses)

        with tab3:
           
            report_status = generate_report(prompt, responses)
            st.success("Report generated and saved to database.")
            
           
            metrics_col1, metrics_col2 = st.columns(2)
            metrics_col1.metric("Estimated Cost", "$0.0042", "-12%")
            metrics_col2.metric("Latency Average", f"{elapsed}s", "Fast")
        with tab4:
            st.markdown("### 📊 Model Performance Dashboard")

            metrics_file = "data/metrics/metrics.csv"

            if not os.path.exists(metrics_file):
                st.warning("No metrics data available yet. Run some prompts first.")
            else:
                df = pd.read_csv(metrics_file)

                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

                st.subheader("⏱️ Average Latency per Model")
                latency_df = df.groupby("model")["latency"].mean().reset_index()
                st.bar_chart(latency_df.set_index("model"))

                st.subheader("📏 Average Response Length")
                length_df = df.groupby("model")["response_length"].mean().reset_index()
                st.bar_chart(length_df.set_index("model"))

                st.subheader("📈 Requests Over Time")
                time_df = df.set_index("timestamp").resample("1min").count()["model"]
                st.line_chart(time_df)


if __name__ == "__main__":
    main()