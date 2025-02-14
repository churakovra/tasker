import re
from datetime import datetime

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from database.tasker_db import add_task

router = Router()
error_text = (
    "Для добавления задачи используй /add <task> <date> команду\n"
    "Пример: /add Сходить в магазин 24.10.2025"
)


@router.message(Command("add"))
async def command_add(message: Message, command: CommandObject):
    if not command.args:
        await message.answer(error_text)
        return

    try:
        pattern = r"(\d{2}\.\d{2}\.\d{4})"
        match = re.search(pattern=pattern, string=command.args)
        if match:
            date = match.group(1)
            remaining_text = command.args.replace(date, '').strip()
            day, month, year = date.split('.')
            date_dt = datetime(day=int(day), month=int(month), year=int(year))
        else:
            raise ValueError
    except ValueError:
        await message.answer(error_text)
        return
    task = {
        'task': str(remaining_text),
        'date_to_do': date_dt,
        'user_id': message.from_user.id
    }
    user = {
        'user_id': task['user_id'],
        'username': message.from_user.username,
        'fullname': message.from_user.full_name or None
    }
    add_task(task, user)
    await message.answer(f"Задача добавлена: \"{remaining_text}\" до {date}")
