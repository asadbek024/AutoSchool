from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import patern
from keyboard import inline
from database.database import set_questions, set_marafon, get_new_id_questions, get_new_id_marafon

class SisAdminStatesGroup(StatesGroup):
    topic = State()
    file = State()
    question = State()
    variants = State()

async def command_start(message:types.Message, state:FSMContext):
    if message.chat.id == patern.sisadmin.id:
        await message.answer("hello sisadmin", reply_markup=inline.keyboard([[["add topic", "add:topic"], ["add marafon", "add:marafon"]]]))
    await message.delete()

async def command_cancel(message:types.Message, state:FSMContext):
    if message.chat.id == patern.sisadmin.id:
        if await state.get_state() != None:
            await state.finish()
        await message.answer("canceled")
        await message.delete()

async def add_handler(callback:types.CallbackQuery, state:FSMContext):
    await callback.answer()
    param = callback.data.split(":")[-1]
    if param == "topic":
        await SisAdminStatesGroup.topic.set()
        await callback.message.answer("send me topic number (id)")
    else:
        await SisAdminStatesGroup.file.set()
        await callback.message.answer("send me file")
    await callback.message.delete()

async def get_topic(message:types.Message, state:FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['topic'] = int(message.text)
        await SisAdminStatesGroup.next()
        await message.answer("And send me file")
    await message.delete()

async def get_file(message:types.Message, state:FSMContext):
    async with state.proxy() as data:
        if message.caption != "None":
            if message.video is not None:
                data['file'] = f"video:{message.video.file_id}"
            else:
                data['file'] = f"photo:{message.photo[-1].file_id}"
        else:
            data['file'] = None
    await message.answer(" good! And send me the question")
    await SisAdminStatesGroup.next()
    await message.delete()

async def get_question(message:types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text
    await message.answer("good! And send me variants")
    await SisAdminStatesGroup.next()
    await message.delete()

async def get_variants(message:types.Message, state:FSMContext):
    varlist = message.text.split('\n')
    variants = "\n\n\n\n".join([f"f{i+1}) {x}:0" for i, x in enumerate(varlist)])
    async with state.proxy() as data:
        data['variants'] = variants
        if data['topic'] is not None:
            new_id = get_new_id_questions(values=[])
            set_questions(values=[new_id, data['topic'], data['file'], data['question'], variants])
        else:
            new_id = get_new_id_marafon(values=[])
            set_marafon(values=[new_id, data['file'], data['question'], variants])
    await state.finish()
    await message.answer("Done!")
    await message.delete()

def register(dp:Dispatcher):
    dp.register_message_handler(command_start, chat_type=types.ChatType.PRIVATE, commands=['start_sisadmin'], state=None)
    dp.register_message_handler(command_cancel, chat_type=types.ChatType.PRIVATE, commands=['cancel_add'], state='*')
    dp.register_callback_query_handler(add_handler, Text(startswith="add:"), state=None)
    dp.register_message_handler(get_topic, content_types=types.ContentTypes.TEXT, state=SisAdminStatesGroup.topic)
    dp.register_message_handler(get_file, content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO], state=SisAdminStatesGroup.file)
    dp.register_message_handler(get_question, content_types=types.ContentTypes.TEXT, state=SisAdminStatesGroup.question)
    dp.register_message_handler(get_variants, content_types=types.ContentTypes.TEXT, state=SisAdminStatesGroup.variants)
