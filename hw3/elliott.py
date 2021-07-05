#!/usr/bin/env python3

#  Caleb Elliott
#  CS 581 Online Social Networks
#  Purpose of assignment is to provide experience with data retreival and
#  analyzing data via a social network's API (youtube in this case)

# USAGE: python3 elliott.py
#        user will then be prompted to enter a search parameter and the max number of results

from copy import deepcopy
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
        if maxResults.isnumeric() and int(maxResults) > 0:
            break
        print("Error: positive integers only")
    
    return [searchTerm, int(maxResults)]

def PerformYoutubeSearch(searchTerm, maxResults):
    print("Performing search for: " + searchTerm + "\n" +
        "Max Results: " + str(maxResults))
        
    # Build search service and search using the search term
    with build('youtube', 'v3') as youtube:
        searchResults = youtube.search().list(part="id,snippet", maxResults=maxResults, type="video", q=searchTerm).execute()
        results = []
        while len(results) < maxResults:
            results += searchResults['items']
            #Only continue searching if there is another page
            if not 'nextPageToken' in searchResults:
                break
            nextPage = searchResults['nextPageToken']
            searchResults = youtube.search().list(part="id,snippet", maxResults=maxResults, type="video", pageToken=nextPage).execute()
        return results[:maxResults]

# Taken from https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

def PerformStatisticsRetrieval(videoList): 
    # id to stats dict of the form 'id' : {title:'', likes:'', ...}
    videoIdDict = {vid['id']['videoId'] : {'title' : vid['snippet']['title']} for vid in videoList}
    videoIds = list(videoIdDict.keys())

    # Max number of ids that can be queried at once
    MAX_YOUTUBE_API = 50
    chunkedIds = list(divide_chunks(videoIds, MAX_YOUTUBE_API))

    for idChuck in chunkedIds:
        # Comma delimited ids to be used in query
        commaDelimIds = ",".join(idChuck)

        # Build videos service and query using video ids
        with build('youtube', 'v3') as youtube:
            videoStatisticsResults = youtube.videos().list(part="statistics,contentDetails", id=commaDelimIds).execute()
            for stat in videoStatisticsResults['items']:
                vidId = stat['id']
                vidDuration = '0'
                vidViewCount = '0'
                vidLikeCount = '0'
                vidDislikeCount = '0'

                if 'duration' in stat['contentDetails']:
                    vidDuration = stat['contentDetails']['duration']
                if 'viewCount' in stat['statistics']:
                    vidViewCount = stat['statistics']['viewCount']
                if 'likeCount' in stat['statistics']:
                    vidLikeCount = stat['statistics']['likeCount']
                if 'dislikeCount' in stat['statistics']:
                    vidDislikeCount = stat['statistics']['dislikeCount']

                videoIdDict[vidId]['videoDuration'] = vidDuration
                videoIdDict[vidId]['viewCount'] = vidViewCount
                videoIdDict[vidId]['likeCount'] = vidLikeCount
                videoIdDict[vidId]['dislikeCount'] = vidDislikeCount

    return videoIdDict

def SortByLikeViewRatio(videoStatistics):
    videoStatsCopy = deepcopy(videoStatistics)
    for videoKey in videoStatistics:
        views = int(videoStatsCopy[videoKey]['viewCount'])
        likes = int(videoStatsCopy[videoKey]['likeCount'])

        # A ratio of -1 will indicate an invalid ratio (i.e. cannot divide by 0)
        ratio = -1
        if views != 0:
            ratio = likes / views
        videoStatsCopy[videoKey]['viewToLikeRatio'] = ratio
    # Creates a sorted list based on view to like ratio (descending).
    # this single line is a modified line of code found on stackoverflow
    sortedList = [(k , v) for k, v in sorted(videoStatsCopy.items(), key = lambda item: item[1]['viewToLikeRatio'], reverse=True)]
    return sortedList

def OutputTop5(sortedList):
    print("Title | Like % | Views | Likes")
    count = 1
    for result in sortedList:
        # Pull out relevant stats from dict
        stats = result[1]
        title = stats['title']
        viewLikeRatio = str(stats['viewToLikeRatio'] * 100) + '%'
        views = stats['viewCount']
        likes = stats['likeCount']

        # Stop printing after 5 iterations or when the ratio is no longer valid
        if count == 6 or float(stats['viewToLikeRatio']) < 0:
            break
        
        print("#" + str(count) + ": " + title + " | " + viewLikeRatio + " | " + views + " | " + likes)
        count += 1

def OutputAll(sortedList):
    print("Video Id | Views | Likes | Dislikes | Duration | Title")
    count = 1
    for result in sortedList:
        # Pull out relevant stats from dict
        vidId = result[0]
        stats = result[1]
        title = stats['title']
        views = stats['viewCount']
        likes = stats['likeCount']
        dislikes = stats['dislikeCount']
        duration = stats['videoDuration']
        asList = [vidId, views, likes, dislikes, duration, title]
        dataString ="#" + str(count) + ": " +  " | ".join(asList) + "\n"
        
        print(dataString)
        count += 1

def WriteToFile(sortedList):
    header = "Video Id,Views,Likes,Dislikes,Duration,Title"
    fileString = header + "\n"
    for result in sortedList:
        # Pull out relevant stats from dict
        vidId = result[0]
        stats = result[1]
        title = stats['title']
        views = stats['viewCount']
        likes = stats['likeCount']
        dislikes = stats['dislikeCount']
        duration = stats['videoDuration']
        asList = [vidId, views, likes, dislikes, duration, title]
        fileString += ",".join(asList) + "\n"
    fp = os.getcwd()
    fileHandle = open(os.path.join(fp, "data.csv"), "w")
    fileHandle.write(fileString)

def OutputResults(sortedList):

    OutputTop5(sortedList)
    OutputAll(sortedList)
    WriteToFile(sortedList)
    

# Main
if __name__ == "__main__":
    # Get user input
    searchTerm,maxResults = GetUserInput()
    
    # Get search results
    videoList = PerformYoutubeSearch(searchTerm, maxResults)

    # Get statistics for videos in search results
    videoStatistics = PerformStatisticsRetrieval(videoList)

    # Sort videos using the statistics
    sortedList = SortByLikeViewRatio(videoStatistics)

    # Print and save result
    OutputResults(sortedList)