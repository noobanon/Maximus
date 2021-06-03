from userbot import CMD_HELP
from userbot.events import register
from userbot import bot
from telethon import events


@bot.on(events.NewMessage(pattern="^[.*]help$"))
async def help(event):
    """ For .help command,"""
    try:
        args = (event.message.text).split(" ", 1)[1]
    except:
        args = None
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit("Please specify a valid module name.")
    else:
        await event.edit("Please specify which module do you want help for !!\
            \nUsage: .help for module list & .help <module name> for more")
        string = ""
        for i in CMD_HELP:
            string += "" + str(i)
            string += "\n"
        await event.reply(string)
