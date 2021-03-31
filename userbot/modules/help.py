from userbot import CMD_HELP
from userbot.events import register


HELP.update(
    {
        "**Admin Tools**": "__ban, unban, promote, demote, kick, mute, unmute, gmute, ungmute, pin, purge, del, invite__",
        "**AFK**": "__afk, unafk__",
        "**Alive**": "__alive, ping__",
        "**Developer**": "__eval, term__",
        "**Misc**": "__paste, tr, whois, id__",
        "**Notes**": "__save, get, clear, clearall, notes__",
        "**Sticker**": "__kang, stkrinfo__",
        "**Greetings**": "__setwelcome, clearwelcome__",
    }
)

@register(outgoing=True, pattern="^.help(?: |$)(.*)")
async def help(event):
    """ For .help command,"""
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit("Please specify a valid module name.")
    else:
        await event.edit("Please specify which module do you want help for !!\
            \nUsage: **.help for module list** & .help <module name> for more")
        string = ""
        for i in CMD_HELP:
            string += "`" + str(i)
            string += "`\n"
        await event.reply(string)
