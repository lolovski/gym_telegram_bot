from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

engine = create_async_engine('sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class BodyPart(Base):
    __tablename__ = 'Body_parts'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))


class Exercise(Base):
    __tablename__ = 'exercises'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    body_part: Mapped[int] = mapped_column(ForeignKey('body_parts.id'))
    number: Mapped[int] = mapped_column()
    text: Mapped[str] = mapped_column(String(4096))
    title: Mapped[str] = mapped_column(String(512))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
