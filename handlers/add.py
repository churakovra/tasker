import re

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

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
        else:
            raise ValueError
    except ValueError:
        await message.answer(error_text)
        return
    # TODO Добавление в БД
    await message.answer(f"Задача добавлена: \"{remaining_text}\" до {date}")
