# SleepyCat SEO Platform (v3.0)

A multi-agent SEO content engine powered by LiteLLM and Streamlit.

## 🚀 Deployment Instructions

### 1. GitHub Setup
- Initialize a new private repository on GitHub.
- Upload all files from this folder (`app.py`, `sleepycat_seo_agent.py`, `requirements.txt`, etc.).

### 2. Hosting (Streamlit Cloud - Recommended)
- Connect your GitHub repo to [Streamlit Community Cloud](https://streamlit.io/cloud).
- In **Settings > Secrets**, add your API keys:
  ```toml
  GEMINI_API_KEY = "your_key_here"
  ANTHROPIC_API_KEY = "your_key_here"
  OPENAI_API_KEY = "your_key_here"
  ```

### 3. Database (Cloudflare D1 Connection)
- The current version uses `agent_memory.json` for local persistent memory.
- To upgrade to Cloudflare D1, update the `_load_memory` function in `sleepycat_seo_agent.py` to call your Cloudflare Worker URL.

## 🧠 Features
- **Plug & Play Models:** Switch between Gemini, Claude, and GPT-4o from the UI.
- **RLHF Memory:** When you reject an output, the reason why is stored and used as a "Negative Constraint" for the next article.
- **Admin Console:** Access the sidebar with passcode `SleepyCat2026` to tune the Brand DNA or view the global agent memory.
- **AEO Ready:** Every output follows the Brand "Final Formula" structure (Direct Answer, Comparison Table, FAQ).
