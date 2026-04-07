from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from MahiMusic import app
from MahiMusic.misc import SUDOERS
from MahiMusic.utils.database import (
    get_lang,
    is_maintenance,
    maintenance_off,
    maintenance_on,
)
from strings import get_string


@app.on_message(filters.command(["maintenance"]) & SUDOERS)
async def maintenance(client, message: Message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")
        
    usage = _["maint_1"]
    
    # The button containing your link
    bot_link_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🎵 MUSIC BOTS", url="https://t.me/betabot_hub/24")]]
    )

    if len(message.command) != 2:
        return await message.reply_text(usage, reply_markup=bot_link_markup)
        
    state = message.text.split(None, 1)[1].strip().lower()
    
    if state == "enable":
        if await is_maintenance() is False:
            await message.reply_text(_["maint_4"], reply_markup=bot_link_markup)
        else:
            await maintenance_on()
            await message.reply_text(_["maint_2"].format(app.mention), reply_markup=bot_link_markup)
    elif state == "disable":
        if await is_maintenance() is False:
            await maintenance_off()
            await message.reply_text(_["maint_3"].format(app.mention), reply_markup=bot_link_markup)
        else:
            await message.reply_text(_["maint_5"], reply_markup=bot_link_markup)
    else:
        await message.reply_text(usage, reply_markup=bot_link_markup)
