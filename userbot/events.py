# Copyright (C) 2018 Raphielscape LLC.
#
# Licensed under the Raphielscape Public License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
#

from telethon import events 
from userbot import bot


def register(**args):
    pattern = args.get('pattern', None)
    groups_only = args.get('groups_only', False)

    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern
    if "groups_only" in args:
        del args['groups_only']

    def decorator(func):
        bot.add_event_handler(func, events.NewMessage(**args))
        bot.add_event_handler(func, events.MessageEdited(**args))
        return func

    return decorator
