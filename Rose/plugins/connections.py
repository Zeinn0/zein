from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Rose.mongo.connectiondb import add_connection, all_connections, if_active, delete_connection
import logging
from Rose import *
from lang import get_command
from Rose.utils.commands import *
from Rose.utils.lang import *
from button import *


CONNECT = get_command("CONNECT")
DISCONNECT = get_command("DISCONNECT")
CONNECTIONS = get_command("CONNECTIONS")

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)



@app.on_message((filters.private | filters.group) & command(CONNECT))
@language
async def addconnection(client, message: Message, _):
    userid = message.from_user.id if message.from_user else None
    chat_id = message.chat.id
    if not userid:
        return await message.reply(_["🖥اتصال1"].format(chat_id))
    chat_type = message.chat.type
    if chat_type == "private":
        try:
            cmd, group_id = message.text.split(" ", 1)
        except:
            await message.reply_text(_["🖥اتصال2"])
            return

    elif chat_type in ["group", "supergroup"]:
        group_id = message.chat.id

    try:
        st = await app.get_chat_member(group_id, userid)
        if (
                st.status != "administrator"
                and st.status != "creator"
        ):
            await message.reply_text(_["🖥اتصال3"])
            return
    except Exception as e:
        logger.exception(e)
        await message.reply_text(_["🖥اتصال4"])

        return
    try:
        connection = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="تواصل معي في الخاص☑️",
                url=f"t.me/{BOT_USERNAME}?start=connections",
            )
        ]
    ]
)
        st = await app.get_chat_member(group_id, "me")
        if st.status == "administrator":
            ttl = await app.get_chat(group_id)
            title = ttl.title

            addcon = await add_connection(str(group_id), str(userid))
            if addcon:
                await message.reply_text(_["🖥اتصال5"].format(title),
                    reply_markup= connection,
                    quote=True,
                    parse_mode="md"
                )
                if chat_type in ["group", "supergroup"]:
                    await app.send_message(
                        userid,
                        f"اتصال ب **{title}** !",
                        parse_mode="md"
                    )
            else:
                await message.reply_text(_["🖥اتصال6"])
        else:
            await message.reply_text(_["🖥اتصال7"])
    except Exception as e:
        logger.exception(e)
        await message.reply_text(_["🖥اتصال8"])
        return


@app.on_message((filters.private | filters.group) & filters.command(DISCONNECT))
@language
async def deleteconnection(client, message: Message, _):
    userid = message.from_user.id if message.from_user else None
    chat_id = message.chat.id
    if not userid:
        return await message.reply(_["🖥اتصال9"].format(chat_id))
    chat_type = message.chat.type

    if chat_type == "private":
        await message.reply_text(_["🖥اتصال10"])

    elif chat_type in ["group", "supergroup"]:
        group_id = message.chat.id

        st = await app.get_chat_member(group_id, userid)
        if (
                st.status != "administrator"
                and st.status != "creator"
        ):
            return

        delcon = await delete_connection(str(userid), str(group_id))
        if delcon:
            await message.reply_text(_["🖥اتصال11"])
        else:
            await message.reply_text(_["🖥اتصال12"])


@app.on_message(filters.private & filters.command(CONNECTIONS))
@language
async def connections(client, message: Message, _):
    userid = message.from_user.id

    groupids = await all_connections(str(userid))
    if groupids is None:
        await message.reply_text(_["🖥اتصال13"])
        return
    buttons = []
    for groupid in groupids:
        try:
            ttl = await app.get_chat(int(groupid))
            title = ttl.title
            active = await if_active(str(userid), str(groupid))
            act = ":✅" if active else ":⛔️"
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                    )
                ]
            )
        except:
            pass
    if buttons:
        await message.reply_text(
"""
◍ المحادثه متصله حاليا

اتصال = ✅
فقد = ⛔️

__اختار الدردشه لاتصال:__
""",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
    else:
        await message.reply_text(_["🖥اتصال13"])
