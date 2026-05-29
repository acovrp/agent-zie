# Claude Final — Brand Reach Engine Build Plan

> **Brand:** SleepyCat (D2C Mattress, India)
> **For:** Agentic AI builder company shipping Brand Reach Engine
> **Role of this doc:** End-to-end product spec for BRE — architecture, agent fleet, multi-LLM routing, build phasing, ownership.
> **Posture shift:** Kimi / GPT / Gemini wrote brand strategy. This doc specs the **product** that operationalizes brand strategy at scale.

---

## 1. Why This Doc Exists

Prior context in this folder:
- `kimi_context.md` — comprehensive SleepyCat brand strategy
- `gpt-strat-note/SKILL.md` — operator governance / SEO discipline
- `g-3-1pro-strat-note/SKILL.md` — content voice + Zomato Mode

All three answered the **strategy question** ("what should SleepyCat do?"). None answered the **product question** ("what is the tool that does it?"). Brand Reach Engine is the tool. This doc specs it.

---

## 2. Critique-in-Brief of Prior Docs

| Doc | Optimized for | Strongest | Critical blind spot |
|---|---|---|---|
| Kimi | Comprehensiveness | Coverage breadth, real India context | No prioritization; no diagnosis; checklist fallacy |
| GPT | Governance | Operator discipline, QA rules, dashboard pattern | Meta but never applied; no hypothesis-driven framing |
| Gemini | Voice | Brand DNA specificity, Zomato Mode is distinctive | Content-only worldview; no system thinking; soft astroturf risk |

**Cross-cutting gap all three share:** no diagnosis, no conversion-side thinking, no competitive teardown, AI Overview hand-waved, no risk stack, no single source of truth, no business model integration.

**What this doc adds:** turns the three into operating layers of a real product.

---

## 3. North Star (one line)

An agentic operating system that runs a D2C brand's discoverability as a closed loop: it **listens** (data), **decides** (priorities), **briefs** (work), **generates** (content), **publishes** (with approval), and **refreshes** (on decay) — across Google, marketplaces, social, community, and creator networks.

## 4. Defensibility Thesis

Surfer / Frase / Jasper optimize *one page*. BRE runs *one brand's whole funnel*.

> **Product truth + claims registry → cross-channel content factory, governed by role-based agents that share state.**
> One brain, ten surfaces.

The moat is the **shared Brand State** every agent reads/writes — not the LLMs (commodity) and not the dashboards (table stakes).

---

## 5. The Four Surfaces (one per persona)

### 5.1 Founder Command Center
**Who:** Founder/CEO. ≤60s/day glance.
**Wow moment:** Single Brand Visibility Index trending line + the 3 levers the system is pulling this week, with revenue attribution.
**Mode:** Watches. Does not operate.

### 5.2 Brand Manager Studio
**Who:** Owns brand love + narrative coherence.
**Wow moment:** Heatmap of *where* SleepyCat is being talked about, *how* (sentiment + theme), and *what* the system queued for each surface this week. One-click approve/edit content calendar. **Voice ratio toggle** (Reviewer / Expert / Zomato).
**Mode:** Decides direction; approves.

### 5.3 SEO Content Factory
**Who:** SEO lead / blogger.
**Wow moment:** Keyword in → publish-ready, schema'd, internally-linked draft out in <2 hours. Human becomes editor not writer.
**Mode:** Operator at every gate.

### 5.4 Creator Network Hub
**Who:** Influencer marketing manager.
**Wow moment:** Open a creator → auto-pre-filled brand-safe brief tied to a keyword/cluster gap → ROAS per creator tracked → micro vs macro decisions become data-driven.
**Mode:** Sourcer + relationship owner.

---

## 6. The Agent Fleet

| Agent | Surface(s) served | Job |
|---|---|---|
| **Research** | SEO, Brand Mgr | GSC/GA4/marketplace + SERP intel → opportunity list |
| **Strategist** | SEO, Brand Mgr | Opportunity → brief, prioritized by ROI |
| **Writer** | SEO, Brand Mgr, Creator | Drafts in target voice for target channel |
| **Optimizer** | SEO | Schema, links, on-page, pre-flight |
| **Caretaker** | SEO, Founder | Decay detection, refresh proposals |
| **Listener** | Brand Mgr, Founder | Reddit/Quora/reviews/social → sentiment + themes + urgency |
| **Brief Composer** | Creator | Per-creator briefs from cluster + claims pack |
| **Roster** | Creator | Creator CRM + micro/macro fit score + ROAS |
| **Visibility Index** | Founder | Composite BVI + weekly narrative |
| **Claims Guard** | All | Hard gate on unsupported claims |

All agents read/write a **shared Brand State** (product truth, claims registry, content inventory, performance history). That shared state is the moat.

---

## 7. The 5-Level SEO Agentic Build

| Level | Agent | Owns | Input | Output | Human in loop |
|---|---|---|---|---|---|
| **L1 Discovery** | Research | Find what to write | GSC striking-distance, PAA, competitor gap, AIO citations | Ranked opportunity list (rank-lift × effort) | Editor picks 3–5/wk |
| **L2 Brief** | Strategist | Decide how to win SERP | L1 pick + SERP teardown + product truth + claims | Brief: angle, outline, word count, schema spec, internal links, sources, evidence flags | Editor approves brief |
| **L3 Draft** | Writer | Produce body | L2 brief + voice rules (cohort pick) | Full draft + JSON-LD + meta + alt text + FAQ block | Editor edits inline |
| **L4 Optimize** | Optimizer | Pre-flight before publish | L3 draft + live-site crawl | Internal-link suggestions, cannibalization check, schema validate, CWV estimate, on-page score | Editor approves publish |
| **L5 Refresh** | Caretaker | Keep it ranking | Rank tracking, decay detection, new PAAs, new competitor entries | Refresh recommendation; low-risk diffs auto-PR with preview | Editor reviews diff |

**v1 includes all 5 levels**, applied to existing `sleepycat.in/blogs/news` from Week 4 onward.

---

## 8. Voice as a Toggleable Cohort

Brand Manager controls voice mix like an ad manager controls SP/SB/SD or branded/non-branded/competition.

```
┌─────────────────────────────────────────────────────────────────┐
│  VOICE MIX                    Last 30 days · Last 90 days       │
│                                                                  │
│  Reviewer  ████████████████░░░░░  62%   CTR 3.4%  Rank Δ +2.1   │
│  Expert    ██████░░░░░░░░░░░░░░░  24%   CTR 2.8%  Rank Δ +1.4   │
│  Zomato    ███░░░░░░░░░░░░░░░░░░  14%   Saves 11k  Brand Δ +9%  │
│                                                                  │
│  ▶ Brand Manager controls                                        │
│  [Target mix:  60 / 25 / 15 ]  ━━●━━━━━━●━━●━━━━  Apply         │
│                                                                  │
│  [+] Add cohort  ·  [↻] Re-run last week with new mix (sim)     │
└─────────────────────────────────────────────────────────────────┘
```

**Mechanics:**
- Every asset tagged `voice = {Reviewer | Expert | Zomato | ...}`.
- Every metric (CTR, rank Δ, save rate, conversion, brand search lift) computed per voice cohort and rolled up.
- Brand Mgr sets target ratio; Strategist Agent biases L1→L2 brief output to hit ratio.
- "Simulate" button: re-runs last week's briefs at the new ratio (LLM-projected) to preview impact.
- New voices add as cohorts (e.g., "Doctor-Reviewed" for back-pain content).

---

## 9. Multi-Lingual Layer (opt-in per language)

```
[ + Add Language ]   Hindi  ✓   Tamil  ✓   Marathi  ☐   Bengali  ☐
                     │
                     ├─ Translation engine:  IndicTrans2 (self-host)
                     ├─ Voice polish:        Claude Sonnet
                     ├─ Native reviewer:     [SleepyCat assigns]
                     └─ Auto-publish gate:   Manual approve (Y) / Auto (N)
```

**Why IndicTrans2:** AI4Bharat's open-source model for 22 Indian languages. Outperforms Google Translate on Indic benchmarks. Self-host on a single A10 GPU (~₹50k/month). Free per-call.

**Two-pass design:**
1. IndicTrans2 produces literal translation.
2. Claude polish re-styles for brand voice in target language.
3. SleepyCat-assigned native reviewer approves before publish (toggle to auto for low-risk content).

---

## 10. Drill-Down Design (2 levels minimum)

Pattern: every top-level KPI clicks into a tier-2 view, which clicks into a tier-3 record-level view. **Tier-3 always ends in an action button.**

**Example — Founder's "Non-branded SoV":**

| Tier | What founder sees |
|---|---|
| **L0 — Top KPI** | SoV: 34%, ▲ 2pt WoW |
| **L1 — Cluster breakdown** | Back-pain 41% ▲ · Cooling 28% ▼ · Price 38% ▲ · Local 22% ━ |
| **L2 — Page-level** | For "Cooling": each keyword × current rank × URL × competitor outranking us, with "Fix this" CTA → spawns brief in SEO Factory L1 |

Same pattern across all 4 personas. **Drill-down always ends in a button that triggers an agent or a brief.** Insights → action; no dead-end metrics.

---

## 11. Metrics System (action-anchored)

Every metric has **definition · source · frequency · owner · decision it drives · trigger threshold**.

### 11.1 Founder Command Center (top 6)

| Metric | Source | Freq | Decision | Trigger |
|---|---|---|---|---|
| Brand Visibility Index (composite) | All agents | Weekly | Hold/accelerate strategy | <5% MoM → review |
| Organic Revenue + ROAS | GA4 + Shopify | Weekly | Budget allocation | ROAS < target → rebalance |
| Non-branded SoV (Top 20 keywords) | GSC + rank tracker | Weekly | Where to push next | Drop > 3 pts → escalate |
| Branded search trend | GSC + Trends | Monthly | PR/influencer ROI | Flat 2 mo → diagnose |
| AI Overview citation rate (category) | Custom monitor | Bi-weekly | Future-proof posture | <10% by Q3 → AIO sprint |
| CAC payback days (organic) | GA4 + Shopify | Monthly | Growth sustainability | >180d → unit econ review |

### 11.2 Brand Manager Studio (top 9)

| Metric | Source | Freq | Decision |
|---|---|---|---|
| Share of conversation (SleepyCat vs competitors) | Listener | Weekly | Where to ship next narrative |
| Sentiment by channel | Listener | Weekly | Crisis vs opportunity |
| Review velocity + theme drift | Listener + Reviews API | Weekly | Product feedback loop |
| Content calendar coverage % | Brand State | Weekly | Bottleneck flag |
| UGC inflow rate | Insta/YT monitors | Weekly | Creator program tuning |
| Story-arc coherence score | Strategist | Weekly | Kill incoherent pieces |
| Top objections trending up | Listener | Weekly | Trigger objection-buster content |
| Brand love proxy (saves+shares+positive mentions) | Multi | Weekly | Voice/persona calibration |
| **Voice mix performance (per cohort)** | All | Continuous | **Toggle Brand Mgr voice dial** |

### 11.3 SEO Blogger (top 6)

| Metric | Decision |
|---|---|
| Briefs queued / in-review / approved | Throughput |
| Drafts in editor queue | Personal load |
| Time-from-keyword-to-publish | System health |
| Post-publish rank @ Day 30 | Writer Agent calibration |
| Refresh-due count | Caretaker workload |
| Cannibalization warnings open | Block before publish |

### 11.4 Influencer Marketing (top 6)

| Metric | Decision |
|---|---|
| Active creators by tier (nano/micro/macro) | Mix tuning |
| Briefs sent / received / live | Funnel health |
| ROAS per creator | Re-contract or cut |
| Earned Media Value vs paid spend | Justify program |
| Brand-safety flags open | Hold payments |
| Creator-to-cluster fit score | Targeting precision |

---

## 12. Dashboard Mockup — Founder Command Center

```
┌─────────────────────────────────────────────────────────────────┐
│  SLEEPYCAT · BRAND VISIBILITY INDEX                  Wk 19/2026 │
│  ●────────●────────●────────●───────●───────●  72 → 78  (+6)   │
│                                                                  │
│  Organic Rev   ₹48.2L   ▲ 11%   │   ROAS   4.2x   ▲ 0.3        │
│  Non-Brand SoV   34%    ▲ 2pt   │   Brand search  ▲ 14% MoM    │
│  AIO citations   18%    ▲ 4pt   │   CAC payback   142d  ▼ 8d   │
│                                                                  │
│  ▼ THIS WEEK THE SYSTEM IS                                       │
│  1. Shipping pillar "Best mattress for back pain India 2026"     │
│     (rank #6 → target #2; competitor: Wakefit /back-pain)        │
│  2. Pushing 12 Quora answers on motion-transfer (Listener flag)  │
│  3. Refreshing 4 city pages with monsoon-specific copy           │
│                                                                  │
│  ⚠  ATTENTION                                                    │
│  • Review velocity dipped 18% — check fulfilment/QA              │
│  • "sleepycat reviews" SERP gained a Reddit thread (neg) — Brand │
└─────────────────────────────────────────────────────────────────┘
```

## 13. Dashboard Mockup — SEO Content Factory

```
┌─────────────────────────────────────────────────────────────────┐
│  CONTENT FACTORY                          You: Aayushi · Editor │
├─────────────────────────────────────────────────────────────────┤
│  L1 DISCOVERY  →  L2 BRIEF  →  L3 DRAFT  →  L4 OPTIMIZE  →  L5  │
│      14            3 await       2 await       1 await    47    │
│                                                                  │
│  ▶ AWAITING YOU (3)                                              │
│  [BRIEF] "memory foam vs latex for indian summer"  open >       │
│  [DRAFT] "best mattress for couples"  edit >                    │
│  [OPT]   "queen size mattress price india"  approve >           │
│                                                                  │
│  ▶ AUTO-REFRESH PROPOSED (5)                                     │
│  "best mattress under 15000" — rank slipped #4→#7  view diff >  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 14. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Next.js)                      │
│  Founder · Brand Mgr · SEO Editor · Influencer Mgr  (4 roles)   │
│  + Agent Console (what's running, triggers, last decisions)     │
│  + Integrations Console (API connect buttons + health)          │
└────────────────────────────┬────────────────────────────────────┘
                             │  REST + WebSocket
┌────────────────────────────▼────────────────────────────────────┐
│                    API GATEWAY (FastAPI)                        │
│        Auth · RBAC · Rate limits · Audit log                    │
└──────┬──────────────────────┬──────────────────────┬────────────┘
       │                      │                      │
       ▼                      ▼                      ▼
┌────────────┐    ┌────────────────────┐   ┌────────────────────┐
│ READ MODEL │    │ AGENT ORCHESTRATOR │   │  INTEGRATIONS HUB  │
│ (Postgres  │    │ (Temporal +        │   │  GSC · GA4 · Shop. │
│  views for │    │  LiteLLM router)   │   │  Amazon · Flipkart │
│  dashboard)│    │                    │   │  Insta · YT · Trans│
└─────▲──────┘    └─────────┬──────────┘   └─────────┬──────────┘
      │                     │                        │
      │                     ▼                        │
      │           ┌────────────────────┐             │
      │           │   AGENT FLEET      │             │
      │           │  Research/Brief/   │             │
      │           │  Writer/Optimize/  │             │
      │           │  Caretaker/Listener│             │
      │           │  Roster/Index/     │             │
      │           │  ClaimsGuard       │             │
      │           └─────────┬──────────┘             │
      │                     ▼                        │
      │           ┌────────────────────┐             │
      └───────────┤    BRAND STATE     │◄────────────┘
                  │ Postgres (facts) + │
                  │ pgvector (embeds)+ │
                  │ S3/R2 (assets)    │
                  │ Redis (queues)     │
                  └────────────────────┘
```

---

## 15. Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | Next.js 15 + Tailwind + shadcn/ui + TanStack Table/Query | Dashboards-heavy; fast SSR; drill-down ergonomics |
| Auth + RBAC | Clerk (or Supabase Auth) | 4 roles out-of-box; audit log; SSO-ready |
| API | FastAPI (Python) | Same lang as agents; type-safe via Pydantic |
| Agent Orchestration | Temporal (durable workflows) + LiteLLM (model router) | L5 Caretaker needs durable retries across weeks |
| Agent Framework | Claude Agent SDK + Pydantic-AI | Typed I/O; native tool use; eval-friendly |
| Data | Postgres 16 + pgvector + S3-compatible (R2) + Redis | One DB to start; Brand State + embeddings co-located |
| Translation | IndicTrans2 (self-host) + Claude polish | SOTA for 22 Indic langs; free per-call |
| Rank tracking | DataForSEO API + GSC | Cheap; solid India coverage |
| Scrape (Reddit/Quora) | Bright Data + Reddit API | Avoid fragile DIY |
| Observability | Langfuse (LLM) + Sentry (app) + PostHog (product) | Captures prompt+cost+latency per agent run |
| Deploy | Vercel + Railway/Render + Supabase/Neon + Cloudflare R2 | Ship in days; migrate at SleepyCat-success |
| Eval | Promptfoo + DeepEval + golden sets per agent | Voice drift + claim accuracy gates |

---

## 16. Multi-LLM Runtime Routing

| Agent | Primary | Fallback | Why primary | Est. cost / run |
|---|---|---|---|---|
| Strategist (briefs) | Claude Opus | Claude Sonnet | Long-horizon synthesis | $0.30–0.60 |
| Writer (draft) | Claude Sonnet | GPT-5 | Best prose + voice control | $0.10–0.20 |
| Optimizer (schema/links) | GPT-5 | Sonnet | Structured output discipline | $0.05 |
| Caretaker (rank/decay) | Kimi K2 | Sonnet | Nightly across many URLs; cost matters | $0.01 |
| Listener (sentiment) | Gemini 2.5 Flash | Sonnet | Long context + cheap + handles Indic mixed | $0.02 |
| Brief Composer (creator) | Claude Sonnet | GPT-5 | Brand-safety + fit reasoning | $0.05 |
| Claims Guard | Claude Opus | Sonnet | Most cautious on health claims | $0.05 |
| Visibility Index | Sonnet | Opus | Founder narrative weekly | $0.10 |
| Translation core | IndicTrans2 (self-host) | Google Translate | SOTA for Indic; free | $0 + GPU |
| Translation polish | Claude Sonnet | Gemini 2.5 | Brand voice in target lang | $0.03/page |
| Bulk embeddings | Voyage / text-embedding-3-large | Cohere | Brand State retrieval | $0.01/1k chunks |
| Cheap classification | Llama 3.3 70B (self-host) or Haiku 4.5 | Kimi | High-volume tags | $0.001 |

**Why multi-model is the moat:** SleepyCat cares about brief quality, voice consistency, and bill — not which model. Multi-model routing serves the right job to the right tool; Claude (the orchestrator) picks.

---

## 17. Agent Visibility Surface (layman view)

Every agent shows as a card:

```
┌─────────────────────────────────────────────────────────────────┐
│  🟢  RESEARCH AGENT                              Last run: 4m ago│
│  ──────────────────────────────────────────────────────────────  │
│  What it does:   Scans GSC + competitors + AI Overviews to find  │
│                  keywords where SleepyCat can climb              │
│  Triggers:       Every Monday 7am  ·  Manual button              │
│  Last decision:  Promoted "memory foam vs latex" to brief queue  │
│                  (rank 8→target 3, effort: medium)               │
│  Cost this week: ₹420                                            │
│  [ View 12 most recent runs ]   [ Pause ]   [ Edit prompt ]      │
└─────────────────────────────────────────────────────────────────┘
```

Every card has: status light · plain-English job · triggers (cron + event + manual) · last decision · weekly cost · pause/edit buttons.

**Integrations Console** mirrors this pattern: each integration (GSC, GA4, Shopify, Amazon, Flipkart, Insta, YT, Translate) gets a card with connect button, health status, last sync, config.

---

## 18. Build Phasing — 6-Week First Cut

| Wk | Backend + Infra | Agents | Frontend | Demo at end of week |
|---|---|---|---|---|
| 1 | Monorepo (Turborepo), Postgres + pgvector, auth, RBAC, Temporal local | Stub all 10; wire LiteLLM | App shell; 4 dashboards (mock) | "Log in as founder; see fake dashboard" |
| 2 | GSC + GA4 + Shopify ingest → Brand State; product truth + claims seeded | Research + Strategist live | Founder real numbers; SEO Factory L1+L2 real | "Real GSC data flows; real briefs come out" |
| 3 | Amazon + Flipkart + Insta + YT ingest; DataForSEO | Writer (L3) + Optimizer (L4); Claims Guard hard-gate | SEO Factory L3+L4; Brand Mgr Listener feed | "Brief → draft → optimized → publishable" |
| 4 | Migrate `sleepycat.in/blogs` corpus; embed all | Caretaker (L5) live on imported corpus; Listener live | Brand Mgr Studio full (voice toggle, sentiment, calendar) | "200 existing blogs tracked; auto-refresh firing" |
| 5 | IndicTrans2 deploy + polish; language toggle | Brief Composer + Roster live | Influencer Hub full; multi-lingual toggle | "Hindi pillar article ships" |
| 6 | Eval harness (Promptfoo); Langfuse dashboards; training; prod cutover | All agents supervised auto-run | Polish; mobile-responsive; agent-console v1 | **First-cut ship to SleepyCat** |

**Critical path = Week 4** (migration of live `sleepycat.in/blogs`). Pre-scope it Week 1 so it doesn't slip.

---

## 19. Who Builds What

You are the orchestrator. Claude (in Claude Code) is the lead implementer + multi-model dispatcher.

| Slice | Who builds | Why |
|---|---|---|
| Architecture, system design, code review, security | Claude | Strongest at long-horizon code; careful design; security |
| Frontend (Next.js + shadcn) | Claude + v0/Cursor for scaffolds | I write logic; v0 accelerates dashboard mockups; I integrate |
| Backend APIs + Temporal workflows | Claude | Type-safe Python; Temporal best fit |
| Agent system prompts + tool definitions | Claude | This is what I'm built for |
| Heavy data ingest (read all SleepyCat blogs, classify, embed) | Bootstrap Gemini 2.5 Pro (1M context); validate Claude | Gemini eats large corpora in fewer calls |
| Integration boilerplate (GSC/GA4/Amazon/Flipkart) | GPT-5 from OpenAPI specs; Claude reviews + business logic | GPT fast at spec→boilerplate |
| Eval harness + golden sets | Claude | Test design carefully |
| DevOps / IaC | Claude | Bash/Terraform careful work |
| Observability config (Langfuse + Sentry) | Claude config; off-the-shelf otherwise | Wiring, not building |
| Documentation + runbooks | Claude | Terse + accurate |
| **In production at runtime** | Multi-LLM routing table §16 | Each agent uses the right model |

**Why Claude is the build orchestrator:**
- Long-horizon coherence across a 6-week multi-component build
- Tool use + Anthropic Agent SDK alignment
- Careful refactor when Week 4 reveals what Week 2 got wrong

**Honest limits Claude has:**
- Not fastest at one-shot boilerplate (GPT is)
- Not cheapest at scale (Kimi/Haiku are)
- Not best at one-shot massive corpus ingest (Gemini is)

These are why we delegate.

---

## 20. Orchestrator Partnership Model

**Your role:**
- Product decisions (default voice ratios, brand-safety bar, competitor watchlist, SleepyCat owner per surface).
- Approve agent prompts before first-live.
- Approve per-agent cost ceilings.
- Final call on scope cuts.

**Claude's role:**
- Build architecture, code, integrations, prompts, dashboards, evals, deploy.
- Pick the right model per slice and explain why.
- Surface tradeoffs before committing code — not after.
- Tell you when I'm wrong, when another model would be better.

**Cadence:**
- Daily: I push code; you review the agent console for outputs that feel off.
- Weekly: Friday demo + cost/eval report + scope check.
- Per major component: spec → build → eval → ship; you gate at each.

---

## 21. Test Plan — Proof-of-Concept Inputs

Before Week 1 production code, run agent fleet on real SleepyCat data:

| Input | Purpose | Form |
|---|---|---|
| GSC export — top 200 queries × pages, last 12 months | Research + Strategist real test | CSV |
| 10 SleepyCat URLs to compete to rank 1–3 for | Strategist target test | URLs + target keyword each |
| Product truth seed: 3 mattress spec sheets + claim ladder + evidence | Brand State seeding | PDF/Doc |
| Claims register stub: 10 claims marked approved/needs-evidence/banned | Claims Guard test | Sheet |
| 5 Reddit/Quora threads about Indian mattress buying | Listener test | URLs |
| 20 reviews (positive + negative) Amazon + site | Listener theme test | CSV |
| 3 competitor URLs (Wakefit, Sleepwell, The Sleep Company) | SERP teardown | URLs |

Deliverable from test run: Day-0 dashboard + first 3 briefs + sentiment map.
**If output is sharp, build. If not, re-spec before burning Sprint 1.**

---

## 22. Decisions to Lock

1. **Cloud target.** Vercel + Render + Supabase (ship in days) **or** AWS-from-day-1 (slower, enterprise-friendly). *Recommend: Vercel-stack now; AWS migrate at SleepyCat-success.*
2. **Multi-tenant from day 1, or SleepyCat-only?** Multi-tenant ~10% more in Week 1; saves 6 weeks at Client #2. *Recommend: multi-tenant.*
3. **Self-host agent runtime, or managed (LangSmith/AgentOps)?** Agent layer is the product moat. *Recommend: self-host.*

---

## 23. Comparison Matrix — BRE vs Prior Docs

| Dimension | Kimi | GPT | Gemini | **Claude (this doc)** |
|---|---|---|---|---|
| Frame | Strategy doc | Operating manual | Content skill | **Product spec** |
| Optimized for | Completeness | Governance | Voice | **Shippability** |
| Output type | 245-line plan | Skill (principles) | Skill (personas) | **Architecture + build phasing** |
| Concreteness | Generic | Meta | Brand-DNA-specific | **Code-level + multi-LLM** |
| Action level | Checklist | Discipline rules | Content patterns | **Build Gantt + runtime routing** |
| Diagnosis-first? | No | No | No | **Test plan precedes Sprint 1** |
| Risk surface | Light | Strong QA section | Light (Zomato risk unaddressed) | **Cost ceilings + eval harness + Claims Guard hard gate** |
| Multi-LLM aware? | No | No | No | **Routing table per agent** |
| Conversion-side? | No | No | No | **CAC payback, ROAS, decision triggers** |

---

*Doc version: claude_final v0.2*
*Author: Claude Opus 4.7 (Claude Code)*
*Role: Build orchestrator + multi-LLM runtime dispatcher*
*Status: Awaiting (a) lock on 3 decisions in §22, (b) test-run inputs in §21*
