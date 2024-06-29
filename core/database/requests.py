from core.database.models import BodyPart, async_postgres_session, Exercise, Photo
from sqlalchemy import select, update, insert, delete


"""async def set_user(tg_id, username, class_user, api_token):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, username=username, class_user=class_user, api_token=api_token))
            await session.commit()
        else:
            return False"""


async def get_body_parts_list():
    async with async_postgres_session() as session:
        body_parts = await session.scalars(select(BodyPart))
        return body_parts


async def get_exercises_list(body_part_id):
    async with async_postgres_session() as session:

        exercises = await session.scalars(select(Exercise).where(Exercise.body_part == int(body_part_id)))
        return exercises


async def get_this_exercise(exercise_id):
    async with async_postgres_session() as session:
        exercise = await session.scalar(select(Exercise).where(Exercise.id == int(exercise_id)))
        return exercise


async def set_photo(file_path, exercise_id, paragraph):
    async with async_postgres_session() as session:
        session.add(Photo(file_path=file_path, exercise_id=int(exercise_id), paragraph=int(paragraph)))
        await session.commit()
        return Photo(file_path=file_path, exercise_id=int(exercise_id), paragraph=int(paragraph))


async def get_photos(exercise_id):
    async with async_postgres_session() as session:
        photos = await session.scalars(select(Photo).where(Photo.exercise_id == int(exercise_id)))
        if photos:
            return photos
        else: return None


async def set_exercise(body_part, name, text, title):
    async with async_postgres_session() as session:
        session.add(Exercise(body_part=int(body_part), name=name, text=text, title=title))
        await session.commit()
        return Exercise(body_part=int(body_part), name=name, text=text, title=title)


async def get_last_exercise():
    async with async_postgres_session() as session:
        last_exercise = await session.scalars(select(Exercise))
        return last_exercise.all()[-1]