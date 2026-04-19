import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from openai import AsyncOpenAI

# Берем все ключи из настроек Variables
TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# OpenAI (модель gpt-4o для зрения и анализа чертежей)
openai_client = AsyncOpenAI(api_key=OPENAI_KEY)
# DeepSeek (для сложной логики и точных расчетов)
deepseek_client = AsyncOpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("🏗 *Eurobau AI Ассистент запущен!*\n\nПрисылайте:\n📸 Фото объекта или чертеж — я их проанализирую.\n📊 Текстовую задачу — я сделаю расчет материалов.")

# --- РАБОТА С ФОТО И ЧЕРТЕЖАМИ (OpenAI Vision) ---
@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    await message.answer("🔍 Изучаю изображение/чертеж...")
    try:
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

        # Отправляем в OpenAI (Vision)
        response = await openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Ты инженер-строитель. Проанализируй этот чертеж/фото. Выдели ключевые размеры и детали для подготовки сметы."},
                        {"type": "image_url", "image_url": {"url": file_url}}
                    ],
                }
            ],
        )
        await message.answer(f"✅ *Анализ чертежа:*\n\n{response.choices[0].message.content}", parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Ошибка зрения: {str(e)}")

# --- ТЕКСТОВЫЕ РАСЧЕТЫ И СМЕТЫ (DeepSeek) ---
@dp.message_handler()
async def handle_text(message: types.Message):
    try:
        # DeepSeek лучше справляется с математикой и логикой расчетов
        response = await deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Ты эксперт в строительных расчетах и инженерии. Твоя задача — делать максимально точные расчеты материалов, объемов и стоимости."},
                {"role": "user", "content": message.text}
            ]
        )
        await message.answer(f"📐 *Инженерный расчет:*\n\n{response.choices[0].message.content}", parse_mode="Markdown")
    except Exception as e:
        # Если DeepSeek не доступен, подстрахуем через OpenAI
        res = await openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": message.text}]
        )
        await message.answer(res.choices[0].message.content)

if _name_ == '_main_':
    executor.start_polling(dp, skip_updates=True)
