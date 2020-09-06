# Copyright (C) 2018 Raphielscape LLC.
#
# Licensed under the Raphielscape Public License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio, sys, io, traceback, inspect, time, subprocess
from getpass import getuser
from telethon import (events, errors, functions, types)
from userbot import *
from userbot.events import register


@register(outgoing=True, pattern="^.eval")
async def _(event):
    if event.fwd_from:
        return
      
    await event.edit("Processing ...")
    cmd = event.text.split(" ", maxsplit=1)[1]
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "**EVAL**: `{}` \n\n **OUTPUT**: \n`{}` \n".format(cmd, evaluation)

    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
            await event.delete()
    else:
        await event.edit(final_output)


async def aexec(code, event):
    exec(
        f'async def __aexec(event): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](event)


@register(outgoing=True, pattern=r"^.exec (.*)")
async def run(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        if e.is_channel and not e.is_group:
            await e.edit("`Exec isn't permitted on channels`")
            return
        code = e.raw_text[5:]
        exec(f"async def __ex(e): " + ""
             .join(f"\n {l}" for l in code.split("\n")))
        result = await locals()["__ex"](e)
        if result:
            if len(result) > 4096:
                f = open("output.txt", "w+")
                f.write(result)
                f.close()
                await e.client.send_file(
                    e.chat_id,
                    "output.txt",
                    reply_to=e.id,
                    caption="`Output too large, sending as file`",
                )
                subprocess.run(["rm", "output.txt"], stdout=subprocess.PIPE)

            await e.edit(
                "**Query: **\n`"
                + e.text[5:]
                + "`\n**Result: **\n`"
                + str(result) + "`"
            )
        else:
            await e.edit(
                "**Query: **\n`"
                + e.text[5:]
                + "`\n**Result: **\n`"
                + "No Result Returned/False"
                + "`"
            )

        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP,
                "Exec query " + e.text[5:] + " was executed successfully"
            )


@register(outgoing=True, pattern="^.term")
async def terminal_runner(term):
    if not term.text[0].isalpha() and term.text[0] not in ("/", "#", "@", "!"):
        if term.is_channel and not term.is_group:
            await term.edit("`Term Commands aren't permitted on channels`")
            return
        message = term.text
        curruser = getuser()
        command = str(message)
        command = str(command[6:])
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        result = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        if len(result) > 4096:
            output = open("output.txt", "w+")
            output.write(result)
            output.close()
            await term.client.send_file(
                term.chat_id,
                "sender.txt",
                reply_to=term.id,
                caption="`Output too large, sending as file`",
            )
            subprocess.run(["rm", "output.txt"], stdout=subprocess.PIPE)

        await term.edit(
            f"`{curruser}:~# "
            + command
            + "`\n`"
            + result + "`"
        )

        if LOGGER:
            await term.client.send_message(
                LOGGER_GROUP,
                "Terminal Command " + command + " was executed sucessfully",
            )
