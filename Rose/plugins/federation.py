from Rose import *
from pyrogram import filters
import time
import uuid
from Rose.mongo.feddb import *
import html
from Rose.utils.custom_filters import owner_filter
from Rose.utils.filter_groups import *
import asyncio
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from Rose.utils.functions import extract_user
import asyncio
from button import *

                                              
@app.on_message(filters.command("joinfed") & owner_filter )
async def JoinFeds(client, message):
    group_id = message.chat.id
    userid = message.from_user.id if message.from_user else None
    if not (
        message.chat.type == 'supergroup'
    ):
        await message.reply(
            "Only supergroups can join feds."
        )
        return 
    
    if not (
        len(message.command) >= 2
    ):
        await message.reply(
            "You need to specify which federation you're asking about by giving me a FedID!"
        )
        return
    st = await app.get_chat_member(group_id, userid)
    if st.status != "creator":
            await message.reply(
            "Only Group Creator can join new fed!"
        )
            return 

    if not (
        is_fed_exist(message.command[1])
    ):
        await message.reply(
            "This FedID does not refer to an existing federation."
        )
        return

    fed_id = message.command[1]
    chat_id = message.chat.id
    chat_title = html.escape(message.chat.title)
    fed_name = get_fed_name(fed_id)

    join_fed_db(chat_id, chat_title,  fed_id)
    await message.reply(
        f'Successfully joined the "{fed_name}" federation! '
    )


@app.on_message(filters.command("leavefed") & owner_filter )
async def leaveFeds(client, message):
    group_id = message.chat.id
    userid = message.from_user.id if message.from_user else None
    if not (
        len(message.command) >= 2
    ):
        await message.reply(
            "You need to specify which federation you're asking about by giving me a FedID!"
        )
        return
    st = await app.get_chat_member(group_id, userid)
    if st.status != "creator":
            await message.reply(
            "Only Group Creator can leave fed!"
        )
            return 

    if not (
        is_fed_exist(message.command[1])
    ):
        await message.reply(
            "This FedID does not refer to an existing federation."
        )
        return

    fed_id = message.command[1]
    chat_id = message.chat.id
    chat_title = html.escape(message.chat.title)
    fed_name = get_fed_name(fed_id)

    leave_fed_db(chat_id, chat_title,  fed_id)
    await message.reply(
        f'Successfully left the "{fed_name}" federation! '
    )



@app.on_message(filters.command("fedinfo") & owner_filter )
async def infoFeds(client, message):
    group_id = message.chat.id
    userid = message.from_user.id if message.from_user else None
    if not (
        len(message.command) >= 2
    ):
        await message.reply(
            "You need to specify which federation you're asking about by giving me a FedID!"
        )
        return
    if not (
        is_fed_exist(message.command[1])
    ):
        await message.reply(
            "This FedID does not refer to an existing federation."
        )
        return
    fed_id = message.command[1]
    name = get_fed_name(fed_id)
    chats = get_connected_chats(fed_id)
    await message.reply(
        f"""
<b>Federation info</b>
<b>Name:</b> {name}
<b>ID:</b> <code>{fed_id}</code>
<b>Chats in the fed:</b> {len(chats)}"""
    )



TELEGRAM_SERVICES_IDs = (
    [
        777000, # Telegram Service Notifications
        1087968824 # GroupAnonymousBot
    ]
)

@app.on_message(filters.command("newfed"))
async def NewFed(client, message):

    if (
        message.chat.type == 'supergroup'
    ):
        await message.reply(
            'Create your federation in my PM - not in a group.'
        )
        return 

    if not (
        len(message.command) >= 2
    ):
        await message.reply(
            "Give your federation a name!"
        )  
        return

    if (
        message.from_user.id in TELEGRAM_SERVICES_IDs
    ):
        await message.reply(
            "This is telegram services IDs, I should not create any new fed for it."
        )
        return

    if (
        len(' '.join(message.command[1:])) > 60
    ):
        await message.reply(
            "Your fed must be smaller than 60 words."
        )
        return

    fed_name = ' '.join(message.command[1:])
    fed_id = str(uuid.uuid4())
    owner_id = message.from_user.id 
    uname = message.from_user.mention
    created_time = time.ctime() 

    new_fed_db(fed_name, fed_id, created_time, owner_id)

    await message.reply(
        (f"""
**Congrats, you have successfully created a federation **   

**Name:** {fed_name}
**ID:** `{fed_id}`
**Creator:** {uname}     
**Created Date** {created_time}

Use this ID to join federation! eg:
`/joinfed {fed_id}`    
        """
        )
    )

    await app.send_message(
        chat_id=LOG_GROUP_ID,
        text=(f"""
**New Federation created with FedID: **

**Name:** {fed_name}
**ID:** `{fed_id}`
**Creator:** {uname}     
**Created Date** {created_time}
"""
        )
    )


@app.on_message(filters.all & filters.group, group=fban)
async def fed_checker(client, message):
    
    chat_id = message.chat.id
    
    if not message.from_user:
        return

    user_id = message.from_user.id 
    fed_id = get_fed_from_chat(chat_id)
    
    if not fed_id == None:
        if is_user_fban(fed_id, user_id):
            fed_reason = get_fed_reason(fed_id, user_id)
            text = (
                    "**This user is banned in the current federation:**\n\n"
                    f"User: {message.from_user.mention} (`{message.from_user.id}`)\n"
                    f"Reason: `{fed_reason}`"
                )
            if await app.chat.ban_member(chat_id, user_id): 
                    text += '\nAction: `Banned`'
            await asyncio.sleep(1)
            await app.chat.unban_member(chat_id, user_id)
            await message.reply(
                text
            )
            return

@app.on_message(filters.command("fedpromote"))
async def FedPromote(client, message):
    user_id = await extract_user(message)
    
    owner_id = message.from_user.id 
    fed_id = get_fed_from_ownerid(owner_id)
    fed_name = get_fed_name(owner_id=owner_id)
    user = await app.get_users(
        user_ids=user_id
    )

    if (
        message.chat.type == 'private'
    ):
        await message.reply(
            "This command is made to be run in a group where the person you would like to promote is present."
        )
        return
    
    if (
        fed_id == None
    ):
        await message.reply(
            "Only federation creators can promote people, and you don't even seem to have a federation to promote to!"
        )
        return
    
    if (
        is_user_fban(fed_id, user_id)
    ):
        await message.reply(
            f"User {user.mention} is fbanned in {fed_name}. You have to unfban them before promoting."
        )
        return

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text='Confirm', callback_data=f'promote_{user_id}_{owner_id}'),
                    InlineKeyboardButton(text='Cancel', callback_data=f'cancel_{user_id}_{owner_id}')
                ]
            ]
        )

    await message.reply(
        f"Please get {user.mention} to confirm that they would like to be fed admin for {fed_name}.",
        reply_markup=keyboard
    )



@app.on_message(filters.command("fban"))
async def fed_ban(client, message):
    chat_id = message.chat.id
    userID = await extract_user(message)
    
    bannerMention = message.from_user.mention 
    banner_name = message.from_user.first_name
    bannedID = message.from_user.id

    fed_id = get_fed_from_chat(chat_id)
    fed_name = get_fed_name(fed_id=fed_id)
    get_user = await app.get_users(
                user_ids=userID
            )

    FED_ADMINS = get_fed_admins(fed_id)
    
    if userID == BOT_ID:
        await message.reply(
            " I am not going to fban myself."
        )
        return
    
    if bannedID not in FED_ADMINS:
        await message.reply(
            f"You aren't a federation admin of {fed_name}."
        )
        return

    if (
        message.reply_to_message 
        and len(message.command) >= 2
    ):
        reason_text = ' '.join(message.text.split()[1:])   
    
    elif (
        len(message.command) >= 3
    ):
        reason_text = ' '.join(message.text.split()[2:])  

    else:
        reason_text = 'No reason was given'
     
    
    reason = f"{reason_text} // Fbanned by {banner_name} id {bannedID}"
    if is_user_fban(fed_id, userID):
        old_reason = get_fed_reason(fed_id, userID)
        if not old_reason == reason:
            update_reason(fed_id, userID, reason)
            fed_message = (
            f'**This user was already banned in the** "{fed_name}" **federation, I\'ll update the reason:**\n\n'
            f"Fed Administrator: {bannerMention}\n"
            f"User: {get_user.mention}\n"
            f"User ID: `{userID}`\n"
            f"Old Reason: `{old_reason}`\n"
            f"Updated Reason: `{reason}`"
        )
        else:
            fed_message = (
                f"User {get_user.mention} has already been fbanned, with the exact same reason."
            )
    else:
        user_fban(fed_id, userID, reason)
        connected_chats = get_connected_chats(fed_id)
        BannedChats = []
        for chat_id in connected_chats:
            GetData = await app.get_chat_member(
                chat_id=chat_id,
                user_id=BOT_ID
            )
            if GetData['can_restrict_members']:
                if await app.chat.ban_member(
                    chat_id,
                    userID
                ):
                    BannedChats.append(chat_id)
            else:
                continue

        fed_message = (
                f'**New Federation Ban in the** "{fed_name}" **federation:**\n\n'
                f"Fed Administrator: {bannerMention}\n"
                f"User: {get_user.mention}\n"
                f"User ID: `{userID}`\n"
                f"Reason: {reason}\n"
                f"Affected Chats: `{len(BannedChats)}`"
            )

    await message.reply(
        fed_message
    )

@app.on_message(filters.command("unfban"))
async def unfed_ban(client, message):
    chat_id = message.chat.id
    userID = await extract_user(message)
    
    bannerMention = message.from_user.mention 
    banner_name = message.from_user.first_name
    bannedID = message.from_user.id

    fed_id = get_fed_from_chat(chat_id)
    fed_name = get_fed_name(fed_id=fed_id)
    get_user = await app.get_users(
                user_ids=userID
            )

    FED_ADMINS = get_fed_admins(fed_id)
    
    if userID == BOT_ID:
        await message.reply(
             "How do you think I would've fbanned myself that you are trying to unfban me? Never seen such retardedness ever before."
        )
        return
    
    if bannedID not in FED_ADMINS:
        await message.reply(
            f"You aren't a federation admin of {fed_name}."
        )
        return

    if (
        message.reply_to_message 
        and len(message.command) >= 2
    ):
        reason_text = ' '.join(message.text.split()[1:])   
    
    elif (
        len(message.command) >= 3
    ):
        reason_text = ' '.join(message.text.split()[2:])  

    else:
        reason_text = 'No reason was given'
     
    
    reason = f"{reason_text} // un-Fbanned by {banner_name} id {bannedID}"
    if is_user_fban(fed_id, userID):
        user_unfban(fed_id, userID)
    else:
        pass

    # await message.reply(
    #     unfed_message
    # )


@app.on_message(filters.command("renamefed"))
async def Rename_fed(client, message):
    owner_id = message.from_user.id 

    if not (
        message.chat.type == 'private'
    ):
        await message.reply(
            "You can only rename your fed in PM."
        )
        return

    if not (
        len(message.command) >= 2
    ):
        await message.reply(
            "You need to give your federation a name! Federation names can be up to 64 characters long."
        )
        return
    
    if (
        len(' '.join(message.command[1:])) > 60
    ):
        await message.reply(
            "Your fed must be smaller than 60 words."
        )
        return

    fed_id = get_fed_from_ownerid(owner_id)
    if fed_id == None:
        await message.reply(
            "It doesn't look like you have a federation yet!"
        )
        return
    
    fed_name = ' '.join(message.command[1:])
    old_fed_name = get_fed_name(owner_id=owner_id)
    

    fed_rename_db(owner_id, fed_name)
    await message.reply(
        f"I've renamed your federation from '{old_fed_name}' to '{fed_name}'. ( FedID: `{fed_id}`.)"
    )

    # Send notification of Rename Fed to the all connected chat

    connected_chats = get_connected_chats(fed_id)
    for chat_id in connected_chats:
        await app.send_message(
            chat_id=chat_id,
            text=(
                "**Federation renamed**\n"
                f"**Old fed name:** {old_fed_name}\n"
                f"**New fed name:** {fed_name}\n"
                f"FedID: `{fed_id}`"
            )
        )

__MODULE__ = f"{fbf}"
__HELP__ = """
💎╖ ❬ م5 ❭ اوامر المطورين ⇊
👮‍♂️╜ « المطور » ⇊
════════ 𝑽𝑨𝑴𝑩𝑰𝑹 ════════ٴ
🤴╖ رفع «» تنزيل ❬ مالك ❭
🔂╢ تغيير رابط الجروب
🔊╢ اذاعه بالمجموعات
👨‍🏭╢ اذاعه بالتوجيه للمجموعات
🤹‍♀╢ اذاعه موجهه بالتثبيت
☀️╢ اذاعه خاص
💘╢ اذاعه بالتوجيه خاص
🎙️╢ اذاعه بالتثبيت
📶╢ جلب نسخه احتياطيه
🏋‍♂╢ رفع نسخه احتياطيه
🍃╢ الاحصائيات
🚷╢ حذف المالكين
📚╜ ❬ + ❭ جميع ماسبق
════════ 𝑽𝑨𝑴𝑩𝑰𝑹 ════════ٴ
💎 « المطور الاساسي » ⇊
════════ 𝑽𝑨𝑴𝑩𝑰𝑹 ════════ٴ
📑╖ اضف «» حذف رد عام
🤴╢ رفع «» تنزيل ❬ مميز عام ❭
💎╢ مسح المميزين عام
🗃️╢ الردود العامه
🧨╢ حذف الردود العامه
🛠╢ اذاعه بالتوجيه خاص
🍃╢ اذاعه بالتوجيه للمجموعات
🎯╢ اذاعه بالتثبيت
☀️╢ اذاعه موجهه بالتثبيت
🧲╢ جلب «» رفع ❬نسخه احتياطيه❭
⏳╢ الاحصائيات
🤴╢ رفع «» تنزيل ❬ مطور ❭
🤖╢ المطورين «» حذف المطورين
🔗╢ ضع اسم للبوت
📝╢ تغيير رساله المغادره
🚫╢ حظر «» كتم  ❬ عام ❭
🥺╢ المكتومين  عام 
💔╢ المحظورين عام
♻️╢ الغاء العام
📚╜ ❬ + ❭ جميع ماسبق
════════ 𝑽𝑨𝑴𝑩𝑰𝑹 ════════
"""
