import tweepy

access_token = "1793711715835666432-az5RXZ6j1h8AnaKFERGablXGZjYIws"
access_token_secret = "RLWysRilQQDSer3HndFE16AFEibM6LvAlu7vaBu0AzISb"
bearer_token = r"AAAAAAAAAAAAAAAAAAAAACUXwAEAAAAAUJENIAH%2BbGK%2BqWjQ3V5PiVT2OEI%3DaDxhIX3mNZdjlejcnkZG7PiGdKPNe2Qc8Ba3NNboxHqbovSJTP"
api_key = "FUNlslh7IpEji2ZEnu95lky4q" #api-key
api_secret = "DaCcAnkCcLt0s1MMFAfI5VTZHKnFyuyz9H1r3Aq6Dmk4BRjuD6" #api key secret
client_id = 'NUh4U1k4ZDd5SFVjVXFZU3Rjb0s6MTpjaQ'
client_secret = 'hFSS8dSCesfv2xG4FAoKch6HRkjABeuhN-SUPkn0z3avt0ZZK_'

# auth = tweepy.OAUTHHandler(client_id, client_secret)
# auth.set_access_token(access_taken, access_token_secret)
# api = tweepy.API(auth, wait_on_rate_limit=True)

# Set up OAuth and integrate with Tweepy
# auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
# api = tweepy.API(auth)

client = tweepy.Client(
    bearer_token,
    api_key, 
    api_secret, 
    access_token, 
    access_token_secret
)


auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

client.create_tweet(
    text="Hello World!"
)

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