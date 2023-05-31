from aiogram import types, Dispatcher
from create_bot import bot
from keyboard import inline
from database.database import *

async def command_start(message:types.Message):
    if check_groups(values=[message.chat.id]):
        if get_group_students(values=[message.chat.id]) != []:
            args:list[str] = message.text.split()
            if len(args) == 3:                    
                if args[-1].isdigit():
                    arg = args[-1]
            elif len(args) == 2:
                if args[1] == 'test':
                    arg = get_group_topic(values=[message.chat.id])+1
                else:
                    await message.answer("argumentlar noto'g'ri")
                    return
            else:
                await message.answer("argumentlar noto'g'ri")
                return
            typeoftest = args[1]
            if not check_question(values=[arg]):
                await message.answer("paragrafda test sinovi mavjud emas yoki ma'lumotlar bazasiga kiritilmagan!!!")
                await message.delete()
                return
            message_id = get_group_message(values=[message.chat.id])
            if message_id != 0:
                try:
                    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
                except:
                    print("Last message has been deleted!!!")
            current_message = await message.answer("test boshlandi!", reply_markup=inline.keyboard([[["start", f"start {typeoftest}{message.chat.id}-{arg}"]]]))
            update_groups(values=[arg, message.chat.id])
            update_groups_message(values=[current_message.message_id, message.chat.id])
        else:
            await message.answer("Bu guruhda ro'yxatdan o'tgan o'quvchilar mavjud emas!!!")
    else:
        await message.answer("Bu guruh ro'yxatdan o'tmagan!!!")
    await message.delete()

async def command_register_group(message:types.Message):
    group_id = message.chat.id
    try:
        set_groups(values=[group_id, message.chat.title,  0, 0])
    except:
        await message.answer("Guruh ma'lumotlar bazasida mavjud!!")
    else:
        await message.answer("Guruh ma'lumotlar bazasiga qo'shildi")
    finally:
        await message.delete()

async def command_register_students(message:types.Message):
    if check_groups(values=[message.chat.id]):
        callback = f"start register{message.chat.id}"
        await message.answer("Guruh o'quvchilari safiga qo'shilish uchun tugmani bosing", reply_markup=inline.keyboard([[["Qo'shilish", callback]]]))
    else:
        await message.answer("Bu guruh ro'yxatdan o'tmagan!!!")
    await message.delete()

async def command_stop(message:types.Message):
    if check_groups(values=[message.chat.id]):
        students = get_group_students([message.chat.id])
        if students != []:
            await message.answer("Test jarayoni yakunlandi!!!")
            message_id = get_group_message(values=[message.chat.id])
            if message_id != 0:
                try:
                    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
                except:
                    print("Last message has been deleted!!!")
            result:list = []
            for student, name, user_name, state, _ in students:
                score = get_student_score(values=[student])
                if state > 0:
                    answers = ', '.join(get_true_answers(values=[student]).split(':')[1:])
                    result.append(f"{name} - @{user_name} \n\t{score} ta to'g'ri javob:\n{answers}")
                else:
                    result.append(f"{name} - @{user_name} qatnashmadi")
                change_score(values=[0, student])
                change_student_state(values=[-1, student])
                change_message_students(values=[message.message_id, student])
                update_true_answers(values=["", student])
            update_groups_message(values=[0, message.chat.id])
            await message.answer("\n\n".join(result))
        else:
            await message.answer("Bu guruhda ro'yxatdan o'tgan o'quvchilar mavjud emas!!!")
    else:
        await message.answer("Bu guruh ro'yxatdan o'tmagan!!!")
    await message.delete()

async def command_delete_group(message:types.Message):
    if check_groups(values=[message.chat.id]):
        try:
            delete_group(values=[message.chat.id])
        except:
            await message.answer("Guruhni o'chirishda tushunarsiz xatolik")
        else:
            await message.answer("Guruh ma'lumotlar bazasidan muvaffaqiyatli o'chirildi!!!")
        finally:
            await message.delete()

async def command_delete_students(message:types.Message):
    if check_groups(values=[message.chat.id]):
        students = get_group_students(values=[message.chat.id])
        if students != []:
            for student, _, _, _, _ in students:
                delete_student(values=[student])
            await message.answer("Guruh o'quvchilari o'chirildi")
        else:
            await message.answer("Bu guruhda ro'yxatdan o'tgan o'quvchilar mavjud emas!!!")
    else:
        await message.answer("Bu guruh ro'yxatdan o'tmagan!!!")
    await message.delete()

def register(dp:Dispatcher):
    dp.register_message_handler(command_start, chat_type=types.ChatType.SUPERGROUP, commands=['start'])
    dp.register_message_handler(command_register_group, chat_type=types.ChatType.SUPERGROUP,  commands=['register_group'])
    dp.register_message_handler(command_register_students, chat_type=types.ChatType.SUPERGROUP, commands=['register_students'])
    dp.register_message_handler(command_stop, chat_type=types.ChatType.SUPERGROUP, commands=['stop'])
    dp.register_message_handler(command_delete_group, chat_type=types.ChatType.SUPERGROUP, commands=['delete_group'])
    dp.register_message_handler(command_delete_students, chat_type=types.ChatType.SUPERGROUP, commands=['delete_students'])
