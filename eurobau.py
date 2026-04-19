import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from openai import AsyncOpenAI

# 1. ТВОИ КЛЮЧИ (Теперь они прописаны прямо здесь)
TELEGRAM_TOKEN = "8258431851:AAE-U-AZ3BtD1NZa5xz0IwVsSHW1XHK91as"
OPENAI_API_KEY = "sk-a9bb08ee2b4144f58205a9726821ae66"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") # Подтянется из Variables, если он там есть

# 2. НАСТРОЙКА
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Инициализируем клиентов
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
deepseek_client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY if DEEPSEEK_API_KEY else "dummy", base_url="https://api.deepseek.com")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Бот Eurobau запущен! Мозги OpenAI и DeepSeek на месте.")

@dp.message_handler()
async def handle_ai(message: types.Message):
    try:
        # Приоритет отдаем OpenAI
        response = await openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        await message.answer(response.choices[0].message.content)
        
    except Exception as e:
        # Если OpenAI выдал ошибку, пробуем DeepSeek
        try:
            response = await deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": message.text}]
            )
            await message.answer(response.choices[0].message.content)
        except Exception as deep_e:
            await message.answer(f"Ошибка обоих ИИ: {str(deep_e)}")

# 3. ЗАПУСК (ОТСТУПЫ ПРОВЕРЕНЫ, ОШИБКИ 44 НЕ БУДЕТ)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
