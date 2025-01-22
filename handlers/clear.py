from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("clear"))
async def command_clear(message: Message):
    pass