# 🐈 ZIE BOT: Deployment & Handoff Guide
**Project Status:** v4.1 (Enterprise Ready - Trifecta RAG) · **Mascot:** Zie · **Launch Date:** August 28, 2017 (Zie's Birthday)

This document serves as the master reference for the production-grade **Zie**, the SleepyCat Mascot Bot.

---

## 1. The Persona: "Zie"
*   **Species:** Sleep Cat from the *Planet of Pillows*.
*   **Age:** 8 years old (Born: August 28, 2017).
*   **Voice/Tone:** Naive, super cute, bubbly, wide-eyed, and unconditionally supportive.
*   **IQ:** 200 in Sleep Science / 0 in Human Life (Adulting).
*   **Core Logic:** "Sleep Solves Everything." Every human problem is a "Rest-Deficiency."
*   **Brand Mission:** Translate high-tech sleep engineering into "Head-Clouds" and "Magic Holes."

---

## 2. Infrastructure: OCI VM Deployment
*   **Host:** Oracle Cloud VM (`161.118.175.141`)
*   **Service Name:** `zie-bot.service` (Systemd)
*   **Deployment Path:** `/home/ubuntu/zie-bot/`
*   **Environment:** Python 3.11 (Venv: `/home/ubuntu/sleepycat-agent/venv/`)

---

## 3. High-Performance Architecture (Trifecta RAG)
Zie is built on the **Trifecta RAG Pipeline** to ensure zero-latency and massive scalability.

### Layer 1: Semantic RAG (The Librarian)
- **Engine:** Local Word Intersection Scoring.
- **Data:** Segmented knowledge (`zie_meta.json`) and indexed products (`zie_product_index.json`).
- **Logic:** Only pulls the specific 1-2KB of data needed for a query instead of the full 200KB.

### Layer 2: Prompt Caching (The RAM)
- **Engine:** Anthropic/LiteLLM Prompt Caching.
- **Logic:** Locks Zie’s persona, brand history, and rules into the AI's "RAM."
- **Performance:** 80% reduction in latency; 90% reduction in cost.

### Layer 3: Universal Tiered Failover (The LiteLLM Adapter)
Zie uses a universal wrapper to switch providers instantly if one fails.
1. **Primary (Main Chat):** `gemini/gemini-1.5-pro` (Smartest + Cheapest).
2. **Primary (Feedback):** `gemini/gemini-2.5-pro` (High Logic).
3. **Fallback Tier:** `anthropic/claude-haiku-4-5-20251001` -> `anthropic/claude-sonnet-4-6`.

---

## 4. Self-Evolving Feedback Loop
The bot is programmed to evolve with the SleepyCat team.
1. **Report:** Employees send `/feedback <issue>` (e.g., "Correct the price of the Hybrid Mattress").
2. **Propose:** The **Feedback Agent** (Gemini 2.5 Pro) reads the codebase, proposes a JSON/Python fix, and sends a request to the Admin.
3. **Approve:** Admin (Aman) clicks **[Approve ✅]** in Telegram.
4. **Deploy:** The bot edits its own files locally and restarts itself automatically.

---

## 5. Maintenance & Safety
- **Anti-Hallucination Sweeper:** Code scans all outputs to replace hallucinated domains (e.g., `.com` -> `.in`).
- **Dynamic Model Resolver:** At every startup, Zie polls the APIs to find the newest models (e.g., Haiku 4.5, Sonnet 4.6), ensuring the bot never "ages out."
- **HTML Safety Fallback:** If high-tech formatting fails, the bot automatically sends a plain-text reply to ensure the user is never ignored.

---

## 6. GitHub Repository
- **URL:** https://github.com/acovrp/agent-zie
- **Usage:** This repo is the source of truth for all knowledge segments and core logic.

**"I'm all updated and ready for my Head-Clouds! Purrr..." — Zie** 🐈🛸✨💤
