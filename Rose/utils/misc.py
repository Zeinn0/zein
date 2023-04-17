import asyncio
from typing import Dict, List, Union
from Rose import *
from Rose import app
from pyrogram.types import InlineKeyboardButton
from Rose import MOD_LOAD, MOD_NOLOAD


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text

def paginate_modules(page_n: int, module_dict: Dict, prefix, chat=None) -> List:
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({})".format(
                        prefix, x.__MODULE__.lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__MODULE__.lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )

    pairs = [modules[i * 2 : (i + 1) * 2] for i in range((len(modules) + 2 - 1) // 2)]

    round_num = len(modules) / 2
    calc = len(modules) - round(round_num)
    if calc == 1:
        pairs.append((modules[-1],))
    elif calc == 1:
        pairs.append((modules[-1],))

    else:
        pairs += [[EqInlineKeyboardButton("اضف البوت الي مجموعتك ✅", url=f"http://t.me/{BOT_USERNAME}?startgroup=new",)]]

    return pairs

def is_module_loaded(name):
    return (not MOD_LOAD or name in MOD_LOAD) and name not in MOD_NOLOAD
