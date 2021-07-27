import re
import tweepy

CONSUMER_KEY = "pfKTHRsx7gCLi1DLyE0hDwJXX"
CONSUMER_KEY_SECRET = "QD94r7SCxMCYkRAkAHrFIwE7vWKNp7t0vGRfQ9Q6mSGQR176Qu"
ACCESS_TOKEN = "1417232109043863553-Udp4AZJofYKQKH6NB9pvQBLNNPoTlz"
ACCESS_TOKEN_SECRET = "RBgHB9QozmI5SSzb5VAdqjCsgTsADFJd6wkJFUWV34VEN"

authenticate = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(authenticate, wait_on_rate_limit=True, 
                 wait_on_rate_limit_notify=True)

def GetUserInput():
    while(True):
        twitterUsername = input("Please input a Twitter username: ")
        #Per Twitter's website, usernames are alphanumeric with optional underscores
        if re.match(r'^\w+$', twitterUsername):
            return twitterUsername
        print("Twitter usernames must be alphanumeric and optionally include underscores")
        continue

def GetTwitterData(username):
    user = None
    try:
        user = api.get_user(username)
    except:
        print("Unable to retrieve information for user: " + username)
        return

    screenName = user.screen_name
    name = user.name
    userID = user.id_str
    location = user.location
    numFriends = user.friends_count
    numFollowers = user.followers_count

    followers = user.followers(count=5)
    if len(followers) == 0:
        print(username + " has no followers")
    for follower in followers:
        print(follower.screen_name)

    tweets = tweepy.Cursor(api.user_timeline, screen_name=username, include_rts=False, exclude_replies=True)
    count = 1
    for tweet in tweets.items():
        print("TWEET"+str(count)+": " + tweet.text + "\n")
        count += 1
        if count == 6:
            break
    if count == 1:
        print(username + " has no tweets")


# Main
if __name__ == "__main__":
    # Get user input
    while(True):
        username = GetUserInput()
        if username == 'STOP':
            print("*--Terminating Program--*")
            break

        twitterData = GetTwitterData(username)