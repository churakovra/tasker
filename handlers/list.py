from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database.tasker_db import get_user_tasks

router = Router()

@router.message(Command("list"))
async def command_list(message: Message):
    await message.answer(get_user_tasks(message.from_user.id))