# Copyright (C) 2018 Raphielscape LLC.
#
# Licensed under the Raphielscape Public License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.

from time import sleep

from telethon.errors import BadRequestError
from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest

from telethon.tl.types import ChatAdminRights, ChatBannedRights, MessageEntityMentionName, MessageMediaPhoto

from userbot import (LOGGER, LOGGER_GROUP)
from userbot.events import register
from userbot import CMD_HELP

PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing image`"
NO_ADMIN = "`You aren't an admin!`"
NO_PERM = "`You don't have sufficient permissions!`"
NO_SQL = "`Database connections failing!`"

CHAT_PP_CHANGED = "`Chat Picture Changed`"
CHAT_PP_ERROR = "`Some issue with updating the pic,`" \
                "`maybe you aren't an admin,`" \
                "`or don't have the desired rights.`"
INVALID_MEDIA = "`Invalid Extension`"

async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(' ', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            return await event.reply("`Pass the user's username, id or reply!`")

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            return await event.reply(str(err))

    return user_obj, extra

@register(outgoing=True, pattern="^.promote(?: |$)(.*)")
async def promote(promt):
    """ For .promote command, promotes the replied/tagged person """
    # Get targeted chat
    chat = await promt.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return

    new_rights = ChatAdminRights(add_admins=False,
                                 invite_users=True,
                                 change_info=False,
                                 ban_users=True,
                                 delete_messages=True,
                                 pin_messages=True)

    await promt.edit("Giving this user power using 6 Stone...")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "Geymin"  # Just in case.
    if user:
        pass
    else:
        return

    # Try to promote if current user is admin or creator
    try:
        await promt.client(
            EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit("**Power increased**")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        await promt.edit(NO_PERM)
        return

@register(outgoing=True, pattern="^.demote$")
async def demote(dmod):
    """ For .demote command, do demote targeted person """
    if not dmod.text[0].isalpha() and dmod.text[0] not in ("/", "#", "@", "!"):
        # Get targeted chat
        chat = await dmod.get_chat()
        # Grab admin status or creator in a chat
        admin = chat.admin_rights
        creator = chat.creator

        # If there's no reply, return
        if not await dmod.get_reply_message():
            await dmod.edit("`Give a reply message`")
            return
        # If not admin and not creator, also return
        if not admin and not creator:
            await dmod.edit("`You aren't an admin!`")
            return

        # If passing, declare that we're going to demote
        await dmod.edit("Wiping this user from admin using infinity stone")

        # New rights after demotion
        newrights = ChatAdminRights(
            add_admins=None,
            invite_users=None,
            change_info=None,
            ban_users=None,
            delete_messages=None,
            pin_messages=None
        )
        # Edit Admin Permission
        try:
            await dmod.client(
                EditAdminRequest(dmod.chat_id,
                                 (await dmod.get_reply_message()).sender_id,
                                 newrights, "admin")
            )

        # If we catch BadRequestError from Telethon
        # Assume we don't have permission to demote
        except BadRequestError:
            await dmod.edit(
                "`You Don't have sufficient permissions to demhott`"
                )
            return
        await dmod.edit("**Wiped Successfully!**")


@register(outgoing=True, pattern="^.ban$")
async def thanos(bon):
    """ For .ban command, do "thanos" at targeted person """
    if not bon.text[0].isalpha() and bon.text[0] not in ("/", "#", "@", "!"):
        banned_rights = ChatBannedRights(
            until_date=None,
            view_messages=True,
            send_messages=True,
            send_media=True,
            send_stickers=True,
            send_gifs=True,
            send_games=True,
            send_inline=True,
            embed_links=True,
        )

        # Here laying the sanity check
        chat = await bon.get_chat()
        admin = chat.admin_rights
        creator = chat.creator

        # For dealing with reply-at-ban
        sender = await bon.get_reply_message()

        # Well
        if not admin and not creator:
            await bon.edit("`You aren't an admin!`")
            return

        # Announce that we're going to whacking the pest
        await bon.edit("`Whacking the pest!`")
        await bon.client(
            EditBannedRequest(
                bon.chat_id,
                sender.sender_id,
                banned_rights
            )
        )

        # Delete message and then tell that the command
        # is done gracefully
        await bon.edit("`Banned!`")

        # Announce to the logging group if we done a banning
        if LOGGER:
            await bon.client.send_message(
                LOGGER_GROUP,
                str((await bon.get_reply_message()).sender_id)
                + " was banned.",
            )


@register(outgoing=True, pattern="^.unban$")
async def nothanos(unbon):
    if not unbon.text[0].isalpha() and unbon.text[0] \
            not in ("/", "#", "@", "!"):
        rights = ChatBannedRights(
            until_date=None,
            send_messages=None,
            send_media=None,
            send_stickers=None,
            send_gifs=None,
            send_games=None,
            send_inline=None,
            embed_links=None,
            )
        replymsg = await unbon.get_reply_message()
        try:
            await unbon.client(EditBannedRequest(
                unbon.chat_id,
                replymsg.sender_id,
                rights
                ))
            await unbon.edit("```Unbanned Successfully```")

            if LOGGER:
                await unbon.client.send_message(
                    LOGGER_GROUP,
                    str((await unbon.get_reply_message()).sender_id)
                    + " was unbanned.",
                )
        except UserIdInvalidError:
            await unbon.edit("`Uh oh my unban logic broke!`")


@register(outgoing=True, pattern="^.mute$")
async def spider(spdr):
    """
    This function basically muting peeps
    """
    if not spdr.text[0].isalpha() and spdr.text[0] not in ("/", "#", "@", "!"):

        # Check if the function running under SQL mode
        try:
            from userbot.modules.sql_helper.spam_mute_sql import mute
        except Exception:
            await spdr.edit("`Running on Non-SQL mode!`")
            return

        # Get the targeted chat
        chat = await spdr.get_chat()
        # Check if current user is admin
        admin = chat.admin_rights
        # Check if current user is creator
        creator = chat.creator

        # If not admin and not creator, return
        if not admin and not creator:
            await spdr.edit("`You aren't an admin!`")
            return

        target = await spdr.get_reply_message()
        # Else, do announce and do the mute
        mute(spdr.chat_id, target.sender_id)
        await spdr.edit("`Gets a tape!`")

        # Announce that the function is done
        await spdr.edit("`Safely taped!`")

        # Announce to logging group
        if LOGGER:
            await spdr.client.send_message(
                LOGGER_GROUP,
                str((await spdr.get_reply_message()).sender_id)
                + " was muted.",
            )


@register(outgoing=True, pattern="^.unmute$")
async def unmoot(unmot):
    if not unmot.text[0].isalpha() and unmot.text[0] \
            not in ("/", "#", "@", "!"):
        rights = ChatBannedRights(
            until_date=None,
            send_messages=None,
            send_media=None,
            send_stickers=None,
            send_gifs=None,
            send_games=None,
            send_inline=None,
            embed_links=None,
            )
        replymsg = await unmot.get_reply_message()
        from userbot.modules.sql_helper.spam_mute_sql import unmute
        unmute(unmot.chat_id, replymsg.sender_id)
        try:
            await unmot.client(EditBannedRequest(
                unmot.chat_id,
                replymsg.sender_id,
                rights
                ))
            await unmot.edit("```Unmuted Successfully```")
        except UserIdInvalidError:
            await unmot.edit("`Uh oh my unmute logic broke!`")


@register(incoming=True)
async def muter(moot):
    try:
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
    except:
        return
    muted = is_muted(moot.chat_id)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
                until_date=None,
                send_messages=True,
                send_media=True,
                send_stickers=True,
                send_gifs=True,
                send_games=True,
                send_inline=True,
                embed_links=True,
                )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                await moot.delete()
                await moot.client(EditBannedRequest(
                    moot.chat_id,
                    moot.sender_id,
                    rights
                    ))
    for i in gmuted:
        if i.sender == str(moot.sender_id):
            await moot.delete()


@register(outgoing=True, pattern="^.ungmute$")
async def ungmoot(ungmoot):
    if not ungmoot.text[0].isalpha() and ungmoot.text[0] \
            not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.gmute_sql import ungmute
        except:
            await ungmoot.edit('`Running on Non-SQL Mode!`')
        ungmute(str((await ungmoot.get_reply_message()).sender_id))
        await ungmoot.edit("```Ungmuted Successfully```")


@register(outgoing=True, pattern="^.gmute$")
async def gspider(gspdr):
    if not gspdr.text[0].isalpha() and gspdr.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.gmute_sql import gmute
        except Exception as err:
            print(err)
            await gspdr.edit("`Running on Non-SQL mode!`")
            return

        gmute(str((await gspdr.get_reply_message()).sender_id))
        await gspdr.edit("`Grabs a huge, sticky duct tape!`")
        sleep(5)
        await gspdr.delete()
        await gspdr.respond("`Taped!`")

        if LOGGER:
            await gspdr.send_message(
                LOGGER_GROUP,
                str((await gspdr.get_reply_message()).sender_id)
                + " was muted.",
            )

@register(outgoing=True, pattern="^.kick(?: |$)(.*)", groups_only=True)
async def kick(usr):
    """ For .kick command, kicks the replied/tagged person from the group. """
    # Admin or creator check
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await usr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(usr)
    if not user:
        await usr.edit("`Couldn't fetch user.`")
        return

    await usr.edit("`Kicking...`")

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(.5)
    except Exception as e:
        await usr.edit(NO_PERM)
        return

    if reason:
        await usr.edit(
            f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}"
        )
    else:
        await usr.edit(
            f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`")

    if LOGGER_GROUP:
        await usr.client.send_message(
            LOGGER_GROUP, "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {usr.chat.title}(`{usr.chat_id}`)\n")

@register(outgoing=True, pattern="^.pin(?: |$)(.*)", groups_only=True)
async def pin(msg):
    """ For .pin command, pins the replied/tagged message on the top the chat. """
    # Admin or creator check
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await msg.edit("`Reply to a message to pin it.`")
        return

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(
            UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await msg.edit(NO_PERM)
        return

    await msg.edit("`Pinned Successfully!`")

    user = await get_user_from_id(msg.from_id, msg)

    if  LOGGER_GROUP:
        await msg.client.send_message(
            LOGGER_GROUP, "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"LOUD: {not is_silent}")


CMD_HELP.update(
    {
        "admin": """
• **Admins Help** •
  `promote` -> Promote a user by bot.
  `demote` -> Demote user by bot.
  `ban` -> Bans user indefinitely.
  `unban` -> Unbans the user.
  `mute` -> Mutes user indefinitely.
  `unmute` -> Unmutes the user.
  `kick` -> Kicks the user out of the group.
  `gmute` -> Doesn't lets a user speak(even admins).
  `ungmute` -> Inverse of what gmute does.
  `pin` -> pins a message.
  `del` -> delete a message.
  `purge` -> purge message(s)
  `adminlist` -> Get adminlist in chat.
"""
    }
)
