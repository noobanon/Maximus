# Copyright (C) 2018 Raphielscape LLC.
#
# Licensed under the Raphielscape Public License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
#

from userbot import LOGGER, LOGGER_GROUP, bot
from userbot.events import register
from userbot import CMD_HELP

@register(outgoing=True, pattern="^\.notes$")
async def notes_active(svd):
    chat = await svd.get_chat()
    if not svd.text[0].isalpha() and svd.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.notes_sql import get_notes
        except:
            await svd.edit("`Running on Non-SQL mode!`")
            return

        notes = get_notes(svd.chat_id)
        message = f'`There are no saved notes in {svd.chat.title}`'
        if notes:
            message = f"Notes saved in {svd.chat.title}: \n\n"
            for note in notes:
                message = message + "• " + note.keyword + "\n"
        await svd.edit(message)


@register(outgoing=True, pattern="^\.clear (\w*)")
async def remove_notes(clr):
    if not clr.text[0].isalpha() and clr.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.notes_sql import rm_note
        except:
            await clr.edit("`Running on Non-SQL mode!`")
            return
        notename = clr.pattern_match.group(1)
        rm_note(clr.chat_id, notename)
        await clr.edit(f"```Note {notename} has removed successfully```")


@register(outgoing=True, pattern="^\.save (\w*)")
async def add_filter(fltr):
    if not fltr.text[0].isalpha():
        try:
            from userbot.modules.sql_helper.notes_sql import add_note
        except:
            await fltr.edit("`Running on Non-SQL mode!`")
            return
        notename = fltr.pattern_match.group(1)
        string = fltr.text.partition(notename)[2]
        if fltr.reply_to_msg_id:
            rep_msg = await fltr.get_reply_message()
            string = rep_msg.text
        add_note(str(fltr.chat_id), notename, string)
        await fltr.edit(
            "Note added successfully. Use` #{} `to get it".format(notename)
        )


@register(pattern="#\w*")
async def incom_note(getnt):
    try:
        if not (await getnt.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.notes_sql import get_notes
            except:
                return
            notename = getnt.text[1:]
            notes = get_notes(getnt.chat_id)
            for note in notes:
                if notename == note.keyword:
                    await getnt.reply(note.reply)
                    return
    except:
        pass


@register(outgoing=True, pattern="^\.rmnotes$")
async def purge_notes(prg):
    try:
        from userbot.modules.sql_helper.notes_sql import rm_all_notes
    except:
        await prg.edit("`Running on Non-SQL mode!`")
        return
    if not prg.text[0].isalpha():
        await prg.edit("```Purging all notes.```")
        rm_all_notes(str(prg.chat_id))
        if LOGGER:
            await prg.client.send_message(
                LOGGER_GROUP, "I cleaned all notes at " + str(prg.chat_id)
            )

CMD_HELP.update(
    {
        "notes": """
『 **Notes** 』
  `save` -> Save a new note. Must be used in reply with one parameter (note name).
  `get` -> Gets the note specified.
  `clear` -> Deletes a note, specified by note name.
  `notes` -> List the saved notes.
"""
    }
)
