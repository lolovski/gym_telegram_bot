from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Упражнения')],
    [KeyboardButton(text='Программы тренировок')],

], resize_keyboard=True)

