import os
from dotenv import load_dotenv
from mongodbConnect import MongoDBManager
from job_scrapper import jobScrapper
from ai_manager import AI_Summary, jobTips
import tweepy


def test_env():
    print("--- Testing Environment Variables ---")
    load_dotenv()
    vars_to_check = [
        "MONGODB_URI", "X_ACCESS_TOKEN", "X_API_KEY", "GEMINI_API_KEY"
    ]
    for var in vars_to_check:
        val = os.getenv(var)
        status = "LOADED" if val else "MISSING"
        print(f"{var}: {status}")

def test_mongodb():
    print("\n--- Testing MongoDB Connection ---")
    try:
        client = MongoDBManager.get_client()
        if client:
            client.admin.command('ismaster')
            print("MongoDB connection successful!")
        else:
            print("MongoDB client not available.")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

def test_scraper():
    print("\n--- Testing Scraper ---")
    try:
        # We'll just check if it can fetch and parse something
        result = jobScrapper()
        print(f"Scraper Result: {result}")
    except Exception as e:
        print(f"Scraper failed: {e}")

def test_twitter():
    print("\n--- Testing Twitter Client Initialization ---")
    try:
        from createxpost import get_twitter_client
        client = get_twitter_client()
        print("Twitter client initialized successfully (logic only, no tweet sent).")
    except Exception as e:
        print(f"Twitter client failed to initialize: {e}")

def test_openai():
    print("\n--- Testing OpenAI Integration ---")
    try:
        tip = jobTips()
        print(f"OpenAI Tip: {tip}")
        summary = AI_Summary("Software Engineer at Google with 5 years experience in Python.", "https://example.com/job")
        print(f"OpenAI Summary: {summary}")
    except Exception as e:
        print(f"OpenAI test failed: {e}")

if __name__ == "__main__":
    test_env()
    test_mongodb()
    test_scraper()
    test_twitter()
    test_openai()




