import random
from pyrogram import filters, enums
from IstkharMusic import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPermissions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from IstkharMusic.utils.nightmodedb import nightdb, nightmode_on, nightmode_off, get_nightchats


CLOSE_CHAT = ChatPermissions(
    can_send_messages=False,
)

OPEN_CHAT = ChatPermissions(
    can_send_messages=True,
)

buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("๏ ᴇɴᴀʙʟᴇ ๏", callback_data="add_night"),
            InlineKeyboardButton("๏ ᴅɪsᴀʙʟᴇ ๏", callback_data="rm_night"),
        ]
    ]
)


@app.on_message(filters.command("nightmode") & filters.group)
async def _nightmode(_, message):
    await message.reply_photo(
        photo="https://telegra.ph/file/06649d4d0bbf4285238ee.jpg",
        caption="**ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ɴɪɢʜᴛᴍᴏᴅᴇ.**",
        reply_markup=buttons,
    )


@app.on_callback_query(filters.regex("^(add_night|rm_night)$"))
async def nightcb(_, query: CallbackQuery):

    chat_id = query.message.chat.id
    user_id = query.from_user.id

    member = await app.get_chat_member(chat_id, user_id)

    if member.status not in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        return await query.answer("Only Admin Can Use This", show_alert=True)

    check = await nightdb.find_one({"chat_id": chat_id})

    if query.data == "add_night":

        if check:
            await query.message.edit_caption("**Nightmode already enabled.**")

        else:
            await nightmode_on(chat_id)
            await query.message.edit_caption(
                "**Nightmode Enabled 🌙\n\nGroup will close at 12AM and open at 6AM (IST).**"
            )

    elif query.data == "rm_night":

        if check:
            await nightmode_off(chat_id)
            await query.message.edit_caption("**Nightmode Disabled ❌**")

        else:
            await query.message.edit_caption("**Nightmode already disabled.**")


async def start_nightmode():

    chats = await get_nightchats()

    for chat in chats:
        chat_id = int(chat["chat_id"])

        try:
            await app.send_message(
                chat_id,
                "**🌙 Good Night Everyone\nGroup is now closing.**",
            )

            await app.set_chat_permissions(chat_id, CLOSE_CHAT)

        except Exception as e:
            print(f"Unable To close Group {chat_id} - {e}")


async def close_nightmode():

    chats = await get_nightchats()

    for chat in chats:
        chat_id = int(chat["chat_id"])

        try:
            await app.send_message(
                chat_id,
                "**☀️ Good Morning Everyone\nGroup is now open.**",
            )

            await app.set_chat_permissions(chat_id, OPEN_CHAT)

        except Exception as e:
            print(f"Unable To open Group {chat_id} - {e}")


scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

scheduler.add_job(start_nightmode, "cron", hour=23, minute=59)
scheduler.add_job(close_nightmode, "cron", hour=6, minute=1)

scheduler.start()