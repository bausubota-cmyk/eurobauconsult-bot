import logging
import asyncio
import base64
import httpx

TELEGRAM_TOKEN = "8258431851:AAEOuEU4L3TKXE86kc8wTuAPSs62cVr1QJA"
DEEPSEEK_API_KEY = "sk-a9bb08ee2b4144f58205a9726821ae66"
ADMIN_CHAT_ID = 934910767

SYSTEM_PROMPT = """Ты умный ассистент EuroBauConsult. Европейская управляющая компания в 28 странах ЕС. Всё общение только письменно. Договор с каждым клиентом. Каждый проект застрахован.

ПРАЙС-ЛИСТ:
1. Осмотр недвижимости: Базовый от 250 EUR, Расширенный от 600 EUR, Полный аудит от 1200 EUR + накладные
2. Юридическое сопровождение: от 500 EUR
3. Демонтаж: плитка 15-25 EUR/м2, снос перегородки от 200 EUR, вывоз мусора от 150 EUR
4. Отопление: тёплый пол 40-80 EUR/м2, радиатор от 300 EUR, котёл от 1500 EUR
5. Сантехника/канализация: трубы 30-60 EUR/м.п., полная разводка от 1500 EUR
6. Гипсокартон Knauf: перегородка 25-40 EUR/м2, выравнивание 15-30 EUR/м2
7. Ремонт под ключ: ванная до 5м2 от 3000 EUR, квартира-студия от 8000 EUR, 1-комнатная от 12000 EUR
8. Замки: умный замок от 400 EUR, бронедверь от 900 EUR
9. Регистрация бизнеса: от 500 EUR

НАКЛАДНЫЕ всегда отдельно: транспорт, доставка материалов, вывоз мусора.

ПРАВИЛА:
- Отвечай на языке клиента автоматически
- При описании объекта сразу давай расчёт с диапазоном цен
- При фото - анализируй состояние и считай стоимость работ
- Всегда предлагай следующий шаг - осмотр или договор
- Упоминай что накладные расходы отдельной строкой в договоре
- Будь конкретным и профессиональным"""

conversations = {}
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def ask_ai(chat_id, user_message, image_base64=None):
    if chat_id not in conversations:
        conversations[chat_id] = []
    
    if image_base64:
        msg = {"role": "user", "content": [
            {"type": "text", "text": user_message},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
        ]}
    else:
        msg = {"role": "user", "content": user_message}
    
    conversations[chat_id].append(msg)
    if len(conversations[chat_id]) > 20:
        conversations[chat_id] = conversations[chat_id][-20:]
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.deepseek.com/chat/completions",
                headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "content-type": "application/json"},
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + conversations[chat_id],
                    "max_tokens": 1024,
                    "temperature": 0.7
                }
            )
            data = response.json()
            if "choices" in data:
                reply = data["choices"][0]["message"]["content"]
                conversations[chat_id].append({"role": "assistant", "content": reply})
                return reply
            logger.error(f"AI error: {data}")
            return "Произошла ошибка. Повторите запрос."
    except Exception as e:
        logger.error(f"AI error: {e}")
        return "Техническая ошибка. Попробуйте позже."

async def send_msg(chat_id, text):
    async with httpx.AsyncClient() as client:
        await client.post(f"{TELEGRAM_API}/sendMessage", json={
            "chat_id": chat_id, "text": text, "parse_mode": "HTML"
        })

async def send_typing(chat_id):
    async with httpx.AsyncClient() as client:
        await client.post(f"{TELEGRAM_API}/sendChatAction", json={"chat_id": chat_id, "action": "typing"})

async def handle_update(update):
    if "message" not in update:
        return
    msg = update["message"]
    chat_id = msg["chat"]["id"]
    user_name = msg.get("from", {}).get("first_name", "Unknown")
    lang = msg.get("from", {}).get("language_code", "ru")[:2]

    # Photo handling
    if "photo" in msg:
        await send_typing(chat_id)
        photo = msg["photo"][-1]
        caption = msg.get("caption", "Проанализируй фото объекта. Опиши состояние и дай примерный расчёт стоимости работ EuroBauConsult.")
        try:
            async with httpx.AsyncClient() as client:
                f = await client.get(f"{TELEGRAM_API}/getFile?file_id={photo['file_id']}")
                fp = f.json()["result"]["file_path"]
                img = await client.get(f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{fp}")
                img_b64 = base64.b64encode(img.content).decode()
            reply = await ask_ai(chat_id, caption, img_b64)
        except Exception as e:
            reply = "Фото получено! Опишите объект подробнее для расчёта стоимости."
        await send_msg(chat_id, reply)
        await send_msg(ADMIN_CHAT_ID, f"Фото от {user_name} ({chat_id})")
        return

    if "text" not in msg:
        await send_msg(chat_id, "Пожалуйста, отправьте текст или фото.")
        return

    text = msg["text"].strip()
    logger.info(f"{user_name}({chat_id}): {text[:50]}")

    if text.startswith("/start"):
        conversations[chat_id] = []
        greetings = {
            "ru": "Добро пожаловать в <b>EuroBauConsult</b>!\n\nЕвропейская управляющая компания. Недвижимость и ремонт в 28 странах ЕС.\n\n<b>Услуги:</b>\n- Осмотр недвижимости от €250\n- Юридическое сопровождение от €500\n- Ремонт под ключ от €3000\n- Отопление, сантехника, стены\n- Демонтаж от €500\n- Замки и безопасность\n\n<i>Только письменное общение. Договор с каждым.</i>\n\nОпишите вашу задачу или пришлите фото объекта!",
            "en": "Welcome to <b>EuroBauConsult</b>!\n\nEuropean management company. Real estate and renovation in 28 EU countries.\n\n<i>Written communication only. Contract with every client.</i>\n\nDescribe your task or send a photo!",
            "de": "Willkommen bei <b>EuroBauConsult</b>!\n\nEuropaisches Managementunternehmen in 28 EU-Landern.\n\n<i>Nur schriftliche Kommunikation.</i>\n\nBeschreiben Sie Ihre Aufgabe!"
        }
        await send_msg(chat_id, greetings.get(lang, greetings["ru"]))
        await send_msg(ADMIN_CHAT_ID, f"Новый пользователь: {user_name} (lang:{lang}) ID:{chat_id}")
        return

    if text.startswith("/reset"):
        conversations[chat_id] = []
        await send_msg(chat_id, "Начнём сначала!")
        return

    if text.startswith("/services"):
        await send_msg(chat_id, "<b>Услуги EuroBauConsult:</b>\n\n- Осмотр от €250\n- Юрист от €500\n- Отопление от €2000\n- Сантехника от €1500\n- Гипсокартон от €800\n- Демонтаж от €500\n- Ремонт под ключ от €3000\n- Замки от €400\n- Регистрация бизнеса от €500\n\neurobauconsult.com")
        return

    await send_typing(chat_id)
    reply = await ask_ai(chat_id, text)
    await send_msg(chat_id, reply)
    if len(conversations.get(chat_id, [])) <= 2:
        await send_msg(ADMIN_CHAT_ID, f"Новый диалог!\n{user_name} (lang:{lang})\n{text[:100]}")

async def run():
    logger.info("EuroBauConsult Bot started!")
    offset = 0
    async with httpx.AsyncClient(timeout=35.0) as client:
        while True:
            try:
                r = await client.get(f"{TELEGRAM_API}/getUpdates", params={"offset": offset, "timeout": 30, "allowed_updates": ["message"]})
                data = r.json()
                if data.get("ok"):
                    for upd in data.get("result", []):
                        offset = upd["update_id"] + 1
                        try:
                            await handle_update(upd)
                        except Exception as e:
                            logger.error(f"Error: {e}")
            except httpx.TimeoutException:
                continue
            except Exception as e:
                logger.error(f"Polling error: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    print("EuroBauConsult Bot starting...")
    asyncio.run(run())
