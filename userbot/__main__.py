# Copyright (C) 2018 Raphielscape LLC.
#
# Licensed under the Raphielscape Public License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
#

import importlib
import sqlite3
import sys

from userbot import BRAIN_CHECKER, LOGS, bot, LOGGER_GROUP
from userbot.modules import ALL_MODULES


async def main():
    bot.start()
    for module_name in ALL_MODULES:
        imported_module = importlib.import_module("userbot.modules." + module_name)
        LOGS.info("Your Bot is alive! Test it by typing .alive on any chat." "Should you need assistance, head to https://t.me/TheBotSupport")
        LOGS.info("Your Bot Version is 2.2-a")
        if len(sys.argv) not in (1, 3, 4):
            bot.disconnect()
    else:
        await bot.send_message(LOGGER_GROUP, "Connection is Alive!")
    await bot.run_until_disconnected()
