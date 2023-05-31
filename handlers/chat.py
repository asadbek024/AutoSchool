from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from config import patern
from keyboard import inline
from database.database import *
from create_bot import bot

def get_variants(variants:str, arg:int, position:int, group:int, typeoftest:str, message_id:int) -> list:
    variants = variants.split('\n\n\n\n')
    varlist:list = []
    for i, variant in enumerate(variants):
        variant = variant.split(':')
        varlist.append([[':'.join(variant[:len(variant)-1]), f"{typeoftest}:{position}:{arg}:{group}:{variant[-1]}:{message_id}:{i}"]])
    return varlist

async def command_start(message:types.Message):
    if message.chat.id == patern.admin.id:
        await message.answer("Admin buyruqlari ro'yxati:\n    /start_admin - savollarning to'g'ri javoblarini tanlash\n    /get_users Gurug nomi - guruh o'quvchilari holati haqida ma'lumot\nSisAdmin buyruqlari ro'yxati:\n    /start_sisadmin - bazaga savol qo'shishni boshlash\n    /cancel_add - so'ngi bo'lmagan har qaysi vaziyatda savol qo'shilishini bekor qilish(/cancel bilan adashtirmang!!!)")
    await message.answer("Assalomu alaykum bu bot guruh bilan ishlashga mo'ljallangan!!!", reply_markup=inline.keyboard([[["Guruhga qo'shish", 'http://t.me/AutoSchool_uz_bot?startgroup=new']]]))

async def command_cancel(message:types.Message):
    user_id = message.chat.id
    change_student_state(values=[-1, user_id])
    change_score(values=[0, user_id])
    group_id = get_students_group(values=[user_id])
    name = get_students(values=[user_id])[0]
    await bot.send_message(chat_id=group_id, text=f"{name} testdan chetlatildi")
    await message.answer("test jarayoni bekor qilindi!!")
    await message.delete()

async def callback_start(callback:types.CallbackQuery):
    user_id = callback.from_user.id
    if patern.admin.id == user_id:
        await callback.answer("/start_admin buyrug'ini kiritib ma'lumotlar bazasidagi savollarning to'g'ri javoblarini belgilab chiqishingiz mumkin!!", show_alert=True)
        return
    if len(callback.data.split()) > 1:
        if callback.data.split()[-1].split('-')[0] == "register":
            # id:int, name:str, user_name:str, state:int, score:int, true_answers message:str, group_id:int
            name = callback.from_user.first_name
            user_name = callback.from_user.username
            group_id = -int(callback.data.split()[-1].split('-')[1])
            if check_groups(values=[group_id]):
                try:
                    set_students(values=[user_id, name, user_name, -1, 0, "", 0, group_id])
                except:
                    if group_id != get_students_group(values=[user_id]):
                        change_group_students(values=[group_id, user_id])
                        await callback.answer("Siz muvaffaqiyatli tarzda avvalgi guruhdan bu guruhga o'tdingiz!", show_alert=True)
                    else:
                        await callback.answer("Siz avval ro'yxatdan o'tgansiz!", show_alert=True)
                else:
                    await callback.answer("Muvaffaqiyatli ro'yxatdan o'tganingiz bilan tabriklayman!!!", show_alert=True)
                finally:
                    return
            else:
                await callback.message.answer("Bu guruh ro'yxatdan o'tkazilmagan!!!")
        args = callback.data.split()[1].split('-')
        if(len(args) < 3):
            await callback.answer("havola noto'g'ri ustozga habar bering", show_alert=True)
            return
        elif check_groups(values=[-int(args[1])]) and check_student(values=[user_id]):
            typeoftest = args[0]
            group = -int(args[1])
            topic = args[2]
            start = 0
        else:
            await callback.answer("Bu havola siz uchun emas", show_alert=True)
            return
        try:
            user_state = get_student_state(values=[user_id])
            message_id = get_message_students(values=[user_id])
            if user_state < 0 and message_id != callback.message.message_id:
                await callback.answer("Botga o'ting test boshlandi!!", show_alert=True)
                await bot.send_message(chat_id=user_id, text=f"Tayyormisiz\n/cancel - bekor qilish", reply_markup=inline.keyboard([[["start", f'{typeoftest}:{start}:{topic}:{group}:0:{callback.message.message_id}']]]))
                change_student_state(values=[0, user_id])
                change_message_students(values=[callback.message.message_id, user_id])
            else:
                await callback.answer("Siz avval bu test uchun ro'yxatdan o'tgansiz!!!", show_alert=True)
        except:
            await callback.answer("Avval botga /start bosing!!", show_alert=True)

async def get_true_test(callback:types.CallbackQuery):
    parametrs = callback.data.split(':')
    await callback.answer()
    student_message_id = int(parametrs[5])
    current_students_message_id = get_message_students(values=[callback.from_user.id])
    value:bool = bool(int(parametrs[4]))
    if current_students_message_id == student_message_id:
        topic = int(parametrs[2])
        position = int(parametrs[1])
        questions = get_questions(values=[topic])
        if value:
            answers = f"{get_true_answers(values=[callback.from_user.id])}:{position}"
            score = get_student_score(values=[callback.from_user.id])
            change_score(values=[score+1, callback.from_user.id])
            update_true_answers(values=[answers, callback.from_user.id])
        change_student_state(values=[position, callback.from_user.id])
        try:
            question_id = [questions[position][0]]
            file, question, variants = get_question(question_id)
            varlist = get_variants(arg=topic, position=1+position, variants=variants, group=-int(parametrs[3]), typeoftest="test", message_id=student_message_id)
            if file is not None:
                file = file.split(':')
                if file[0] == "photo":
                    await callback.message.answer_photo(photo=file[1], caption=f"{position+1}-savol:\n\t{question}", reply_markup=inline.keyboard(varlist))
                else:
                    await callback.message.answer_video(video=file[1], caption=f"{position+1}-savol:\n\t{question}", reply_markup=inline.keyboard(varlist))
            else:
                await callback.message.answer(text=f"{position+1}-savol:\n\t{question}", reply_markup=inline.keyboard(varlist))
        except:
            score = get_student_score(values=[callback.from_user.id])
            name = get_students(values=[callback.from_user.id])
            answers = ", ".join(get_true_answers(values=[callback.from_user.id]).split(':')[1:])
            await callback.message.answer(f"{topic}-paragraf:\n{score} ta to'g'ri javob")
            await bot.send_message(chat_id=get_students_group(values=[callback.from_user.id]), text=f"{topic}-paragraf:\n{name[0]} {score} ta to'g'ri javob:\n{answers}")
    try:
        await callback.message.delete()
    except:
        name:str = ''
        if not callback.from_user.username is None:
            name = f"@{callback.from_user.username}"
        else:
            name = f'<a href="tg://user?id={callback.from_user.id}">{callback.from_user.first_name}</a>'
        print(f">>> {callback.from_user.first_name} eskirgan tugmani bosdi !!!\a")
        await bot.send_message(chat_id=patern.admin.id, text=f">>> {name} eskirgan tugmani bosdi !!!")

async def get_true_marafon(callback:types.CallbackQuery):
    parametrs = callback.data.split(':')
    await callback.answer()
    student_message_id = int(parametrs[5])
    current_students_message_id = get_message_students(values=[callback.from_user.id])
    value:bool = bool(int(parametrs[4]))
    if current_students_message_id == student_message_id:
        topic = int(parametrs[2])
        position = int(parametrs[1])
        questions = get_marafons(values=[topic])
        if value:
            answers = f"{get_true_answers(values=[callback.from_user.id])}:{position}"
            score = get_student_score(values=[callback.from_user.id])
            change_score(values=[score+1, callback.from_user.id])
            update_true_answers(values=[answers, callback.from_user.id])
        change_student_state(values=[position, callback.from_user.id])
        try:
            question_id = [questions[position][0]]
            file, question, variants = get_marafon(question_id)
            varlist = get_variants(arg=topic, position=1+position, variants=variants, group=-int(parametrs[3]), typeoftest="marafon", message_id=student_message_id)
            if file is not None:
                file = file.split(':')
                if file[0] == "photo":
                    await callback.message.answer_photo(photo=file[1], caption=f"{position+1}-savol:\n\t{question}", reply_markup=inline.keyboard(varlist))
                else:
                    await callback.message.answer_video(video=file[1], caption=f"{position+1}-savol:\n\t{question}", reply_markup=inline.keyboard(varlist))
            else:
                await callback.message.answer(text=f"{position+1}-savol:\n\t{question}", reply_markup=inline.keyboard(varlist))
        except:
            score = get_student_score(values=[callback.from_user.id])
            name = get_students(values=[callback.from_user.id])
            answers = ", ".join(get_true_answers(values=[callback.from_user.id]).split(':')[1:])
            await callback.message.answer(f"{topic}-bilet:\n{score} ta to'g'ri javob")
            await bot.send_message(chat_id=get_students_group(values=[callback.from_user.id]), text=f"{topic}-paragraf:\n{name[0]} {score} ta to'g'ri javob:\n{answers}")
    try:
        await callback.message.delete()
    except:
        name:str = ''
        if not callback.from_user.username is None:
            name = f"@{callback.from_user.username}"
        else:
            name = f'<a href="tg://user?id={callback.from_user.id}">{callback.from_user.first_name}</a>'
        print(f">>> {callback.from_user.first_name} eskirgan tugmani bosdi !!!\a")
        await bot.send_message(chat_id=patern.admin.id, text=f">>> {name} eskirgan tugmani bosdi !!!")

def register(dp:Dispatcher):
    dp.register_message_handler(command_cancel, chat_type=types.ChatType.PRIVATE, commands=['cancel'])
    dp.register_message_handler(command_start, chat_type=types.ChatType.PRIVATE, commands=['start', 'help'])
    dp.register_callback_query_handler(callback_start, Text(startswith="start"))
    dp.register_callback_query_handler(get_true_test, Text(startswith="test:"))
    dp.register_callback_query_handler(get_true_marafon, Text(startswith="marafon:"))
