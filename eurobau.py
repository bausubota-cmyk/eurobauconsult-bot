import logging
from aiogram import Bot, Dispatcher, executor, types
from openai import AsyncOpenAI

# 1. ТВОИ КЛЮЧИ НАПРЯМУЮ (БЕЗ ВОДЫ)
TELEGRAM_TOKEN = "8258431851:AAE-U-AZ3BtD1NZa5xz0IwVsSHW1XHK91as"
OPENAI_API_KEY = "sk-a9bb08ee2b4144f58205a9726821ae66"

# 2. НАСТРОЙКА БОТА
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Инициализация OpenAI
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Инженерный ассистент Eurobau запущен и готов к работе!")

@dp.message_handler()
async def handle_ai(message: types.Message):
    try:
        # Прямой запрос к OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        await message.answer(response.choices[0].message.content)
    except Exception as e:
        await message.answer(f"Ошибка ИИ: {str(e)}")

# 3. ТОЧКА ЗАПУСКА (ОШИБКА 44 ИСПРАВЛЕНА)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
