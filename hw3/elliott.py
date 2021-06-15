#!/usr/bin/env python3

from googleapiclient.discovery import build      # use build function to create a service object
import os

# Provides api key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/mnt/c/Users/caleb/Documents/git/Online_Social_Networks_CS581/hw3/cs581elliott-4c2e3cfe3662.json"

# Gets search term and max results
# Max results must be an integer
def GetUserInput():
    searchTerm = ""
    maxResults = 1

    searchTerm = input("Please input a search term: ")
    
    # Loop until integer is entered
    while(True):
        maxResults = input("Please input max results: ")
        if maxResults.isnumeric():
            break
        print("Error: input integers only")
    
    return [searchTerm, int(maxResults)]

def PerformYoutubeSearch(searchTerm, maxResults):
    print("Performing search for: " + searchTerm + "\n" +
        "Max Results: " + str(maxResults))
    with build('youtube', 'v3') as youtube:
        searchResults = youtube.search().list(part="id,snippet", maxResults=maxResults, type="video", q=searchTerm).execute()
        for result in searchResults['items']:
            print("Title: " + result['snippet']['title'])

# Main
if __name__ == "__main__":
    # Get user input
    searchTerm,maxResults = GetUserInput()
    
    PerformYoutubeSearch(searchTerm, maxResults)