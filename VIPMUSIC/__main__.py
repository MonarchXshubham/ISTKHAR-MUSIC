from flask import Flask
import threading
import asyncio
import importlib
from sys import argv
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from VIPMUSIC import LOGGER, app, userbot
from VIPMUSIC.core.call import VIP
from VIPMUSIC.misc import sudo
from VIPMUSIC.plugins import ALL_MODULES
from VIPMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

async def init():
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER(__name__).error(
            "𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 V2 𝐒𝐞𝐬𝐬𝐢𝐨𝐧🤬"
        )

    await sudo()
    
    # Load banned users
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            if user_id not in BANNED_USERS:
                BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).error(f"Error loading users: {e}")
    
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("VIPMUSIC.plugins" + all_module)

    LOGGER("VIPMUSIC.plugins").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

    await userbot.start()
    await VIP.start()
    await VIP.decorators()
    
    # Start the bot's main functionality
    LOGGER("VIPMUSIC").info("╔═════ஜ۩۞۩ஜ════╗\n  ♨️𝗠𝗔𝗗𝗘 𝗕𝗬 𝗜𝗦𝗧𝗞𝗛𝗔𝗥♨️\n╚═════ஜ۩۞۩ஜ════╝")
    
    await idle()
    
    await app.stop()
    await userbot.stop()

    LOGGER("VIPMUSIC").info("╔═════ஜ۩۞۩ஜ════╗\n  ♨️𝗠𝗔𝗗𝗘 𝗕𝗬 𝗜𝗦𝗧𝗞𝗛𝗔𝗥♨️\n╚═════ஜ۩۞۩ஜ════╝")

if __name__ == "__main__":
    # Start the Flask app in a thread
    def run_flask():
        app.run(host='0.0.0.0', port=8080)

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Start the asyncio event loop for the bot
    asyncio.get_event_loop().run_until_complete(init())
