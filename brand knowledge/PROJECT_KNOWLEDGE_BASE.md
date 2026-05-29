# 🐈 SleepyCat SEO Platform: 360° Knowledge Base (v6.2)

## 1. Project Mission
To transform SleepyCat’s content strategy from "AI-assisted drafting" to a "Data-Driven, Multi-Agent SEO Factory." The platform generates 1000-1500 word AEO-optimized blog posts grounded in real-time competitor data and verified product specs (E-E-A-T).

---

## 2. Technical Architecture: The 5-Agent Pipeline
The system utilizes a sequential hand-off model:

1.  **🕵️ The SERP Spy (Agent 1):** Scrapes top 3 Google results + 150-char paragraph previews.
2.  **🐈 The Brand Strategist (Agent 2):** Produces a structured 6-section brief (Angle, Gaps, Tone, Product Pushes).
3.  **🧪 The Lab Tester / Drafter (Agent 3):** Writes a 1500-word draft following the Brand Final Formula. (Anti-Jargon enforced).
4.  **🏗️ The SEO Architect (Agent 4):** Optimizes for AEO. Adds 40-50 word bold snippets, comparison tables, and internal links. **Does not shorten.**
5.  **✍️ The Senior Editor / Humanizer (Agent 5):** Final pass for brand soul. Preserves all AEO/SEO structures.

---

## 3. Key Enterprise Features (v6.2)
-   **Knowledge Vault:** Auto-archives every generation to `/outputs/`.
-   **Cloud Sync:** Admin-controlled button to push all local archival data to GitHub (100GB permanent storage).
-   **RLHF Two-Field Memory:** History tab lets users submit what was good (→ positive memory) and what was bad (→ negative memory). Both injected into all 5 agents on next run.
-   **Enterprise Security:** Domain-locked Google OAuth v2 (`@sleepycat.in`).
-   **Model-Agnostic Routing:** Supports Claude 4.x, Gemini 2.5, GPT-4o, and Kimi.
-   **Company Defaulting:** Prioritizes `COMPANY_CLAUDE_KEY` from secrets with session-based user fallback.

---

## 4. File Map & Environment
- `brand_guidelines.txt`: Core brand DNA.
- `sleepycat-products.json`: Verified spec source for 69 products (Production DB).
- `sleepycat-tech-glossary.md`: Proprietary tech definitions.
- `sleepycat-context.md`: High-level history and strategy deep-dive.
- `humanizer_rules.txt`: Voice/Tone constraints for the final pass.
- `outputs/`: Folder for auto-archived markdown files.


---

## 5. Deployment Specs
-   **URL:** `https://sleepycat-seo1.streamlit.app/`
-   **Passcode:** `SleepyCat2026` (Admin Tab)
-   **Repository:** `acovrp/sleepycat-seo-platform`

---

## 6. Agent Prompt Specifications (v5.9 Claude Suggestions)

Each agent's system prompt is defined in `sleepycat_seo_agent.py`. This section documents the intended behaviour so future edits don't regress content quality.

### Agent 1 — SERP Spy
- Scrapes **3 URLs**, 3s timeout
- Extracts: H2/H3 headings (up to 6) + first 2 paragraph previews (150 chars each)
- Output: raw competitor structure passed to Strategist

### Agent 2 — Brand Strategist
- Produces a **structured strategy brief** with 6 sections: Article Angle, Target Reader, H2 Structure (5-6 headings), Key Product Pushes, Content Gaps, Tone Note
- Has full brand DNA + product DB in system prompt
- Temperature: 0.7 (creative angles needed)

### Agent 3 — Lab Tester / Drafter
- Writes **1000-1500 word full draft** following the Brand Final Formula
- Formula: Hook → 4-5 H2 sections → "Why SleepyCat?" section → CTA closing
- Anti-jargon enforced: no feel/materials/support — use feel/materials/support
- Temperature: 0.4 (factual but natural)
- Uses only verified specs from product_catalog.json

### Agent 4 — SEO Architect
- **Does NOT shorten the article** — common regression point
- Adds 40-50 word AEO snippet immediately after H1 (bold, direct answer)
- Adds/improves comparison table with: Mattress | Technology | Key Benefit | Firmness | Best For | Link
- Adds internal links: Ultima/Original/Ortho → sleepycat.in/products/{name}
- Temperature: 0.1 (precise, structural)

### Agent 5 — Senior Editor / Humanizer
- Receives full humanizer_rules.txt content as system prompt
- Must preserve ALL content — tables, links, AEO snippet, length (1000+ words)
- Temperature: 0.5

---

## 7. Changelog

| Version | Date | Change |
|---------|------|--------|
| v6.2 | May 2026 | **(Claude) RLHF Two-Field Memory.** `agent_memory.json` now stores `type: positive/negative`. History tab replaced with two-field feedback form. All 5 agents inject both "WHAT WORKED WELL" and "PAST FEEDBACK TO AVOID". Fixed product DB regression (reverted to `product_catalog.json`). Fixed Claude model names (`claude-sonnet-4-6`). |
| v6.1.1 | May 2026 | **Unified Aligned Busupport.** Merged Claude's v5.9 deep-content prompts. Restored Enterprise Cloud Sync, Knowledge Vault, and Admin controls. |
| v5.9 | May 2026 | (Claude Suggestion) Rewrote all 5 agent system prompts. Strategist now produces structured brief. Drafter outputs 1000-1500 words using Brand Final Formula. SEO Architect no longer shortens content — adds AEO snippet at top instead. |
| v5.8 | May 2026 | (Gemini CLI) Ultra-Performance overhaul. Reduced generation time to <2 mins. |
| v5.0 | May 2026 | Google OAuth, Streamlit Cloud hosting, @sleepycat.in domain restriction |

---
*Unified v6.2 Busupport - May 2026*
