import streamlit as st
import os
import json
import urllib.parse
import requests
import time
import subprocess
from datetime import datetime
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# ==========================================
# SleepyCat SEO Platform (v6.1 - SUPER AGENT)
# Merged: Deep Content + Enterprise Controls
# ==========================================

st.set_page_config(page_title="SleepyCat Engine", page_icon="🐈", layout="wide")

MODEL_MAP = {
    "Claude Sonnet (Company)": "anthropic/claude-sonnet-4-6",
    "Claude Opus (Company)":   "anthropic/claude-opus-4-7",
    "Claude Sonnet":           "anthropic/claude-sonnet-4-6",
    "Claude Opus":             "anthropic/claude-opus-4-7",
    "Gemini Flash":            "gemini/gemini-2.5-flash",
    "Gemini Pro":              "gemini/gemini-2.5-pro",
    "GPT-4o":                  "gpt-4o",
    "GPT-4o Mini":             "gpt-4o-mini",
    "Kimi 8K":                 "moonshot/moonshot-v1-8k",
}

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
HISTORY_PATH = os.path.join(BASE_PATH, "generation_history.json")
VAULT_PATH = os.path.join(BASE_PATH, "outputs")
MEMORY_PATH = os.path.join(BASE_PATH, "agent_memory.json")
if not os.path.exists(VAULT_PATH): os.makedirs(VAULT_PATH)

# --- Canonical Auth (Strict v6.1) ---
CLIENT_ID = "160422986634-5gpernee6sn90rtng8uqphrc7rris4t4.apps.googleusercontent.com"
CLIENT_SECRET = st.secrets.get("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "https://sleepycat-seo1.streamlit.app/"

if 'user_email' not in st.session_state:
    st.session_state['user_email'] = None

def login_ui():
    st.title("🐈 SleepyCat SEO Engine (v6.1)")
    st.info("Authorized access for @sleepycat.in domains only.")

    if not CLIENT_SECRET:
        st.error("⚠️ GOOGLE_CLIENT_SECRET missing from Streamlit Secrets.")
        return

    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "prompt": "select_account",
        "access_type": "online"
    }
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"

    st.link_button("🚀 Sign in with SleepyCat Google", auth_url, use_container_width=True, type="primary")

    # OAuth callback handler
    qp = st.query_params
    if "code" in qp:
        with st.spinner("Authenticating..."):
            try:
                res = requests.post("https://oauth2.googleapis.com/token", data={
                    "code": qp["code"],
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "redirect_uri": REDIRECT_URI,
                    "grant_type": "authorization_code"
                })
                tokens = res.json()
                if "id_token" in tokens:
                    info = id_token.verify_oauth2_token(tokens["id_token"], google_requests.Request(), CLIENT_ID)
                    email = info.get("email")
                    if email and (email.endswith("@sleepycat.in") or email == "admin@sleepycat.in"):
                        st.session_state["user_email"] = email
                        st.query_params.clear()
                        st.rerun()
                    else:
                        st.error(f"Access denied: {email} is not authorized.")
                else:
                    st.error(f"Token exchange failed: {tokens.get('error_description', str(tokens))}")
            except Exception as e:
                st.error(f"Auth error: {e}")

if not st.session_state["user_email"]:
    login_ui()
    st.stop()

# --- Sidebar ---
with st.sidebar:
    st.header(f"👤 {st.session_state['user_email']}")
    st.markdown("---")
    comp_k = st.secrets.get("COMPANY_CLAUDE_KEY") or os.environ.get("COMPANY_CLAUDE_KEY")
    if comp_k: st.success("🏢 Company Claude: Active")

    st.header("🔑 Session Keys")
    st.caption("Personal keys for individual quotas.")
    g_key   = st.text_input("Gemini",  type="password", value=st.session_state.get("GEMINI_KEY", ""))
    c_key   = st.text_input("Claude",  type="password", value=st.session_state.get("CLAUDE_KEY", ""))
    oai_key = st.text_input("OpenAI",  type="password", value=st.session_state.get("OPENAI_KEY", ""))

    models = []
    if comp_k: models.extend(["Claude Sonnet (Company)", "Claude Opus (Company)"])
    if g_key:
        st.session_state["GEMINI_KEY"] = g_key
        models.extend(["Gemini Flash", "Gemini Pro"])
    if c_key:
        st.session_state["CLAUDE_KEY"] = c_key
        models.extend(["Claude Sonnet", "Claude Opus"])
    if oai_key:
        st.session_state["OPENAI_KEY"] = oai_key
        models.extend(["GPT-4o", "GPT-4o Mini"])

    if st.button("Logout"):
        st.session_state["user_email"] = None
        st.rerun()

# --- Functions ---
def save_to_vault(keyword, content):
    filename = f"{datetime.now().strftime('%Y%m%d')}_{keyword.replace(' ', '_')}.md"
    safe_filename = "".join([c for c in filename if c.isalnum() or c in ('_', '.')]).rstrip()
    file_path = os.path.join(VAULT_PATH, safe_filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return safe_filename

def run_pipeline(kw, model_choice):
    from sleepycat_seo_agent import Orchestrator
    # Inject Keys
    if "Company" in model_choice:
        os.environ["ANTHROPIC_API_KEY"] = st.secrets.get("COMPANY_CLAUDE_KEY") or os.environ.get("COMPANY_CLAUDE_KEY", "")
    elif "Claude" in model_choice and st.session_state.get("CLAUDE_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = st.session_state["CLAUDE_KEY"]
    if st.session_state.get("GEMINI_KEY"):
        os.environ["GEMINI_API_KEY"] = st.session_state["GEMINI_KEY"]
    if st.session_state.get("OPENAI_KEY"):
        os.environ["OPENAI_API_KEY"] = st.session_state["OPENAI_KEY"]

    litellm_model = MODEL_MAP.get(model_choice, model_choice)
    engine = Orchestrator(model=litellm_model)
    
    with st.status("Super-Agent Active...", expanded=True) as s:
        st.write("🕵️ SERP Spy Analyzing...")
        serp = engine.serp_agent.execute_task(kw)
        st.write("🐈 Strategist Blueprinting...")
        brief = engine.strategist.execute_task(f"KW: {kw}\nSERP: {serp}")
        st.write("🧪 Drafting Deep Content (1500 words)...")
        draft = engine.drafter.execute_task(brief, engine.products)
        st.write("🏗️ SEO Architecting AEO...")
        opt = engine.seo_editor.execute_task(draft, kw, engine.products)
        st.write("✍️ Senior Editor Final Pass...")
        final, dur = engine.run(kw)
        s.update(label=f"Done in {dur}s!", state="complete")
        return final

def log_generation(kw, user, content, filename):
    hist = []
    try:
        if os.path.exists(HISTORY_PATH):
            with open(HISTORY_PATH, "r") as f: hist = json.load(f)
        hist.append({
            "id": len(hist) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "user": user,
            "keyword": kw,
            "content": content,
            "filename": filename,
            "status": "Pending Review"
        })
        with open(HISTORY_PATH, "w") as f: json.dump(hist, f, indent=2)
    except: pass

def update_feedback(gen_id, feedback, status):
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r") as f: hist = json.load(f)
        for i in hist:
            if i.get('id') == gen_id:
                i['feedback'] = feedback
                i['status'] = status
                break
        with open(HISTORY_PATH, "w") as f: json.dump(hist, f, indent=2)

def write_memory(keyword, feedback_text, memory_type):
    mem = []
    try:
        if os.path.exists(MEMORY_PATH):
            with open(MEMORY_PATH, "r") as f: mem = json.load(f)
    except: pass
    mem.append({
        "type": memory_type,
        "feedback": feedback_text,
        "keyword": keyword,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    with open(MEMORY_PATH, "w") as f: json.dump(mem, f, indent=2)

# --- Tabs ---
t1, t2, t3 = st.tabs(["🚀 Generator", "📜 History", "🛠️ Admin"])

with t1:
    col1, col2 = st.columns([2, 1])
    with col1:
        kw = st.text_input("Target Keyword", placeholder="How to choose the perfect mattress...")
        engine_choice = st.selectbox("Engine", models if models else ["No Keys Found"])
        generate_btn = st.button("Generate Blog Post", type="primary")

    with col2:
        st.subheader("Knowledge Vault")
        st.write(f"📁 **Storage:** {len(os.listdir(VAULT_PATH))} articles archived.")
        st.info("Every generation is backed up to the SleepyCat GitHub Vault.")

    if generate_btn and kw:
        final_content = run_pipeline(kw, engine_choice)
        vault_file = save_to_vault(kw, final_content)
        log_generation(kw, st.session_state['user_email'], final_content, vault_file)
        
        st.markdown("---")
        st.markdown(final_content)
        st.download_button("Download Markdown", final_content, vault_file)

with t2:
    st.subheader("Recent Generations")
    if os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, "r") as f:
                hist = json.load(f)
                for i in hist[::-1]:
                    with st.expander(f"[{i.get('timestamp')}] {i.get('keyword')} (by {i.get('user')})"):
                        st.markdown(i.get('content', '*No content archived.*'))
                        st.markdown("---")
                        st.write(f"**Status:** {i.get('status', 'Legacy')}")
                        if i.get('feedback'): st.info(f"**Feedback:** {i['feedback']}")
                        
                        iid = i.get('id')
                        status_val = i.get('status', 'Pending Review')
                        if iid and status_val == "Pending Review":
                            f1, f2 = st.columns(2)
                            with f1:
                                if st.button("👍 Approve", key=f"acc_{iid}"):
                                    update_feedback(iid, "Verified Quality", "Approved")
                                    st.rerun()
                            with f2:
                                if st.button("👎 Give Feedback", key=f"rej_{iid}"):
                                    st.session_state[f"fb_mode_{iid}"] = True
                            if st.session_state.get(f"fb_mode_{iid}", False):
                                good = st.text_area("What was good? (optional)", key=f"good_{iid}")
                                bad  = st.text_area("What was bad? (optional)",  key=f"bad_{iid}")
                                if st.button("Submit Feedback", key=f"sub_{iid}"):
                                    kw = i.get('keyword', '')
                                    if good.strip(): write_memory(kw, good.strip(), "positive")
                                    if bad.strip():  write_memory(kw, bad.strip(),  "negative")
                                    update_feedback(iid, (good + " | " + bad).strip(" |"), "Reviewed")
                                    st.session_state[f"fb_mode_{iid}"] = False
                                    st.rerun()
        except: st.error("History load error.")

with t3:
    st.subheader("Platform Administration")
    admin_code = st.text_input("Admin Passcode", type="password")
    if admin_code == "SleepyCat2026":
        st.success("Admin mode unlocked.")
        
        if st.button("🚀 Sync to GitHub Cloud Vault"):
            try:
                subprocess.run(["git", "config", "user.email", "admin@sleepycat.in"], check=True)
                subprocess.run(["git", "config", "user.name", "SleepyCat Admin"], check=True)
                subprocess.run(["git", "add", "outputs/*"], check=True)
                subprocess.run(["git", "add", "*.json"], check=True)
                subprocess.run(["git", "commit", "-m", f"Vault Sync: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
                subprocess.run(["git", "push", "origin", "master"], check=True)
                st.success("Successfully synced all articles to GitHub 100GB Vault!")
            except Exception as e: st.error(f"Sync Failed: {e}")
            
        st.markdown("---")
        st.subheader("🧐 Memory Review Queue")
        if os.path.exists(HISTORY_PATH):
            with open(HISTORY_PATH, "r") as f: hist = json.load(f)
            rejections = [i for i in hist if i.get('status') == "Rejected"]
            if rejections:
                for r in rejections:
                    with st.container(border=True):
                        st.write(f"**Keyword:** {r.get('keyword')} | **Reason:** {r.get('feedback')}")
                        rid = r.get('id')
                        if rid and st.button("🧠 Update Agent Memory", key=f"mem_{rid}"):
                            write_memory(r.get('keyword', ''), r['feedback'], "negative")
                            update_feedback(rid, r['feedback'], "Memory Updated")
                            st.success("Agent brain updated!")
                            st.rerun()
            else: st.write("No pending memory updates.")
    elif admin_code: st.error("Incorrect code.")
