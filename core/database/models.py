from sqlalchemy import String, BigInteger, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
import os
from dotenv import load_dotenv
load_dotenv()
postgres_engine = create_async_engine(str(os.getenv('DATABASE_URL')))
async_postgres_session = async_sessionmaker(postgres_engine)

"""sqlite_engine = create_async_engine('sqlite+aiosqlite:///db.sqlite3')
async_sqlite_session = async_sessionmaker(sqlite_engine)
sqlite_session = async_postgres_session()"""

class Base(AsyncAttrs, DeclarativeBase):
    pass


class BodyPart(Base):
    __tablename__ = 'body_parts'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(32))


class Exercise(Base):
    __tablename__ = 'exercises'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    body_part: Mapped[int] = mapped_column(ForeignKey('body_parts.id'))
    text: Mapped[str] = mapped_column(String(4096))
    title: Mapped[str] = mapped_column(String(512))

    day_replies: Mapped[list['TrainingDay']] = relationship(
        back_populates='exercise_replied',
        secondary='day_exercises',

    )


class Photo(Base):
        __tablename__ = 'photos'
        photo_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
        file_path: Mapped[str] = mapped_column(String(1024))
        exercise_id: Mapped[int] = mapped_column(ForeignKey('exercises.id'))
        paragraph: Mapped[int] = mapped_column(nullable=True)


class Training(Base):
    __tablename__ = 'trainings'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    text: Mapped[str] = mapped_column(String(2048))


class TrainingDay(Base):
    __tablename__ = 'training_days'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    training_id: Mapped[int] = mapped_column(ForeignKey('trainings.id'))
    number: Mapped[int] = mapped_column()
    exercise_replied: Mapped[list['Exercise']] = relationship(
        back_populates='day_replies',
        secondary='day_exercises',
    )


class DayExercises(Base):
    __tablename__ = 'day_exercises'
    day_id: Mapped[int] = mapped_column(ForeignKey('training_days.id', ondelete='CASCADE'), primary_key=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey('exercises.id', ondelete='CASCADE'), primary_key=True)


async def async_main():
    async with postgres_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


"""async def add_table_db(list_new_bp):
    async with async_postgres_session() as session:
        for new_body_part in list_new_bp:
            session.add(new_body_part)
            await session.commit()
            print(new_body_part)


async def dump_db():
    list_new_bp = []
    async with async_sqlite_session() as session:
        body_parts = await session.scalars(select(Training))
        for body_part in body_parts:
            new_body_part = Training(

            )
            list_new_bp.append(new_body_part)
        print(list_new_bp)
        return list_new_bp
"""


