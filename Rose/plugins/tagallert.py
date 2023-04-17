from Rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Rose.utils.commands import *
from Rose.utils.lang import *
from Rose.mongo import taggeddb
from button import *

def get_info(id):
    return taggeddb.find_one({"id": id})

@app.on_message(command(["tagalert"]))
@language
async def locks_dfunc(client, message: Message, _):
   lol = await message.reply(_["spoil2"])
   if len(message.command) != 2:
      return await lol.edit(_["tagg1"])

   parameter = message.text.strip().split(None, 1)[1].lower()

   if parameter == "on" or parameter=="ON":
     if not message.from_user:
       return
     if not message.from_user.username:
       return await lol.edit(_["tagg2"])

     uname=str(message.from_user.username)
     uname = uname.lower()
     taggeddb.insert_one({f"teg": uname})
     return await lol.edit(_["tagg3"].format(uname))

   if parameter == "off" or parameter=="OFF":
     if not message.from_user:
       return
     if not message.from_user.username:
       return await lol.edit(_["tagg2"])
     uname = message.from_user.username
     uname = uname.lower()
     taggeddb.delete_one({f"teg": uname})
     return await lol.edit(_["tagg5"])
   else:
     await lol.edit(_["tagg1"])
       
@app.on_message(filters.incoming)
async def mentioned_alert(client, message):   
    try:
        if not message:
            message.continue_propagation()
            return
        if not message.from_user:
            message.continue_propagation()
            return    
        input_str = message.text
        input_str = input_str.lower()
        if "@" in input_str:
            
            input_str = input_str.replace("@", "  |")
            Rose = input_str.split("|")[1]
            text = Rose.split()[0]
        isittrue = taggeddb.find_one({f"teg": text})    
        if isittrue == None:
          return
        if text == message.chat:
          return 
        try:
            chat_name = message.chat.title
            tagged_msg_link = message.link   
        except:
            return message.continue_propagation()
        user_ = message.from_user.mention or f"@{message.from_user.username}"
        final_tagged_msg = f"""
**🗣 قام شخص بعمل منشن عليك**

**الجروب:** {chat_name}
**يوزر المستخدم:** {user_}
**الرساله:**
{message.text} """
        button_s = InlineKeyboardMarkup([[InlineKeyboardButton("📮 معلومات اكثر عن الرساله", url=tagged_msg_link)]])
        try:
            sz = await client.send_message(chat_id=f"{text}", text=final_tagged_msg,reply_markup=button_s,disable_web_page_preview=True)
            pin = await sz.pin(disable_notification=True, both_sides=True)
            await pin.delete()
        except:
            return message.continue_propagation()
        message.continue_propagation()
    except:
        return message.continue_propagation()
    
