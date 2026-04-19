import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from openai import AsyncOpenAI

# Загрузка ключей из Railway
TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")

# Настройка клиента ИИ (Приоритет OpenAI)
if OPENAI_KEY:
    client = AsyncOpenAI(api_key=OPENAI_KEY, base_url="https://api.openai.com/v1")
    AI_MODEL = "gpt-4o"
    print("Используем OpenAI (gpt-4o)")
else:
    client = AsyncOpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com/v1")
    AI_MODEL = "deepseek-chat"
    print("Используем DeepSeek")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я твой инженерный ассистент. Пришли фото объекта для анализа.")

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    await message.answer("Анализирую фото, подождите...")
    try:
        # Здесь логика отправки фото в ИИ
        # Используем переменную AI_MODEL для автоматического выбора
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=[{"role": "user", "content": "Проанализируй это фото на соответствие стандартам."}]
        )
        await message.reply(response.choices[0].message.content)
    except Exception as e:
        await message.reply(f"Ошибка анализа: {str(e)}. Проверьте баланс.")

if _name_ == '_main_':
    executor.start_polling(dp, skip_updates=True)
