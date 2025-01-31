from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.tasker_db import clear_user_tasks

router = Router()


@router.message(Command("clear"))
async def command_clear(message: Message):
    is_tasks_cleared = clear_user_tasks(message.from_user.id)
    if is_tasks_cleared:
        await message.answer(text="Задачи удалены!")
    else:
        await message.answer(text="Упс! Ничего не вышло!")
