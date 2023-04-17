from asyncio import get_running_loop, sleep
from time import time
from pyrogram import filters
from pyrogram.types import (CallbackQuery, ChatPermissions,
                            InlineKeyboardButton, InlineKeyboardMarkup,
                            Message)
from Rose import app
from Rose import *
from Rose.mongo.flooddb import *
from Rose.utils.filter_groups import flood_group
from lang import get_command
from Rose.utils.custom_filters import admin_filter
from button import *

#COMMANDS
FLOOD = get_command("FLOOD")
DB = {}  # TODO Use mongodb instead of a fucking dict.


def reset_flood(chat_id, user_id=0):
    for user in DB[chat_id].keys():
        if user != user_id:
            DB[chat_id][user] = 0


@app.on_message(
    ~filters.service
    & ~filters.me
    & ~filters.private
    & ~filters.channel
    & ~filters.bot
    & ~filters.edited,
    group=flood_group,
)
async def flood_control_func(_, message: Message):
    if not message.chat:
        return
    chat_id = message.chat.id
    if not (await is_flood_on(chat_id)):
        return
    if chat_id not in DB:
        DB[chat_id] = {}

    if not message.from_user:
        reset_flood(chat_id)
        return

    user_id = message.from_user.id
    mention = message.from_user.mention

    if user_id not in DB[chat_id]:
        DB[chat_id][user_id] = 0

    reset_flood(chat_id, user_id)
    
    # Mute if user sends more than 10 messages in a row
    if DB[chat_id][user_id] >= 10:
        DB[chat_id][user_id] = 0
        try:
            await message.chat.restrict_member(
                user_id,
                permissions=ChatPermissions(),
                until_date=int(time() + 5),
            )
        except Exception:
            return
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Unmute 🔇",
                        callback_data=f"_unmute_{user_id}",
                    )
                ]
            ]
        )
        m = await message.reply_text(
            f"Yeah, I don't like your flooding. Quiet now {mention}, Muted  for 5 sec",
            reply_markup=keyboard,
        )

        async def delete():
            await sleep(300)
            try:
                await m.delete()
            except Exception:
                pass

        loop = get_running_loop()
        return loop.create_task(delete())
    DB[chat_id][user_id] += 1


@app.on_message(filters.command("antiflood") & admin_filter)
async def flood_toggle(_, message: Message):  
    if len(message.command) != 2:
        return await message.reply_text("Usage: /antiflood `on` or `off`")
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        await flood_on(chat_id)
        await message.reply_text("Enabled Flood Checker.")
    elif status == "off":
        await flood_off(chat_id)
        await message.reply_text("Disabled Flood Checker.")
    else:
        await message.reply_text("Usage: /antiflood `on` or `off`")





__MODULE__ = f"{kgb}"
__HELP__ = """
◍ اهلا بك فى اوامر التسليه
√"""
__helpbtns__ = (
        [[
            InlineKeyboardButton
                (
                    "اوامر التسليه 2️⃣", callback_data="_anssx"
                ),           
            InlineKeyboardButton
                (
                    "اوامر التسليه 1️⃣", callback_data="_anl"
                )
        ]]
)

 

