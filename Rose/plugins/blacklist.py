from re import escape as re_escape
from time import time
from pyrogram.types import ChatPermissions, Message
from Rose.utils.regex_utils import regex_searcher
from html import escape
from pyrogram import filters
from pyrogram.types import  Message
from Rose import  app 
from Rose.mongo.blacklistdb import Blacklist
from Rose.utils.custom_filters import command, owner_filter, restrict_filter
from Rose.utils.kbhelpers import rkb as ikb
from lang import get_command
from Rose.utils.commands import *
from Rose.utils.lang import *
from Rose.utils.filter_groups import *
from Rose.mongo.approvedb import Approve
from Rose.mongo.warnsdb import Warns, WarnSettings
from Rose.utils.caching import ADMIN_CACHE, admin_cache_reload
from Rose.utils.custom_filters import command, restrict_filter
from Rose.utils.parser import mention_html
from Rose.utils.lang import *
from Rose.plugins.fsub import ForceSub
from button import *

BLACKLIST = get_command("BLACKLIST")
ADDBLACK = get_command("ADDBLACK")
BLACKREASON = get_command("BLACKREASON")
UNBLCK = get_command("UNBLCK")
BLMODE = get_command("BLMODE")
RMBLALL = get_command("RMBLALL")



@app.on_message(command("لكلمات الممنوعه") & filters.group)
@language
async def view_blacklist(client, message: Message, _):
    FSub = await ForceSub(app, message)
    if FSub == 400:
        return

    db = Blacklist(message.chat.id)

    blacklists_chat = (f"◍ ها هي قائمه من الكلمات الحاليه\n√")
    all_blacklisted = db.get_blacklists()

    if not all_blacklisted:
        await message.reply_text(_["black2"])
        return

    blacklists_chat += "\n".join(
        f"• <code>{escape(i)}</code>" for i in all_blacklisted
    )

    await message.reply_text(blacklists_chat)
    return


@app.on_message(command("منع") & restrict_filter)
@language
async def add_blacklist(client, message: Message, _):
    FSub = await ForceSub(app, message)
    if FSub == 400:
        return
    db = Blacklist(message.chat.id)

    if len(message.text.split()) < 2:
        await message.reply_text(_["black3"])
        return

    bl_words = ((message.text.split(None, 1)[1]).lower()).split()

    all_blacklisted = db.get_blacklists()

    already_added_words, rep_text = [], ""

    for bl_word in bl_words:
        if bl_word in all_blacklisted:
            already_added_words.append(bl_word)
            continue
        db.add_blacklist(bl_word)

    if already_added_words:
        rep_text = (
            ", ".join([f"<code>{i}</code>" for i in bl_words])
            + "◍ تمت اضافتها بنجاح في قائمه المنع\n√"
        )
    await message.reply_text(
        (("Added <code>{trigger}</code> in blacklist words!")).format(
            trigger=", ".join(f"<code>{i}</code>" for i in bl_words),
        ))
    await message.stop_propagation()


@app.on_message(
    command(BLACKREASON) & restrict_filter,
)
async def blacklistreason(_, message: Message):
    db = Blacklist(message.chat.id)

    if len(message.text.split()) == 1:
        curr = db.get_reason()
        await message.reply_text(
            f"◍ السبب الحالي لقائمه المنع:\n<code>{curr}</code>\n√",
        )
    else:
        reason = message.text.split(None, 1)[1]
        db.set_reason(reason)
        await message.reply_text(
            f"◍ تم تحديث قائمه المنع:\n<code>{reason}</code>\n√",
        )
    return


@app.on_message(
    command(UNBLCK) & restrict_filter,
)
async def rm_blacklist(_, message: Message):
    db = Blacklist(message.chat.id)

    if len(message.text.split()) < 2:
        await message.reply_text("◍ من فضلك افحص قائمه الاوامر لمعرفه كيفيه الاستخدام\n√")
        return

    chat_bl = db.get_blacklists()
    non_found_words, rep_text = [], ""
    bl_words = ((message.text.split(None, 1)[1]).lower()).split()

    for bl_word in bl_words:
        if bl_word not in chat_bl:
            non_found_words.append(bl_word)
            continue
        db.remove_blacklist(bl_word)

    if non_found_words == bl_words:
        await message.reply_text("◍ لم يتم العثور علي اي كلمات ممنوعه\n√")
        return
    if non_found_words:
        rep_text = (
            "◍ لا استطيع ايجاد " + ", ".join(f"<code>{i}</code>\n√" for i in non_found_words)
        ) + "◍ تخطي الكلمات في قائمه المنع\n√."

    await message.reply_text(
        ((f"◍ تمت ازالتها {bl_words} من قائمه المنع بنجاح\n√")).format(
            bl_words=", ".join(f"<code>{i}</code>" for i in bl_words),
        )
        + (f"\n{rep_text}" if rep_text else ""),
    )
    await message.stop_propagation()


@app.on_message(
    command(BLMODE) & restrict_filter,
)
async def set_bl_action(_, message: Message):
    db = Blacklist(message.chat.id)

    if len(message.text.split()) == 2:
        action = message.text.split(None, 1)[1]
        valid_actions = ("بالحظر", "بالطرد", "بالكتم", "بالتحذير", "none")
        if action not in valid_actions:
            await message.reply_text(
                (
                    "◍ اختر نوع المنع\n√"
                    + ", ".join(f"<code>{i}</code>" for i in valid_actions)
                ),
            )

            return
        db.set_action(action)
        await message.reply_text("◍ تم تحديد نوع المنع بنجاح\n√ <b>{action}</b>".format(action=action))
    elif len(message.text.split()) == 1:
        action = db.get_action()
        await message.reply_text(f"""◍
      هذا هو الاجراء الحالي لقائمه المنع في المجموعه<i><b>{action}</b></i>
      ◍ جميع الكلمات الممنوعه في القائمه يتم حذفها √.
      ◍ اذا كنت تريد تغير ذلك فاختر نوع الفعل بدلا من هذا √.
      ◍ الافعال المحتمله <code>لاشئ</code>/<code>تحذير</code>/<code>كتم</code>/<code>حظر</code>""".format(action=action))
        
    else:
        await message.reply_text("◍ من فضلك افحص قائمه الاوامر لمعرفه استخدام الامر\n√")

    return


@app.on_message(
    command(RMBLALL) & owner_filter,
)
async def rm_allblacklist(_, message: Message):
    db = Blacklist(message.chat.id)

    all_bls = db.get_blacklists()
    if not all_bls:
        await message.reply_text("◍ لا يوجد ملاحظات في قائمه المنع\n√")
        return

    await message.reply_text(
        "◍ هل انت متأكد من انك تريد حذف جميع الكلمات الممنوعه\n√",
        reply_markup=ikb(
            [[("⚠️ حذف", "rm_allblacklist"), ("❌ الغاء", "close_admin")]],
        ),
    )
    return

#scan
@app.on_message(filters.text & filters.group, group=black)
async def bl_watcher(_, m: Message):
    if m and not m.from_user:
        return

    bl_db = Blacklist(m.chat.id)

    async def perform_action_blacklist(m: Message, action: str, trigger: str):
        if action == "رد":
            await m.chat.kick_member(m.from_user.id, int(time() + 45))
            await m.reply_text(f"◍ تم طرد {m.from_user.username} لارساله كلمه ممنوعه\n√")

        elif action == "ظر":
            (
                await m.chat.kick_member(
                    m.from_user.id,
                )
            )
            await m.reply_text(f"◍ تم حظر {m.from_user.username} لاستخدامه كلمه ممنوعه\n√")

        elif action == "تم":
            await m.chat.restrict_member(
                m.from_user.id,
                ChatPermissions(),
            )

            await m.reply_text(f"◍ تم كتم {m.from_user.username} لاستخدامه كلمه ممنوعه\n√")

        elif action == "حذير":
            warns_settings_db = WarnSettings(m.chat.id)
            warns_db = Warns(m.chat.id)
            warn_settings = warns_settings_db.get_warnings_settings()
            warn_reason = bl_db.get_reason()
            _, num = warns_db.warn_user(m.from_user.id, warn_reason)
            if num >= warn_settings["warn_limit"]:
                if warn_settings["warn_mode"] == "رد":
                    await m.chat.ban_member(
                        m.from_user.id,
                        until_date=int(time() + 45),
                    )
                    action = "رد"
                elif warn_settings["warn_mode"] == "ظر":
                    await m.chat.ban_member(m.from_user.id)
                    action = "banned"
                elif warn_settings["warn_mode"] == "تم":
                    await m.chat.restrict_member(m.from_user.id, ChatPermissions())
                    action = "muted"
                await m.reply_text(
                    (
                        f"◍ تم تحذير {num}/{warn_settings['warn_limit']}\n"
                        f"{(await mention_html(m.from_user.first_name, m.from_user.id))} has been <b>{action}!</b>"
                    ),
                )
                return
            await m.reply_text(
                (
                    f"{(await mention_html(m.from_user.first_name, m.from_user.id))} warned {num}/{warn_settings['warn_limit']}\n"
                    f"Last warn was for:\n<i>{warn_reason}</i>"
                ),
            )
        return


    # If no blacklists, then return
    chat_blacklists = bl_db.get_blacklists()
    if not chat_blacklists:
        return

    # Get admins from admin_cache, reduces api calls
    try:
        admin_ids = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admin_ids = await admin_cache_reload(m, "blacklist_watcher")

    if m.from_user.id in admin_ids:
        return

    # Get approved user from cache/database
    app_users = Approve(m.chat.id).list_approved()
    if m.from_user.id in {i[0] for i in app_users}:
        return

    # Get action for blacklist
    action = bl_db.get_action()
    for trigger in chat_blacklists:
        pattern = r"( |^|[^\w])" + re_escape(trigger) + r"( |$|[^\w])"
        match = await regex_searcher(pattern, m.text.lower())
        if not match:
            continue
        if match:
            try:
                await perform_action_blacklist(m, action, trigger)
                await m.delete()
            except Exception as e:
                return await app.send_message(LOG_GROUP_ID,text= f"{e}")
            break
    return