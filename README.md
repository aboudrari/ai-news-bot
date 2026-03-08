# 🤖 AI News Daily — Telegram Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)
![Railway](https://img.shields.io/badge/Hosted_on-Railway-8B5CF6?style=for-the-badge&logo=railway&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**A fully automated AI-powered Telegram bot that delivers the top 10 AI news stories every morning — in English, Arabic, or French.**

[🚀 Try the Bot](#try-the-bot) • [✨ Features](#features) • [⚙️ Setup](#setup) • [📦 Deploy](#deploy)

</div>

---

## 📸 Preview

```
🤖 AI News Daily — Sunday, 08 March 2026
━━━━━━━━━━━━━━━━━━━━━━
Your top 10 AI stories:

1. OpenAI Releases GPT-5 with Unprecedented Reasoning Capabilities
New model scores 95% on graduate-level benchmarks, surpassing all previous...
📰 TechCrunch
🔗 Read article

2. Google DeepMind Announces Breakthrough in Protein Folding Research
...
━━━━━━━━━━━━━━━━━━━━━━
⚡ AI News Daily Bot — /stop to unsubscribe
```

---

## ✨ Features

- 📰 **Top 10 daily AI news** — curated from hundreds of sources
- 🌍 **Multilingual** — English, Arabic (عربي), and French (Français)
- ⏰ **Automated delivery** — every morning at 8:00 AM
- 👥 **Public subscription** — anyone can subscribe with `/start`
- 🔗 **Clickable links** — every story links to the full article
- ⚡ **On-demand news** — get news instantly with `/news`
- ☁️ **Cloud hosted** — runs 24/7 on Railway, no PC needed

---

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Subscribe to daily news |
| `/stop` | Unsubscribe |
| `/news` | Get today's news right now |
| `/language` | Switch language (EN / AR / FR) |

---

## 🚀 Try the Bot

Search for **@YourBotUsername** on Telegram and press **Start**.

> Free. No spam. Unsubscribe anytime with `/stop`.

---

## ⚙️ Setup

### Prerequisites
- Python 3.11+
- A [Telegram Bot Token](https://t.me/BotFather)
- A [NewsAPI key](https://newsapi.org) (free tier works)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/aboudrari/ai-news-bot.git
cd ai-news-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your credentials
# Open ai_news_agent_public.py and fill in:
#   TELEGRAM_TOKEN   = "your token here"
#   TELEGRAM_CHAT_ID = "your chat id"
#   NEWS_API_KEY     = "your api key"

# 4. Run the bot
python ai_news_agent_public.py
```

---

## 📦 Deploy

This bot is ready to deploy on **Railway** in one click:

1. Fork this repo
2. Go to [railway.app](https://railway.app)
3. Click **New Project → Deploy from GitHub**
4. Select this repo — done! ✅

The `Procfile` and `runtime.txt` are already configured.

---

## 🗂️ Project Structure

```
ai-news-bot/
├── ai_news_agent_public.py   # Main bot script
├── requirements.txt           # Python dependencies
├── Procfile                   # Railway deployment config
├── runtime.txt                # Python version
└── subscribers.json           # Auto-generated subscriber list
```

---

## 🛠️ Built With

- [Python](https://python.org) — core language
- [NewsAPI](https://newsapi.org) — news source
- [Schedule](https://schedule.readthedocs.io) — task scheduling
- [Railway](https://railway.app) — cloud hosting

---

## 📄 License

MIT License — free to use, modify, and share.

---

<div align="center">

Made with ❤️ by [aboudrari](https://github.com/aboudrari)

⭐ Star this repo if you found it useful!

</div>
