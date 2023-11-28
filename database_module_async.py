from __future__ import annotations

import asyncio
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload

import greenlet

from functions import read_json_file

data_load = asyncio.run(read_json_file('files/config.json'))
dsn = f"postgresql+asyncpg://{data_load['pg_data']['user']}:{data_load['pg_data']['password_pg']}@{data_load['pg_data']['ip_addr']}:5432/{data_load['pg_data']['database']}"


class Base(AsyncAttrs, DeclarativeBase):
    pass

class Tgusers(Base):
    __tablename__ = "tg_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_userid: Mapped[str]
    tg_username: Mapped[str] = mapped_column(nullable=True)
    tg_first_name: Mapped[str] = mapped_column(nullable=True)
    tg_last_name: Mapped[str] = mapped_column(nullable=True)
    accses: Mapped[bool]

    rel: Mapped[List[ProjectsAndUsers]] = relationship()
    rel: Mapped[List[Issues]] = relationship()
    

    async def __str__(self) -> str:
        return f'{self.id}: {self.tg_userid},{self.tg_username},{self.tg_first_name},{self.tg_last_name},{self.accses}'


class Projects(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_name: Mapped[str]

    rel: Mapped[List[ProjectsAndUsers]] = relationship()
    
    async def __str__(self) -> str:
        return f'{self.id}: {self.project_name}'
    
class ProjectsAndUsers(Base):
    __tablename__ = "projects_and_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey("tg_users.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    
    rel: Mapped[List[Tgusers]] = relationship()

    async def __str__(self) -> str:
        return f'{self.id}: {self.tg_id},{self.project_id}'
    
class Issues(Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey("tg_users.id"))
    issue: Mapped[str]

    async def __str__(self) -> str:
        return f'{self.id}: {self.tg_id}, {self.issue}'
    
async def async_main() -> None:
    engine = create_async_engine(dsn,echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await insert_objects(async_session)
    await engine.dispose()

async def insert_objects(async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [
                    # Tgusers(rel=[Issues(issue = '123')], tg_userid="a100", accses = True),
                    Projects(rel = [ProjectsAndUsers(rel =[Tgusers(rel=[], tg_userid="a1232", accses = False)] ,project_id = 6622)], project_name = 'ADM_BL')
                    # Tgusers(rel=[], tg_userid="a1232", accses = False),
                ]
            )

asyncio.run(async_main())