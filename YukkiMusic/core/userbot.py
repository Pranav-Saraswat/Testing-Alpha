#
# Copyright (C) 2021-present by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

import sys
from pyrogram import Client
import config
from ..logging import LOGGER

class Userbot(Client):
    def __init__(self):
        self.assistants = []
        self.assistantids = []

    async def start_assistant(self, i, session_string):
        assistant = Client(
            f"YukkiString{i}",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(session_string),
            no_updates=True,
        )
        await assistant.start()
        
        self.assistants.append(assistant)

        try:
            await assistant.send_message(config.LOG_GROUP_ID, "Assistant Started")
        except:
            LOGGER(__name__).error(
                f"Assistant Account {i} has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin! "
            )
            sys.exit()

        get_me = await assistant.get_me()
        assistant.username = get_me.username
        assistant.id = get_me.id
        self.assistantids.append(get_me.id)
        assistant.name = f"{get_me.first_name} {get_me.last_name}" if get_me.last_name else get_me.first_name
        LOGGER(__name__).info(f"Assistant {i} Started as {assistant.name}")

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistant Clients")
        for i in range(1, 6):
            session_string = getattr(config, f"STRING{i}", None)
            if session_string:
                await self.start_assistant(i, session_string)

if __name__ == "__main__":
    userbot = Userbot()
    userbot.run()
