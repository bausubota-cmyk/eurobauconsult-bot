import telebot
import os
import requests
import base64
from telebot import types

# Берем данные из переменных Railway
token = os.getenv("TELEGRAM_TOKEN")
api_key = os.getenv("DEEPSEEK_API_KEY")

# Ваш ID (из скриншота 8c6fdf76)
admin_id = 934910767 

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "🏗 *Eurobau Consult AI*\n\n"
        "Здравствуйте! Я ваш интеллектуальный инженерный ассистент.\n\n"
        "📸 *Пришлите фото объекта*, и я проведу технический анализ на соответствие европейским стандартам."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    status_msg = bot.reply_to(message, "🔍 Анализирую изображение... Пожалуйста, подождите.")
    
    try:
        # 1. Загрузка и подготовка фото
        file_info = bot.get_file(message.photo[-1].file_id)
        file_content = bot.download_file(file_info.file_path)
        base64_image = base64.b64encode(file_content).decode('utf-8')

        # 2. Запрос к AI (используем модель Vision)
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "model": "gpt-4o", 
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Ты ведущий инженер Eurobau Consult. Проведи профессиональный технический анализ этого фото. Найди дефекты или нарушения норм ЕС."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ]
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        analysis = response.json()['choices'][0]['message']['content']

        # 3. Отправка результата и кнопки сбора лидов
        bot.send_message(message.chat.id, analysis, parse_mode="Markdown")
        
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(types.KeyboardButton(text="📱 Получить консультацию эксперта", request_contact=True))
        bot.send_message(message.chat.id, "Хотите обсудить этот анализ с нашим специалистом лично?", reply_markup=markup)
        
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка анализа. Проверьте баланс API или ключ.")
    finally:
        bot.delete_message(message.chat.id, status_msg.message_id)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact is not None:
        # Уведомление вам (админу)
        report = (
            f"🚀 *НОВАЯ ЗАЯВКА*\n\n"
            f"Имя: {message.contact.first_name}\n"
            f"Телефон: {message.contact.phone_number}"
        )
        bot.send_message(admin_id, report, parse_mode="Markdown")
        
        # Ответ клиенту
        bot.send_message(message.chat.id, "Спасибо! Запрос принят. Мы свяжемся с вами в ближайшее время.", reply_markup=types.ReplyKeyboardRemove())

bot.polling(none_stop=True)