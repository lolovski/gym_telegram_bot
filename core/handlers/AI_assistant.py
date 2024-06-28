from asyncio import WindowsSelectorEventLoopPolicy

from aiogram import types, Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
import asyncio
from core.database.requests import get_body_parts_list, get_exercises_list, get_this_exercise, get_photos
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, FSInputFile
from core.AI_client import client

from ..utils.commands import set_commands
from .. import filters

import requests
from ..keyboards.inline import get_body_part_keyboard, get_exercises_keyboard, BackCbData, BackActions, cancel_exercises_keyboard
from aiogram.fsm.state import State, StatesGroup


router = Router(name=__name__)
messages = []

class AIAssistantStates(StatesGroup):
    questions = State()


@router.message(F.text == 'ИИ')
async def assistant_greeting(message: types.Message, state: FSMContext):
    await message.answer('Привет, это исскуственный интеллект, твой личный тренер, чем могу помочь?')
    await state.set_state(AIAssistantStates.questions)


@router.message(AIAssistantStates.questions)
async def ask_questions(message: types.Message, state: FSMContext):

    user_input = message.text + 'ГОВОРИ ТОЛЬКО ПО-РУССКИ'

    if user_input.lower() == "exit":
        await message.answer("Exiting chat...")

    messages.append({"role": "user", "content": user_input})

    try:

        response = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo",
        )
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
        gpt_response = response.choices[0].message.content
        await message.answer(gpt_response)
        messages.append({"role": "assistant", "content": gpt_response})
    except Exception as e:
        await message.answer('Извините, ошибка /start')
