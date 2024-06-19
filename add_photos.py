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


@router.message(Command('add_photo'))
async def add_photo(message: types.Message, bot: Bot, state: FSMContext):
    await state.set_state(AddPhotosForm.photos)


@router.message(AddPhotosForm.photos)
async def add_photos(message: types.Message, bot: Bot):
    await message.answer('!')
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = os.path.join(PHOTOS_DIR, file_info.file_unique_id + '.jpg')
    await bot.download(photo, file_path)
    new_photo = await set_photo(file_path=file_path, exercise_id=1)


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
