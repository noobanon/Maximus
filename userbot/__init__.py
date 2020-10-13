#!/usr/bin/env bash
# shellcheck source=/dev/null
#
# Copyright (C) 2018 Raphielscape LLC.
#
# Licensed under the Raphielscape Public License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
#
import os

from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb

from dotenv import load_dotenv
from requests import get
from telethon import TelegramClient
from telethon.sessions import StringSession


load_dotenv("config.env")

basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=INFO
)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 8:
    LOGS.error(
        "You MUST have a python version of at least 3.8."
        "Multiple features depend on this. Bot quitting."
    )
    quit(1)

try:
    print(___________PLOX_______REMOVE_____THIS_____LINE__________)
except NameError:
    API_KEY = os.environ.get("API_KEY", None)

    API_HASH = os.environ.get("API_HASH", None)
    
    SUDO_USERS = os.environ.get("SUDO_USERS", None)
    LOGSPAMMER = sb(os.environ.get("LOGSPAMMER", "False"))

    LOGGER_GROUP = int(os.environ.get("LOGGER_GROUP", "0"))

    LOGGER = sb(os.environ.get(
        "LOGGER", "False"
    ))  # Incase you want to turn off logging, put this to false

    PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

    CONSOLE_LOGGER_VERBOSE = sb(
        os.environ.get("CONSOLE_LOGGER_VERBOSE", "False")
        )

    DB_URI = os.environ.get("DATABASE_URL", None)
    STRING_SESSION = os.environ.get("STRING_SESSION", None)

    SCREENSHOT_LAYER_ACCESS_KEY = os.environ.get(
        "SCREENSHOT_LAYER_ACCESS_KEY", None
        )

    OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)

    SUDO = os.environ.get("SUDO", None)
    if CONSOLE_LOGGER_VERBOSE:
        basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=DEBUG,
        )
        LOGS = getLogger(__name__)
else:
    LOGS.error(
        "Your config file seems to be un-edited."
        "Doing so is not allowed. Bot exiting!"
    )
    quit(1)
    
if STRING_SESSION:
    # pylint: disable=invalid-name
    bot = TelegramClient(StringSession(STRING_SESSION),
                         API_KEY,
                         API_HASH,
                         auto_reconnect=False,
                         lang_code='en')
else:
    # pylint: disable=invalid-name
    bot = TelegramClient("userbot",
                         API_KEY,
                         API_HASH,
                         auto_reconnect=False,
                         lang_code='en')

#BotHelp
bot = TelegramClient("userbot", API_KEY, API_HASH)
# Global Variables
SNIPE_TEXT = ""
COUNT_MSG = 0
BRAIN_CHECKER = []
USERS = {}
SPAM = False
WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000
COUNT_PM = {}
CMD_HELP = {}
ISAFK = False
ENABLE_KILLME = True
SNIPE_ID = 0
MUTING_USERS = {}
MUTED_USERS = {}
AFKREASON = "No Reason "
SPAM_ALLOWANCE = 3
SPAM_CHAT_ID = []
DISABLE_RUN = False
NOTIF_OFF = False
