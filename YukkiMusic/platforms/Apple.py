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
import aiohttp
from bs4 import BeautifulSoup
from youtubesearchpython.__future__ import VideosSearch
from typing import Union

class AppleAPI:
    def __init__(self):
        self.regex = r"^(https:\/\/music.apple.com\/)(.*)$"
        self.base = "https://music.apple.com/in/playlist/"

    async def valid(self, link: str) -> bool:
        return bool(re.search(self.regex, link))

    async def get_html_content(self, url: str) -> Union[str, None]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                return await response.text()

    async def track(self, url: str, playid: Union[bool, str] = None) -> Union[dict, bool]:
        url = self.base + url if playid else url
        html_content = await self.get_html_content(url)
        if html_content is None:
            return False

        soup = BeautifulSoup(html_content, "html.parser")
        search = next((tag.get("content", None) for tag in soup.find_all("meta", property="og:title")), None)

        if search is None:
            return False

        results = VideosSearch(search, limit=1)
        result = (await results.next())["result"][0]

        track_details = {
            "title": result["title"],
            "link": result["link"],
            "vidid": result["id"],
            "duration_min": result["duration"],
            "thumb": result["thumbnails"][0]["url"].split("?")[0],
        }
        return track_details, result["id"]

    async def playlist(self, url: str, playid: Union[bool, str] = None) -> Union[list, bool]:
        url = self.base + url if playid else url
        html_content = await self.get_html_content(url)
        if html_content is None:
            return False

        soup = BeautifulSoup(html_content, "html.parser")
        applelinks = soup.find_all("meta", attrs={"property": "music:song"})
        results = []

        for item in applelinks:
            try:
                xx = ((item["content"]).split("album/")[1]).split("/")[0].replace("-", " ")
            except IndexError:
                xx = ((item["content"]).split("album/")[1]).split("/")[0]
            results.append(xx)

        playlist_id = url.split("playlist/")[1]
        return results, playlist_id
