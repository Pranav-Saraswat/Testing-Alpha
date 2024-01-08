#
# Copyright (C) 2021-present by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

from pyrogram import filters
from pyrogram.types import Message

from strings import get_command
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database.memorydatabase import (
    get_active_chats, get_active_video_chats)

# Commands
ACTIVEVC_COMMAND = get_command("ACTIVEVC_COMMAND")
ACTIVEVIDEO_COMMAND = get_command("ACTIVEVIDEO_COMMAND")


@app.on_message(filters.command(ACTIVEVC_COMMAND) & SUDOERS)
async def activevc(_, message: Message):
    mystic = await message.reply_text("Getting active voice chats.. Please hold")
    served_chats = await get_active_chats()
    text = ""
    for j, x in enumerate(served_chats):
        try:
            chat = await app.get_chat(x)
            title = chat.title
        except Exception:
            title = "Private Group"
        if chat.username:
            user = chat.username
            text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
    if not text:
        await mystic.edit_text("No Active Voice Chats")
    else:
        await mystic.edit_text(
            f"**Active Voice Chats:-**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(ACTIVEVIDEO_COMMAND) & SUDOERS)
async def activevi_(_, message: Message):
    mystic = await message.reply_text("Getting active video chats.. Please hold")
    served_chats = await get_active_video_chats()
    text = ""
    for j, x in enumerate(served_chats):
        try:
            chat = await app.get_chat(x)
            title = chat.title
        except Exception:
            title = "Private Group"
        if chat.username:
            user = chat.username
            text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
    if not text:
        await mystic.edit_text("No Active Video Calls")
    else:
        await mystic.edit_text(
            f"**Active Video Calls:-**\n\n{text}",
            disable_web_page_preview=True,
        )
