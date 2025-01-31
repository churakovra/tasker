from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.tasker_db import get_user_tasks

router = Router()


@router.message(Command("list"))
async def command_list(message: Message):
    data = get_user_tasks(message.from_user.id)
    if len(data) > 0:
        tasks = '\n'.join(data)
        await message.answer(tasks)
    else:
        await message.answer(text="Список задач пуст!")
