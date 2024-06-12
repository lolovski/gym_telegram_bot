import requests
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Bot, Dispatcher, Router, MagicFilter
from aiogram import F

router = Router(name=__name__)

