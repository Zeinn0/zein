from time import time
import asyncio
from pyrogram.types import Message, CallbackQuery, ChatMemberUpdated,ChatPermissions
from Rose.utils.extract_user import extract_user
from Rose import BOT_ID, SUDOERS, app
from Rose.utils.caching import ADMIN_CACHE, admin_cache_reload
from Rose.utils.functions import extract_user_and_reason,time_converter
from pyrogram.types import Message
from lang import get_command
from Rose.utils.commands import *
from Rose.utils.lang import *
from Rose.utils.custom_filters import restrict_filter
from Rose.plugins.fsub import ForceSub
from button import *

KICK_ME = get_command("KICK_ME")
SKICK = get_command("SKICK")
KICK = get_command("KICK")
BAN = get_command("BAN")
UNBAN = get_command("UNBAN")
SBAN = get_command("SBAN")


@app.on_message(command(KICK_ME) )
@language
async def kickFunc(client, message: Message, _):
    reason = None
    if len(message.text.split()) >= 2:
        reason = message.text.split(None, 1)[1]
    try:
        await message.chat.ban_member(message.from_user.id)
        txt = f"◍ مع السلامه {message.from_user.mention}, ومتنساش تقفل الباب وراك😹\n√"
        txt += f"\n<b>Reason</b>: ◍ لا يمكنني طرد الادمن\n√" if reason else ""
        await message.reply_text(txt)
        await message.chat.unban_member(message.from_user.id)
    except Exception as ef:
        await message.reply_text(f"{ef}")
    return


@app.on_message(command(SKICK) & restrict_filter)
@language
async def kickFunc(client, message: Message, _):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        return
    try:
        user_id = await extract_user(message)
    except Exception:
        return   
    if not user_id:
        await message.reply_text(_["ban2"])
        return  
    st = await client.get_chat_member(message.chat.id, user_id)
    if (
                st.status == "administrator"
                and st.status == "creator"
        ):
            return
    try:
        await message.chat.ban_member(user_id)
        await message.delete()
        if message.reply_to_message:
            await message.reply_to_message.delete()
        await message.chat.unban_member(user_id)
    except Exception as ef:
        await message.reply_text(f"{ef}")
    return



@app.on_message(command(KICK) & restrict_filter & SUDOERS)
@language
async def kickFunc(client, message: Message, _):
    FSub = await ForceSub(app, message)
    if FSub == 400:
        return
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if not user_id:
        return await message.reply_text(_["ban3"])
    if user_id == BOT_ID:
        return await message.reply_text(_["ban4"])
    if user_id in SUDOERS:
        return await message.reply_text("◍ عفوا لا استطيع طرد مطوري نور عيني❤\n√")
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "رد")

    if user_id in admins_group:    
        return await message.reply_text("◍ عفوا لايمكنك طرد المالك او ادمن الجروب بطل هطل😹\n√")
    mention = (await app.get_users(user_id)).mention
    msg = f"""
◍ تم طرد {mention} 
بوسطة: {message.from_user.mention if message.from_user else 'Anon'}
√
"""
    if message.command[0][0] == "ط":
        await message.reply_to_message.delete()
    await message.chat.ban_member(user_id)
    await message.reply_text(msg)
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)


@app.on_message(command(BAN)& restrict_filter & SUDOERS)
@language
async def banFunc(client, message: Message, _):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if not user_id:
        return await message.reply_text(_["ban3"])
    if user_id == BOT_ID:
        return await message.reply_text(_["ban4"])
    if user_id in SUDOERS:
        return await message.reply_text("◍ عفوا لا استطيع حظر مطوري نور عيني❤\n√")
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "ظر")

    if user_id in admins_group:
        return await message.reply_text("◍ عفوا لايمكنك حظر المالك او ادمن الجروب بطل هطل😹\n√")
    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    await message.chat.ban_member(user_id)
    msg = (
        f"◍ تم حظر {mention}\n"
        f"بواسطة {message.from_user.mention if message.from_user else 'Anon'}\n"
        f"√\n"
    )
    if message.command[0][0] == "ح":
        await message.reply_to_message.delete()
    if message.command[0] == "ظر لمده":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_ban = await time_converter(message, time_value)
        msg += f"◍ تم حظره لمده {time_value}\n√"
        if temp_reason:
            msg += f"السبب {temp_reason}"
        try:
            if len(time_value[:-1]) < 3:
                await message.chat.ban_member(user_id, until_date=temp_ban)
                await message.reply_text(msg)
            else:
                await message.reply_text(_["ban14"])
        except AttributeError:
            pass
        return
    if reason:
        msg += f"◍ السبب {reason}\n√"
    await message.chat.ban_member(user_id)
    await message.reply_text(msg)


@app.on_message(command(UNBAN)  & restrict_filter & SUDOERS)
@language
async def unbanFunc(client, message: Message, _):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text("◍ استخدم الامر مع يوزر المستخدم او بالرد علي رساله من المستخدم\n√")
        await message.stop_propagation()

    if message.reply_to_message and not message.reply_to_message.from_user:
        user_id, user_first_name = (
            message.reply_to_message.sender_chat.id,
            message.reply_to_message.sender_chat.title,
        )
    else:
        try:
            user_id, user_first_name, _ = await extract_user(app, message)
        except Exception:
            return
    await message.chat.unban_member(user_id)
    await message.reply_text(f"◍ تم الغاء حظر{user_first_name} \nبواسطة {message.from_user.mention}\n√")


@app.on_message(command(SBAN) & restrict_filter)
async def kickunc(client, message: Message, _):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        return
    try:
        user_id = await extract_user(message)
    except Exception:
        return   
    if not user_id:
        await message.reply_text("Can't find user to kick")
        return   
    st = await app.get_chat_member(message.chat.id, user_id)
    if (
                st.status == "administrator"
                and st.status == "creator"
        ):
        return     
    try:
        await message.chat.ban_member(user_id)
        await message.delete()
        if message.reply_to_message:
            await message.reply_to_message.delete()
    except Exception as ef:
        await message.reply_text(f"{ef}")
    return