import os
from dotenv import load_dotenv
from mongodbConnect import MongoDBManager
from job_scrapper import jobScrapper
# from gemini_ai import AI_Summary  # Dependency failed to install on Python 3.14
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

if __name__ == "__main__":
    test_env()
    test_mongodb()
    test_scraper()
    test_twitter()



