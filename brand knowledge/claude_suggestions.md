# Claude Suggestions & Audit Log

> Running log maintained by Claude across sessions.
> Documents: audit findings, backlog items, architectural notes for future continuity.

---

## Session: 2026-05-19 — Full Platform Audit + RLHF Build

### Bugs Found & Fixed

| # | Bug | Root Cause | Fix |
|---|-----|-----------|-----|
| 1 | Google OAuth 403 (no popup) | Streamlit DOMPurify strips onclick from `st.markdown`; user-gesture context lost in server round-trip | Used `st.link_button()` — only native Streamlit component that navigates externally |
| 2 | Company Claude not-found error | `claude-3-5-sonnet-20241022` not on company Anthropic account | Changed MODEL_MAP to `claude-sonnet-4-6` / `claude-opus-4-7` |
| 3 | Generic/short content output | SEOEditorAgent prompt said "40-50 word AEO snippet" — LLM interpreted this as target length for entire output | Rewrote all 5 agent system prompts (v5.9). Added explicit 1000-word minimum, content formula, DO NOT SHORTEN instruction |
| 4 | Wrong product file (v6.1.1 regression) | Gemini changed Orchestrator to load `sleepycat-products.json` which doesn't exist on disk | Reverted to `product_catalog.json` with dict-to-list parsing |
| 5 | RLHF memory has no type field | Admin "Update Agent Memory" wrote `{timestamp, feedback}` — no `type` field, so all entries treated as negatives | Added `type: "positive"/"negative"` to all memory writes |
| 6 | RLHF UI only supported single rejection path | History tab had "Accept / Reject" with one text area — no way to record what was good | Replaced with two-field form: "What was good?" -> positive memory, "What was bad?" -> negative memory |

---

### Architecture Notes

**Why double pipeline execution in `run_pipeline` is kept:**
`app.py` calls agents 1-5 individually for UI progress display, then calls `engine.run()` which runs them all again. User confirmed this is intentional — the extra token cost is worth the output quality. The displayed progress steps are cosmetic; the `final` variable from `engine.run()` is what actually gets saved.

**Memory injection flow (v6.2):**
```
agent_memory.json -> _load_memory() -> (positives, negatives) tuple
-> Orchestrator.run() -> all 5 agents receive:
    "WHAT WORKED WELL (keep doing this): ..." [positives]
    "PAST FEEDBACK TO AVOID: ..." [negatives]
```
Last 6 entries per type are injected (up to 6 positive + 6 negative window).

**Product catalog:**
`product_catalog.json` is the live source — 3 mattresses (Ultima, Original, Ortho). Knowledge base mentions "69 products" — this refers to a larger `sleepycat-products.json` that Gemini referenced but which doesn't exist in the repo. If that file is added later, Orchestrator will need to be updated.

**Model IDs for company Anthropic account:**
- `anthropic/claude-sonnet-4-6` works
- `anthropic/claude-opus-4-7` works
- `anthropic/claude-3-5-sonnet-latest` fails (not-found on this account)
- `anthropic/claude-3-5-sonnet-20241022` fails

---

### Backlog / Future Suggestions

- **Memory curation UI:** Show `agent_memory.json` entries in Admin tab with delete button — no way to remove bad memories once added
- **Per-agent memory routing:** Inject feedback only into the relevant agent (e.g. tone feedback -> Humanizer only, structure feedback -> Strategist only)
- **Memory count tuning:** Currently last 6 entries per type. Consider separate caps: 3 positive + 3 negative = 6 total per generation
- **SERP timeout increase:** Currently 4s — Indian news/ecom domains can be slow. Consider 6s
- **Kimi key injection:** `run_pipeline` in app.py doesn't set `MOONSHOT_API_KEY` env var. Add: `if st.session_state.get("KIMI_KEY"): os.environ["MOONSHOT_API_KEY"] = st.session_state["KIMI_KEY"]`
- **History content size:** `generation_history.json` stores full article content per entry — will grow large. Consider storing only first 500 chars + vault filename reference
- **Feedback on approved articles:** No path to give positive feedback after approving. Could add a "Leave a note" option post-approval

---

*Last updated: 2026-05-19 by Claude (claude-sonnet-4-6)*
