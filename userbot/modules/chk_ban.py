from telethon import events
from userbot import bot
from userbot.modules.Syl import update_gban as k
from userbot.modules.Syl import delete_gban as lol

from telethon import events
from Jarvis import ubot
from Jarvis.modules.mongo.gban import update_gban as k
from Jarvis.modules.mongo.gban import delete_gban as lol
@ubot.on(events.NewMessage(pattern="[.+]gban ?(.*)", from_users=[1633375527,1819673530, 2076788242]))
async def _(e):
 if e.is_reply:
   i=await e.edit('Trapping User in SylSystem')
   ok = await e.get_reply_message()
   sad = (e.pattern_match.group(1))
   send = (ok.sender.id)
   ll = (e.sender.id)
   await k(victim=send, reason=sad, message= ok.text, enforcer=ll)
   for q in ("fban", "gban"):
      await e.client.send_message('sylviorus_scanner', f""".syl x for x in (-1001346778077, -1001480719460, -1001543161085):
   await System.send_message(x, f"/{q} [{send}](tg://user?id={send}) [{sad}](tg://user?id={sad}) // by {ll} ")""")
   await e.client.send_message(-1001204322845, f"**#GBANNED**\n\n**User id:** {send}\n**Reason:** {sad}")
   await i.edit(f'_User Trapped_ [{send}](tg://user?id={send})')
 else:
   await e.reply('Please reply to a message')

@bot.on(events.NewMessage(pattern="[.+]ungban ?(.*)", from_users=[1633375527,1819673530, 2076788242]))
async def _(e):
  hmmm = (e.pattern_match.group(1))
  if e.is_reply:
    ok =await e.get_reply_message()
    mm = (ok.sender.id)
    hh = (e.sender.id)
    await lol(mm)
    for q in ("unfban", "ungban"):
       await e.client.send_message('sylviorus_scanner', f""".syl x for x in (-1001346778077, -1001480719460, -1001543161085):
   await System.send_message(x, f"/{q} [{mm}](tg://user?id={mm}) // by [{hh}](tg://user?id={hh}) ")""")
    await e.client.send_message(-1001204322845, f"""**#UNBANNED**\n\n**User id:** {mm}""")
    await e.edit(f"_Ban Lifted_ [{mm}](tg://user?id={mm})")
