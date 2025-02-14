from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from database.tasker_db import delete_task

router = Router()
error_text = (
    "Для удаления задачи используй /delete <номер задачи> команду\n"
    "Пример: /delete 1"
)


@router.message(Command("delete"))
async def command_delete(message: Message, command: CommandObject):
    if not command.args:
        await message.answer(text=error_text)
        return

    try:
        task_id = command.args.strip()
        if int(task_id):
            task_deleted = delete_task(user_id=message.from_user.id, task_num=int(task_id))
        else:
            raise ValueError
    except ValueError:
        await message.answer(text=error_text)
        return

    if task_deleted:
        await message.answer(text="Задача удалена")
    else:
        await message.answer(text=error_text)
