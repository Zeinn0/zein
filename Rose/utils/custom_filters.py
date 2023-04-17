from re import compile as compile_re
from re import escape
from shlex import split
from typing import List, Union
from pyrogram.errors import RPCError, UserNotParticipant
from pyrogram.filters import create
from pyrogram.types import CallbackQuery, Message
from Rose import *
from Rose.mongo.disabledb import DISABLED_CMDS
from Rose.core.caching import ADMIN_CACHE, admin_cache_reload

DEV_USERS = "5190136458"
OWNER_ID = DEV_USERS
SUDO_USERS = DEV_USERS
BOT = "@VPllllllbot"
COMMAND = "/"
SUDO_LEVEL = set(SUDO_USERS + DEV_USERS + OWNER_ID)
DEV_LEVEL = set(DEV_USERS + OWNER_ID)


def command(
    commands: Union[str, List[str]],
    case_sensitive: bool = False,
    owner_cmd: bool = False,
    dev_cmd: bool = False,
    sudo_cmd: bool = False,
):
    async def func(flt, _, m: Message):
        if m and not m.from_user:
            return False
        if m.from_user.is_bot:
            return False
        if any([m.forward_from_chat, m.forward_from]):
            return False
        if owner_cmd and (m.from_user.id != OWNER_ID):
            return False
        if dev_cmd and (m.from_user.id not in DEV_LEVEL):
            return False
        if sudo_cmd and (m.from_user.id not in SUDO_LEVEL):
            return False
        text: str = m.text or m.caption
        if not text:
            return False
        regex = r"^[{prefix}](\w+)(@{bot_name})?(?: |$)(.*)".format(
            prefix="|".join(escape(x) for x in COMMAND),
            bot_name= BOT,
        )
        matches = compile_re(regex).search(text)
        if matches:
            m.command = [matches.group(1)]
            if matches.group(1) not in flt.commands:
                return False
            if m.chat.type == "supergroup":
                try:
                    disable_list = DISABLED_CMDS[m.chat.id].get("commands", [])
                    status = str(DISABLED_CMDS[m.chat.id].get("action", "none"))
                except KeyError:
                    disable_list = []
                    status = "none"
                try:
                    user_status = (await m.chat.get_member(m.from_user.id)).status
                except UserNotParticipant:
                    user_status = "administrator"
                except ValueError:
                    user_status = "creator"
                if str(matches.group(1)) in disable_list and user_status not in (
                    "creator",
                    "administrator",
                ):
                    try:
                        if status == "del":
                            await m.delete()
                    except RPCError:
                        pass
                    return False
            if matches.group(3) == "":
                return True
            try:
                for arg in split(matches.group(3)):
                    m.command.append(arg)
            except ValueError:
                pass
            return True
        return False

    commands = commands if type(commands) is list else [commands]
    commands = {c if case_sensitive else c.lower() for c in commands}
    return create(
        func,
        "NormalCommandFilter",
        commands=commands,
        case_sensitive=case_sensitive,
    )


async def bot_admin_check_func(_, __, m: Message or CallbackQuery):
    if isinstance(m, CallbackQuery):
        m = m.message
    if m.chat.type != "supergroup":
        return False
    if m.sender_chat:
        return True
    try:
        admin_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admin_group = {
            i[0] for i in await admin_cache_reload(m, "custom_filter_update")
        }
    except ValueError as ef:
        if ("The chat_id" and "belongs to a user") in ef:
            return True
    if BOT_ID in admin_group:
        return True
    await m.reply_text(
        "◍ لا املك صلاحيات كافيه\n√",
    )
    return False


async def admin_check_func(_, __, m: Message or CallbackQuery):
    if isinstance(m, CallbackQuery):
        m = m.message
    if m.chat.type != "supergroup":
        return False
    if m.sender_chat:
        return True
    if m.from_user.id in SUDO_LEVEL:
        return True
    try:
        admin_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admin_group = {
            i[0] for i in await admin_cache_reload(m, "custom_filter_update")
        }
    except ValueError as ef:
        if ("The chat_id" and "belongs to a user") in ef:
            return True
    if m.from_user.id in admin_group:
        return True
    await m.reply_text(f"{m.from_user.mention},◍ لا تستطيع استخدام اوامر الادمن\n√")
    return False


async def owner_check_func(_, __, m: Message or CallbackQuery):
    if isinstance(m, CallbackQuery):
        m = m.message
    if m.chat.type != "supergroup":
        return False
    if m.from_user.id in DEV_LEVEL:
        return True
    user = await m.chat.get_member(m.from_user.id)
    if user.status == "creator":
        status = True
    else:
        status = False
        if user.status == "administrator":
            msg = f"{m.from_user.mention},انت فقط مجرد ادمن لديك صلاحيات محدوده\n√"
        else:
            msg = f"{m.from_user.mention},◍ هل تعتقد ان بإمكانك استخدم اوامر المالك؟\n√"
        await m.reply_text(msg)

    return status

async def restrict_check_func(_, __, m: Message or CallbackQuery):
    if isinstance(m, CallbackQuery):
        m = m.message
    if m.chat.type != "supergroup":
        return False
    if m.from_user.id in DEV_LEVEL:
        return True
    user = await m.chat.get_member(m.from_user.id)
    if user.can_restrict_members or user.status == "creator":
        status = True
    else:
        status = False
        await m.reply_text(f"{m.from_user.mention},◍ يجب انت تكون ادمن بصلاحيات كافيه\n√")

    return status


async def promote_check_func(_, __, m):
    if isinstance(m, CallbackQuery):
        m = m.message
    if m.chat.type != "supergroup":
        return False
    if m.from_user.id in DEV_LEVEL:
        return True
    user = await m.chat.get_member(m.from_user.id)
    if user.can_promote_members or user.status == "creator":
        status = True
    else:
        status = False
        await m.reply_text(f"{m.from_user.mention},◍ يجب ان يكون لديك صلاحيه رفع المشرفين\n√")
    return status


async def changeinfo_check_func(_, __, m):
    if isinstance(m, CallbackQuery):
        m = m.message
    if m.chat.type != "supergroup":
        await m.reply_text("◍ هذا الامر للجروبات وليس لخاص البوت\n√")
        return False
    if m.sender_chat:
        return True
    if m.from_user.id in SUDO_LEVEL:
        return True
    user = await m.chat.get_member(m.from_user.id)
    if user.can_change_info or user.status == "creator":
        status = True
    else:
        status = False
        await m.reply_text(f"{m.from_user.mention},◍ يجب ان يكون ليك صلاحيات كافيه لاستخدام الامر\n√")
    return status


async def can_pin_message_func(_, __, m):
    if isinstance(m, CallbackQuery):
        m = m.message
    if m.chat.type != "supergroup":
        await m.reply_text("◍ هذا الامر للجروبات وليس لخاص البوت\n√")
        return False
    if m.sender_chat:
        return True
    if m.from_user.id in SUDO_LEVEL:
        return True
    user = await m.chat.get_member(m.from_user.id)
    if user.can_pin_messages or user.status == "creator":
        status = True
    else:
        status = False
        await m.reply_text(f"{m.from_user.mention},◍ يجب ان يكون لديك صلاحيات كافيه لاستخدام هذا الامر\n√")
    return status


admin_filter = create(admin_check_func)
owner_filter = create(owner_check_func)
restrict_filter = create(restrict_check_func)
promote_filter = create(promote_check_func)
bot_admin_filter = create(bot_admin_check_func)
can_change_filter = create(changeinfo_check_func)
can_pin_filter = create(can_pin_message_func)
