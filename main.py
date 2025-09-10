import os
import re
import datetime
import requests
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from tavily import TavilyClient
import yfinance as yf
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from litellm import completion

load_dotenv()

print("🔍 Performing initial news search with Tavily...")
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY is not set in the .env file.")

client = TavilyClient(api_key=tavily_api_key)
try:
    search_results = client.search(query="US financial markets news last 24 hours", search_depth="basic", max_results=5)
    search_content = str(search_results['results'])
    print("✅ Search complete.")
except Exception as e:
    print(f"❌ Error during Tavily search: {e}")
    search_content = "No search results found due to an error."



analyst = Agent(
    role='Senior Financial News Analyst',
    goal='Analyze the provided financial news data and identify the most significant points',
    backstory=(
        "You are an expert financial analyst. You don't search for news yourself, "
        "but you are a master at analyzing raw news data provided to you and extracting key insights."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[]
)

writer = Agent(
    role='Expert Financial Analyst and Multilingual Writer',
    goal='Create a concise financial summary based on the analysts report and translate it into Arabic, Hindi, and Hebrew',
    backstory=(
        "You are a skilled financial writer who takes an analysts report and crafts a clear, engaging summary for the public. "
        "You are also a master linguist, fluent in English, Arabic, Hindi, and Hebrew."
    ),
    verbose=True,
    allow_delegation=False,
)


analysis_task = Task(
    description=(
        "Analyze the following raw financial news data. Identify the top 3-5 most significant market-moving stories, "
        "key stock performances, and any major economic announcements. "
        "Here is the raw data to analyze:\n\n"
        f"--- RAW NEWS DATA ---\n{search_content}\n--- END OF RAW NEWS DATA ---"
    ),
    expected_output='A structured report with bullet points highlighting the most important news and insights.',
    agent=analyst
)

write_task = Task(
    description=(
        "Review the analysts report and write a final, compelling summary for the public. "
        "The summary must be less than 500 words. After writing the summary, translate the final English summary "
        "into three languages: Arabic, Hindi, and Hebrew. Present the final output as a single block of text with the "
        "English summary first, followed by each translation under a clear heading (e.g., '--- ARABIC TRANSLATION ---')."
    ),
    expected_output='A single text block containing the English summary and its three translations.',
    agent=writer
)

financial_crew = Crew(
    agents=[analyst, writer],
    tasks=[analysis_task, write_task],
    process=Process.sequential,
    verbose=True
)

print("🚀 The Financial News Crew is starting its work...")
final_report_text = financial_crew.kickoff().raw

print("\n\n########################")
print("## Crew Work Complete. Final Report Text:")
print(final_report_text)
print("########################\n")

print("🖼️ Finding and downloading related images...")
summary_part = final_report_text.split("---")[0]
tickers = re.findall(r"\b[A-Z]{1,5}\b", summary_part)
if not tickers:
    tickers = ["S&P 500", "NASDAQ Composite"] 

image_filenames = []
for topic in list(set(tickers))[:2]: 
    try:
        image_search_results = client.search(query=f"latest financial chart for {topic}", search_depth="basic", include_images=True)
        if image_search_results.get('images'):
            image_url = image_search_results['images'][0]
            response = requests.get(image_url, stream=True)
            response.raise_for_status() 
            
            filename = f"image_{topic.replace(' ', '_')}.jpg"
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            image_filenames.append(filename)
            print(f"✅ Downloaded image for {topic}")

    except Exception as e:
        print(f"Could not find or download image for {topic}: {e}")


print("📊 Generating final PDF report...")
try:
    pdf_path = "daily_market_summary_v2.pdf" 
    run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    w, h = letter
    text_obj = c.beginText(40, h - 40)
    text_obj.setFont("Helvetica-Bold", 14)
    text_obj.textLine(f"Daily Market Summary ({run_time})")
    text_obj.textLine("")
    from reportlab.pdfbase import ttfonts, pdfmetrics
    try:
        pdfmetrics.registerFont(ttfonts.TTFont('Arial', 'Arial.ttf'))
        text_obj.setFont("Arial", 10)
    except:
        text_obj.setFont("Helvetica", 10)
        print("Arial font not found, some characters may not render correctly in the PDF.")
    for line in final_report_text.split('\n'):
        text_obj.textLine(line)
        if text_obj.getY() < 100:
            c.drawText(text_obj)
            c.showPage()
            text_obj = c.beginText(40, h-40)
            text_obj.setFont("Arial" if 'Arial' in pdfmetrics.getRegisteredFontNames() else "Helvetica", 10)
    c.drawText(text_obj)
    for img in image_filenames:
        c.showPage()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, h - 40, "Related Images Found")
        c.drawImage(img, 40, h - 400, width=500, preserveAspectRatio=True)
    c.save()
    print(f"✅ Successfully created updated PDF: {pdf_path}")
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        print("📲 Sending updated report to Telegram...")
        url = f"https://api.telegram.org/bot{token}/sendDocument"
        with open(pdf_path, "rb") as f:
            files = {"document": f}
            data = {"chat_id": chat_id, "caption": f"Updated Daily Market Summary {run_time}"}
            response = requests.post(url, files=files, data=data, timeout=30)
            if response.status_code == 200:
                print("✅ Report sent successfully to Telegram.")
            else:
                print(f"❌ Failed to send to Telegram: {response.text}")
except Exception as e:
    print(f"❌ An error occurred during PDF creation or sending: {e}")
