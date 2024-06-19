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


async def get_body_part_keyboard():
    journal_keyboard = InlineKeyboardBuilder()
    body_parts = await get_body_parts_list()
    print(body_parts)
    for i in body_parts:
        journal_keyboard.add(InlineKeyboardButton(text=f'{i.name}', callback_data=f'body_part {i.id}'))
    return journal_keyboard.adjust(1).as_markup()


async def get_exercises_keyboard(body_part_id):
    exercises_keyboard = InlineKeyboardBuilder()
    exercises_list = await get_exercises_list(body_part_id)
    for i in exercises_list:
        exercises_keyboard.add(InlineKeyboardButton(text=f'{i.name}', callback_data=f'exercise {i.id}'))
    exercises_keyboard.add(InlineKeyboardButton(text='cancel', callback_data='exercise cancel'))
    return exercises_keyboard.adjust(1).as_markup()

cancel_exercises_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='cancel', callback_data='this_exercise cancel')]
])


