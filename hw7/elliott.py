import re

def GetUserInput():
    while(True):
        twitterUsername = input("Please input a Twitter username: ")
        #Per Twitter's website, usernames are alphanumeric with optional underscores
        if re.match(r'^\w+$', twitterUsername):
            return twitterUsername
        print("Twitter usernames must be alphanumeric and optionally include underscores")
        continue

# Main
if __name__ == "__main__":
    # Get user input
    while(True):
        username = GetUserInput()

        if username == 'STOP':
            break