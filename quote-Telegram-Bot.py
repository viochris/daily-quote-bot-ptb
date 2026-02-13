import os
import asyncio
from prefect import flow, task
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Import Library Telegram Bot
from telegram import Bot 
from telegram.error import TelegramError, NetworkError

# Load environment variables (useful for local testing)
load_dotenv()

# Fetch credentials from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@task(name="Generate Quote", retries=3, retry_delay_seconds=5)
def generate_quote():
    """
    Task to generate a motivational quote using Google Gemini AI.
    """
    # 1. Initialization Log
    print("\n⏰ ACTION TIME! Initiating connection to Gemini AI...")

    try:
        # 2. Model Configuration
        # Initialize the Gemini client with the specific Flash model and API Key.
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.7
        )

        # 3. Prompt Engineering
        # Define the instruction for the AI (Requesting English Quote).
        # Ensures the output is clean without conversational filler.
        prompt_text = "Create 1 short, punchy motivational quote for a programmer. Just the quote, no intro text."
        
        # 4. API Execution
        # Invoke the model and extract the text content from the response object.
        response = llm.invoke(prompt_text)
        ai_msg = response.content

        # 5. Console Logging
        # Display the result in the terminal for real-time verification.
        print("------------------------------------------------")
        print(f"🤖 AI MENTOR SAYS:\n{ai_msg}")
        print("------------------------------------------------")

        # 6. Output Delivery
        # Return the valid quote string to be used by the downstream task.
        return ai_msg

    except Exception as e:
        # 7. Secure Error Handling
        # Convert the raw exception to a lowercase string for safe parsing.
        # We strictly avoid printing 'e' directly to prevent API Key leakage in logs.
        error_str = str(e).lower()
        
        # 8. Error Categorization
        # Identify specific Google API errors to provide user-friendly feedback.
        if "401" in error_str or "api_key" in error_str:
            safe_msg = "❌ Gemini Auth Error: Invalid API Key."
        elif "429" in error_str or "quota" in error_str:
            safe_msg = "⏳ Gemini Quota Error: Rate limit exceeded."
        elif "connection" in error_str:
            safe_msg = "❌ Gemini Network Error: Failed to connect."
        else:
            safe_msg = "❌ Gemini Internal Error (Details hidden)."

        # 9. Failure Trigger
        # Print the safe message and raise Exception to trigger Prefect's retry mechanism.
        print(safe_msg)
        raise Exception(safe_msg)

@task(name="Send to Telegram")
def to_telegram(msg):
    """
    Task to send the generated message to a specific Telegram Chat.
    """
    # 1. Credential Validation
    # Ensure that the necessary Telegram API credentials exist before proceeding.
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Error: Telegram credentials are missing.")
        raise ValueError("Missing Telegram Credentials")

    # 2. Async Wrapper Definition
    # Define an inner asynchronous function to handle the 'python-telegram-bot' logic
    # because the library requires 'await' for network operations.
    async def send_via_ptb():
        # Initialize the Bot instance using the secure token
        bot = Bot(token=TELEGRAM_TOKEN)
        print("🚀 Sending message via Python-Telegram-Bot...")

        # Send the actual message using the bot instance
        await bot.sendMessage(
            chat_id= TELEGRAM_CHAT_ID,
            text= msg,
            parse_mode= "Markdown"
        )

    try:
        # 3. Execution Bridge
        # Use asyncio.run() to execute the async function within this synchronous Prefect task.
        asyncio.run(send_via_ptb())
        print("✅ Success: Message sent to Telegram (via PTB)!")
            
    except Exception as e:
        # 4. Secure Error Handling
        # Convert exception to string for safe analysis.
        # This prevents the 'url' variable (which might contain the token) from leaking in the logs.
        error_str = str(e).lower()
        safe_msg = ""

        # 5. Error Categorization
        # Identify the type of error to provide a clear, safe log message.
        if "connection" in error_str or "dns" in error_str:
            safe_msg = "❌ Network Error: Failed to connect to Telegram API."
        elif "timeout" in error_str:
            safe_msg = "⏳ Timeout Error: Telegram API did not respond."
        elif "ssl" in error_str:
            safe_msg = "🔒 SSL Error: Certificate verification failed."
        else:
            safe_msg = "❌ Telegram Send Failed: Unknown error occurred."
            
        # Log the sanitized message to the console
        print(safe_msg)
        
        # 6. Trigger Failure
        # Raise the exception so Prefect marks the task as 'Failed' and triggers the retry mechanism.
        raise Exception(safe_msg)

@flow(name="Daily Mentor Flow", log_prints=True)
def main_flow():
    """
    Main orchestration flow:
    1. Get Quote -> 2. Send to Telegram
    Because we use 'raise', we don't need 'if quote:' checks anymore.
    """
    quote = generate_quote()
    to_telegram(quote)

if __name__ == "__main__":
    # ==========================================
    # 🚀 EXECUTION MODE
    # ==========================================

    # --- OPTION 1: FOR GITHUB ACTIONS (ACTIVE) ---
    # This calls the function immediately (Run Once).
    # GitHub's YAML scheduler handles the timing (CRON).
    # When finished, the script exits to save server resources.
    main_flow()

    # --- OPTION 2: FOR LOCAL SERVER / VPS (COMMENTED OUT) ---
    # Use this if you run the script on your own laptop or a 24/7 server.
    # The '.serve()' method keeps the script running indefinitely 
    # and handles the scheduling internally.
    
    # main_flow.serve(
    #     name="deployment-mentor-pagi",
    #     # cron="0 7 * * *", # Run daily at 07:00 AM (server time)
    #     interval=10,        # Or run every 10 seconds (for testing)
    #     tags=["ai", "daily"]
    # )