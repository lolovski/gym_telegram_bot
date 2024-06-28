from aiogram import Router, types, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ContentType, FSInputFile
from sqlalchemy.orm import sessionmaker
from aiogram.filters import CommandStart, Command
from core.database.requests import set_photo, get_photos
import os


router = Router(name=__name__)


PHOTOS_DIR = 'photos'

if not os.path.exists(PHOTOS_DIR):
    os.makedirs(PHOTOS_DIR)


class AddPhotosForm(StatesGroup):
   start = State()
   photos = State()


@router.message(Command(commands=['get_photo']))
async def send_photo(message: types.Message):
    user_id = message.from_user.id
    photo_record = await get_photos(1)
    if photo_record:
        for photo in photo_record:
            photo_file = FSInputFile(photo.file_path)
            await message.answer_photo(photo_file)
    else:
        await message.reply("Фотография не найдена.")
