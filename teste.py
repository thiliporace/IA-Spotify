import csv
import os
import re
import pandas as pd
import matplotlib.pyplot as plt

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID", "09f25e82858a47a2b4580e68e6efecdd")
CLIENT_SECRET = os.getenv("CLIENT_SECRET","79cc894e039440a4a69ee3c728e5829a")
OUTPUT_FILE_NAME = "track_info.csv"

PLAYLIST_LINK = "https://open.spotify.com/playlist/4kaY2WgIOFd0S9ta4l4g13?si=LPk_uG3rSxKwyEu3km2ZwQ"

client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
    playlist_uri = match.groups()[0]
else:
    raise ValueError("Expected format: https://open.spotify.com/playlist/...")

tracks = session.playlist_tracks(playlist_uri)["items"]

with open(OUTPUT_FILE_NAME, "w", encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    
    artists_ids = []

    # write header column names
    writer.writerow(["track", "artist","genres","followers","popularity","year"])

    # extract name and artist
    # for index, track in enumerate(tracks):
    #     name = track["track"]["name"]
    #     artists = ", ".join(
    #         [artist["name"] for artist in track["track"]["artists"]]
    #     )

    #     for artist in track["track"]["artists"]:
    #         artists_ids.append(artist["id"])

    #     artists_data = session.artists(artists_ids)
        
    #     popularity = track["track"]["popularity"]
    #     album = track["track"]["album"]
    #     release_date = album["release_date"]

    #     splitat = 4
    #     year = release_date[:splitat]

    #     genres_list = []
    #     followers_list = []
    #     # write to csv
    #     for artist in artists_data["artists"]:
    #         genres_list.append(artist["genres"])
    #         followers_list.append(artist["followers"]["total"])
        
    #     writer.writerow([name, artists,genres_list[index],followers_list[index],popularity,year])

df = pd.read_csv(r'E:\IA Roger Roger\IA-Spotify\track_info.csv')
df.head(5)

df['genres'] = df['genres'].apply(eval)

df_filtered = df[df['genres'].apply(lambda x: 'k-pop' in ' '.join(x))]

# print(df_filtered)
del df_filtered['genres']
del df_filtered['followers']
del df_filtered['track']
del df_filtered['artist']
# print(df_filtered)

# plt.scatter(df_filtered['year'], df_filtered['popularity'])
# plt.xlabel('Year')
# plt.ylabel('Popularity')
# plt.title('Year vs Popularity')
# plt.show()

X = df_filtered[['popularity']]
y = df_filtered['year']

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.05)

lr = LinearRegression()
lr.fit(X_train, y_train)

y_pred = lr.predict(X_test)

r2 = r2_score(y_test, y_pred)

print(f'R^2 Score: {r2}')
    
