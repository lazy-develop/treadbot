import tweepy
import time
import os
from dotenv import load_dotenv
load_dotenv()
def auth_cred(): #authentication process
    # api_token = os.getenv('API_KEY')
    # api_secret = os.getenv('API_SECRET')
    # auth_token = os.getenv('ASCCESS_KEY')
    # auth_secret_token = os.getenv('ACCESS_SECRET')

    auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET")) #using oauth authetication is done
    auth.set_access_token(os.getenv("ACCESS_KEY"), os.getenv("ACCESS_SECRET"))

    global api # referred as global for it being used outside the function
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True) #api is been declared


    try:  #verifying the credentials
        api.verify_credentials()
    except Exception as e:
        print("Error creating API")
        raise e
    return api

def recipt():
    mention = api.mentions_timeline(count= 1)
    global tweet
    for tweet in mention:
        return tweet.user.id

def recipt_1():
    text = open("id.txt", 'w')
    i = str(recipt())
    text.write(i)
    text.close()

def syst():
    m = open("id.txt","r")
    last_1 = m.readlines(1)
    for line3 in last_1:
        return line3


def message():
    x = open('mx.txt','r')
    m = x.readlines(1)
    for lines in m:
        return lines



def mention(api,since_id):

    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():

        new_since_id = max(tweet.id, new_since_id)

        if tweet.in_reply_to_status_id is not None:

            if not tweet.user.following:
                tweet.user.follow()

            status_id = tweet.in_reply_to_status_id
            tweet_u = api.get_status(status_id,tweet_mode='extended')

            print(tweet_u.full_text)
            f = open('mx.txt', 'w')
            f.write(tweet_u.full_text)
            f.close()


    return new_since_id


def main(): #order of process being done
    api = auth_cred()
    since_id = 1 #the last mention you have.
    print(since_id)
    print('inside..') 
    d = mention(api,since_id)
    print(recipt()) 
    print(message()) 
    api.send_direct_message(recipt(),message())
    print('success.... ') 
    time.sleep(60)

if __name__ == "__main__":
    main()
