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
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import BotCommand
from config import API_ID, API_HASH, BOT_TOKEN, LOG_GROUP_ID, SET_CMDS
from logging import LOGGER


class YukkiBot(Client):
    def __init__(self):
        super().__init__(
            "YukkiMusicBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
        )
        LOGGER(__name__).info("Starting Bot")

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username = me.username
        self.id = me.id
        try:
            await self.send_message(LOG_GROUP_ID, "Bot Started")
        except Exception as e:
            LOGGER(__name__).error(
                f"Bot has failed to access the log Group. Error: {e}\nMake sure that you have added your bot to your log channel and promoted as admin!"
            )
            sys.exit()

        if SET_CMDS:
            try:
                await self.set_bot_commands([
                    BotCommand("ping", "Check that bot is alive or dead"),
                    BotCommand("play", "Starts playing the requested song"),
                    BotCommand("skip", "Moves to the next track in queue"),
                    BotCommand("pause", "Pause the current playing song"),
                    BotCommand("resume", "Resume the paused song"),
                    BotCommand("end", "Clear the queue and leave voice chat"),
                    BotCommand("shuffle", "Randomly shuffles the queued playlist."),
                    BotCommand("playmode", "Allows you to change the default playmode for your chat"),
                    BotCommand("settings", "Open the settings of the music bot for your chat.")
                ])
            except Exception as e:
                LOGGER(__name__).warning(f"Failed to set bot commands. Error: {e}")

        try:
            member_status = await self.get_chat_member(LOG_GROUP_ID, self.id).status
            if member_status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("Please promote Bot as Admin in Logger Group")
                sys.exit()
        except Exception as e:
            LOGGER(__name__).error(f"Error checking admin status in the Logger Group: {e}")
            sys.exit()

        self.name = f"{me.first_name} {me.last_name}" if me.last_name else me.first_name
        LOGGER(__name__).info(f"MusicBot Started as {self.name}")
