from Rose import *
from Rose import bot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup, CallbackQuery
from Rose.utils.lang import *



keyboard =InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="عربي 🇪🇬", callback_data="languages_en"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🇱🇰 සිංහල", callback_data="languages_si"
            ), 
            InlineKeyboardButton(
                text="🇮🇳 हिन्दी", callback_data="languages_hi"
            )
        ], 
        [
            InlineKeyboardButton(
                text="🇮🇹 Italiano", callback_data="languages_it"
            ), 
            InlineKeyboardButton(
                text="🇮🇳 తెలుగు", callback_data="languages_ta"
            )
        ], 
        [
            InlineKeyboardButton(
                text="🇮🇩 Indonesia", callback_data="languages_id"
            ), 
            InlineKeyboardButton(
                text="English 🇬🇬", callback_data="languages_ar"
            ),
        ], 
        [
            InlineKeyboardButton(
                text="🇮🇳 മലയാളം", callback_data="languages_ml"
            ), 
            InlineKeyboardButton(
                text="🇲🇼 Chichewa", callback_data="languages_ny"
            ),
        ], 
        [
            InlineKeyboardButton(
                text="🇩🇪 German", callback_data="languages_ge"
            ), 
            InlineKeyboardButton(
                text="🇷🇺 Russian", callback_data="languages_ru"
            ), 
        ], 
        [  
            InlineKeyboardButton(
                text="ضيـف البـوت لمجـموعتـك ✅",
                url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
            )
        ]
    ]
)

@app.on_callback_query(filters.regex("_langs"))
@languageCB
async def commands_callbacc(client, CallbackQuery, _):
    user = CallbackQuery.message.from_user.mention
    await app.send_message(
        CallbackQuery.message.chat.id,
        text= "◍ اهلا بك في قسم اللغات..\nاختر من اللغات ما يناسبك..\nمن خلال الضغط علي ذر اللغه\n√",
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )

@app.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.answer("الرجوع الي البدايه⚡")
    await query.edit_message_text(
        f"""ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
🎤╖ أهلآ بك عزيزي أنا بوت « {BOT_MENTION} »
⚙️╢ وظيفتي حماية المجموعات
✅╢ لتفعيل البوت عليك اتباع مايلي 
🔘╢ أضِف البوت إلى مجموعتك
⚡️╢ ارفعهُ » مشرف
⬆️╜ سيتم ترقيتك مالك في البوت
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("الاوامر 📚", callback_data="bot_commands"),
                    InlineKeyboardButton("ℹ️ حول", callback_data="_about"),
                ],
                [InlineKeyboardButton("تغير اللغه 🌐", callback_data="_langs")],
                [
                    InlineKeyboardButton(
                        "ضيـف البـوت لمجـموعتـك ✅", url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
    

@app.on_callback_query(filters.regex("_about"))
async def cbguides(_, query: CallbackQuery):
    await query.answer("معلومات عن المبرمج⚡")
    await query.edit_message_text(
        f"""⋖≔≖☤≖≕〖 ᥉᥆υᖇᥴᥱ ᥴᖇᎥ᥉ƚᥱꪀ 〗≔≖☤≖≕⋗\n\n么 [𓏺سۅٛࢪس ڪࢪستيڼ](https://t.me/pp_g3)\n\n么 [𓏺أݪهڪࢪ ࢪ࣪يڼ ⚡](https://t.me/devpokemon)\n\n么[𓏺ڪࢪستيڼ🗽](https://t.me/dr_criss) \n\n⋖≔≖☤≖≕〖 ᥉᥆υᖇᥴᥱ ᥴᖇᎥ᥉ƚᥱꪀ 〗≔≖☤≖≕⋗\n\n⍟ 𝚃𝙷𝙴 𝙱𝙴𝚂𝚃 𝚂𝙾𝚄𝚁𝙲𝙴 𝙾𝙽 𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼
""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 رجوع", callback_data="cbstart")]]
        ),
    )