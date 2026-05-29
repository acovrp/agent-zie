import streamlit as st
import os
import sys

st.set_page_config(page_title="Debug Console", page_icon="⚙️")

st.title("⚙️ SleepyCat SEO: Cloud Diagnostics")

st.write("### 1. Environment Info")
st.write(f"Python Version: {sys.version}")
st.write(f"Working Directory: {os.getcwd()}")

st.write("### 2. File Check")
files = os.listdir(".")
st.write(f"Files in current dir: {files}")

important_files = ["sleepycat_seo_agent.py", "product_catalog.json", "brand_guidelines.txt"]
for f in important_files:
    exists = os.path.exists(f)
    st.write(f"File `{f}` exists: {'✅' if exists else '❌'}")

st.write("### 3. Dependency Test")
try:
    import litellm
    st.write("`litellm` import: ✅")
except Exception as e:
    st.error(f"`litellm` import failed: {e}")

try:
    from sleepycat_seo_agent import Orchestrator
    st.write("`Orchestrator` import: ✅")
    st.success("App structure is healthy. Proceeding to render main UI...")
    
    # If healthy, show a button to switch to main UI
    if st.button("Launch Main Engine"):
        st.session_state['mode'] = 'main'
        st.rerun()
except Exception as e:
    st.error(f"Orchestrator import failed: {e}")
    st.info("Check if any requirements are missing or if there's a syntax error in `sleepycat_seo_agent.py`.")
