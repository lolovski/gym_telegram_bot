from enum import Enum, auto

from aiogram.filters import Command
from core.database.requests import get_body_parts_list, get_exercises_list
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from aiogram import Bot, Router


class BackActions(Enum):
    exercises = 'exercises'
    body_part = 'body_part'
    this_exercise = 'this_exercise'


class BackCbData(CallbackData, prefix='back_journal'):
    action: BackActions


async def get_body_part_keyboard(add=False):
    journal_keyboard = InlineKeyboardBuilder()
    body_parts = await get_body_parts_list()

    for i in body_parts:
        if add:
            journal_keyboard.add(InlineKeyboardButton(text=f'{i.name}', callback_data=f'add body_part {i.id}'))
        else:
            journal_keyboard.add(InlineKeyboardButton(text=f'{i.name}', callback_data=f'body_part {i.id}'))
    return journal_keyboard.adjust(1).as_markup()


async def get_exercises_keyboard(body_part_id, add=False):
    exercises_keyboard = InlineKeyboardBuilder()
    exercises_list = await get_exercises_list(body_part_id)
    for i in exercises_list:
        if add:
            exercises_keyboard.add(InlineKeyboardButton(text=f'{i.name}', callback_data=f'add exercise {i.id}'))
        else:
            exercises_keyboard.add(InlineKeyboardButton(text=f'{i.name}', callback_data=f'exercise {i.id}'))
    exercises_keyboard.add(InlineKeyboardButton(text='cancel', callback_data='exercise cancel'))
    return exercises_keyboard.adjust(1).as_markup()

cancel_exercises_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='cancel', callback_data='this_exercise cancel')]
])
new_exercise = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='new add exercise')]
])
new_photo = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='new add photo')]
])


async def add_photo_again(exercise):
    add_photo_again_keyboard = InlineKeyboardBuilder()
    add_photo_again_keyboard.add(InlineKeyboardButton(text='Ещё одна фото', callback_data=f'again add photo {exercise}'))
    add_photo_again_keyboard.add(InlineKeyboardButton(text='Всё', callback_data=f'final add photo'))
    return add_photo_again_keyboard.as_markup()


async def add_new_photo_exercise(exercise):
    add_new_photo_keyboard = InlineKeyboardBuilder()
    add_new_photo_keyboard.add(InlineKeyboardButton(text='Добавить фото', callback_data=f'new add photo {exercise}'))
    add_new_photo_keyboard.add(InlineKeyboardButton(text='Всё', callback_data=f'final add exercise'))
    return add_new_photo_keyboard.as_markup()


