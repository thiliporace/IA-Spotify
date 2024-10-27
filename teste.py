import csv
import os
import re

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID", "09f25e82858a47a2b4580e68e6efecdd")
CLIENT_SECRET = os.getenv("CLIENT_SECRET","79cc894e039440a4a69ee3c728e5829a")
OUTPUT_FILE_NAME = "track_info.csv"

PLAYLIST_LINK = "https://open.spotify.com/playlist/6JQN1t4ArWfOT7blwmWqG5?si=wNqUr5JgTyir3lB8eqr9nQ"

# authenticate
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

# create spotify session object
session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# get uri from https link
if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
    playlist_uri = match.groups()[0]
else:
    raise ValueError("Expected format: https://open.spotify.com/playlist/...")

# get list of tracks in a given playlist (note: max playlist length 100)
tracks = session.playlist_tracks(playlist_uri)["items"]

# create csv file
with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    artists_ids = []

    # write header column names
    writer.writerow(["track", "artist","popularity","genres"])

    # extract name and artist
    for index, track in enumerate(tracks):
        name = track["track"]["name"]
        artists = ", ".join(
            [artist["name"] for artist in track["track"]["artists"]]
        )

        for artist in track["track"]["artists"]:
            artists_ids.append(artist["id"])

        artists_data = session.artists(artists_ids)
        
        popularity = track["track"]["popularity"]

        artist_list = []
        # write to csv
        for artist in artists_data["artists"]:
            artist_list.append(artist["genres"])
        
        writer.writerow([name, artists, popularity,artist_list[index]])
    

    reader = csv.reader(open("track_info.csv", "rb"))

    
        


