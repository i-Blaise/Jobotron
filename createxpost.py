import time
import os
from dotenv import load_dotenv
import tweepy
from logs import logProcesses

load_dotenv()

def get_twitter_client():
    """Initializes and returns a Tweepy Client."""
    return tweepy.Client(
        bearer_token=os.getenv("X_BEARER_TOKEN"),
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
    )

def postJob(post, max_retries=3):
    """Posts a tweet with exponential backoff retry logic."""
    retry_count = 0
    backoff_factor = 2 # Seconds to wait initially
    
    while retry_count <= max_retries:
        try:
            client = get_twitter_client()
            
            # Attempt to create a tweet
            client.create_tweet(text=post)
            response = "Tweet posted successfully!"
            results = {
                "status": True,
                "response": response
            }
            logProcesses(results["response"])
            return results
            
        except tweepy.TweepyException as e:
            # Check if it's a 503 Service Unavailable or other transient error
            error_msg = str(e)
            is_transient = "503" in error_msg or "Service Unavailable" in error_msg
            
            if is_transient and retry_count < max_retries:
                retry_count += 1
                wait_time = backoff_factor ** retry_count
                msg = f"X API Service Unavailable (503). Retrying in {wait_time}s... (Attempt {retry_count}/{max_retries})"
                print(msg)
                logProcesses(msg)
                time.sleep(wait_time)
                continue
            
            response = f"An error occurred with Tweepy: {e}"
            results = {
                "status": False,
                "response": response
            }
            logProcesses(results["response"])
            return results
        except Exception as e:
            response = f"Unexpected error in postJob: {e}"
            results = {
                "status": False,
                "response": response
            }
            logProcesses(results["response"])
            return results












# def postJob(post):
#     client = tweepy.Client(
#         bearer_token,
#         api_key, 
#         api_secret, 
#         access_token, 
#         access_token_secret
#     )


#     auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
#     api = tweepy.API(auth)

#     client.create_tweet(
#         text = post
#     )

# Post a tweet
# tweet = "Hello, world! :)"
# api.update_status(status=tweet)

# try:
#     api.update_status(status=tweet)
#     print("Tweet posted successfully!")
# except tweepy.TweepyException as e:
#     print(f"Error occurred: {e}")


# print("Tweet posted successfully!")

# text = 'Hello World'

# client.create_tweet(text=text)
# print('tweeted')