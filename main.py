import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from db import Database
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

bot = Bot(token="6714486222:AAG8QlCMvj4pZy5T4VSM9oqjHKxNXWBy35E")
dp = Dispatcher()
db = Database('database.db')


@dp.message(CommandStart())

async def command_start_handler(message: Message) -> None:
    if message.chat.type == 'private':
        photo = FSInputFile("Photo/Photo1.jpg")
        await bot.send_photo(message.chat.id, photo, caption=f"Приветствую, <b>{message.from_user.full_name}</b>!"
                                                             f" Я буду присылать вам анонсы прямых эфиров и всего самого интересного от MC Банкир.",
                             parse_mode="HTML")
        if message.chat.type == 'private':
            if not db.user_exists(message.from_user.id):
                db.add_user(message.from_user.id)

@dp.message(Command('send_all'))
async def send_all(message: types.Message) -> None:
    if message.chat.type == 'private':
        if message.from_user.id == 1313756443:
            text = message.text[10:]
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text)
                    if int(row[1]) != 1:
                        db.set_user_active(row[0], 1)
                except:
                    db.set_user_active(row[0], 0)
            await bot.send_message(message.from_user.id, "Успешная рассылка")



async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())