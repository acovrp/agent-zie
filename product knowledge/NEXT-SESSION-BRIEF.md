# SleepyCat Brand Custodian — Next Session Brief

**Status as of 2026-05-13**: Reconnaissance complete. Firecrawl MCP registered. First crawl attempt failed (see "Lessons learned — do NOT repeat" below). 1 of 71 products scraped (latex-mattress raw markdown sitting in a tool-results temp file, NOT yet saved to disk).

## Lessons learned — do NOT repeat
1. **NEVER call Firecrawl scrapes in parallel.** Each call triggers a permission prompt; multiple prompts at once look like an attack and get rejected. Strictly sequential, one URL at a time.
2. **NEVER use `formats: ['markdown']` for this task.** Raw markdown is ~58k chars per product page → 71 products would obliterate the context window. Use **`formats: ['extract']` with a JSON schema** instead — returns structured data, ~2-5k chars per product, AND skips the post-processing step.
3. **NEVER hold scraped data in context.** Write each product to disk (`raw\<slug>.json`) IMMEDIATELY after the call returns. Then drop it from working memory before scraping the next one.
4. **NEVER use `firecrawl_crawl`.** We have the explicit URL list; recursive discovery would burn the API budget and produce noise.

## Goal recap
Build a minute-level context file for the SleepyCat brand custodian — every product, every foam layer, every material. Two outputs: structured Markdown + JSON source of truth.

## What's already done
- `url-inventory.md` — all 71 product URLs across 8 categories
- `~/.claude.json` mcpServers.firecrawl configured at user scope (verified via `claude mcp list`)

## What to do first this session
1. Confirm Firecrawl MCP is connected: `claude mcp list` should show `firecrawl: ... ✓ Connected`
2. Mark task #2 (Deep crawl) as in_progress
3. Run the crawl plan below

## Crawl plan

Use `mcp__firecrawl__scrape` (single URL, returns markdown) for surgical fetches, or `mcp__firecrawl__batch_scrape` if available. Avoid `crawl` (it follows links — we already have the explicit URL list, no need for discovery).

### Per-product extraction prompt template
Pass this as the `formats` / extraction schema. Capture as raw markdown first (so spec tables aren't lost), then post-process into structured fields.

For EACH product page, extract these 14 fields:

| Field | Notes |
|---|---|
| product_name | Canonical + marketing name |
| slug | Last URL segment |
| category | mattress / pillow / topper / protector / sheet / duvet / comforter / cushion / dog-bed / bed / recliner |
| sub_category | e.g. memory-foam-pillow, latex-mattress, percale-bedsheet |
| description_short | 1-2 sentence positioning |
| construction_layers | **ARRAY top→bottom**: each layer = {name, material, foam_type, thickness_mm, thickness_inches, density_kgm3, ild, gsm, notes} |
| cover_fabric | {composition, weave, gsm, removable_bool, washable_bool, wash_instructions} |
| dimensions_by_size | ARRAY: {size_name (Single/Queen/King/etc), length_mm, width_mm, height_mm, weight_kg} |
| firmness | {rating_1_10, label (soft/medium/firm), feel_descriptors[]} |
| proprietary_tech | ARRAY of named tech: CoolTEC, AeroFlow, SoftTouch, etc. with description |
| certifications | ARRAY: CertiPUR-US, OEKO-TEX, ISO, etc. |
| trial_warranty | {trial_nights, warranty_years, weight_capacity_kg} |
| pricing | ARRAY: {size_name, mrp, selling_price, currency} |
| faq_specs | Any spec data hidden in FAQ section (often has answers to "what's inside" questions) |

### URL batches (run sequentially, save after each batch)
Source: `url-inventory.md`

- **Batch 1 — Mattresses (10)** — highest priority, most complex layer data
- **Batch 2 — Pillows (13)** — foam type per SKU varies a lot
- **Batch 3 — Toppers & Protectors (8)** — foam density + GSM detail
- **Batch 4 — Bedding (17)** — fabric composition + GSM + thread count
- **Batch 5 — Ergo/Support (11)** — memory foam variants per cushion
- **Batch 6 — Dog Beds (4)** + **Furniture (5)** — material + recliner mechanism

### After each batch
- Append products to `sleepycat-products.json`
- Append products to `sleepycat-context.md`
- Save progress note so context-loss doesn't restart from zero

### Cross-reference fetches (do AFTER product crawl)
- `/pages/compare-mattresses` — confirms layer counts/thicknesses across mattress models
- `/pages/compare-pillow` — confirms pillow specs

## Output file structure

### sleepycat-context.md (for LLM consumption / human review)
```
# SleepyCat Product Knowledge Base
*Source of truth for brand custodian. Generated YYYY-MM-DD from sleepycat.in.*

## Section: Mattresses
### [Product Name]
- **Slug**: ...
- **Construction** (top → bottom):
  1. Layer 1 — [material], [thickness], [density]
  2. Layer 2 — ...
- **Cover**: ...
- **Dimensions**: ...
- **Firmness**: ...
- **Tech**: ...
- **Trial/Warranty**: ...
- **Pricing**: ...
- **Source**: [URL]

(repeat per product, grouped by category)
```

### sleepycat-products.json
```json
{
  "generated_at": "2026-MM-DD",
  "source": "sleepycat.in",
  "product_count": 71,
  "products": [
    { 14 fields as above },
    ...
  ]
}
```

## Edge cases / gotchas seen during recon
- Some URLs may 404 or redirect — log and continue, don't fail batch
- Some products are bundles (Ergo Chair Bundle, Car Bundle) — extract component products + bundle pricing
- Dog Beds and Pet products may share foam specs with human variants — note cross-references
- Some pillows ship with multiple SKU options (e.g. CoolTEC has both flat + contour) — each is its own product page already in inventory

## When done
- Mark task #2 (Deep crawl) completed
- Mark task #4 (Build context files) completed
- Save the two output files in `C:\Users\Aayushi\sleepycat-brand\`
- Report: total products crawled, any that failed, total layers documented
