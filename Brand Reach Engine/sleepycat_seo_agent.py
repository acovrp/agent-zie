import os
import csv
import json
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from google import genai
from google.genai import types

# ==========================================
# SleepyCat True Multi-Agent E-E-A-T System
# (Wired to Local Data Feeds)
# Requirements: pip install google-genai beautifulsoup4 requests googlesearch-python
# ==========================================

CONTEXT_DIR = "context_files"

def read_file_safe(filename, default_text=""):
    filepath = os.path.join(CONTEXT_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return content if content else default_text
    return default_text

class BaseAgent:
    """Base class for all specialized agents."""
    def __init__(self, name, role_description):
        self.name = name
        self.role_description = role_description
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set. Run: setx GEMINI_API_KEY 'your_key'")
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-pro"
        
        self.config = types.GenerateContentConfig(
            system_instruction=self.role_description,
            temperature=0.7
        )

    def execute_task(self, prompt_context):
        print(f"\n[Agent: {self.name}] Executing task...")
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt_context,
            config=self.config
        )
        return response.text


class SERPScraperAgent:
    """Agent 1: Competition Analysis (Using free googlesearch-python)"""
    def __init__(self):
        self.name = "The SERP Spy"
        
    def execute_task(self, keyword):
        print(f"\n[Agent: {self.name}] Scraping Google for: '{keyword}'...")
        scraped_data = []
        try:
            # Search Google and get top 3 URLs
            for url in search(keyword, num_results=3, lang="en", region="in"):
                print(f"  -> Scraping: {url}")
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    res = requests.get(url, headers=headers, timeout=5)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    headings = [h.text.strip() for h in soup.find_all(['h2', 'h3'])[:5]]
                    scraped_data.append(f"URL: {url}\nHeadings: {', '.join(headings)}")
                except Exception as e:
                    scraped_data.append(f"URL: {url} - Failed to scrape: {e}")
        except Exception as e:
            return f"Failed to search Google: {e}. Fallback to generic competitor assumptions."
            
        return "\n".join(scraped_data)

class BrandStrategistAgent(BaseAgent):
    """Agent 2: Brand DNA Injector"""
    def __init__(self):
        brand_dna = read_file_safe("brand_guidelines.txt", default_text="SleepyCat relies on AirGen foam, Orthopedic support, and direct-to-consumer pricing.")
        super().__init__(
            name="The Brand Strategist",
            role_description=(
                "You are the SleepyCat Brand Strategist. Your job is to take raw competitor data "
                f"and map it against SleepyCat's Brand DNA:\n{brand_dna}\n"
                "Output a concise 'Strategy Brief' outlining exactly how we will beat the competitors "
                "on this specific keyword by highlighting our unique tech."
            )
        )

class ReviewerPersonaAgent(BaseAgent):
    """Agent 3: E-E-A-T Drafter"""
    def __init__(self):
        product_specs = read_file_safe("product_catalog.json", default_text="{'products': ['Original Mattress', 'Ultima Mattress']}")
        super().__init__(
            name="The Lab Tester (Drafter)",
            role_description=(
                "You are a SleepyCat Product Tester. You write from a first-person 'Reviewer Persona' "
                "based on real lab stress tests. You never use generic marketing speak. "
                f"Use this Product Catalog to pull exact specs: {product_specs}\n"
                "Your job is to draft the core content based on the Strategy Brief provided to you."
            )
        )

class SEOEditorAgent(BaseAgent):
    """Agent 4: Semantic Optimizer"""
    def __init__(self):
        lsi_keywords = read_file_safe("gsc_lsi_keywords.csv", default_text="spinal alignment, breathability, edge support")
        super().__init__(
            name="The SEO Architect",
            role_description=(
                "You are a Technical SEO Editor. Your job is to take a draft and cross-reference it "
                "with high-value LSI keywords pulled from Google Search Console. "
                f"You must seamlessly weave in terms from this list: {lsi_keywords}. "
                "Do not change the core meaning, just optimize the vocabulary."
            )
        )

class HumanizerAgent(BaseAgent):
    """Agent 5: Anti-AI Scrubbing"""
    def __init__(self):
        humanizer_rules = read_file_safe("humanizer_rules.txt", default_text="Remove 'In today's fast paced world'. Be witty, relatable, and human.")
        super().__init__(
            name="The Senior Editor (Humanizer)",
            role_description=(
                "You are the final Senior Editor for the SleepyCat blog. Your job is to make text sound 100% human. "
                f"Follow these strict editorial rules: {humanizer_rules}\n"
                "Add sentence variance. Ensure the tone is relatable, highly expert, and slightly edgy. "
                "Output the final markdown, ready to publish."
            )
        )


class Orchestrator:
    """Manages the hand-offs between the 5 distinct agents."""
    def __init__(self):
        self.serp_agent = SERPScraperAgent()
        self.strategist = BrandStrategistAgent()
        self.drafter = ReviewerPersonaAgent()
        self.seo_editor = SEOEditorAgent()
        self.humanizer = HumanizerAgent()

    def run(self, keyword):
        print(f"\n🚀 Starting Orchestrator Pipeline for keyword: '{keyword}'")
        
        # Step 1: Scrape
        serp_data = self.serp_agent.execute_task(keyword)
        
        # Step 2: Strategize
        brief_prompt = f"Target Keyword: {keyword}\nCompetitor Data:\n{serp_data}"
        strategy_brief = self.strategist.execute_task(brief_prompt)
        
        # Step 3: Draft
        draft_prompt = f"Target Keyword: {keyword}\nFollow this Strategy Brief closely:\n{strategy_brief}\nWrite a 600-word draft."
        draft = self.drafter.execute_task(draft_prompt)
        
        # Step 4: Optimize
        optimize_prompt = f"Optimize this draft with LSI keywords:\n\n{draft}"
        optimized_draft = self.seo_editor.execute_task(optimize_prompt)
        
        # Step 5: Humanize
        humanize_prompt = f"Perform a final humanizer pass on this optimized draft:\n\n{optimized_draft}"
        final_content = self.humanizer.execute_task(humanize_prompt)
        
        print("\n==========================================")
        print("✨ MULTI-AGENT WORKFLOW COMPLETE ✨")
        print("==========================================\n")
        print(final_content)
        
        # Save output
        filename = f"{keyword.replace(' ', '_')}_final.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"\n[+] Saved to {filename}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target = " ".join(sys.argv[1:])
    else:
        target = input("Enter target SEO keyword (e.g., 'Best mattress brand in India'): ")
    orchestrator = Orchestrator()
    orchestrator.run(target)
