# EUROBAUCONSULT bot

Telegram-бот @EurobauConsultingBot. aiogram 3.x, polling, один инстанс.
AI: DeepSeek активен сразу; GPT-4o включается переменной `AI_PROVIDER=openai`.

## Файлы
- `eurobau.py` — логика, FSM, AI, маршрутизация заявок
- `texts.py` — все тексты на 4 языках (de/en/et/ru)
- `requirements.txt`, `Procfile`, `.gitignore`, `.env.example`

## Перед запуском впиши 3 значения
В Railway → Variables (или в локальный `.env`):
1. `BOT_TOKEN` — от BotFather
2. `DEEPSEEK_API_KEY` — ключ DeepSeek (баланс должен быть пополнен)
3. `MANAGER_CHAT_ID` — твой chat_id (узнать у @userinfobot), куда падают заявки
4. `EMERGENCY_PHONE` — реальный номер для аварийной ветки

`OPENAI_API_KEY` оставь пустым, пока OpenAI не оплачен — бот это переживёт.

## Локальный запуск
```
pip install -r requirements.txt
cp .env.example .env   # заполни значения
python eurobau.py
```

## Деплой на Railway (worker, ~$5/мес Hobby)
1. Залей папку в репозиторий GitHub.
2. Railway → New Project → Deploy from GitHub repo.
3. Settings → тип процесса возьмётся из `Procfile` (worker). Порт не нужен.
4. Variables → впиши переменные из списка выше.
5. Deploy. Смотри логи: «Бот запущен (polling). Один инстанс!»

## Важно
- **Ровно один работающий экземпляр.** Пока бот в облаке — не запускай `python eurobau.py` локально, иначе polling conflict.
- Токен только в переменных окружения, не в коде.
- Заявки и аварийка шлются в `MANAGER_CHAT_ID`. Если он пуст — заявка пишется в лог (бот не падает). Интеграцию с Notion через Make.com можно добавить позже в `notify_manager()`.

## Когда оплатишь OpenAI
Поставь `AI_PROVIDER=openai` и заполни `OPENAI_API_KEY`. Перезапуск — больше ничего.
