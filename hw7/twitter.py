#   Author: Cheryl Dugas

#  This program accesses data from a twitter user site (hard-coded as Stevens)

#  To run in a terminal window:   python3  twitter_data.py


import tweepy

### PUT AUTHENTICATOIN KEYS HERE ###
CONSUMER_KEY = "pfKTHRsx7gCLi1DLyE0hDwJXX"
CONSUMER_KEY_SECRET = "QD94r7SCxMCYkRAkAHrFIwE7vWKNp7t0vGRfQ9Q6mSGQR176Qu"
ACCESS_TOKEN = "1417232109043863553-Udp4AZJofYKQKH6NB9pvQBLNNPoTlz"
ACCESS_TOKEN_SECRET = "RBgHB9QozmI5SSzb5VAdqjCsgTsADFJd6wkJFUWV34VEN"

# Authentication

authenticate = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#  use wait_on_rate_limit to avoid going over Twitter's rate limits
api = tweepy.API(authenticate, wait_on_rate_limit=True, 
                 wait_on_rate_limit_notify=True)
                 
# Get Information About a Twitter User Account

twitter_user = api.get_user('FollowStevens')

# Get Basic Account Information
print("twitter_user id: ", twitter_user.id)

print("twitter_user name: ", twitter_user.name)

# Determine an Account’s Friends 
friends = []

print("\nFirst 5 friends:")

# Creating a Cursor
cursor = tweepy.Cursor(api.friends, screen_name='FollowStevens')

# Get and print 5 friends
for account in cursor.items(5):
    print(account.screen_name)
    