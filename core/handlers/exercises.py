from aiogram import types, Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
import asyncio
from core.database.requests import get_body_parts_list, get_exercises_list, get_this_exercise
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from ..utils.commands import set_commands
from .. import filters

import requests
from ..keyboards.inline import get_body_part_keyboard, get_exercises_keyboard, BackCbData, BackActions
from aiogram.fsm.state import State, StatesGroup


router = Router(name=__name__)


class ExercisesForm(StatesGroup):
    body_part = State()
    exercises = State()


@router.message(Command('exercises'))
@router.message((F.text == 'Упражнения') | (F.data.startswith == 'back'))
@router.message(BackCbData.filter(F.action == BackActions.exercises))
async def body_part_info(message: types.Message, bot: Bot, state: FSMContext):
    await message.answer(text='Группы мышц', reply_markup=await get_body_part_keyboard())
    await state.set_state(ExercisesForm.body_part)


@router.callback_query(ExercisesForm.body_part)
@router.callback_query(BackCbData.filter(F.action == BackActions.body_part))
async def exercises_info(call: CallbackQuery, bot: Bot, state: FSMContext):
    body_part_id = call.data.split(' ')[1]
    await call.message.answer('Упражнения', reply_markup=await get_exercises_keyboard(body_part_id))
    await state.set_state(ExercisesForm.exercises)


@router.message(F.text.casefold() == 'cancel')
async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_data()
    if current_state is None:
        return
    await state.clear()
    await message.answer('Вы вышли в главное меню', reply_markup=ReplyKeyboardRemove())



@router.callback_query(ExercisesForm.exercises)
@router.callback_query(BackCbData.filter(F.action == BackActions.this_exercise))
async def this_exercise(call: CallbackQuery, bot: Bot, state: FSMContext):
    this_exercise_id = call.data.split(' ')[1]
    this_exercise = await get_this_exercise(this_exercise_id)
    await call.message.answer(f'{this_exercise.title}')

