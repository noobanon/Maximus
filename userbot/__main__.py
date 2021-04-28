import importlib
import sqlite3
import sys

from userbot import BRAIN_CHECKER, LOGS, bot
from userbot.modules import ALL_MODULES


bot.start()

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("userbot.modules." + module_name)

LOGS.info("Your Bot is alive! Test it by typing .alive on any chat."
          "Should you need assistance, head to https://t.me/TheBotSupport")
LOGS.info("Your Bot Version is 2.2 By @noobanon")

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
