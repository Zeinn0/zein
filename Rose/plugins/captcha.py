import asyncio
from  Rose import app
from Rose.mongo.captcha import captchas
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from pyrogram import filters
from . antlangs import *
from Rose.Inline.query import *
from lang import get_command
from Rose.utils.commands import *
from Rose.utils.lang import *
from Rose.utils.custom_filters import restrict_filter
from button import *

CAPTCH = get_command("CAPTCH")
REMOVEC = get_command("REMOVEC")
db = {}

@app.on_message(command(CAPTCH) & ~filters.private & restrict_filter)
@language
async def add_chat(client, message: Message, _):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user = await bot.get_chat_member(chat_id, user_id)
    if user.status == "creator" or user.status == "administrator":

      chat = captchas().chat_in_db(chat_id)
      if chat:
            await message.reply_text(_["capt1"])
      else:
           await message.reply_text(text=_["capt2"],
                                    reply_markup=InlineKeyboardMarkup(
                                        [
                                            [
                                                InlineKeyboardButton(text="Captcha On ✅", callback_data=f"new_{chat_id}_{user_id}_E"),
                                                InlineKeyboardButton(text="Captcha Off ❌", callback_data=f"off_{chat_id}_{user_id}")
                                            ],
                                            [
                                                InlineKeyboardButton(text="Close Menu ✖️", callback_data=f"close_data")
                                            ],
                                    ]))
    
      
      args = get_arg(message)
      lower_args = args.lower()
      if lower_args == "on":     
        await message.reply_text(text=_["capt2"],
                                    reply_markup=InlineKeyboardMarkup(
                                        [
                                            [
                                                InlineKeyboardButton(text="فتح التحقق", callback_data=f"new_{chat_id}_{user_id}_E"),
                                                InlineKeyboardButton(text="قفل التحقق ❌", callback_data=f"off_{chat_id}_{user_id}")
                                            ],
                                            [
                                                InlineKeyboardButton(text="حذف القائمه ✖️", callback_data=f"close_data")
                                            ],
                                    ]))  
      if lower_args == "off":     
           await message.reply_text(text=_["capt2"],
                                    reply_markup=InlineKeyboardMarkup(
                                        [
                                            [
                                                InlineKeyboardButton(text="فتح التحقق✅", callback_data=f"new_{chat_id}_{user_id}_E"),
                                                InlineKeyboardButton(text="قفل التحقق ❌", callback_data=f"off_{chat_id}_{user_id}")
                                            ],
                                            [
                                                InlineKeyboardButton(text="حذف القائمه✖️", callback_data=f"close_data")
                                            ],
                                    ]))                                                      
      

async def send_captcha(app,message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    chat = captchas().chat_in_db(chat_id)
    if not chat:
        return
    try:
        user_s = await app.get_chat_member(chat_id, user_id)
        if (user_s.is_member is False) and (db.get(user_id, None) is not None):
            try:
                await app.delete_messages(
                    chat_id=chat_id,
                    message_ids=db[user_id]["msg_id"]
                )
            except:
                pass
            return
        elif (user_s.is_member is False):
            return
    except UserNotParticipant:
        return
    chat_member = await app.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
        if chat_member.restricted_by.id == (await app.get_me()).id:
            pass
        else:
            return
    try:
        if db.get(user_id, None) is not None:
            try:
                await app.send_message(
                    chat_id=chat_id,
                    text=f"◍ قم بلانضمام️ {message.from_user.mention} مره اخري للمجموعه وحل التحقق\n\n"
                         f"◍ يمكنك التجربه مره اخري بعد 5 دقائق\n√.",
                    disable_web_page_preview=True
                )
                await app.delete_messages(chat_id=chat_id,
                                             message_ids=db[user_id]["msg_id"])
            except:
                pass
            await asyncio.sleep(300)
            del db[user_id]
    except:
        pass
    try:
        await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
    except:
        return
    await app.send_message(chat_id,
                              text=f"◍ اهلا {message.from_user.mention}, بك في {message.chat.title} المجموعه\n\n لاستمرار يرجي التحقق من انك لست روبوت\n√",
                              reply_markup=InlineKeyboardMarkup(
                                  [
                                      [
                                          InlineKeyboardButton(text="حل التحقق🤖", callback_data=f"verify_{chat_id}_{user_id}"),
                                          InlineKeyboardButton(text="تخطي ❗️", callback_data=f"_unmute_{user_id}")
                                          
                                      ]
                                      ]
                                ))
    return 400

def MakeCaptchaMarkup(markup, _number, sign):
    __markup = markup
    for i in markup:
        for k in i:
            if k["text"] == _number:
                k["text"] = f"{sign}"
                k["callback_data"] = "done_"
                return __markup

@app.on_message(command(REMOVEC) & ~filters.private)
@language
async def del_chat(client, message: Message, _):
    chat_id = message.chat.id
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if user.status == "creator" or user.status == "administrator" :
        j = captchas().delete_chat(chat_id)
        if j:
            await message.reply_text(_["capt3"])

__MODULE__ = f"{fff}"
__HELP__ = f"""
👮‍♂️╖ ❬ م4 ❭ اوامر اصحاب الرتب ⇊
⚠️╜ الادمن «» المنشئ «» المالك
⋖≔≖☤≖≕〖 ᥉᥆υᖇᥴᥱ ᥴᖇᎥ᥉ƚᥱꪀ 〗≔≖☤≖≕⋗
🥳 « المميز » ⇊
⋖≔≖☤≖≕〖 ᥉᥆υᖇᥴᥱ ᥴᖇᎥ᥉ƚᥱꪀ 〗≔≖☤≖≕⋗
🙈╖ كشف
🔇╢ المحظورين
🔕╢ المكتومين
🍿╜ بس كده 😹💔
⋖≔≖☤≖≕〖 ᥉᥆υᖇᥴᥱ ᥴᖇᎥ᥉ƚᥱꪀ 〗≔≖☤≖≕⋗
🐣 « الادمن » ⇊
⋖≔≖☤≖≕〖 ᥉᥆υᖇᥴᥱ ᥴᖇᎥ᥉ƚᥱꪀ 〗≔≖☤≖≕⋗
🥳╖ رفع مميز «» تنزيل مميز
🙋╢ الترحيب
🤬╢ اضف مغادره «» مسح المغادره
💩╢ رساله المغادره
🤖╢ كشف البوتات
🥳╢ المميزين «» حذف المميزين
🛡╢ حظر «» الغاء حظر
🗡╢ كتم «» الغاء كتم
🗑╢ حظر لمده + المده
🧺╢ كتم لمده + المده
😠╢ طرد «» تطهير 
📌╢ تثبيت «» تثبيت بدون اشعار
🧷╢ الغاء تثبيت الكل
📚╜ ❬ + ❭ جميع ماسبق
⋖≔≖☤≖≕〖 ᥉᥆υᖇᥴᥱ ᥴᖇᎥ᥉ƚᥱꪀ 〗≔≖☤≖≕⋗
🤵 « المنشئ » ⇊
⋖≔≖☤≖≕〖 ᥉᥆υᖇᥴᥱ ᥴᖇᎥ᥉ƚᥱꪀ 〗≔≖☤≖≕⋗
🐣╖ رفع «» تنزيل ادمن
💌╢ اضف «» حذف  ❬ رد ❭
👨‍🎨╢ الردود «» حذف الردود
🔕╢ ايقاف المنشن
💫╢ تعيين «» مسح  ❬ الايدي ❭
🍫╢ الادمنيه «» حذف الادمنيه
🍻╢ اضف ترحيب
🎲╢ حذف المحظورين «» المكتومين
🎯╢ منع + الكلمه
🚜╢ الغاء منع + الكلمه
🚨╢ حذف الكلمات الممنوعه
🔍╢ المميزين عام
📚╜ ❬ + ❭ جميع ماسبق
⋖≔≖☤≖≕〖 ᥉᥆υᖇᥴᥱ ᥴᖇᎥ᥉ƚᥱꪀ 〗≔≖☤≖≕⋗
👮‍♂️ « المالك » ⇊
⋖≔≖☤≖≕〖 ᥉᥆υᖇᥴᥱ ᥴᖇᎥ᥉ƚᥱꪀ 〗≔≖☤≖≕⋗
🔼╖ اضف صوره «» وصف (للجروب)
🤵╢ رفع منشئ «» تنزيل منشئ
🔊╢ تاج للاعضاء «» للكل
🔗╢ اضف رابط «» مسح الرابط
🔖╢ اضف «» حذف  ❬ امر ❭
📝╢ الاوامر المضافه
🗑╢ حذف الاوامر المضافه
🔏╢ اضف اسم «» تحديث
🍿╢ المنشئين «» حذف المنشئين
📚╜ ❬ + ❭ جميع ماسبق
⋖≔≖☤≖≕〖 ᥉᥆υᖇᥴᥱ ᥴᖇᎥ᥉ƚᥱꪀ 〗≔≖☤≖≕⋗
"""
