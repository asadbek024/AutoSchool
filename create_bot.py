from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import patern

storage:MemoryStorage = MemoryStorage()

bot:Bot = Bot(token=patern.bot.token, parse_mode="HTML")
dp:Dispatcher = Dispatcher(bot=bot, storage=storage)
