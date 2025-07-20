import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv

# Загрузка токена из переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройка логов
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Пример базы квартир (заглушка)
FLATS = [
    {
        "id": 1,
        "district": "таирова",
        "rooms": 1,
        "price": 8500,
        "description": "1-к на Таирова, 8500 грн. Новый ремонт.",
        "url": "https://example.com/flat123",
        "phone": "+380931234567"
    },
    {
        "id": 2,
        "district": "центр",
        "rooms": 2,
        "price": 11000,
        "description": "2-к в Центре, 11000 грн. Вид на море.",
        "url": "https://example.com/flat456",
        "phone": "+380987654321"
    },
]

# Стартовая команда
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Я помогу тебе найти квартиру в Одессе.\nНапиши, например:\n\n"
        "«1-комнатная Таирова до 9000»\n"
        "или\n"
        "«2-к Центр до 12000»"
    )

# Поиск квартир
@dp.message_handler()
async def search_flat(message: types.Message):
    text = message.text.lower()
    results = []

    for flat in FLATS:
        if flat["district"] in text and str(flat["rooms"]) in text and str(flat["price"]) in text:
            results.append(flat)
        elif flat["district"] in text and str(flat["rooms"]) in text:
            if "до" in text:
                try:
                    max_price = int("".join([c for c in text.split("до")[-1] if c.isdigit()]))
                    if flat["price"] <= max_price:
                        results.append(flat)
                except:
                    continue

    if results:
        for flat in results:
            keyboard = InlineKeyboardMarkup().add(
                InlineKeyboardButton("📞 Позвонить", url=f"tel:{flat['phone']}"),
                InlineKeyboardButton("📷 Смотреть", url=flat["url"])
            )
            await message.answer(flat["description"], reply_markup=keyboard)
    else:
        await message.answer("😕 К сожалению, ничего не найдено. Попробуй другой запрос!")

# Запуск
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
