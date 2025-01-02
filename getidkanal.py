
# Bot tokeningizni kiriting
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

BOT_TOKEN = "7091254660:AAEDwpV2NaW3xzeS8FZ3fBH_bnrQz-R7Vv4"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text.startswith("/start"))
async def send_welcome(message: Message):
    await message.reply("Salom! Kanalga xabar yuboring, men ID ni aniqlayman.")

@dp.message(F.chat.type.in_(["group", "supergroup", "channel"]))
async def get_channel_id(message: Message):
    chat_id = message.chat.id
    await message.reply(f"Kanal yoki guruh ID: `{chat_id}`")

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print('ishladi')
    asyncio.run(main())
