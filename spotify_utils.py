# -*- coding: utf-8 -*-
"""
Created on Tue May 14 23:39:00 2024

@author: stopfer
"""


import os
import sys

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

from spotipy.oauth2 import SpotifyOAuth




def log_in_to_spotify():
    '''
    function that requires an input to log into spotify and returns the spotify object
    '''    
    scope = "playlist-modify-public"

    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    return spotify


def add_my_local_songs_to_spotfiy(path: str):
    '''
    function that add the songs from a certain path to playlists in a spotify account
    '''
    spotify = log_in_to_spotify()
    
    user_info = spotify.current_user()
    user_id = user_info['id']
    my_playlists = spotify.current_user_playlists()
    
    #iterate through the path and add the songs
    failed_songs = []
    for root_folder, sub_directoies, files in os.walk(path):
        playlist_name = root_folder.split("\\")[-1]
        if playlist_name != "Music":
            playlist_created = spotify.user_playlist_create(user_id, playlist_name)
            playlist_created_id = playlist_created['id']
            for filename in files:
                if filename.endswith('.mp3'):
                    song_name = filename[:-4]
                    try:
                        song = spotify.search(q=song_name, limit=1, type='track')
                        song_uri = [song['tracks']['items'][0]['uri']]
                        spotify.playlist_add_items(playlist_created_id, song_uri)
                        print(f"added {song_name} to {playlist_name}")
                    except:
                        failed_songs.append(song_name)
                        print("error for " + song_name)
        
    return failed_songs


music_path = "C:\\Users\\User\\Music"
failed_songs = add_my_local_songs_to_spotfiy(music_path)
