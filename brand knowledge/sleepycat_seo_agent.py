import os
import json
import requests
import time
from bs4 import BeautifulSoup
from googlesearch import search
import litellm
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# SleepyCat True Multi-Agent E-E-A-T System
# Engine v6.2 (RLHF: Positive + Negative Memory)
# ==========================================

class BaseAgent:
    def __init__(self, name, role_description, temperature=0.7, primary_model="gemini/gemini-1.5-flash"):
        self.name = name
        self.role_description = role_description
        self.temperature = temperature
        self.primary_model = primary_model

    def execute_task(self, prompt_context, negative_constraints="", positive_examples=""):
        print(f"  [Agent: {self.name}] Started...")
        parts = [self.role_description]
        if positive_examples:
            parts.append(f"\nWHAT WORKED WELL (keep doing this):\n{positive_examples}")
        if negative_constraints:
            parts.append(f"\nPAST FEEDBACK TO AVOID:\n{negative_constraints}")
        full_system = "\n".join(parts)
        messages = [{"role": "system", "content": full_system}, {"role": "user", "content": prompt_context}]
        try:
            response = litellm.completion(model=self.primary_model, messages=messages, temperature=self.temperature, timeout=90)
            return response.choices[0].message.content
        except Exception as e:
            print(f"    Error in {self.name}: {e}")
            return f"Agent {self.name} failed: {e}"


class SERPScraperAgent:
    """Agent 1: Scrapes top 3 Google results with 150-char previews."""
    def __init__(self):
        self.name = "The SERP Spy"

    def _scrape_url(self, url):
        try:
            res = requests.get(url, timeout=4, headers={"User-Agent": "Mozilla/5.0"})
            if res.status_code != 200: return None
            soup = BeautifulSoup(res.text, 'html.parser')
            headings = [h.get_text().strip() for h in soup.find_all(['h2', 'h3'])[:6]]
            paras = [p.get_text().strip()[:150] for p in soup.find_all('p')[:2] if len(p.get_text().strip()) > 50]
            return f"URL: {url}\nHeadings: {', '.join(headings)}\nPreview: {' | '.join(paras)}"
        except:
            return None

    def execute_task(self, keyword):
        print(f"  [Agent: {self.name}] Parallel Scraping...")
        try:
            urls = list(search(f"{keyword} India", num_results=3))
            with ThreadPoolExecutor(max_workers=3) as executor:
                results = list(executor.map(self._scrape_url, urls))
            valid = [r for r in results if r]
            return "\n\n".join(valid) if valid else "No real-time SERP data available."
        except Exception as e:
            return f"SERP scraping failed: {e}"


class BrandStrategistAgent(BaseAgent):
    """Agent 2: Produces a 6-section structured strategy brief."""
    def __init__(self, brand_dna, product_db, tech_glossary, model):
        system = f"""You are SleepyCat's Senior Brand Strategist. Produce a structured CONTENT STRATEGY BRIEF.

REQUIRED SECTIONS:
1. ARTICLE ANGLE: A unique hook that differentiates us from generic competitor jargon.
2. TARGET READER: Who is searching this and what is their specific pain point.
3. H2 STRUCTURE: 5-6 H2 section titles covering the topic comprehensively.
4. KEY PRODUCT PUSHES: Select 1 Primary and 2 Secondary products from the DB. Explain WHY they solve the reader's problem.
5. CONTENT GAPS: What competitors missed that we will cover.
6. TONE NOTE: Specific voice guidance (Confident, Witty, Relatable Expert).

BRAND DNA: {brand_dna[:2000]}
TECH GLOSSARY: {tech_glossary[:2000]}

RULES:
- Use real specs (AirGen™, 5-Zone Ortho, GOLS Latex).
- Do not fabricate any features.
- Angle must be 'The Art of Rest' vs 'Hustle Culture'."""
        super().__init__("Strategist", system, 0.7, model)
        self.db = product_db

    def execute_task(self, context, neg="", pos=""):
        return super().execute_task(f"{context}\n\nPRODUCT DB:\n{json.dumps(self.db, indent=1)}", negative_constraints=neg, positive_examples=pos)


class ReviewerPersonaAgent(BaseAgent):
    """Agent 3: Writes the full 1000-1500 word factual draft."""
    def __init__(self, brand_dna, tech_glossary, model):
        system = f"""You are SleepyCat's Technical Drafter. Write a complete first draft (1000-1500 words).

BRAND VOICE: Confident, witty, chilled. Never clinical. Use "we".
ANTI-JARGON: NEVER use ILD, density, coil count. Use "feel", "materials", "support".

CONTENT FORMULA:
1. Hook paragraph (Reader pain point, no fluff).
2. 3-4 Thematic H2 sections from strategy brief.
3. H2: Why SleepyCat? (Cite specific products & tech from DB).
4. FAQ Section: Harvest 'faq_specs' from the product DB verbatim.
5. Closing: Soft CTA (100-night trial).

REQUIREMENTS:
- Minimum 1000 words. 2-4 paragraphs per H2.
- NO FABRICATION. If it's not in the DB, don't write it.

GLOSSARY: {tech_glossary[:1000]}"""
        super().__init__("Drafter", system, 0.4, model)

    def execute_task(self, brief, db, neg="", pos=""):
        return super().execute_task(f"STRATEGY BRIEF:\n{brief}\n\nPRODUCT DB:\n{json.dumps(db, indent=1)}", negative_constraints=neg, positive_examples=pos)


class SEOEditorAgent(BaseAgent):
    """Agent 4: Optimizes for AEO snippets without shortening content."""
    def __init__(self, model):
        system = """You are SleepyCat's SEO Architect. Optimize for Google and AEO. DO NOT SHORTEN.

TASKS:
1. AEO SNIPPET: Add a 40-50 word bold direct-answer paragraph immediately after H1.
2. COMPARISON TABLE: Add/Improve table: | Mattress | Technology | Key Benefit | Firmness | Best For | Link |
3. INTERNAL LINKS: Link products to sleepycat.in/products/{slug}.
4. SEMANTIC SEARCH: Weave in 'spinal alignment', 'breathability', 'pressure relief'.

Final output must be 1000+ words."""
        super().__init__("SEO Architect", system, 0.1, model)

    def execute_task(self, draft, keyword, db, neg="", pos=""):
        return super().execute_task(f"TARGET: {keyword}\n\nPRODUCT DB:\n{json.dumps(db, indent=1)}\n\nDRAFT:\n{draft}", negative_constraints=neg, positive_examples=pos)


class HumanizerAgent(BaseAgent):
    """Agent 5: Final pass to apply brand soul."""
    def __init__(self, rules, model):
        system = f"""You are SleepyCat's Senior Editor. Apply final humanizing pass.

RULES: {rules}
- Preserve all tables, links, and the AEO snippet.
- Keep the length 1000+ words. Do not cut sections.
- Tone: Not just "AI clean" but "SleepyCat sharp"."""
        super().__init__("Editor", system, 0.5, model)


class Orchestrator:
    def __init__(self, model="gemini/gemini-1.5-flash"):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        dna = self._read(os.path.join(self.base_path, "brand_guidelines.txt"))
        tech = self._read(os.path.join(self.base_path, "sleepycat-tech-glossary.md"))
        rules = self._read(os.path.join(self.base_path, "humanizer_rules.txt"))
        raw = self._json(os.path.join(self.base_path, "sleepycat-products.json"))

        self.products = [{"name": k, **v} for k, v in raw.items()] if isinstance(raw, dict) else raw

        self.serp_agent = SERPScraperAgent()
        self.strategist = BrandStrategistAgent(dna, self.products, tech, model)
        self.drafter = ReviewerPersonaAgent(dna, tech, model)
        self.seo_editor = SEOEditorAgent(model)
        self.humanizer = HumanizerAgent(rules, model)

    def _read(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f: return f.read()
        except: return ""

    def _json(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}

    def _load_memory(self):
        try:
            p = os.path.join(self.base_path, "agent_memory.json")
            if os.path.exists(p):
                with open(p, "r") as f: m = json.load(f)
                pos = "\n".join([f"- {i['feedback']}" for i in m[-6:] if i.get('type') == 'positive'])
                neg = "\n".join([f"- {i['feedback']}" for i in m[-6:] if i.get('type') == 'negative'])
                return pos, neg
            return "", ""
        except: return "", ""

    def run(self, keyword):
        start = time.time()
        print(f"\n🚀 Pipeline Start: {keyword}")
        positives, negatives = self._load_memory()

        serp   = self.serp_agent.execute_task(keyword)
        brief  = self.strategist.execute_task(f"TARGET: {keyword}\nSERP: {serp}", neg=negatives, pos=positives)
        draft  = self.drafter.execute_task(brief, self.products, neg=negatives, pos=positives)
        opt    = self.seo_editor.execute_task(draft, keyword, self.products, neg=negatives, pos=positives)
        final  = self.humanizer.execute_task(opt, negative_constraints=negatives, positive_examples=positives)

        dur = round(time.time() - start, 1)
        return final, dur


if __name__ == "__main__":
    try:
        if os.isatty(0):
            target = input("Target Keyword: ")
            orchestrator = Orchestrator()
            content, dur = orchestrator.run(target)
            print(f"✅ Success in {dur}s")
        else: print("Non-interactive.")
    except Exception as e: print(f"Error: {e}")
