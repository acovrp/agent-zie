# Paste this into your Claude Code session to restart the crawl cleanly

---

You botched the first crawl attempt by going parallel + raw markdown. Reset and restart with this protocol — read `NEXT-SESSION-BRIEF.md` "Lessons learned" section first.

## Protocol (strict)

1. **One URL at a time, sequentially.** Wait for each `mcp__firecrawl__firecrawl_scrape` call to return AND for me to approve the next permission prompt before starting the next URL.

2. **Use `extract` format with this schema** (NOT raw markdown):

```json
{
  "formats": [{
    "type": "json",
    "schema": {
      "type": "object",
      "properties": {
        "product_name": {"type": "string"},
        "category": {"type": "string"},
        "sub_category": {"type": "string"},
        "description_short": {"type": "string"},
        "construction_layers": {
          "type": "array",
          "description": "Top-to-bottom layers of the product",
          "items": {
            "type": "object",
            "properties": {
              "position": {"type": "integer"},
              "name": {"type": "string"},
              "material": {"type": "string"},
              "foam_type": {"type": "string"},
              "thickness_mm": {"type": "number"},
              "thickness_inches": {"type": "number"},
              "density_kgm3": {"type": "number"},
              "ild": {"type": "number"},
              "gsm": {"type": "number"},
              "notes": {"type": "string"}
            }
          }
        },
        "cover_fabric": {
          "type": "object",
          "properties": {
            "composition": {"type": "string"},
            "weave": {"type": "string"},
            "gsm": {"type": "number"},
            "removable": {"type": "boolean"},
            "washable": {"type": "boolean"},
            "wash_instructions": {"type": "string"}
          }
        },
        "dimensions_by_size": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "size_name": {"type": "string"},
              "length_mm": {"type": "number"},
              "width_mm": {"type": "number"},
              "height_mm": {"type": "number"},
              "weight_kg": {"type": "number"}
            }
          }
        },
        "firmness": {
          "type": "object",
          "properties": {
            "rating_1_10": {"type": "number"},
            "label": {"type": "string"},
            "feel_descriptors": {"type": "array", "items": {"type": "string"}}
          }
        },
        "proprietary_tech": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "description": {"type": "string"}
            }
          }
        },
        "certifications": {"type": "array", "items": {"type": "string"}},
        "trial_warranty": {
          "type": "object",
          "properties": {
            "trial_nights": {"type": "number"},
            "warranty_years": {"type": "number"},
            "weight_capacity_kg": {"type": "number"}
          }
        },
        "pricing": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "size_name": {"type": "string"},
              "mrp": {"type": "number"},
              "selling_price": {"type": "number"},
              "currency": {"type": "string"}
            }
          }
        },
        "faq_specs": {
          "type": "array",
          "description": "Spec-relevant FAQ Q&A pairs",
          "items": {
            "type": "object",
            "properties": {
              "question": {"type": "string"},
              "answer": {"type": "string"}
            }
          }
        }
      }
    }
  }],
  "onlyMainContent": true
}
```

3. **Save to disk immediately.** After each scrape returns, write the result to `C:\Users\Aayushi\sleepycat-brand\raw\<slug>.json`. Then drop the data from working memory before the next URL.

4. **Batches.** Process in this order, save progress after each batch:
   - Batch 1: Mattresses (10) — IDs 1-10 in url-inventory.md
   - Batch 2: Pillows (13)
   - Batch 3: Toppers & Protectors (8)
   - Batch 4: Bedding (17)
   - Batch 5: Ergo/Support (11)
   - Batch 6: Dog Beds (4) + Furniture (5)

5. **After ALL batches done**, build the final two outputs:
   - `sleepycat-context.md` — structured per category, human/LLM readable
   - `sleepycat-products.json` — single JSON array of all 71 products

6. **First, before doing anything else**, salvage the latex-mattress data from the tool-results temp file (Batch 1 product 1) and save it to `raw\latex-mattress.json`. Don't re-scrape it.

## Confirm before starting
Reply with:
- Number of products you're about to scrape (should be 70, since latex-mattress is already done)
- Confirmation you'll go one-at-a-time, schema-based extract, save-to-disk-each
- The first URL you'll hit

Then wait for me to say "go".
