from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)


statsb = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="احصائيات النظام 🖥", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="احصائيات البيانات 📟", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="احصائيات البوت 🤖", callback_data=f"bot_stats"
            )
        ],
    ]
)
