# -*- coding: utf-8 -*-
"""
EUROBAUCONSULT — Telegram-бот (@EurobauConsultingBot)
aiogram 3.x · polling · один инстанс.

AI: DeepSeek активен сразу. GPT-4o включается переменной AI_PROVIDER=openai.
Все секреты и настройки — из переменных окружения (os.getenv). Ничего не хардкодим.

Запуск локально:  python eurobau.py
Деплой:           Railway worker (Procfile: worker: python eurobau.py)
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from texts import AI_SYSTEM, CHOOSE_LANG, LANGS, TEXTS, t

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("ebc-bot")

# ─────────────────────────── КОНФИГ (env) ───────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

AI_PROVIDER = os.getenv("AI_PROVIDER", "deepseek").lower()  # deepseek | openai
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Куда падают заявки: ID чата менеджера (или твой личный ID на старте).
MANAGER_CHAT_ID = os.getenv("MANAGER_CHAT_ID", "")        # TODO: впиши свой chat_id
# Контактные данные для экранов "Связаться" и "Аварийка".
EMERGENCY_PHONE = os.getenv("EMERGENCY_PHONE", "+XX XXX XXX XXX")  # TODO
MANAGER_USERNAME = os.getenv("MANAGER_USERNAME", "@EuroBauConsult")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "info@eurobauconsult.com")
CONTACT_SITE = os.getenv("CONTACT_SITE", "eurobauconsult.com")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в переменных окружения")

# ─────────────────────────── AI-слой ───────────────────────────
# DeepSeek API совместим с OpenAI SDK — отличаются только base_url и модель.
# Переключение провайдера = одна переменная AI_PROVIDER, логика общая.
try:
    from openai import AsyncOpenAI
except ImportError:
    AsyncOpenAI = None


def _ai_client():
    """Возвращает (client, model) или (None, None), если AI недоступен."""
    if AsyncOpenAI is None:
        return None, None
    if AI_PROVIDER == "openai" and OPENAI_API_KEY:
        return AsyncOpenAI(api_key=OPENAI_API_KEY), "gpt-4o"
    if DEEPSEEK_API_KEY:  # дефолт и fallback
        return (
            AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com"),
            "deepseek-chat",
        )
    return None, None


AI_CLIENT, AI_MODEL = _ai_client()
log.info("AI provider: %s | model: %s", AI_PROVIDER, AI_MODEL or "OFF")


async def ask_ai(lang: str, user_text: str) -> str | None:
    """Запрос к AI. None → недоступен (нет ключа/баланса/ошибка)."""
    if AI_CLIENT is None:
        return None
    try:
        resp = await AI_CLIENT.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": AI_SYSTEM.get(lang, AI_SYSTEM["ru"])},
                {"role": "user", "content": user_text},
            ],
            max_tokens=600,
            temperature=0.4,
        )
        return resp.choices[0].message.content
    except Exception as e:  # нет баланса, таймаут, и т.п.
        log.warning("AI error: %s", e)
        return None


# ─────────────────────────── FSM ───────────────────────────
class Flow(StatesGroup):
    lead_objtype = State()
    lead_location = State()
    lead_desc = State()
    lead_photo = State()
    lead_contact = State()
    emerg_desc = State()
    emerg_phone = State()
    photo_wait = State()
    ai_chat = State()


router = Router()


# ─────────────────────────── helpers ───────────────────────────
async def get_lang(state: FSMContext) -> str:
    data = await state.get_data()
    return data.get("lang", "ru")


def kb_lang():
    b = InlineKeyboardBuilder()
    for code, label in LANGS:
        b.button(text=label, callback_data=f"lang:{code}")
    b.adjust(2)
    return b.as_markup()


def kb_main(lang):
    b = InlineKeyboardBuilder()
    b.button(text=t(lang, "btn_services"), callback_data="menu:services")
    b.button(text=t(lang, "btn_emergency"), callback_data="menu:emergency")
    b.button(text=t(lang, "btn_photo"), callback_data="menu:photo")
    b.button(text=t(lang, "btn_ai"), callback_data="menu:ai")
    b.button(text=t(lang, "btn_contact"), callback_data="menu:contact")
    b.button(text=t(lang, "btn_lang"), callback_data="menu:lang")
    b.adjust(1, 2, 2, 1)
    return b.as_markup()


SERVICES = ["inspect", "plumb", "bath", "heatpump"]


def kb_services(lang):
    b = InlineKeyboardBuilder()
    for key in SERVICES:
        b.button(text=t(lang, f"svc_{key}_title"), callback_data=f"svc:{key}")
    b.button(text=t(lang, "btn_back"), callback_data="menu:main")
    b.adjust(1)
    return b.as_markup()


def kb_service_leaf(lang, key):
    b = InlineKeyboardBuilder()
    b.button(text=t(lang, "btn_request"), callback_data=f"req:{key}")
    b.button(text=t(lang, "btn_back"), callback_data="menu:services")
    b.adjust(1)
    return b.as_markup()


def kb_objtype(lang):
    b = InlineKeyboardBuilder()
    b.button(text=t(lang, "obj_apartment"), callback_data="obj:apartment")
    b.button(text=t(lang, "obj_house"), callback_data="obj:house")
    b.button(text=t(lang, "obj_commercial"), callback_data="obj:commercial")
    b.adjust(3)
    return b.as_markup()


def kb_skip(lang):
    b = InlineKeyboardBuilder()
    b.button(text=t(lang, "btn_skip"), callback_data="lead:skipphoto")
    return b.as_markup()


def kb_yes_no(lang):
    b = InlineKeyboardBuilder()
    b.button(text=t(lang, "btn_yes"), callback_data="photo:yes")
    b.button(text=t(lang, "btn_no"), callback_data="menu:main")
    b.adjust(2)
    return b.as_markup()


def kb_menu_only(lang):
    b = InlineKeyboardBuilder()
    b.button(text=t(lang, "btn_menu"), callback_data="menu:main")
    return b.as_markup()


async def show_main(target, lang, state: FSMContext):
    """Сброс активного шага (язык сохраняется) и показ главного меню."""
    await state.set_state(None)
    await target.answer(t(lang, "main_title"), reply_markup=kb_main(lang))


async def notify_manager(bot: Bot, text: str, photo_id: str | None = None):
    """Отправка заявки менеджеру. Если MANAGER_CHAT_ID не задан — только лог."""
    if not MANAGER_CHAT_ID:
        log.info("LEAD (MANAGER_CHAT_ID не задан):\n%s", text)
        return
    try:
        chat_id = int(MANAGER_CHAT_ID)
        if photo_id:
            await bot.send_photo(chat_id, photo_id, caption=text)
        else:
            await bot.send_message(chat_id, text)
    except Exception as e:
        log.warning("notify_manager error: %s", e)


# ─────────────────────────── /start и язык ───────────────────────────
@router.message(CommandStart())
async def cmd_start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(CHOOSE_LANG, reply_markup=kb_lang())


@router.callback_query(F.data.startswith("lang:"))
async def set_lang(cb: CallbackQuery, state: FSMContext):
    lang = cb.data.split(":", 1)[1]
    if lang not in TEXTS:
        lang = "ru"
    await state.update_data(lang=lang)
    await cb.message.answer(t(lang, "main_title"), reply_markup=kb_main(lang))
    await cb.answer()


@router.callback_query(F.data == "menu:lang")
async def menu_lang(cb: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    await cb.message.answer(CHOOSE_LANG, reply_markup=kb_lang())
    await cb.answer()


@router.callback_query(F.data == "menu:main")
async def menu_main(cb: CallbackQuery, state: FSMContext):
    await show_main(cb.message, await get_lang(state), state)
    await cb.answer()


# ─────────────────────────── Услуги ───────────────────────────
@router.callback_query(F.data == "menu:services")
async def menu_services(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    await state.set_state(None)
    await cb.message.answer(t(lang, "services_title"), reply_markup=kb_services(lang))
    await cb.answer()


@router.callback_query(F.data.startswith("svc:"))
async def service_leaf(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    key = cb.data.split(":", 1)[1]
    text = f"{t(lang, f'svc_{key}_title')}\n\n{t(lang, f'svc_{key}_desc')}"
    await cb.message.answer(text, reply_markup=kb_service_leaf(lang, key))
    await cb.answer()


# ─────────────────────────── Форма заявки (LEAD) ───────────────────────────
@router.callback_query(F.data.startswith("req:"))
async def lead_start(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    key = cb.data.split(":", 1)[1]
    await state.update_data(service=key, photo_id=None)
    await state.set_state(Flow.lead_objtype)
    await cb.message.answer(t(lang, "lead_objtype"), reply_markup=kb_objtype(lang))
    await cb.answer()


@router.callback_query(Flow.lead_objtype, F.data.startswith("obj:"))
async def lead_objtype(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    await state.update_data(objtype=cb.data.split(":", 1)[1])
    await state.set_state(Flow.lead_location)
    await cb.message.answer(t(lang, "lead_location"))
    await cb.answer()


@router.message(Flow.lead_location)
async def lead_location(msg: Message, state: FSMContext):
    lang = await get_lang(state)
    await state.update_data(location=msg.text)
    await state.set_state(Flow.lead_desc)
    await msg.answer(t(lang, "lead_desc"))


@router.message(Flow.lead_desc)
async def lead_desc(msg: Message, state: FSMContext):
    lang = await get_lang(state)
    await state.update_data(desc=msg.text)
    await state.set_state(Flow.lead_photo)
    await msg.answer(t(lang, "lead_photo"), reply_markup=kb_skip(lang))


@router.message(Flow.lead_photo, F.photo)
async def lead_photo_received(msg: Message, state: FSMContext):
    lang = await get_lang(state)
    await state.update_data(photo_id=msg.photo[-1].file_id)
    await state.set_state(Flow.lead_contact)
    await msg.answer(t(lang, "lead_contact"))


@router.callback_query(Flow.lead_photo, F.data == "lead:skipphoto")
async def lead_photo_skip(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    await state.set_state(Flow.lead_contact)
    await cb.message.answer(t(lang, "lead_contact"))
    await cb.answer()


@router.message(Flow.lead_contact)
async def lead_finish(msg: Message, state: FSMContext):
    lang = await get_lang(state)
    await state.update_data(contact=msg.text)
    data = await state.get_data()

    summary = (
        "🟢 НОВАЯ ЗАЯВКА\n"
        f"Услуга: {data.get('service')}\n"
        f"Тип объекта: {data.get('objtype')}\n"
        f"Локация: {data.get('location')}\n"
        f"Описание: {data.get('desc')}\n"
        f"Контакт: {data.get('contact')}\n"
        f"Язык клиента: {lang} | @{msg.from_user.username or msg.from_user.id}"
    )
    await notify_manager(msg.bot, summary, data.get("photo_id"))

    await state.set_state(None)
    await msg.answer(t(lang, "lead_done"), reply_markup=kb_menu_only(lang))


# ─────────────────────────── Аварийный вызов ───────────────────────────
@router.callback_query(F.data == "menu:emergency")
async def emergency_start(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    await state.set_state(Flow.emerg_desc)
    await cb.message.answer(t(lang, "emerg_desc"))
    await cb.answer()


@router.message(Flow.emerg_desc)
async def emergency_desc(msg: Message, state: FSMContext):
    lang = await get_lang(state)
    await state.update_data(emerg_desc=msg.text)
    await state.set_state(Flow.emerg_phone)
    await msg.answer(t(lang, "emerg_phone"))


@router.message(Flow.emerg_phone)
async def emergency_finish(msg: Message, state: FSMContext):
    lang = await get_lang(state)
    data = await state.get_data()
    summary = (
        "🚨 АВАРИЙНЫЙ ВЫЗОВ\n"
        f"Проблема: {data.get('emerg_desc')}\n"
        f"Телефон: {msg.text}\n"
        f"@{msg.from_user.username or msg.from_user.id}"
    )
    await notify_manager(msg.bot, summary)
    await state.set_state(None)
    await msg.answer(
        t(lang, "emerg_done").format(phone=EMERGENCY_PHONE),
        reply_markup=kb_menu_only(lang),
    )


# ─────────────────────────── Фото объекта ───────────────────────────
@router.callback_query(F.data == "menu:photo")
async def photo_start(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    await state.set_state(Flow.photo_wait)
    await cb.message.answer(t(lang, "photo_prompt"))
    await cb.answer()


@router.message(Flow.photo_wait, F.photo)
async def photo_received(msg: Message, state: FSMContext):
    lang = await get_lang(state)
    await state.update_data(photo_id=msg.photo[-1].file_id)
    await msg.answer(t(lang, "photo_more"), reply_markup=kb_yes_no(lang))


@router.callback_query(F.data == "photo:yes")
async def photo_to_lead(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    await state.update_data(service="photo")
    await state.set_state(Flow.lead_objtype)
    await cb.message.answer(t(lang, "lead_objtype"), reply_markup=kb_objtype(lang))
    await cb.answer()


# ─────────────────────────── Консультация (AI) ───────────────────────────
@router.callback_query(F.data == "menu:ai")
async def ai_start(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    await state.set_state(Flow.ai_chat)
    await cb.message.answer(t(lang, "ai_prompt"), reply_markup=kb_menu_only(lang))
    await cb.answer()


@router.message(Flow.ai_chat, F.text)
async def ai_reply(msg: Message, state: FSMContext):
    lang = await get_lang(state)
    answer = await ask_ai(lang, msg.text)
    if answer is None:
        answer = t(lang, "ai_off")
    await msg.answer(answer, reply_markup=kb_menu_only(lang))


# ─────────────────────────── Связаться ───────────────────────────
@router.callback_query(F.data == "menu:contact")
async def contact(cb: CallbackQuery, state: FSMContext):
    lang = await get_lang(state)
    body = t(lang, "contact_body").format(
        manager=MANAGER_USERNAME,
        email=CONTACT_EMAIL,
        phone=EMERGENCY_PHONE,
        site=CONTACT_SITE,
    )
    text = f"{t(lang, 'contact_title')}\n\n{body}"
    await cb.message.answer(text, reply_markup=kb_menu_only(lang))
    await cb.answer()


# ─────────────────────────── Fallback: свободный текст → AI ───────────────────────────
@router.message(F.text)
async def fallback_text(msg: Message, state: FSMContext):
    lang = await get_lang(state)
    answer = await ask_ai(lang, msg.text)
    if answer is None:
        # AI выключен → не молчим, ведём в меню
        await show_main(msg, lang, state)
        return
    await msg.answer(answer, reply_markup=kb_menu_only(lang))


# ─────────────────────────── запуск ───────────────────────────
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    # drop_pending_updates снижает риск конфликта при перезапуске
    await bot.delete_webhook(drop_pending_updates=True)
    log.info("Бот запущен (polling). Один инстанс!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
