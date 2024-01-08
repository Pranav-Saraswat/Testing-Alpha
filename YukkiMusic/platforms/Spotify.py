#
# Copyright (C) 2021-present by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

import re
from typing import Union
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython.__future__ import VideosSearch
import config

class SpotifyAPI:
    def __init__(self):
        self.regex = r"^(https:\/\/open.spotify.com\/)(.*)$"
        self.client_id = config.SPOTIFY_CLIENT_ID
        self.client_secret = config.SPOTIFY_CLIENT_SECRET
        self.spotify = self.initialize_spotify()

    def initialize_spotify(self):
        if self.client_id and self.client_secret:
            client_credentials_manager = SpotifyClientCredentials(
                self.client_id, self.client_secret
            )
            return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        else:
            return None

    async def valid(self, link: str) -> bool:
        return bool(re.search(self.regex, link))

    async def get_track_info(self, track) -> dict:
        info = track["name"]
        for artist in track["artists"]:
            fetched = f' {artist["name"]}'
            if "Various Artists" not in fetched:
                info += fetched
        return info

    async def track(self, link: str) -> Union[dict, None]:
        if not self.spotify:
            return None

        track = self.spotify.track(link)
        info = await self.get_track_info(track)

        results = VideosSearch(info, limit=1)
        result = (await results.next())["result"][0]

        track_details = {
            "title": result["title"],
            "link": result["link"],
            "vidid": result["id"],
            "duration_min": result["duration"],
            "thumb": result["thumbnails"][0]["url"].split("?")[0],
        }

        return track_details, result["id"]

    async def playlist(self, url: str) -> Union[list, None]:
        if not self.spotify:
            return None

        playlist = self.spotify.playlist(url)
        playlist_id = playlist["id"]
        results = []

        for item in playlist["tracks"]["items"]:
            music_track = item["track"]
            info = await self.get_track_info(music_track)
            results.append(info)

        return results, playlist_id

    async def album(self, url: str) -> Union[tuple, None]:
        if not self.spotify:
            return None

        album = self.spotify.album(url)
        album_id = album["id"]
        results = []

        for item in album["tracks"]["items"]:
            info = await self.get_track_info(item)
            results.append(info)

        return results, album_id

    async def artist(self, url: str) -> Union[list, None]:
        if not self.spotify:
            return None

        artist_info = self.spotify.artist(url)
        artist_id = artist_info["id"]
        results = []

        artist_top_tracks = self.spotify.artist_top_tracks(url)
        for item in artist_top_tracks["tracks"]:
            info = await self.get_track_info(item)
            results.append(info)

        return results, artist_id
