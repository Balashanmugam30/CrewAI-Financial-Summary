````markdown
# CrewAI Financial Market Summary Agent 🚀📈

Automate your daily US financial market insights with AI-powered summaries, relevant images, and multilingual reports—delivered straight to your Telegram!  

This Python-based multi-agent system leverages the **CrewAI framework** to generate and distribute a professional financial market summary every day after US markets close.

---

## 🌟 Features

- **Automated News Gathering** 📰  
  Fetches the latest US financial news using the Tavily API.  

- **AI-Powered Summarization** 🤖  
  Uses LLMs to analyze news and create concise, insightful market summaries.  

- **Multilingual Translation** 🌐  
  Translates the summary into **Arabic, Hindi, and Hebrew**.  

- **Related Image Discovery** 🖼️  
  Finds and downloads relevant charts or images from the web based on the news summary’s content.  

- **PDF Report Generation** 📝  
  Compiles the summary, translations, and found images into a professional PDF document.  

- **Automated Distribution** 📬  
  Sends the final PDF to a designated Telegram channel automatically.  

---

## 🛠 Tech Stack

- **Language:** Python  
- **Framework:** CrewAI (latest)  
- **LLM Provider:** LiteLLM with OpenAI GPT-3.5-Turbo  
- **Search Tool:** Tavily  
- **PDF Generation:** reportlab  

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Balashanmugam30/CrewAI-Financial-Summary.git
cd CrewAI-Financial-Summary
````

### 2. Create a Virtual Environment

```bash
python -m venv .venv
# On Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install crewai crewai-tools litellm "tavily-python" yfinance matplotlib reportlab python-dotenv requests
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add the following keys:

```
TAVILY_API_KEY="your_tavily_api_key"
OPENAI_API_KEY="your_openai_api_key"
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
TELEGRAM_CHAT_ID="your_telegram_channel_id"
```

---

## ▶️ How to Run

```bash
python main.py
```

The script will execute the entire workflow and send the report to your Telegram channel.

---

## 🚀 Why This Project is Awesome

* Fully automated end-to-end financial report system.
* Multilingual support for global reach.
* Finds and embeds real market-related images and charts.
* Professional PDF reports, ready for executives.
* Demonstrates advanced AI integration and multi-agent coordination.

---

## 🔮 Future Improvements

* Add support for more languages.
* Include additional sources for image discovery.
* Schedule daily reports with cron or a cloud function.

---

Made with ❤️ by **Balashanmugam S**
