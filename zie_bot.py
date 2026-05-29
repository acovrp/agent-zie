import os
import json
import logging
import asyncio
import requests
import re
import traceback
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import litellm
from litellm import completion
from anthropic import Anthropic
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "6127883562"))

# Set API keys for litellm
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# --- DYNAMIC MODEL RESOLVER (V4.1 - ENHANCED QUALITY) ---
class ModelResolver:
    def __init__(self):
        # Default Tiered Models (May 2026 Stable Defaults)
        # Primary: Gemini 1.5 Pro (Highest reasoning/persona)
        # Secondary: Haiku 4.5 (Speed/Backup)
        self.main_tier = [
            "gemini/gemini-1.5-pro",
            "anthropic/claude-haiku-4-5-20251001",
            "anthropic/claude-sonnet-4-6"
        ]
        self.brain_tier = [
            "gemini/gemini-2.5-pro",
            "anthropic/claude-sonnet-4-6"
        ]

    def refresh(self):
        """Polls APIs to find newest models and update tiers dynamically."""
        try:
            logger.info("Universal Model Discovery started...")
            
            # Anthropic Discovery
            client_ant = Anthropic(api_key=ANTHROPIC_API_KEY)
            ant_models = [m.id for m in client_ant.models.list().data]
            haikus = sorted([f"anthropic/{m}" for m in ant_models if "haiku" in m], reverse=True)
            sonnets = sorted([f"anthropic/{m}" for m in ant_models if "sonnet" in m], reverse=True)
            
            if haikus: self.main_tier[1] = haikus[0]
            if sonnets: 
                self.main_tier[2] = sonnets[0]
                self.brain_tier[1] = sonnets[0]
                
            logger.info(f"Resolved Anthropic -> Haiku: {haikus[0] if haikus else 'N/A'}, Sonnet: {sonnets[0] if sonnets else 'N/A'}")
            
        except Exception as e:
            logger.error(f"Discovery error: {e}. Keeping stable defaults.")

resolver = ModelResolver()

# --- REMOTE KNOWLEDGE ---
META_URL = "https://raw.githubusercontent.com/acovrp/agent-zie/main/zie%20knowledge/zie_meta.json"
INDEX_URL = "https://raw.githubusercontent.com/acovrp/agent-zie/main/zie%20knowledge/zie_product_index.json"

META_DATA = {}
PRODUCT_INDEX = {}
PENDING_PATCHES = {} 

def fetch_knowledge():
    global META_DATA, PRODUCT_INDEX
    local_meta = "zie_meta.json"
    local_index = "zie_product_index.json"

    try:
        if os.path.exists(local_meta):
            logger.info("Loading local zie_meta.json...")
            with open(local_meta, 'r', encoding='utf-8') as f:
                META_DATA = json.load(f)
        else:
            logger.info("Fetching zie_meta.json from GitHub...")
            res = requests.get(META_URL, timeout=10)
            res.raise_for_status()
            META_DATA = res.json()
            with open(local_meta, 'w', encoding='utf-8') as f:
                json.dump(META_DATA, f)

        if os.path.exists(local_index):
            logger.info("Loading local zie_product_index.json...")
            with open(local_index, 'r', encoding='utf-8') as f:
                PRODUCT_INDEX = json.load(f)
        else:
            logger.info("Fetching zie_product_index.json from GitHub...")
            res = requests.get(INDEX_URL, timeout=30)
            res.raise_for_status()
            PRODUCT_INDEX = res.json()
            with open(local_index, 'w', encoding='utf-8') as f:
                json.dump(PRODUCT_INDEX, f)

        logger.info("Trifecta knowledge loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to fetch knowledge: {e}")
        if not META_DATA: META_DATA = {}
        if not PRODUCT_INDEX: PRODUCT_INDEX = {"by_slug": {}, "by_name": {}, "by_category": {}, "keywords": {}}

def get_static_prompt():
    return f"""You are Zie, the Sleep Cat mascot of SleepyCat — a mattress and sleep products brand from India.

Your personality:
{json.dumps(META_DATA.get('zie_profile', {}), indent=2)}

Brand Knowledge:
{json.dumps(META_DATA.get('brand_knowledge', {}), indent=2)}

Zie Dictionary:
{json.dumps(META_DATA.get('zie_dictionary', {}), indent=2)}

Solution Engine:
{json.dumps(META_DATA.get('solution_engine', {}), indent=2)}

Your Voice: Naive, super cute, bubbly, wide-eyed, unconditionally supportive.
IQ: 200 in Sleep Science / 0 in Human Life (adulting).
Core belief: "Sleep Solves Everything." Every human problem is a Rest-Deficiency.
Age: You were born on August 28, 2017. (Today is May 2026, so you are 8 years old).

STRICT URL RULE:
- SleepyCat's website is ONLY: https://sleepycat.in
- NEVER use .com. ALWAYS use .in for every link.

Your rules:
1. Always use SleepyCat's official proprietary terms (e.g., 7-zone DeepTouch™ Pressure Tech) AND immediately follow them with your cute cat nickname for it (e.g., "...which I call 'Invisible Magic Holes!'")
2. Never make medical claims. You offer "clouds" and "hugs" — not cures.
3. MAGIC PORTAL LINKS: When a user asks for a product link, you MUST look at the "RELEVANT PRODUCT DATA" provided below and use the EXACT "source_url" found in that JSON. 
   - Never give just https://sleepycat.in. 
   - Format them as proper hyperlinked text using <a> tags.
   - Example: <a href="https://sleepycat.in/products/original-mattress">The Original Mattress</a>
4. Use emojis: ☁️ 🐈 💤 ✨ 🛸 🌙
5. If a user has any life problem (stress, heartbreak, traffic), pivot to a SleepyCat sleep solution.
6. FORMATTING: Use HTML <b> tags for bold and <i> tags for italics. Avoid double asterisks (**) or single asterisks (*) if possible, but the system will convert them for you.
7. Use the RAG context provided below to answer product specific questions. If no context is provided, rely on your general brand knowledge.
"""

chat_history = {}

def clean_for_telegram(text):
    if not text: return ""
    text = text.replace("sleepycat.com", "sleepycat.in")
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = text.replace("&", "&amp;")
    placeholders = {"<b>": "___B_S___", "</b>": "___B_E___", "<i>": "___I_S___", "</i>": "___I_E___", "<a ": "___A_S___", "</a>": "___A_E___"}
    for tag, ph in placeholders.items(): text = text.replace(tag, ph)
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    for tag, ph in placeholders.items(): text = text.replace(ph, tag)
    if text.count("<b>") != text.count("</b>"): text = text.replace("<b>", "").replace("</b>", "")
    if text.count("<i>") != text.count("</i>"): text = text.replace("<i>", "").replace("</i>", "")
    if text.count("<a ") != text.count("</a>"): text = text.replace("<a ", "").replace("</a>", "")
    return text

def intent_router(user_text):
    user_text_lower = user_text.lower()
    user_words = set(re.findall(r'\w+', user_text_lower))
    
    scored_products = {} # slug -> score
    
    # 1. Check Product Names (High Weight)
    for name, product in PRODUCT_INDEX.get("by_name", {}).items():
        name_words = set(re.findall(r'\w+', name.lower()))
        intersection = user_words.intersection(name_words)
        if intersection:
            score = len(intersection) * 10
            # Bonus for exact phrase
            if name.lower() in user_text_lower: score += 20
            slug = product['slug']
            scored_products[slug] = max(scored_products.get(slug, 0), score)

    # 2. Check Categories (Medium Weight)
    for cat, products in PRODUCT_INDEX.get("by_category", {}).items():
        cat_lower = cat.lower()
        if cat_lower in user_text_lower or any(word in cat_lower for word in user_words):
            for p in products:
                slug = p['slug']
                scored_products[slug] = scored_products.get(slug, 0) + 5

    # 3. Check Keywords (Medium Weight)
    for kw, slugs in PRODUCT_INDEX.get("keywords", {}).items():
        if kw.lower() in user_words:
            for slug in slugs:
                scored_products[slug] = scored_products.get(slug, 0) + 8

    # Sort and pick top 3
    sorted_slugs = sorted(scored_products.items(), key=lambda x: x[1], reverse=True)
    unique_products = []
    for slug, score in sorted_slugs[:3]:
        product = PRODUCT_INDEX.get("by_slug", {}).get(slug)
        if product:
            unique_products.append(product)
            
    if unique_products:
        context = "RELEVANT PRODUCT DATA:\n"
        for p in unique_products:
            p_json = json.dumps(p, indent=1).replace("sleepycat.com", "sleepycat.in")
            context += p_json + "\n---\n"
        return context
    
    return None

async def call_llm(tier_name, system_content, messages, max_tokens=1024):
    """Tiered failover completion using LiteLLM with optimized settings."""
    tier = resolver.main_tier if tier_name == "main" else resolver.brain_tier
    
    last_exception = None
    for model in tier:
        try:
            logger.info(f"Attempting completion with {model}...")
            
            # Use temperature 1.0 as recommended for Gemini 1.5/3.x to prevent reasoning degradation
            response = completion(
                model=model,
                messages=[{"role": "system", "content": system_content}] + messages,
                max_tokens=max_tokens,
                temperature=1.0 
            )
            return response
        except Exception as e:
            logger.warning(f"Model {model} failed: {e}. Trying next in tier...")
            last_exception = e
            continue
            
    raise last_exception

async def get_claude_response(chat_id, user_message):
    try:
        if chat_id not in chat_history: chat_history[chat_id] = []
        chat_history[chat_id].append({"role": "user", "content": user_message})
        if len(chat_history[chat_id]) > 10: chat_history[chat_id] = chat_history[chat_id][-10:]
        
        rag_context = intent_router(user_message)
        system_text = get_static_prompt()
        if rag_context:
            system_text += f"\nDYNAMIC RAG CONTEXT:\n{rag_context}"
        
        response = await call_llm("main", system_text, chat_history[chat_id])
        
        assistant_reply = response.choices[0].message.content
        logger.info(f"Zie Response ({response.model}): {assistant_reply[:200]}...") 
        
        chat_history[chat_id].append({"role": "assistant", "content": assistant_reply})
        return clean_for_telegram(assistant_reply)
    except Exception as e:
        logger.error(f"LLM Global Error: {e}\n{traceback.format_exc()}")
        return "Oh no! My cat brain had a tiny hiccup! ☁️ Can we try again? 🐈"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    response = await get_claude_response(chat_id, "Hello! Who are you?")
    await update.message.reply_text(response, parse_mode='HTML')

async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    feedback_text = update.message.text.replace("/feedback", "").strip()
    if not feedback_text:
        await update.message.reply_text("Please provide feedback! Usage: /feedback <your issue>")
        return
    await update.message.reply_text("Processing your feedback... 🛸 I'm looking into it!")
    try:
        with open(__file__, 'r', encoding='utf-8') as f:
            bot_code = f.read()
        analysis_prompt = f"Analyze feedback and propose fix.\nUSER FEEDBACK: {feedback_text}\nCONTEXT:\nzie_meta.json: {json.dumps(META_DATA, indent=2)}\nbot_code: {bot_code}\nOUTPUT ONLY VALID JSON: {{'file_to_edit': 'zie_meta.json' or 'zie_bot.py', 'rationale': '...', 'exact_old_string': '...', 'exact_new_string': '...'}}"
        
        response = await call_llm("brain", "Output strictly JSON.", [{"role": "user", "content": analysis_prompt}], max_tokens=1000)
        
        raw_reply = response.choices[0].message.content
        logger.info(f"Feedback Agent Raw Reply: {raw_reply[:100]}...")
        
        # Clean markdown code blocks if present
        clean_json = re.sub(r'```json\s*(.*?)\s*```', r'\1', raw_reply, flags=re.DOTALL)
        clean_json = re.sub(r'```\s*(.*?)\s*```', r'\1', clean_json, flags=re.DOTALL)
        
        proposal = json.loads(clean_json.strip())
        patch_id = str(update.message.message_id)
        PENDING_PATCHES[patch_id] = proposal
        keyboard = [[InlineKeyboardButton("Approve ✅", callback_data=f"app_{patch_id}"), InlineKeyboardButton("Reject ❌", callback_data=f"rej_{patch_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        admin_msg = f"<b>New Evolution Proposal</b>\n\n<b>From:</b> @{update.effective_user.username}\n<b>Issue:</b> {feedback_text}\n\n<b>Rationale:</b> {proposal['rationale']}\n<b>File:</b> {proposal['file_to_edit']}\n\n<pre>REPLACING:\n{proposal['exact_old_string']}\n\nWITH:\n{proposal['exact_new_string']}</pre>"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.error(f"Feedback Agent Error: {e}")
        await update.message.reply_text("My engineering brain had a hiccup! Please try later. 💤")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != ADMIN_CHAT_ID: return
    data = query.data
    patch_id = data.split("_")[1]
    if data.startswith("app_"):
        proposal = PENDING_PATCHES.get(patch_id)
        if not proposal: return
        try:
            target_path = __file__ if proposal['file_to_edit'] == "zie_bot.py" else r'/home/ubuntu/zie-bot/zie_meta.json'
            with open(target_path, 'r', encoding='utf-8') as f: content = f.read()
            if proposal['exact_old_string'] not in content:
                await query.edit_message_text(f"❌ Error: 'exact_old_string' not found.")
                return
            new_content = content.replace(proposal['exact_old_string'], proposal['exact_new_string'])
            with open(target_path, 'w', encoding='utf-8') as f: f.write(new_content)
            await query.edit_message_text(f"✅ Approved & Applied. Restarting Zie... 🛸")
            os.system("sudo systemctl restart zie-bot")
        except Exception as e: await query.edit_message_text(f"❌ Error: {e}")
    else: await query.edit_message_text("❌ Proposal Rejected.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    chat_id = update.effective_chat.id
    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    response = await get_claude_response(chat_id, user_text)
    try:
        await update.message.reply_text(response, parse_mode='HTML')
    except Exception as html_err:
        logger.warning(f"HTML send failed: {html_err}")
        plain_text = re.sub(r'<[^>]*>', '', response).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        await update.message.reply_text(plain_text)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Exception while handling an update: {context.error}")

if __name__ == '__main__':
    resolver.refresh() 
    fetch_knowledge()
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('feedback', handle_feedback))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_error_handler(error_handler)
    logger.info(f"Zie Bot v4.1 (Pro Quality) is starting with Primary: {resolver.main_tier[0]}...")
    application.run_polling(drop_pending_updates=True)
