import tweepy
from logs import logProcesses
import env_config

def get_twitter_client():
    """Initializes and returns a Tweepy Client."""
    return tweepy.Client(
        bearer_token=env_config.X_BEARER_TOKEN,
        consumer_key=env_config.X_API_KEY,
        consumer_secret=env_config.X_API_SECRET,
        access_token=env_config.X_ACCESS_TOKEN,
        access_token_secret=env_config.X_ACCESS_TOKEN_SECRET
    )

def postJob(post):
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