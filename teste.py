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

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID", "09f25e82858a47a2b4580e68e6efecdd")
CLIENT_SECRET = os.getenv("CLIENT_SECRET","79cc894e039440a4a69ee3c728e5829a")
OUTPUT_FILE_NAME = "track_info.csv"

PLAYLIST_LINK = "https://open.spotify.com/playlist/37i9dQZF1EIXtL62omEoXC?si=m0MWtfirSoCdM0NooEjTLw&pi=u-7GvSnvAER6GO"

client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
    playlist_uri = match.groups()[0]
else:
    raise ValueError("Expected format: https://open.spotify.com/playlist/...")

# tracks = session.playlist_tracks(playlist_uri)["items"]

# with open(OUTPUT_FILE_NAME, "w", encoding="utf-8", newline='') as file:
#     writer = csv.writer(file)
    
#     artists_ids = []

#     # write header column names
#     writer.writerow(["track", "artist","genres","followers","popularity","year"])

#     # extract name and artist
#     for index, track in enumerate(tracks):
#         name = track["track"]["name"]
#         artists = ", ".join(
#             [artist["name"] for artist in track["track"]["artists"]]
#         )

#         for artist in track["track"]["artists"]:
#             artists_ids.append(artist["id"])

#         artists_data = session.artists(artists_ids)
        
#         popularity = track["track"]["popularity"]
#         album = track["track"]["album"]
#         release_date = album["release_date"]

#         splitat = 4
#         year = release_date[:splitat]

#         genres_list = []
#         followers_list = []
#         # write to csv
#         for artist in artists_data["artists"]:
#             genres_list.append(artist["genres"])
#             followers_list.append(artist["followers"]["total"])
        
#         writer.writerow([name, artists,genres_list[index],followers_list[index],popularity,year])

df = pd.read_csv(r'E:\IA Roger Roger\IA-Spotify\track_info.csv')
df.head(5)
del df['genres']
del df['followers']
del df['track']
del df['artist']
print(df)

plt.scatter(df['year'], df['popularity'])
plt.xlabel('Year')
plt.ylabel('Popularity')
plt.title('Year vs Popularity')
plt.show()

y = df['year']
X = df[['popularity']]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2)

dt = DecisionTreeClassifier(criterion='entropy', random_state=42)
dt.fit(X_train, y_train)

y_pred = dt.predict(X_test)

print(y_train.value_counts())
print(y_test.value_counts())

print(classification_report(y_test, y_pred, zero_division=0))

accuracy = dt.score(X_test,y_test)
print(f'Acurácia do modelo: {accuracy}')
    
