# 📢 Daily Quote Automator: AI-Powered Motivation Bot

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Prefect](https://img.shields.io/badge/Prefect-Orchestration-070E28?logo=prefect&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Google%20Gemini-Generative%20AI-8E75B2?logo=google&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Delivery-26A5E4?logo=telegram&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📌 Overview
**Daily Quote Automator** is a streamlined automation tool designed to deliver daily doses of inspiration.

Orchestrated by **Prefect**, this bot functions as your personal AI mentor. It leverages **Google's Gemini 2.5 Flash** model via LangChain to generate unique, punchy motivational quotes specifically tailored for programmers, and instantly broadcasts them to a **Telegram Channel** using the robust **Python Telegram Bot (Async)** library. It is built for reliability with automatic retries and modular task execution.

> **💡 Alternative Version:** Looking for a simpler, synchronous version? Check out the **[Standard Requests Variant](https://github.com/viochris/trial-simple-quote-bot)**. It uses the lightweight `requests` library for direct HTTP calls without the async overhead of PTB.

## ✨ Key Features

### 🧠 Generative AI Integration
* **Gemini 2.5 Flash:** Utilizes `langchain-google-genai` to tap into Google's efficient large language model for generating context-aware content.
* **Custom Prompting:** Specifically engineered to create short, impactful quotes for developers, stripping away unnecessary conversational filler.

### 🛡️ Robust Orchestration
* **Prefect Flows:** Wraps logic in resilient tasks with automatic **Retry Policies** (3 retries, 5s delay) to handle potential API timeouts.
* **Error Handling:** Graceful exception management ensures the flow logs errors clearly (e.g., Auth failures, Network issues) without exposing sensitive API keys.

### 📨 Async Delivery (PTB)
* **Python Telegram Bot:** Uses the modern `python-telegram-bot` library with asynchronous execution (`asyncio`) for reliable, non-blocking message delivery.
* **Markdown Support:** Sends messages with proper formatting to ensure readability.

## 🛠️ Tech Stack
* **Orchestrator:** Prefect (Workflow Management)
* **Language:** Python 3.11
* **AI Provider:** Google Gemini API (`langchain-google-genai`)
* **Notification:** Python Telegram Bot (`python-telegram-bot`)
* **Environment Management:** `python-dotenv`

## 🚀 The Automation Pipeline
1.  **Generate:** Connects to Google Gemini to synthesize a fresh motivational quote.
2.  **Validate:** Ensures the API response is valid and extracts the core message.
3.  **Load (Publish):** Asynchronously pushes the generated text to the specified Telegram Chat via the Bot API.
4.  **Log:** Prints the interaction details to the console for monitoring.

## ⚙️ Configuration (Environment Variables)
Create a `.env` file in the root directory:
```ini
GOOGLE_API_KEY=your_google_gemini_api_key
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_target_chat_id
```

## 📦 Local Installation
1. **Clone the Repository**
```bash
git clone https://github.com/viochris/daily-quote-bot-ptb.git
cd daily-quote-bot-ptb
```

2. **Install Dependencies**
```bash
pip install prefect langchain-google-genai python-telegram-bot python-dotenv
```

3. **Run the Automation**
```bash
python quote-Telegram-Bot.py
```

### 🖥️ Expected Output
You should see **Prefect** orchestrating the tasks in real-time:
```text
10:00:00.123 | INFO    | Flow run 'Daily Mentor Flow' - Process Started
10:00:00.456 | INFO    | Task run 'Generate Quote' - ⏰ ACTION TIME! Initiating connection to Gemini AI...
------------------------------------------------
🤖 AI MENTOR SAYS:
"Code is like humor. When you have to explain it, it’s bad."
------------------------------------------------
10:00:02.789 | INFO    | Task run 'Generate Quote' - Finished in state Completed()
10:00:03.112 | INFO    | Task run 'Send to Telegram' - 🚀 Sending message via Python-Telegram-Bot...
10:00:03.223 | INFO    | Task run 'Send to Telegram' - ✅ Success: Message sent to Telegram (via PTB)!
10:00:03.334 | INFO    | Flow run 'Daily Mentor Flow' - Finished in state Completed()
```

## 🚀 Deployment Options
This bot supports two release methods depending on your infrastructure:
| Method | Description | Use Case |
| --- | --- | --- |
| **GitHub Actions** | **Serverless.** Uses `cron` scheduling in `.github/workflows/daily_quote.yml`. Runs on GitHub servers for free. | Best for daily/scheduled runs without paying for a VPS. |
| **Local / VPS** | **Always On.** Uses `main_flow.serve()` to run as a background service. | Best if you need sub-minute updates or complex triggers. |

---

**Author:** [Silvio Christian, Joe](https://www.linkedin.com/in/silvio-christian-joe)
*"Code automated, motivation daily."*
