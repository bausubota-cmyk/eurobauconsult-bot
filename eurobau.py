import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from openai import AsyncOpenAI

# 1. КОНФИГУРАЦИЯ КЛЮЧЕЙ
TELEGRAM_TOKEN = "8258431851:AAE-U-AZ3BtD1NZa5xz0IwVsSHW1XHK91as"
OPENAI_API_KEY = "sk-a9bb08ee2b4144f58205a9726821ae66"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") # Берется из Variables

# 2. ИНИЦИАЛИЗАЦИЯ СИСТЕМ
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Основной интеллект (OpenAI GPT-4o)
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
# Инженерный интеллект (DeepSeek)
deepseek_client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY if DEEPSEEK_API_KEY else "dummy", base_url="https://api.deepseek.com")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "🏗️ **Eurobau Инженерный Ассистент 2026**\n"
        "Система готова. Я понимаю эстонский, немецкий и русский.\n"
        "Отправьте адрес для анализа логистики или фото чертежа."
    )
    await message.reply(welcome_text, parse_mode="Markdown")

@dp.message_handler()
async def handle_ai(message: types.Message):
    try:
        # Основной запрос идет через оплаченный OpenAI
        response = await openai_client.chat.completions.create(
            model="gpt-4o", # Используем новейшую модель для анализа
            messages=[{"role": "user", "content": message.text}]
        )
        await message.answer(response.choices[0].message.content)
    except Exception as e:
        # Резервный канал через DeepSeek
        try:
            res = await deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": message.text}]
            )
            await message.answer(res.choices[0].message.content)
        except:
            await message.answer(f"⚠️ Ошибка связи с ИИ. Проверьте баланс или лимиты: {str(e)}")

# 3. ЗАПУСК БЕЗ ОШИБОК
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
