from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeAllChatAdministrators
from config import patern

async def set_admins_commands(bot:Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand("start", "args test and marafon"),
            BotCommand("stop","for stop the test"),
            BotCommand("register_group", "for register the group"),
            BotCommand("register_students", "for update list of group students"),
            BotCommand("delete_students", "for clear list of group students"),
            BotCommand("delete_group", "for delete the group"),
        ],
        scope=BotCommandScopeAllChatAdministrators()
    )

async def set_admins_chat_commands(bot:Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('start', "simple start the bot"),
            BotCommand('start_admin', 'start select the tru answers'),
            BotCommand('get_users', "arg Group name for get the group users"),
        ],
        scope=BotCommandScopeChat(chat_id=patern.admin.id)
    )

async def set_sisadmin_commands(bot:Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('start_sisadmin', 'start update list of question'),
            BotCommand('cancel_add', 'cancel or stop the updating')
        ],
        scope=BotCommandScopeChat(chat_id=patern.sisadmin.id)
    )