from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from config import patern
from keyboard import inline
from database.database import *

def get_variants(topic:int, new_position:int, buttons:list, variants:str) -> list:
    variants = variants.split('\n\n\n\n')
    varlist:list = []
    for i, variant in enumerate(variants):
        variant = variant.split(':')
        if variant[-1] == "1":
            varlist.append([[f"✅ {':'.join(variant[:len(variant)-1])}", f"admin:{i}:{variant[-1]}:{topic}:{new_position}"]])
        else:
            varlist.append([[':'.join(variant[:len(variant)-1]), f"admin:{i}:{variant[-1]}:{topic}:{new_position}"]])
    varlist.append(buttons)
    return varlist

async def command_start(message:types.Message):
    if message.chat.id == patern.admin.id:
        if len(message.text.split()) > 1:
            typeof = message.text.split()[-1]
            if typeof.isdigit():
                topic = int(message.text.split()[-1])
                buttons = [["☑️", f"move:{topic}:0:done"],["➡️", f"move:{topic}:0:1"]]
                questions = get_questions(values=[topic])
                try:
                    file, question, variants = get_question([questions[0][0]])
                except:
                    await message.answer("Bu paragraf mavjud emas yoki ma'lumotlar bazasiga kiritilmagan")
                    await message.delete()
                    return
                varlist = get_variants(topic, 0, buttons, variants)
                if file is not None:
                    file = file.split(':')
                    if file[0] == "photo":
                        await message.answer_photo(photo=file[1], caption=f"1-savol:\n\t{question}", reply_markup=inline.keyboard(varlist))
                    else:
                        await message.answer_video(photo=file[1], caption=f"1-savol:\n\t{question}", reply_markup=inline.keyboard(varlist))
                else:
                    await message.answer(text=f"1-savol:\n\t{question}", reply_markup=inline.keyboard(varlist))
            elif typeof == "marafon":
                file, question, variants = get_marafon()
        else:
            await message.answer("start_admin buyrug'idan so'ng argument kiriting")
    await message.delete()

async def command_get_users(message:types.Message):
    if patern.admin.id == message.chat.id or True:
        group_name = " ".join(message.text.split()[1:])
        group_id = get_id_from_name([group_name])[0]
        students = get_group_students([group_id])
        result:list = []
        result.append(f"Guruh: {group_name}")
        for id, name, user_name, state, _ in students:
            if state == -1:
                result.append(f"O'quvchi ismi: {name} id=<code>{id}</code>\n\t\t@{user_name}\n\t\to'quvchi holati: 🟥 Passiv")
            else:
                result.append(f"O'quvchi ismi: {name} id=<code>{id}</code>\n\t\t@{user_name}\n\t\to'quvchi holati: {state}- test yechildi")
        await message.answer("\n\n".join(result))
    await message.delete()

async def move(callback:types.CallbackQuery):
    await callback.answer()
    params = callback.data.split(':')
    topic = int(params[1])
    delta = params[-1]
    if delta == "done":
        await callback.message.answer("Qabul qilindi")
        await callback.message.delete()
        return
    current_position = int(params[2])
    new_position = current_position + int(delta)
    buttons = [["⬅️",f'move:{topic}:{new_position}:-1'],["☑️", f"move:{topic}:{new_position}:done"],["➡️", f"move:{topic}:{new_position}:1"]]
    questions = get_questions(values=[topic])
    if new_position == 0:
        buttons = buttons[1:] 
    try:
        get_question([questions[new_position+1][0]])
    except:
        buttons = buttons[:-1]
    file, question, variants = get_question([questions[new_position][0]])
    varlist = get_variants(topic, new_position, buttons, variants)
    if file is not None:
        file = file.split(':')
        if file[0] == "photo":
            await callback.message.answer_photo(photo=file[1], caption=f"{new_position+1}-savol:\n\t{question}", reply_markup=inline.keyboard(varlist))
            await callback.message.delete()
            return
        else:
            await callback.message.answer_video(video=file[1], caption=f"{new_position+1}-savol:\n\t{question}", reply_markup=inline.keyboard(varlist))
            await callback.message.delete()
            return
    else:
        await callback.message.answer(text=f"{new_position+1}-savol:\n\t{question}", reply_markup=inline.keyboard(varlist))
        await callback.message.delete()
    

async def change_to_true(callback:types.CallbackQuery):
    parametrs = callback.data.split(':')
    varnumber = int(parametrs[1])
    value:bool = bool(int(parametrs[2]))
    topic = int(parametrs[3])
    position = int(parametrs[4])
    if not value:
        await callback.answer()
        question_id = get_questions(values=[topic])[position][0]
        _, _, variants = get_question([question_id])
        varlist:list = variants.split('\n\n\n\n')
        for i, var in enumerate(varlist):
            if i == varnumber:
                varlist[i] = ':'.join(var.split(':')[:-1]+['1'])
            else:
                varlist[i] = ':'.join(var.split(':')[:-1]+['0'])
        update_questions(values=['\n\n\n\n'.join(varlist), question_id])
        buttons = [["⬅️",f'move:{topic}:{position}:-1'],["☑️", f"move:{topic}:{position}:done"],["➡️", f"move:{topic}:{position}:1"]]
        questions = get_questions(values=[topic])
        if position == 0:
            buttons = buttons[1:] 
        try:
            get_question([questions[position+1][0]])
        except:
            buttons = buttons[:-1]
        file, question, variants = get_question([questions[position][0]])
        varlist = get_variants(topic, position, buttons, variants)
        if file is not None:
            await callback.message.edit_caption(caption=f"{position+1}-savol:\n\t{question}", reply_markup=inline.keyboard(varlist))
        else:
            await callback.message.edit_text(text=f"{position+1}-savol:\n\t{question}", reply_markup=inline.keyboard(varlist))
    else:
        await callback.answer("Avval ham shu javob to'g'ri deb topilgan", show_alert=True)

def register(dp:Dispatcher):
    dp.register_message_handler(command_start, chat_type=types.ChatType.PRIVATE, commands=['start_admin'])
    dp.register_message_handler(command_get_users, chat_type=types.ChatType.PRIVATE, commands=['get_users'])
    dp.register_callback_query_handler(move, Text(startswith="move:"))
    dp.register_callback_query_handler(change_to_true, Text(startswith="admin:"))
