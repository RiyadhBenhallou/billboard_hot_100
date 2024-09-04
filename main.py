import requests
from bs4 import BeautifulSoup
import lxml
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

user_input = input('Enter the date you want to fetch the hot songs for in the format YYYY-MM-DD: ')

content = requests.get(f'https://www.billboard.com/charts/hot-100/{user_input}/')

soup = BeautifulSoup(content.text, 'lxml')

songs_list = soup.select('ul li #title-of-a-story')


scope = "playlist-modify-private,playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=os.environ['SPOTIFY_CLIENT_ID'], client_secret=os.environ['SPOTIFY_CLIENT_SECRET'], redirect_uri=os.environ['SPOTIFY_REDIRECT_URI']))

items = []
for song in songs_list:
    item = sp.search(song, limit=1, offset=0, type='track', market=None)
    items.append(item['tracks']['items'][0]["external_urls"]["spotify"])

sp.playlist_add_items(os.environ['PLAYLIST_ID'], items, position=None)
