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



def add_my_local_songs_to_spotfiy(path: str):
    '''
    function that add the songs from a certain path to playlists in a spotify account
    '''
    spotify = log_in_to_spotify()
    
    user_info = spotify.current_user()
    user_id = user_info['id']
    
    my_playlists = get_current_playlists(spotify)
    
    #iterate through the given path and add the songs
    failed_songs = []
    for root_folder, sub_directoies, files in os.walk(path):
        playlist_name = root_folder.split("\\")[-1]
        if playlist_name != "Music":
            if playlist_name not in my_playlists:
                playlist_created = spotify.user_playlist_create(user_id, playlist_name)
                playlist_to_change_id = playlist_created['id']
            else: #playlist already exists
                playlist_to_change_id = my_playlists[playlist_name]['id']
                
            for filename in files:
                if filename.endswith('.mp3'):
                    song_name = filename[:-4]
                    try:
                        song = spotify.search(q=song_name, limit=1, type='track')
                        song_uri = [song['tracks']['items'][0]['uri']]
                        spotify.playlist_remove_all_occurrences_of_items(playlist_to_change_id, song_uri)
                        spotify.playlist_add_items(playlist_to_change_id, song_uri)
                        print(f"added {song_name} to {playlist_name}")
                    except:
                        failed_songs.append(song_name)
                        print("error for " + song_name)
                        
    write_failed_songs_to_txt(failed_songs, 'failed_songs.txt')
    return failed_songs


def log_in_to_spotify():
    '''
    function that redirects to a spotify log-in and returns the spotify object
    '''    
    scope = "playlist-modify-public"

    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    return spotify


def get_current_playlists(spotify):
    ''' 
    function to create dict with the currently existing playlists for a user
    '''
    my_playlists = {}
    user_playlists = spotify.current_user_playlists()
    for playlist in user_playlists['items']:
        existing_playlist_name = playlist['name']
        my_playlists[existing_playlist_name] = {}
        my_playlists[existing_playlist_name]['id'] = playlist['id']
        my_playlists[existing_playlist_name]['uri'] = playlist['uri']
    return my_playlists


def write_failed_songs_to_txt(failed_songs: list, filename: str):
    with open(filename, 'w', encoding='utf-8') as file:
        for song in failed_songs:
            file.write(song + '\n')

    
music_path = "C:\\Users\\User\\Music"
failed_songs = add_my_local_songs_to_spotfiy(music_path)
