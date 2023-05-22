from aiogram import executor
from handlers import chat, group, admin, sisadmin
from create_bot import dp, bot
from database.database import connect
from my_bot_commands.set_bot_commands import set_admins_commands, set_admins_chat_commands, set_sisadmin_commands
async def on_startup(_):
    print(await set_admins_commands(bot))
    print(await set_admins_chat_commands(bot))
    print(await set_sisadmin_commands(bot))
    connect()
group.register(dp)
admin.register(dp)
chat.register(dp)
sisadmin.register(dp)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)