from core.database.models import BodyPart, async_session, Exercise
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
    async with async_session() as session:
        body_parts = await session.scalars(select(BodyPart))
        return body_parts


async def get_exercises_list(body_part_id):
    async with async_session() as session:
        exercises = await session.scalars(select(Exercise).where(Exercise.body_part == body_part_id))
        return exercises


async def get_this_exercise(exercise_id):
    async with async_session() as session:
        exercise = await session.scalar(select(Exercise).where(Exercise.id == exercise_id))
        return exercise

