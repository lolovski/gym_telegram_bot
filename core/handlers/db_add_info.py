
from aiogram.filters import CommandStart, Command
from core.database.requests import get_body_parts_list, get_exercises_list, get_this_exercise, get_photos, set_exercise, set_photo, get_last_exercise
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, FSInputFile
from aiogram import Router, types, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ContentType, FSInputFile
from sqlalchemy.orm import sessionmaker
from aiogram.filters import CommandStart, Command
import os

from ..utils.commands import set_commands
from .. import filters

import requests
from ..keyboards.inline import get_body_part_keyboard, get_exercises_keyboard, BackCbData, BackActions, cancel_exercises_keyboard, add_photo_again, new_exercise, new_photo
from aiogram.fsm.state import State, StatesGroup


router = Router(name=__name__)

PHOTOS_DIR = 'photos'

if not os.path.exists(PHOTOS_DIR):
    os.makedirs(PHOTOS_DIR)


class AddExerciseForm(StatesGroup):
    body_part = State()
    name = State()
    text = State()
    photo = State()


class AddPhotosForm(StatesGroup):
    body_part = State()
    exercise = State()
    paragraph = State()
    photo = State()


@router.message(Command('add_exercise'))
async def add_exercise(message: Message, state: FSMContext):
    await message.answer('Группа тела', reply_markup=await get_body_part_keyboard(add=True))
    await state.set_state(AddExerciseForm.body_part)


@router.callback_query(AddExerciseForm.body_part)
async def add_exercise_body_part(call: CallbackQuery, state: FSMContext):
    await state.update_data(body_part=call.data.split(' ')[-1])
    await call.answer()
    await call.message.answer('Напиши название упражнения')
    await state.set_state(AddExerciseForm.name)


@router.message(AddExerciseForm.name)
async def add_exercise_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Напиши текст упражнения')
    await state.set_state(AddExerciseForm.text)


@router.message(AddExerciseForm.text)
async def add_exercise_text(message: Message, state: FSMContext):
    text = message.text
    if len(text) > 501:
        title = text[:500]
    else:
        title = text + '...'

    context = await state.get_data()
    exercise = await set_exercise(context['body_part'], context['name'], text, title)
    last_exercise = await get_last_exercise()
    await message.answer(f'{exercise.name} \n добавить фото', reply_markup=await add_photo_again(last_exercise.id + 1))

@router.message(F.data)

@router.message(Command('add_photo'))
async def add_photo(message: types.Message, bot: Bot, state: FSMContext):
    await message.answer('Группа мышщ', reply_markup=await get_body_part_keyboard(add=True))
    await state.set_state(AddPhotosForm.body_part)


@router.callback_query(AddPhotosForm.body_part)
async def add_photo_body_part(call: CallbackQuery, state: FSMContext):
    body_part = call.data.split(' ')[-1]
    await state.update_data(body_part=body_part)
    await call.answer()
    await call.message.answer('Упражнение', reply_markup= await get_exercises_keyboard(body_part, add=True))
    await state.set_state(AddPhotosForm.exercise)


@router.callback_query(AddPhotosForm.exercise)
async def add_photo_exercise(call: CallbackQuery, state: FSMContext):
    exercise = call.data.split(' ')[-1]
    await state.update_data(exercise=exercise)
    await call.answer()
    await call.message.answer('введите номер абзаца')
    await state.set_state(AddPhotosForm.paragraph)


@router.message(AddPhotosForm.paragraph)
async def add_photo_paragraph(message: types.Message, state: FSMContext):
    paragraph = int(message.text)
    await state.update_data(paragraph=paragraph)
    await message.answer('Отправьте фото')
    await state.set_state(AddPhotosForm.photo)


@router.message(AddPhotosForm.photo)
async def full_add_photo(message: types.Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = os.path.join(PHOTOS_DIR, file_info.file_unique_id + '.jpg')
    await bot.download(photo, file_path)
    context = await state.get_data()

    await set_photo(file_path=file_path, exercise_id=context['exercise'], paragraph=context['paragraph'])

    await message.answer('Готово', reply_markup=await add_photo_again(context['exercise']))


@router.callback_query(F.data.startswith('again add photo'))
async def again_add_photo(call: CallbackQuery, state: FSMContext):
    await state.update_data(paragraph=None)
    await state.set_state(AddPhotosForm.exercise)
    await call.answer()


@router.callback_query(F.data.startswith('final add photo'))
async def final_add_photo(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer('/add_exercise', reply_markup=new_exercise)
    await call.answer()

