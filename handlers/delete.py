from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("delete"))
async def command_delete(message: Message):
    pass