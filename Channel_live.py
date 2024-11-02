# -*- coding: utf-8 -*-

import os
import googleapiclient.discovery

def channel_id(channel_id):
    # Define API service name and version
    api_service_name = "youtube"
    api_version = "v3"
    api_key = "[Your API KEY]"  # Replace with your API key

    # Create a YouTube client
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    # Make a request to the YouTube API
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,  # Use the passed channel ID
        eventType="live",
        maxResults=25,
        q="live",
        type="video"
    )
    
    # Execute the request and get the response
    result = request.execute()
    video_playlist = {}
    for item in result['items']:
        video_title = item['snippet']['title']
        video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        video_playlist[video_title] = video_url
    
    # Return the response
    return video_playlist

# Call the function and print the result
#Example:
print(channel_id("UCLA_DiR1FfKNvjuUpBHmylQ"))

#now i have to return a dictionary with the video title and the video url

