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
import aiohttp
from bs4 import BeautifulSoup
from youtubesearchpython.__future__ import VideosSearch

class RessoAPI:
    def __init__(self):
        self.regex = r"^(https:\/\/m.resso.com\/)(.*)$"
        self.base = "https://m.resso.com/"

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
        title = None
        des = None

        for tag in soup.find_all("meta"):
            if tag.get("property") == "og:title":
                title = tag.get("content")
            if tag.get("property") == "og:description":
                des = tag.get("content", "").split("·")[0]

        if des == "":
            return None

        results = VideosSearch(title, limit=1)
        result = (await results.next())["result"][0]

        track_details = {
            "title": result["title"],
            "link": result["link"],
            "vidid": result["id"],
            "duration_min": result["duration"],
            "thumb": result["thumbnails"][0]["url"].split("?")[0],
        }

        return track_details, result["id"]
