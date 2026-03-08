import requests
import schedule
import time
import json
import os
import threading
from datetime import datetime

# ============================================================
#   CONFIGURATION
# ============================================================
TELEGRAM_TOKEN  = "8723153041:AAHOurhS7dOJ2ZOt0tTleZNQRH0mdNn-jn8"
NEWS_API_KEY    = "3752e4a00554420bae8d8488d41ebc5e"
SEND_TIME       = "08:00"
NUM_ARTICLES    = 10
SUBSCRIBERS_FILE = "subscribers.json"

# ============================================================
#   TRANSLATIONS
# ============================================================
MESSAGES = {
    "en": {
        "welcome": (
            "👋 Welcome to <b>AI News Daily</b>!\n\n"
            "You'll receive the top 10 AI news stories every morning at 8:00 AM.\n\n"
            "📌 Commands:\n"
            "/start — Subscribe\n"
            "/stop — Unsubscribe\n"
            "/language — Change language\n"
            "/news — Get news right now\n\n"
            "✅ You are now subscribed!"
        ),
        "already": "✅ You're already subscribed! Use /stop to unsubscribe.",
        "stopped": "😢 You've been unsubscribed. Send /start anytime to resubscribe.",
        "not_subscribed": "You are not subscribed. Send /start to subscribe.",
        "language_prompt": "🌍 Choose your language:\n\n1️⃣ /lang_en — English\n2️⃣ /lang_ar — Arabic (عربي)\n3️⃣ /lang_fr — French (Français)",
        "language_set": "✅ Language set to English!",
        "header": "🤖 <b>AI News Daily — {date}</b>\n━━━━━━━━━━━━━━━━━━━━━━\nYour top {n} AI stories:\n",
        "footer": "\n━━━━━━━━━━━━━━━━━━━━━━\n⚡ <b>AI News Daily Bot</b> — /stop to unsubscribe",
        "read": "🔗 Read article",
        "source": "📰",
        "no_news": "⚠️ Could not fetch news right now. Try again later.",
        "unknown": "❓ Unknown command. Use /start, /stop, /language or /news.",
    },
    "ar": {
        "welcome": (
            "👋 مرحباً بك في <b>أخبار الذكاء الاصطناعي اليومية</b>!\n\n"
            "ستتلقى أهم 10 أخبار في مجال الذكاء الاصطناعي كل صباح.\n\n"
            "📌 الأوامر:\n"
            "/start — اشتراك\n"
            "/stop — إلغاء الاشتراك\n"
            "/language — تغيير اللغة\n"
            "/news — احصل على الأخبار الآن\n\n"
            "✅ تم اشتراكك بنجاح!"
        ),
        "already": "✅ أنت مشترك بالفعل! أرسل /stop لإلغاء الاشتراك.",
        "stopped": "😢 تم إلغاء اشتراكك. أرسل /start في أي وقت للاشتراك مجدداً.",
        "not_subscribed": "أنت غير مشترك. أرسل /start للاشتراك.",
        "language_prompt": "🌍 اختر لغتك:\n\n1️⃣ /lang_en — English\n2️⃣ /lang_ar — العربية\n3️⃣ /lang_fr — Français",
        "language_set": "✅ تم تعيين اللغة إلى العربية!",
        "header": "🤖 <b>أخبار الذكاء الاصطناعي — {date}</b>\n━━━━━━━━━━━━━━━━━━━━━━\nأبرز {n} أخبار اليوم:\n",
        "footer": "\n━━━━━━━━━━━━━━━━━━━━━━\n⚡ <b>بوت أخبار الذكاء الاصطناعي</b> — /stop لإلغاء الاشتراك",
        "read": "🔗 اقرأ المقال",
        "source": "📰",
        "no_news": "⚠️ تعذر جلب الأخبار الآن. حاول مرة أخرى لاحقاً.",
        "unknown": "❓ أمر غير معروف. استخدم /start أو /stop أو /language أو /news.",
    },
    "fr": {
        "welcome": (
            "👋 Bienvenue sur <b>AI News Daily</b>!\n\n"
            "Vous recevrez les 10 meilleures actualités IA chaque matin à 8h00.\n\n"
            "📌 Commandes:\n"
            "/start — S'abonner\n"
            "/stop — Se désabonner\n"
            "/language — Changer de langue\n"
            "/news — Recevoir les news maintenant\n\n"
            "✅ Vous êtes maintenant abonné!"
        ),
        "already": "✅ Vous êtes déjà abonné! Utilisez /stop pour vous désabonner.",
        "stopped": "😢 Vous avez été désabonné. Envoyez /start pour vous réabonner.",
        "not_subscribed": "Vous n'êtes pas abonné. Envoyez /start pour vous abonner.",
        "language_prompt": "🌍 Choisissez votre langue:\n\n1️⃣ /lang_en — English\n2️⃣ /lang_ar — العربية\n3️⃣ /lang_fr — Français",
        "language_set": "✅ Langue définie sur le Français!",
        "header": "🤖 <b>AI News Daily — {date}</b>\n━━━━━━━━━━━━━━━━━━━━━━\nVos {n} actualités IA du jour:\n",
        "footer": "\n━━━━━━━━━━━━━━━━━━━━━━\n⚡ <b>AI News Daily Bot</b> — /stop pour se désabonner",
        "read": "🔗 Lire l'article",
        "source": "📰",
        "no_news": "⚠️ Impossible de récupérer les actualités. Réessayez plus tard.",
        "unknown": "❓ Commande inconnue. Utilisez /start, /stop, /language ou /news.",
    }
}

# ============================================================
#   SUBSCRIBER STORAGE
# ============================================================
def load_subscribers():
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_subscribers(subs):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(subs, f, indent=2)

def get_lang(chat_id):
    subs = load_subscribers()
    return subs.get(str(chat_id), {}).get("lang", "en")

# ============================================================
#   TELEGRAM HELPERS
# ============================================================
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"  ⚠ Failed to send to {chat_id}: {e}")

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"timeout": 30, "offset": offset}
    try:
        r = requests.get(url, params=params, timeout=35)
        r.raise_for_status()
        return r.json().get("result", [])
    except:
        return []

# ============================================================
#   NEWS FETCHER
# ============================================================
def fetch_ai_news(lang="en"):
    queries = {
        "en": '("artificial intelligence" OR "ChatGPT" OR "OpenAI" OR "Gemini" OR "LLM" OR "machine learning" OR "Anthropic" OR "Grok") AND (launch OR release OR breakthrough OR funding OR research)',
        "ar": '("الذكاء الاصطناعي" OR "ChatGPT" OR "OpenAI" OR "نماذج اللغة") AND (إطلاق OR بحث OR تطوير OR تمويل)',
        "fr": '("intelligence artificielle" OR "ChatGPT" OR "OpenAI" OR "apprentissage automatique") AND (lancement OR recherche OR financement)',
    }
    lang_codes = {"en": "en", "ar": "ar", "fr": "fr"}
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": queries.get(lang, queries["en"]),
        "language": lang_codes.get(lang, "en"),
        "sortBy": "publishedAt",
        "pageSize": NUM_ARTICLES,
        "apiKey": NEWS_API_KEY,
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    articles = r.json().get("articles", [])

    # Filter out junk articles
    filtered = []
    for a in articles:
        title = (a.get("title") or "").lower()
        skip_keywords = ["[removed]", "cookie", "privacy policy", "terms of service"]
        if not any(k in title for k in skip_keywords) and a.get("url"):
            filtered.append(a)
    return filtered[:NUM_ARTICLES]

def build_news_message(articles, lang="en"):
    t = MESSAGES[lang]
    now = datetime.now().strftime("%A, %d %B %Y")
    lines = [t["header"].format(date=now, n=len(articles))]

    for i, article in enumerate(articles, 1):
        title  = (article.get("title") or "No title").strip()
        url    = article.get("url", "")
        source = article.get("source", {}).get("name", "Unknown")
        desc   = (article.get("description") or "").strip()
        if len(desc) > 160:
            desc = desc[:157] + "..."

        lines.append(f"<b>{i}. {title}</b>")
        if desc:
            lines.append(f"<i>{desc}</i>")
        lines.append(f"{t['source']} {source}")
        lines.append(f"<a href='{url}'>{t['read']}</a>")
        lines.append("")

    lines.append(t["footer"])
    return "\n".join(lines)

# ============================================================
#   COMMAND HANDLERS
# ============================================================
def handle_start(chat_id):
    subs = load_subscribers()
    key = str(chat_id)
    lang = subs.get(key, {}).get("lang", "en")
    t = MESSAGES[lang]
    if key in subs and subs[key].get("active"):
        send_message(chat_id, t["already"])
    else:
        subs[key] = {"active": True, "lang": lang}
        save_subscribers(subs)
        send_message(chat_id, t["welcome"])
    print(f"  ✅ /start from {chat_id} (lang: {lang})")

def handle_stop(chat_id):
    subs = load_subscribers()
    key = str(chat_id)
    lang = subs.get(key, {}).get("lang", "en")
    t = MESSAGES[lang]
    if key in subs:
        subs[key]["active"] = False
        save_subscribers(subs)
        send_message(chat_id, t["stopped"])
    else:
        send_message(chat_id, t["not_subscribed"])
    print(f"  🛑 /stop from {chat_id}")

def handle_language(chat_id):
    lang = get_lang(chat_id)
    send_message(chat_id, MESSAGES[lang]["language_prompt"])

def handle_set_language(chat_id, new_lang):
    subs = load_subscribers()
    key = str(chat_id)
    if key not in subs:
        subs[key] = {"active": False, "lang": new_lang}
    else:
        subs[key]["lang"] = new_lang
    save_subscribers(subs)
    send_message(chat_id, MESSAGES[new_lang]["language_set"])
    print(f"  🌍 Language changed to {new_lang} for {chat_id}")

def handle_news_now(chat_id):
    lang = get_lang(chat_id)
    t = MESSAGES[lang]
    try:
        articles = fetch_ai_news(lang)
        if not articles:
            send_message(chat_id, t["no_news"])
            return
        msg = build_news_message(articles, lang)
        send_message(chat_id, msg)
    except Exception as e:
        send_message(chat_id, t["no_news"])
        print(f"  ❌ Error fetching for {chat_id}: {e}")

def handle_unknown(chat_id):
    lang = get_lang(chat_id)
    send_message(chat_id, MESSAGES[lang]["unknown"])

# ============================================================
#   DAILY BROADCAST
# ============================================================
def broadcast_news():
    subs = load_subscribers()
    active = {k: v for k, v in subs.items() if v.get("active")}
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 📡 Broadcasting to {len(active)} subscribers...")

    # Fetch once per language
    news_cache = {}
    for chat_id, info in active.items():
        lang = info.get("lang", "en")
        if lang not in news_cache:
            try:
                articles = fetch_ai_news(lang)
                news_cache[lang] = build_news_message(articles, lang) if articles else None
            except Exception as e:
                news_cache[lang] = None
                print(f"  ❌ Fetch error for lang {lang}: {e}")

        msg = news_cache.get(lang)
        if msg:
            send_message(chat_id, msg)
            print(f"  📨 Sent to {chat_id} [{lang}]")
            time.sleep(0.3)  # avoid Telegram rate limit
        else:
            send_message(chat_id, MESSAGES[lang]["no_news"])

    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Broadcast complete.\n")

# ============================================================
#   POLLING LOOP (listens for user messages)
# ============================================================
def polling_loop():
    print("  👂 Listening for new subscribers...")
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            chat_id = msg.get("chat", {}).get("id")
            text = (msg.get("text") or "").strip()

            if not chat_id or not text:
                continue

            print(f"  💬 Message from {chat_id}: {text}")

            if text.startswith("/start"):
                handle_start(chat_id)
            elif text.startswith("/stop"):
                handle_stop(chat_id)
            elif text.startswith("/language"):
                handle_language(chat_id)
            elif text.startswith("/lang_en"):
                handle_set_language(chat_id, "en")
            elif text.startswith("/lang_ar"):
                handle_set_language(chat_id, "ar")
            elif text.startswith("/lang_fr"):
                handle_set_language(chat_id, "fr")
            elif text.startswith("/news"):
                handle_news_now(chat_id)
            else:
                handle_unknown(chat_id)

        time.sleep(1)

# ============================================================
#   MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("   🤖 AI News Daily — Public Bot")
    print(f"   📅 Daily broadcast at {SEND_TIME}")
    print(f"   🌍 Languages: English, Arabic, French")
    print(f"   📁 Subscribers saved in: {SUBSCRIBERS_FILE}")
    print("=" * 55)

    # Start polling in background thread
    t = threading.Thread(target=polling_loop, daemon=True)
    t.start()

    # Schedule daily broadcast
    schedule.every().day.at(SEND_TIME).do(broadcast_news)
    print(f"\n⏰ Bot is running. Daily news at {SEND_TIME}.")
    print("   Share your bot username so people can subscribe!")
    print("   Press Ctrl+C to stop.\n")

    while True:
        schedule.run_pending()
        time.sleep(30)
