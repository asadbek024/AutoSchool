from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def keyboard(data:list) -> InlineKeyboardMarkup:
    buttons:list = []
    for step in data:
        step_list:list = []
        for call in step:
            if call[1].startswith('http'):
                step_list.append(InlineKeyboardButton(text=call[0], url=call[1]))
            elif call[1].startswith('@'):
                step_list.append(InlineKeyboardButton(text=call[0], url=f"https://t.me/{call[1][1:]}"))
            else:
                step_list.append(InlineKeyboardButton(text=call[0], callback_data=call[1]))
        buttons.append(step_list)
    return InlineKeyboardMarkup(inline_keyboard=buttons)