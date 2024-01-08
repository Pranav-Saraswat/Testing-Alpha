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

from config import BANNED_USERS
from strings import get_command
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database import add_gban_user, remove_gban_user
from YukkiMusic.utils.decorators.language import language


@app.on_message(filters.command(["block"]) & SUDOERS)
@language
async def block_user(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in BANNED_USERS:
            return await message.reply_text(
                _["block_1"].format(user.mention)
            )
        await add_gban_user(user.id)
        BANNED_USERS.add(user.id)
        await message.reply_text(_["block_2"].format(user.mention))
    else:
        if message.reply_to_message.from_user.id in BANNED_USERS:
            return await message.reply_text(
                _["block_1"].format(
                    message.reply_to_message.from_user.mention
                )
            )
        await add_gban_user(message.reply_to_message.from_user.id)
        BANNED_USERS.add(message.reply_to_message.from_user.id)
        await message.reply_text(
            _["block_2"].format(
                message.reply_to_message.from_user.mention
            )
        )


@app.on_message(filters.command(["unblock"]) & SUDOERS)
@language
async def unblock_user(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id not in BANNED_USERS:
            return await message.reply_text(_["block_3"])
        await remove_gban_user(user.id)
        BANNED_USERS.remove(user.id)
        await message.reply_text(_["block_4"])
    else:
        user_id = message.reply_to_message.from_user.id
        if user_id not in BANNED_USERS:
            return await message.reply_text(_["block_3"])
        await remove_gban_user(user_id)
        BANNED_USERS.remove(user_id)
        await message.reply_text(_["block_4"])


@app.on_message(filters.command(["blocked"]) & SUDOERS)
@language
async def list_blocked_users(client, message: Message, _):
    if not BANNED_USERS:
        return await message.reply_text(_["block_5"])
    mystic = await message.reply_text(_["block_6"])
    msg = _["block_7"]
    count = 0
    for user_id in BANNED_USERS:
        try:
            user = await app.get_users(user_id)
            user = (
                user.first_name if not user.mention else user.mention
            )
            count += 1
        except Exception:
            continue
        msg += f"{count}➤ {user}\n"
    if count == 0:
        return await mystic.edit_text(_["block_5"])
    else:
        return await mystic.edit_text(msg)
