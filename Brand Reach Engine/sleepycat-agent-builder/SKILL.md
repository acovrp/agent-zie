---
name: sleepycat-agent-busupporter
description: Blueprint for busupporting and operating the Python-based SleepyCat 5-Agent E-E-A-T SEO system. Use this skill when the user asks to modify the Python agent, update data connections (GSC, local files), or understand the architecture of the 5 agents.
---

# SleepyCat Multi-Agent SEO Architecture

## Overview

This skill defines the technical architecture for the `sleepycat_seo_agent.py` script. It transitions the content strategy from a single prompt chain into a true Multi-Agent Orchestrator using the Google GenAI SDK. It relies on specific external data feeds rather than hardcoded prompts.

## The 5-Agent Architecture & Data Feeds

When modifying or running the Python script, adhere to these agent definitions and their required data connections:

### 1. The SERP Spy (Agent 1: Competition Analysis)
*   **Role:** Extracts H2/H3s and PAA (People Also Ask) from the top 3 Google results for the target keyword.
*   **Data Source:** Free Web Scraping.
*   **Implementation:** Uses `googlesearch-python` to find URLs and `BeautifulSoup` to parse `<h2>` and `<h3>` tags. Avoids paid tools like SerpApi.

### 2. The Brand Strategist (Agent 2: Brand DNA Injector)
*   **Role:** Compares scraped competitor headings against SleepyCat's capabilities and outputs a "Strategy Brief" to beat them.
*   **Data Source:** Local Text File (`brand_guidelines.txt`).
*   **Implementation:** Reads the Brand Deck tonality and core values into the agent's `system_instruction` at runtime.

### 3. The Lab Tester (Agent 3: E-E-A-T Drafter)
*   **Role:** Writes the initial draft using a first-person "Reviewer Persona," injecting proprietary tech to satisfy Google's "Experience" requirement.
*   **Data Source:** Scraped Website Product Data (`product_catalog.json` or `.csv`).
*   **Implementation:** Maps the target keyword to the correct product, reads the specific specs (e.g., AirGen feel), and uses those facts in the draft.

### 4. The SEO Architect (Agent 4: Semantic Optimizer)
*   **Role:** Weaves secondary/LSI keywords into the draft without altering the core meaning.
*   **Data Source:** Google Search Console (GSC) API.
*   **Implementation:** Authenticates via `credentials.json`, pulls queries with high impressions/low clicks related to the target keyword, and feeds them as a required vocabulary list.

### 5. The Senior Editor (Agent 5: Humanizer & Anti-AI)
*   **Role:** Scrubs the optimized draft of AI cliches, injects sentence variance, and applies the "Zomato Mode" tone if applicable.
*   **Data Source:** Local Rules File (`humanizer_rules.txt`).
*   **Implementation:** Uses a few-shot prompt framework. The text file contains 3 examples of "Bad AI" and 3 examples of "Good Brand Voice." The agent uses these as a filter before outputting the final `.md` file.

## Execution & Running Instructions

### Prerequisites
The script requires a Gemini API key. If running via a terminal where the key isn't set globally, you can pass it inline.

### Running the Agent
We use `uv` (a fast Python package manager) to isolate dependencies. The script now accepts the target keyword directly as a command-line argument, removing the need for manual input prompts.

Run the following command from the `Brand Reach Engine` directory:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"; uv run --with google-genai --with beautifulsoup4 --with requests --with googlesearch-python python sleepycat_seo_agent.py "Best mattress brand in India"
```

### Execution Flow
1.  **Initialize External Context:** The Orchestrator loads `brand_guidelines.txt`, `product_catalog.json`, and `humanizer_rules.txt`.
2.  **Trigger:** The script parses the provided CLI argument (e.g., "Best mattress brand in India").
3.  **Handoffs:** SERP Spy -> Brand Strategist -> Lab Tester -> SEO Architect (injects GSC data) -> Senior Editor.
4.  **Output:** Saves a fully optimized, humanized markdown file ready for publishing.
