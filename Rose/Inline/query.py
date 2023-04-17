from  Rose import bot as app
from Rose.mongo.captcha import captchas
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Rose.plugins.antlangs import *
from Rose.plugins.captcha import *
from Rose.mongo.connectiondb import *
from Rose.plugins.lang import *
from Rose.mongo.approvedb import Approve
from Rose.plugins.lock import *
from Rose.plugins.warn import *
from EmojiCaptcha import Captcha as emoji_captcha
import random
from captcha.image import ImageCaptcha
from Rose.mongo.disabledb import Disabling
from Rose.mongo.filterdb import Filters
from Rose.mongo.notesdb import Notes
from Rose.mongo.blacklistdb import Blacklist
from Rose.mongo.feddb import *
import uuid
from Rose.mongo.welcomedb import Greetings
from Rose.utils.string import (
    build_keyboard,
    parse_button,
)
from typing import Optional
from Rose import app
from pyrogram import filters, emoji
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid, MessageNotModified
)
from pyrogram.types import (
    User,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery,
    ChosenInlineResult
)
from Rose.plugins.wishper import *

import json

try:
    with open('data.json') as f:
        whispers = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    whispers = {}
open('data.json', 'w').close()

#===============================================================
@app.on_chosen_inline_result()
async def chosen_inline_result(_, cir: ChosenInlineResult):
    query = cir.query
    split = query.split(' ', 1)
    len_split = len(split)
    if len_split == 0 or len(query) > lengths \
            or (query.startswith('@') and len(split) == 1):
        return
    if len_split == 2 and query.startswith('@'):
        receiver_uname, text = split[0][1:] or '@', split[1]
    else:
        receiver_uname, text = None, query
    sender_uid = cir.from_user.id
    inline_message_id = cir.inline_message_id
    whispers[inline_message_id] = {
        'sender_uid': sender_uid,
        'receiver_uname': receiver_uname,
        'text': text
    }
#===============================================================
db = {}
dbf = Filters()
dbns = Notes()
LocalDB = {}

def MakeCaptchaMarkup(markup, _number, sign):
    __markup = markup
    for i in markup:
        for k in i:
            if k["text"] == _number:
                k["text"] = f"{sign}"
                k["callback_data"] = "done_"
                return __markup

def emoji_() -> dict:
    maker = emoji_captcha().generate()
    emojis_list = ['🃏', '🎤', '🎥', '🎨', '🎩', '🎬', '🎭', '🎮', '🎯', '🎱', '🎲', '🎷', '🎸', '🎹', '🎾', '🏀', '🏆', '🏈', '🏉', '🏐', '🏓', '💠', '💡', '💣', '💨', '💸', '💻', '💾', '💿', '📈', '📉', '📊', '📌', '📍', '📎', '📏', '📐', '📞', '📟', '📠', '📡', '📢', '📣', '📦', '📹', '📺', '📻', '📼', '📽', '🖥', '🖨', '🖲', '🗂', '🗃', '🗄', '🗜', '🗝', '🗡', '🚧', '🚨', '🛒', '🛠', '🛢', '🧀', '🌭', '🌮', '🌯', '🌺', '🌻', '🌼', '🌽', '🌾', '🌿', '🍊', '🍋', '🍌', '🍍', '🍎', '🍏', '🍚', '🍛', '🍜', '🍝', '🍞', '🍟', '🍪', '🍫', '🍬', '🍭', '🍮', '🍯', '🍺', '🍻', '🍼', '🍽', '🍾', '🍿', '🎊', '🎋', '🎍', '🎏', '🎚', '🎛', '🎞', '🐌', '🐍', '🐎', '🐚', '🐛', '🐝', '🐞', '🐟', '🐬', '🐭', '🐮', '🐯', '🐻', '🐼', '🐿', '👛', '👜', '👝', '👞', '👟', '💊', '💋', '💍', '💎', '🔋', '🔌', '🔪', '🔫', '🔬', '🔭', '🔮', '🕯', '🖊', '🖋', '🖌', '🖍', '🥚', '🥛', '🥜', '🥝', '🥞', '🦊', '🦋', '🦌', '🦍', '🦎', '🦏', '🌀', '🌂', '🌑', '🌕', '🌡', '🌤', '⛅️', '🌦', '🌧', '🌨', '🌩', '🌰', '🌱', '🌲', '🌳', '🌴', '🌵', '🌶', '🌷', '🌸', '🌹', '🍀', '🍁', '🍂', '🍃', '🍄', '🍅', '🍆', '🍇', '🍈', '🍉', '🍐', '🍑', '🍒', '🍓', '🍔', '🍕', '🍖', '🍗', '🍘', '🍙', '🍠', '🍡', '🍢', '🍣', '🍤', '🍥', '🍦', '🍧', '🍨', '🍩', '🍰', '🍱', '🍲', '🍴', '🍵', '🍶', '🍷', '🍸', '🍹', '🎀', '🎁', '🎂', '🎃', '🎄', '🎈', '🎉', '🎒', '🎓', '🎙', '🐀', '🐁', '🐂', '🐃', '🐄', '🐅', '🐆', '🐇', '🐕', '🐉', '🐓', '🐖', '🐗', '🐘', '🐙', '🐠', '🐡', '🐢', '🐣', '🐤', '🐥', '🐦', '🐧', '🐨', '🐩', '🐰', '🐱', '🐴', '🐵', '🐶', '🐷', '🐸', '🐹', '👁\u200d🗨', '👑', '👒', '👠', '👡', '👢', '💄', '💈', '🔗', '🔥', '🔦', '🔧', '🔨', '🔩', '🔰', '🔱', '🕰', '🕶', '🕹', '🖇', '🚀', '🤖', '🥀', '🥁', '🥂', '🥃', '🥐', '🥑', '🥒', '🥓', '🥔', '🥕', '🥖', '🥗', '🥘', '🥙', '🦀', '🦁', '🦂', '🦃', '🦄', '🦅', '🦆', '🦇', '🦈', '🦉', '🦐', '🦑', '⭐️', '⏰', '⏲', '⚠️', '⚡️', '⚰️', '⚽️', '⚾️', '⛄️', '⛅️', '⛈', '⛏', '⛓', '⌚️', '☎️', '⚜️', '✏️', '⌨️', '☁️', '☃️', '☄️', '☕️', '☘️', '☠️', '♨️', '⚒', '⚔️', '⚙️', '✈️', '✉️', '✒️']
    r = random.random()
    random.shuffle(emojis_list, lambda: r)
    new_list = [] + maker["answer"]
    for i in range(15):
        if emojis_list[i] not in new_list:
            new_list.append(emojis_list[i])
    n_list = new_list[:15]
    random.shuffle(n_list, lambda: r)
    maker.update({"list": n_list})
    return maker

def number_() -> dict:
    filename = "./cache/" + uuid.uuid4().hex + '.png'
    image = ImageCaptcha(width = 280, height = 140, font_sizes=[80,83])
    final_number = str(random.randint(0000, 9999))
    image.write("   " + final_number, str(filename))
    try:
        data = {"answer":list(final_number),"captcha": filename}
    except Exception as t_e:
        print(t_e)
        data = {"is_error": True, "error":t_e}
    return data



@app.on_callback_query()
async def cb_handler(bot, query):
    cb_data = query.data
    if query.data == "close_data":
        await query.message.delete()
    if query.data == "show_whisper":
        inline_message_id = query.inline_message_id
        whisper = whispers[inline_message_id]
        sender_uid = whisper['sender_uid']
        receiver_uname: Optional[str] = whisper['receiver_uname']
        whisper_text = whisper['text']
        from_user: User = query.from_user
        if receiver_uname and from_user.username \
            and from_user.username.lower() == receiver_uname.lower():
            await query.answer(whisper_text, show_alert=True)
            return
        if from_user.id == sender_uid or receiver_uname == '@':
            await query.answer(whisper_text, show_alert=True)
            return
        if not receiver_uname:
            await query.answer(whisper_text, show_alert=True)
            return
        await query.answer("◍ عفوا هذا ليس لك\n√", show_alert=True)
       
    if query.data == 'promote':
        user_id = query.data.split("_")[1]
        owner_id = query.data.split("_")[2]
        fed_id = get_fed_from_ownerid(owner_id)
        fed_name = get_fed_name(owner_id=owner_id)
        user = await bot.get_users(
        user_ids=user_id
     )
        owner = await bot.get_users(
        user_ids=owner_id
     ) 
        if user_id == query.from_user.id:
            fed_promote(fed_id, user_id)
            await query.edit_message_text(
                text=(
                    f"◍ المستخدم {user.mention} اصبح الان ادمن {fed_name} ({fed_id})\n√"
                )
            )
        else:
            await query.answer(
                text=(
                    "◍ أنت لست المستخدم الذي يتم ترقيته\n√"
                )
            )

    if query.data == 'cancel':
        if user_id == query.from_user.id:
            await query.edit_message_text(
                text=(
                    f"◍ تم رفض تفويض ترقيت الادمن بواسطه {user.mention}.\n√"
                )
            )

        elif owner_id == query.from_user.id:
            await query.edit_message_text(
                text=(
                    f"◍ تم الغاء ترقيته ادمن بواسطه {owner.mention}.\n√"
                )
            )
        else:
            await query.answer(
                text=(
                    "◍ أنت لست المستخدم الذي يتم ترقيته\n√"
                )
            )
    if "report_" in query.data: 
     splitter = (str(query.data).replace("report_", "")).split("=")
     chat_id = int(splitter[0])
     action = str(splitter[1])
     user_id = int(splitter[2])
     message_id = int(splitter[3])
     if action == "kick":
        try:
            await app.ban_chat_member(chat_id, user_id)
            await query.answer("✅ تم طرده بنجاح")
            await app.unban_chat_member(chat_id, user_id)
            return
        except RPCError as err:
            await query.answer("خطأ اثناء طرده!"
            )
     elif action == "ban":
        try:
            await app.ban_chat_member(chat_id, user_id)
            await query.answer("✅ تم حظره بنجاح")
            return
        except RPCError as err:
            await query.answer("خطأ اثناء حظره!")
     elif action == "del":
        try:
            await app.delete_messages(chat_id, message_id)
            await query.answer("✅ تم مسح الرساله")
            return
        except RPCError as err:
            await query.answer("خطأ اثناء مسح الرساله!")
    if "clear_rules" in query.data: 
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         await query.answer(
            "◍ أنت لست مسؤول حتى لا تحاول هذا الهراء المتفجر\n√",
         )
         return
        if user_status != "creator":
         await query.answer(
            "◍ انت مجرد ادمن وليس المالك صلاحياتك محدوده\n√",
        )
         return
        Rule(query.message.chat.id).clear_rules()
        await query.message.edit_text("◍ تم مسح قواعد الجروب بنجاح\n√")
        await query.answer("◍ مسحت القواعد لهذه المجموعه بنجاح\n√") 
    if "clear_warns" in query.data: 
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         await query.answer(
            "◍ انت لست ادمن كف عن هذا الهراء\n√",
         )
         return
        if user_status != "creator":
         await query.answer(
            "◍ انت مجرد ادمن ولست المالك صلاحياتك محدوده\n√",
        )
         return
        warn_db = WarnSettings(query.chat.id)
        warn_db.resetall_warns(query.message.chat.id)
        await query.message.edit_text("◍ إزالة جميع التحذر من جميع المستخدمين في هذه الدردشة\n√")
        await query.answer("◍ إزالة جميع التحذر من جميع المستخدمين في هذه الدردشة\n√")
    if "clear_notes" in query.data: 
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         await query.answer(
            "◍ انت لست ادمن كف عن هذا الهراء..√",
         )
         return
        if user_status != "creator":
         await query.answer(
            "◍ انت مجرد ادمن ولست المالك صلاحياتك محدوده..√",
        )
         return
        dbns.rm_all_notes(query.message.chat.id)
        await query.message.edit_text("◍ اذيلة جميع الملاحظات\n√")
    if "rm_allblacklist" in query.data: 
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         await query.answer(
            "◍ انت لست ادمن كف عن هذا الهراء..√",
         )
         return
        if user_status != "creator":
         await query.answer(
            "◍ انت مجرد ادمن ولست المالك صلاحياتك محدوده..√",
        )
         return
        dbb = Blacklist(query.message.chat.id)
        dbb.rm_all_blacklist()
        await query.message.delete()
        await query.answer("◍ تم مسح جميع المحظورين بنجاح\n√")

    if "rm_allfilters" in query.data: 
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         await query.answer(
            "◍ انت لست ادمن كف عن هذا الهراء..√",
         )
         return
        if user_status != "creator":
         await query.answer(
            "◍ انت مجرد ادمن ولست المالك صلاحياتك محدوده..√",
        )
         return
        dbf.rm_all_filters(query.message.chat.id)
        await query.message.edit_text(f"◍ تم اذالة جميع الفلاتر ل {query.message.chat.title}\n√")
        await query.answer("◍ تنظيف جميع الفلاتر\n√")
        return
    if "enableallcmds" in query.data: 
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         await query.answer(
            "◍ انت لست ادمن كف عن هذا الهراء..√",
         )
         return
        if user_status != "creator":
         await query.answer(
            "◍ انت مجرد ادمن ولست المالك صلاحياتك محدوده..√",
        )
         return
        db = Disabling(query.message.chat.id)
        db.rm_all_disabled()
        await query.message.edit_text("Enabled all!")    
 
    if "_unwarn" in query.data:    
      from_user = query.from_user
      chat_id = query.message.chat.id
      permissions = await member_permissions(chat_id, from_user.id)
      permission = "can_restrict_members"
      if permission not in permissions:
        return await query.answer("◍ ليس لديك صلاحيات كافية لأداء هذا الإجراء..√")
      user_id = query.data.split("_")[1]
      warn_db = Warns(query.message.chat.id)
      sup = warn_db.remove_warn(user_id)
      text = query.message.text.markdown
      text = f"~~{text}~~\n\n"
      text += f"__تم اذالة التحظير بواسطة {from_user.mention}__"
      await query.message.edit(text)

    if "_unban" in query.data:    
      from_user = query.from_user
      chat_id = query.message.chat.id
      permissions = await member_permissions(chat_id, from_user.id)
      permission = "can_restrict_members"
      if permission not in permissions:
        return await query.answer("◍ ليس لديك صلاحيات كافية لأداء هذا الإجراء..√")
      user_id = query.data.split("_")[1]
      await query.message.chat.unban_member(user_id)
      text = query.message.text.markdown
      text = f"~~{text}~~\n\n"
      text += f"__تم الغاء الحظر بواسطة {from_user.mention}__"
      await query.message.edit(text)
    if "_unmute" in query.data:    
      from_user = query.from_user
      chat_id = query.message.chat.id
      permissions = await member_permissions(chat_id, from_user.id)
      permission = "can_restrict_members"
      if permission not in permissions:
        return await query.answer("◍ ليس لديك صلاحيات كافية لأداء هذا الإجراء..√")
      user_id = query.data.split("_")[1]
      await query.message.chat.unban_member(user_id)
      text = query.message.text.markdown
      text = f"~~{text}~~\n\n"
      text += f"__تم الغاء كتمه بواسطة {from_user.mention}__"
      await query.message.edit(text)  
    if "unapprovecb" in query.data:
        user_id = query.data.split(":")[1]
        db = Approve(query.message.chat.id)
        approved_people = db.list_approved()
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
          await query.answer("◍ أنت لست حتي الان ادمم...√")
          return
        if user_status != "creator":
          await query.answer("◍ انت مجرد ادمن ولست المالك..√!")
          return
        db.unapprove_all()
        for i in approved_people:
          await query.message.chat.restrict_member(
            user_id=i[0],
            permissions=query.message.chat.permissions,
        )
          await query.message.delete()
          await query.answer("◍ رفض جميع المستخدمين\n√")
          return  
    if "unpinallcb" in query.data:
        user_id = query.data.split(":")[1]
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
           await query.answer("◍ أنت لست حتي الان ادمم...√!")
           return
        if user_status != "creator":
            await query.answer("◍ انت مجرد ادمن ولست المالك..√!")
            return
        try:
            await app.unpin_all_chat_messages(query.message.chat.id)

            await query.message.edit_text("◍ جميع الرسائل المثبتة كانت غير مؤمنة\n√")
        except Exception as e:
            return await app.send_message(LOG_GROUP_ID,text= f"{e}")
    if "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await app.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "تم الاتصال :✅"
            cb = "connectcb"
        else:
            stat = "انقطع الاتصالt:⛔️"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"الحاله ♻️", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("تنظيف🧹", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("⚒ الاوامر", callback_data="connectcb_")],
            [InlineKeyboardButton("« العودة", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"""
**📟 الدردشه المتصله حاليا √:**    

**🌐اسم المجموعه** : {title}
**🆔ايدي المجموعه** : `{group_id}`
**ℹ️عدد الاعضاء:**  `{hr.members_count}`   
**♻️الاحتيال:** `{hr.is_scam} `
            """,
            reply_markup=keyboard,
            parse_mode="md"
        )
        return 
    if "connectcb_" in query.data:  
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("« العوده", callback_data="backcb")]
        ])
        await query.message.edit_text(
            f"""
**◍ تتوفر الإجراءات مع المجموعات المتصلة..√:**

 • عرض وتوفير الفلاتر.
 • معلومات اكثر
            """,
            reply_markup=keyboard,
            parse_mode="md"
        )
        return 

    if "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await app.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"◍ تم الاتصال ب **{title}**\n√",
                parse_mode="md"
            )
        else:
            await query.message.edit_text('◍ حدث بعض الأخطاء..🚫', parse_mode="md")
        return 
    if "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await app.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"انقطع الاتصال من **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text(
                f"◍ حدث بعض الأخطاء..🚫",
                parse_mode="md"
            )
        return 
    if "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "◍ تم مسح الاتصال بنجاح\n√"
            )
        else:
            await query.message.edit_text(
                f"◍ حدث بعض الأخطاء..🚫",
                parse_mode="md"
            )
        return 
    if query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "◍ لا توجد اتصالات نشطة !! اتصل ببعض المجموعات أولا.\n√",
            )
            return await query.answer('◍ القرصنة هي الجريمة')
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
                            text=f"{title}{act}", callback_data=f"المجموعه🌎:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "◍ تفاصيل المجموعة المتصلة ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )


    if cb_data.startswith("new_"):
        chat_id = query.data.rsplit("_")[1]
        user_id = query.data.split("_")[2]
        captcha = query.data.split("_")[3]
        if query.from_user.id != int(user_id):
            await query.answer("❗️ هذه الرسالة ليست لك!", show_alert=True)
            return
        if captcha == "N":
            type_ = "Number"
        elif captcha == "E":
            type_ = "Emoji"
        chk = captchas().add_chat(int(chat_id), captcha)
        if chk == 404:
            await query.message.edit("◍ التحقق مفعل في المجموعه اكتب اذاله لايقاف التحقق\n√")
            return
        else:
            await query.message.edit(f"{type_} ◍ التحقق مفعل في مجموعتك\n√")
    if cb_data.startswith("off_"):
        chat_id = query.data.rsplit("_")[1]
        user_id = query.data.split("_")[2]
        if query.from_user.id != int(user_id):
            await query.answer("❗️ هذه الرسالة ليست لك!", show_alert=True)
            return
        j = captchas().delete_chat(chat_id)
        if j:
            await query.message.edit("◍ التحقق مغلق في مجموعتك\n√")

    if cb_data.startswith("verify_"):
        chat_id = query.data.split("_")[1]
        user_id = query.data.split("_")[2]
        if query.from_user.id != int(user_id):
            await query.answer("❗️ هذه الرسالة ليست لك!", show_alert=True)
            return
        chat = captchas().chat_in_db(int(chat_id))
        if chat:
            c = chat["captcha"]
            markup = [[],[],[]]
            if c == "N":
                await query.answer("◍ يتم صنع تحقق لك\n√", show_alert=True)
                data_ = number_()
                _numbers = data_["answer"]
                list_ = ["0","1","2","3","5","6","7","8","9"]
                random.shuffle(list_)
                tot = 2
                LocalDB[int(user_id)] = {"answer": _numbers, "list": list_, "mistakes": 0, "captcha": "N", "total":tot, "msg_id": None}
                count = 0
                for i in range(3):
                    markup[0].append(InlineKeyboardButton(f"{list_[count]}", callback_data=f"jv_{chat_id}_{user_id}_{list_[count]}"))
                    count += 1
                for i in range(3):
                    markup[1].append(InlineKeyboardButton(f"{list_[count]}", callback_data=f"jv_{chat_id}_{user_id}_{list_[count]}"))
                    count += 1
                for i in range(3):
                    markup[2].append(InlineKeyboardButton(f"{list_[count]}", callback_data=f"jv_{chat_id}_{user_id}_{list_[count]}"))
                    count += 1
            if c == "E":
                await query.answer("◍ يتم صنع تحقق لك...\n√", show_alert=True)
                data_ = emoji_()
                _numbers = data_["answer"]
                list_ = data_["list"]
                count = 0
                tot = 3
                for i in range(5):
                    markup[0].append(InlineKeyboardButton(f"{list_[count]}", callback_data=f"jv_{chat_id}_{user_id}_{list_[count]}"))
                    count += 1
                for i in range(5):
                    markup[1].append(InlineKeyboardButton(f"{list_[count]}", callback_data=f"jv_{chat_id}_{user_id}_{list_[count]}"))
                    count += 1
                for i in range(5):
                    markup[2].append(InlineKeyboardButton(f"{list_[count]}", callback_data=f"jv_{chat_id}_{user_id}_{list_[count]}"))
                    count += 1
                LocalDB[int(user_id)] = {"answer": _numbers, "list": list_, "mistakes": 0, "captcha": "E", "total":tot, "msg_id": None}
            c = LocalDB[query.from_user.id]['captcha']
            if c == "N":
                typ_ = "number"
            if c == "E":
                typ_ = "emoji"
            msg = await bot.send_photo(chat_id=chat_id,
                            photo=data_["captcha"],
                            caption=f"{query.from_user.mention} يرجى النقر على كل زر {typ_} الذي يتم عرضه في الصورة، {tot} mistacks مسموح بها.",
                            reply_markup=InlineKeyboardMarkup(markup))
            LocalDB[query.from_user.id]['msg_id'] = msg.message_id
            await query.message.delete()
    if cb_data.startswith("jv_"):
        chat_id = query.data.rsplit("_")[1]
        user_id = query.data.split("_")[2]
        _number = query.data.split("_")[3]
        if query.from_user.id != int(user_id):
            await query.answer("◍ هذه الرسالة ليست لك..!", show_alert=True)
            return
        if query.from_user.id not in LocalDB:
            await query.answer("◍ حاول مرة أخرى بعد إعادة الانضمام\n√", show_alert=True)
            return
        c = LocalDB[query.from_user.id]['captcha']
        tot = LocalDB[query.from_user.id]["total"]
        if c == "N":
            typ_ = "number"
        if c == "E":
            typ_ = "emoji"
        if _number not in LocalDB[query.from_user.id]["answer"]:
            LocalDB[query.from_user.id]["mistakes"] += 1
            await query.answer(f"◍ لقد ضغط علي ذارار خطأ {typ_}\n√", show_alert=True)
            n = tot - LocalDB[query.from_user.id]['mistakes']
            if n == 0:
                await query.message.edit_caption(f"{query.from_user.mention}, ◍ انت فشلت في حل لغز التحقق\n\n"
                                               f"◍ يمكنك المحاوله مره اخري بعد 5 دقائق\n√",
                                               reply_markup=None)
                await asyncio.sleep(300)
                del LocalDB[query.from_user.id]
                return
            markup = MakeCaptchaMarkup(query.message["reply_markup"]["inline_keyboard"], _number, "❌")
            await query.message.edit_caption(f"{query.from_user.mention}, حدد كل الذي {typ_}s تراه في الصوره. "
                                           f"يسمح لك فقط {n} بلاخطاء\n√",
                                           reply_markup=InlineKeyboardMarkup(markup))
        else:
            LocalDB[query.from_user.id]["answer"].remove(_number)
            markup = MakeCaptchaMarkup(query.message["reply_markup"]["inline_keyboard"], _number, "✅")
            await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(markup))
            if not LocalDB[query.from_user.id]["answer"]:
                await query.answer("تم التحقق بنجاح ✅", show_alert=True)
                #send welcome message
                greatdb = Greetings(chat_id)
                status = greatdb.get_welcome_status()
                raw_text = greatdb.get_welcome_text()
                if not raw_text:
                  return
                text, button = await parse_button(raw_text)
                button = await build_keyboard(button)
                button = InlineKeyboardMarkup(button) if button else None

                if "{chatname}" in text:
                   text = text.replace("{chatname}", query.message.chat.title)
                if "{mention}" in text:
                   text = text.replace("{mention}", (await app.get_users(user_id)).mention)
                if "{id}" in text:
                  text = text.replace("{id}", (await app.get_users(user_id)).id)
                if "{username}" in text:
                  text = text.replace("{username}", (await app.get_users(user_id)).username)
                if "{first}" in text:
                  text = text.replace("{first}", (await app.get_users(user_id)).first_name)     
                if "{last}" in text:
                  text = text.replace("{last}", (await app.get_users(user_id)).last_name) 
                if "{count}" in text:
                  text = text.replace("{count}", await app.get_chat_members_count(chat_id)) 
                if status:
                   await app.send_message(
                         chat_id,
                               text=text,
                               reply_markup=button,
                               disable_web_page_preview=True,
                     )           
                del LocalDB[query.from_user.id]
                await bot.unban_chat_member(chat_id=query.message.chat.id, user_id=query.from_user.id)
                await query.message.delete(True)
            await query.answer()
    if cb_data.startswith("done_"):
        await query.answer("◍ لا تضغط علي نفس الزر مره اخري\n√", show_alert=True)
    if cb_data.startswith("wrong_"):
        await query.answer("◍ لا تضغط علي نفس الزر مره اخري\n√", show_alert=True)