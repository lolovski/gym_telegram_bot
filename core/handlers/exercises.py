from aiogram import types, Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
import asyncio
from core.database.requests import get_body_parts_list, get_exercises_list, get_this_exercise, get_photos
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, FSInputFile

from ..utils.commands import set_commands
from .. import filters

import requests
from ..keyboards.inline import get_body_part_keyboard, get_exercises_keyboard, BackCbData, BackActions, cancel_exercises_keyboard
from aiogram.fsm.state import State, StatesGroup


router = Router(name=__name__)


class ExercisesForm(StatesGroup):
    body_part = State()
    exercises = State()


@router.message(Command('exercises'))
@router.message((F.text == 'Упражнения') or (F.data.startswith('cancel')))
async def body_part_info(message: types.Message, bot: Bot, state: FSMContext):
    await message.answer(text='Группы мышц', reply_markup=await get_body_part_keyboard())


@router.callback_query(F.data.startswith('body_part'))
@router.callback_query(BackCbData.filter(F.action == BackActions.body_part))
async def exercises_info(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(ExercisesForm.body_part)
    body_part_id = call.data.split(' ')[1]
    await state.update_data(body_part=body_part_id)
    await call.message.answer('Упражнения', reply_markup=await get_exercises_keyboard(body_part_id))


@router.callback_query(F.data.startswith('exercise'))
async def this_exercise(call: CallbackQuery, bot: Bot, state: FSMContext):

    if call.data.split(' ')[1] == 'cancel':
        await state.clear()
        await call.answer()
        await call.message.answer(text='Группы мышц', reply_markup=await get_body_part_keyboard())
    else:

        await state.set_state(ExercisesForm.exercises)

        this_exercise_id = call.data.split(' ')[1]
        await state.update_data(exercises=this_exercise_id)
        this_exercise = await get_this_exercise(this_exercise_id)
        text = this_exercise.text.split('\n\n')
        print(text)
        photo_record = await get_photos(this_exercise_id)
        photo_record = sorted(photo_record.all(), key=lambda x: x.paragraph, reverse=False)
        print(len(text))
        for photo in photo_record:
            print(photo.paragraph)
        for i in range(len(text)):
            for photo in photo_record:
                if photo.paragraph == i:
                    photo_file = FSInputFile(photo.file_path)
                    await call.message.answer_photo(photo_file)
            await call.message.answer(text=text[i])
        await call.message.answer(reply_markup=cancel_exercises_keyboard, text='Вернуться назад')
        await call.answer()
        await state.set_state(ExercisesForm.exercises)


@router.callback_query(F.data.startswith('this_exercise'))
async def this_exercise_control(call: CallbackQuery, bot: Bot, state: FSMContext):
    if call.data.split(' ')[1] == 'cancel':
        context = await state.get_data()
        await state.set_state(ExercisesForm.exercises)
        await call.message.answer('Упражнения', reply_markup=await get_exercises_keyboard(context['body_part']))
        await state.update_data(exercises=None)