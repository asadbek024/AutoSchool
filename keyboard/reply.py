from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

def keyboard(data:list) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=map(lambda step:[KeyboardButton(text=text[0]) for text in step] , data),
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='select button ↓',
        )

def Phone(button_text:str, input_field:str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                    text=button_text
                )]
            ],
        resize_keyboard=True,
        input_field_placeholder=input_field,
    )

def remove() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()