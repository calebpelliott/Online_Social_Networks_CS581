#!/usr/bin/env python3

#  Caleb Elliott
#  CS 581 Online Social Networks
#  Purpose of assignment is to provide experience with data retreival and
#  displaying data via a social network's API (twitter in this case)

# USAGE: python3 elliott.py
#        user will then be prompted to enter a valid Twitter username

import re
import tweepy

# Keys and tokens
CONSUMER_KEY = "pfKTHRsx7gCLi1DLyE0hDwJXX"
CONSUMER_KEY_SECRET = "QD94r7SCxMCYkRAkAHrFIwE7vWKNp7t0vGRfQ9Q6mSGQR176Qu"
ACCESS_TOKEN = "1417232109043863553-Udp4AZJofYKQKH6NB9pvQBLNNPoTlz"
ACCESS_TOKEN_SECRET = "RBgHB9QozmI5SSzb5VAdqjCsgTsADFJd6wkJFUWV34VEN"

# Twitter API authentication
authenticate = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(authenticate, wait_on_rate_limit=True, 
                 wait_on_rate_limit_notify=True)

# Gets twitter username via console. Must be a valid twitter username.
def GetUserInput():
    while(True):
        twitterUsername = input("Please input a Twitter username: ")
        #Per Twitter's website, usernames are alphanumeric with optional underscores
        if re.match(r'^\w+$', twitterUsername):
            return twitterUsername
        print("Twitter usernames must be alphanumeric and optionally include underscores")
        continue

# Prints data from a twitter user object
def PrintUserData(user):
    screenName = user.screen_name
    name = user.name
    description = user.description
    userID = user.id_str
    location = user.location
    numFriends = user.friends_count
    numFollowers = user.followers_count

    print()
    print("Screen name: " + screenName)
    print("Name: " + name)
    print("User id: " + userID)
    print("Description: " + description)
    print("Location: " + location)
    print("Friends: " + str(numFriends))
    print("Followers: " + str(numFollowers))
    print()

# Prints n followers from a given twitter user object
def Print_n_Followers(user, n):
    print()
    print("Followers:")
    followers = user.followers(count=n)
    if len(followers) == 0:
        print(username + " has no followers")
    for follower in followers:
        print(follower.screen_name)

# Prints n cursor items' text
def Print_n_Cursor(cursor, n):
    count = 1
    print()
    for item in cursor.items(n):
        print("TWEET" + str(count) + ": " + item.text + "\n")
        count += 1
        if count == 6:
            break
    if count == 1:
        print(username + " has no tweets")

# Retrieves a user objects by using the twitter API
def GetTwitterData(username):
    user = None
    try:
        user = api.get_user(username)
    except:
        print("Unable to retrieve information for user: " + username)
        return

    PrintUserData(user)
    Print_n_Followers(user, 5)
    Print_n_Cursor(tweepy.Cursor(api.user_timeline, screen_name=username, include_rts=False, exclude_replies=True), 5)


# Main
if __name__ == "__main__":
    # Get user input
    while(True):
        username = GetUserInput()
        if username == 'STOP':
            print("*--Terminating Program--*")
            break

        twitterData = GetTwitterData(username)