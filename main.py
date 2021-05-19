import tweepy as t
import logging
import time
import os
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger()

def auth_cred(): #authentication process
    api_token = os.getenv('API_KEY')
    api_secret = os.getenv('API_SECRET')
    auth_token = os.getenv('ACCESS_KEY')
    auth_secret_token = os.getenv('ACCESS_SECRET')

    auth = t.OAuthHandler(api_token , api_secret) #using oauth authetication is done
    auth.set_access_token(auth_token , auth_secret_token)

    global api # referred as global for it being used outside the function
    api = t.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True) #api is been declared


    try:  #verifying the credentials
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


# def since_id(): #since_id inorder to fetch the id of the last tweet(feature)
#     tweety = []
#     for tweet in t.Cursor(api.mentions_timeline).items():
#         if len(tweety) > 1:
#             break
#         else:
#             tweety.append(tweet)
#             new_tweet = tweety[0].id
#         return new_tweet

def data_txt(obj):
    file = open('data.txt','w')
    file.write(obj)
    file.close()

def Mention(api,since_id): #mentioning function

    logger.info("Collecting info")

    new_since_id = since_id

    for tweet in t.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)

        if tweet.in_reply_to_status_id is not None:
            status_id = tweet.in_reply_to_status_id
            tweet_re = api.get_status(status_id,tweet_mode='extended')
            print(tweet_re.full_text)
    return new_since_id

def main():
    api = auth_cred()
    id = 1 #the last mention you have.
    while True:
        print(id)
        mention = Mention(api,id)
        data_txt(mention)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
