# -*- coding: utf-8 -*-
"""
EUROBAUCONSULT bot — все тексты на 4 языках (de / en / et / ru).
Один источник правды. Объединяет UI и описания услуг.
(Заменяет ранее созданный EBC_service_texts.py.)

Добавить новый язык = скопировать блок и перевести ключи. Логику не трогать.
"""

# Языки, которые показываются на экране выбора
LANGS = [
    ("de", "🇩🇪 Deutsch"),
    ("ru", "🇷🇺 Русский"),
    ("en", "🇬🇧 English"),
    ("et", "🇪🇪 Eesti"),
]

CHOOSE_LANG = "🌐 Choose your language / Sprache wählen / Выберите язык / Valige keel"

TEXTS = {
    # ─────────────────────────── DEUTSCH ───────────────────────────
    "de": {
        "main_title": "🏠 EUROBAUCONSULT — Womit können wir helfen?",
        "btn_services": "🛠 Leistungen",
        "btn_emergency": "🚨 Notdienst",
        "btn_photo": "📷 Objektfoto",
        "btn_ai": "💬 Beratung",
        "btn_contact": "☎️ Kontakt",
        "btn_lang": "🌐 Sprache",
        "btn_request": "Anfrage senden",
        "btn_back": "← Zurück",
        "btn_menu": "🏠 Menü",
        "btn_skip": "Überspringen",
        "btn_yes": "Ja",
        "btn_no": "Nein",

        "services_title": "Welche Leistung interessiert Sie?",
        "svc_inspect_title": "🔍 Immobilienbesichtigung",
        "svc_inspect_desc": "Professionelle Zustandsbewertung Ihrer Immobilie vor Kauf, Vermietung oder Sanierung — mit Vor-Ort-Begehung, technischem Bericht und klaren Handlungsempfehlungen.",
        "svc_plumb_title": "🚿 Sanitärarbeiten",
        "svc_plumb_desc": "Installation, Austausch und Reparatur von Sanitäranlagen jeder Komplexität — von der Leckbehebung bis zur kompletten Rohrverlegung. Mit Gewährleistung.",
        "svc_bath_title": "🛁 Bad-Komplettsanierung",
        "svc_bath_desc": "Schlüsselfertige Badsanierung: Planung, Abbruch, Sanitär, Fliesen und Übergabe des fertigen Bades. Ein Auftragnehmer — eine Verantwortung.",
        "svc_heatpump_title": "♨️ Wärmepumpen",
        "svc_heatpump_desc": "Auswahl, Lieferung und Installation von Wärmepumpen für Heizung und Warmwasser — energieeffiziente Lösungen mit Amortisationsberechnung.",

        "lead_objtype": "Objekttyp?",
        "obj_apartment": "Wohnung",
        "obj_house": "Haus",
        "obj_commercial": "Gewerbe",
        "lead_location": "Ort / Adresse?",
        "lead_desc": "Kurz: was ist zu tun?",
        "lead_photo": "Foto anhängen? (optional)",
        "lead_contact": "Telefon oder Telegram für Rückruf?",
        "lead_done": "✅ Anfrage erhalten — wir melden uns in Kürze.",

        "emerg_desc": "🚨 Notfall. Beschreiben Sie kurz das Problem.",
        "emerg_phone": "Telefonnummer für sofortigen Rückruf?",
        "emerg_done": "✅ Aufgenommen. Direkt erreichbar: {phone}",

        "photo_prompt": "Senden Sie Fotos des Objekts.",
        "photo_more": "Foto erhalten. Möchten Sie dazu eine Anfrage stellen?",

        "ai_prompt": "💬 Stellen Sie Ihre Frage zu Renovierung, Sanitär oder Wärmepumpen.",
        "ai_error": "Entschuldigung, momentan nicht verfügbar. Bitte später erneut versuchen.",
        "ai_off": "Die Beratung ist vorübergehend nicht verfügbar. Bitte hinterlassen Sie eine Anfrage.",

        "contact_title": "☎️ Kontakt",
        "contact_body": "Telegram: {manager}\nE-Mail: {email}\nTelefon: {phone}\nWebseite: {site}",
    },

    # ─────────────────────────── РУССКИЙ ───────────────────────────
    "ru": {
        "main_title": "🏠 EUROBAUCONSULT — чем можем помочь?",
        "btn_services": "🛠 Услуги",
        "btn_emergency": "🚨 Срочный вызов",
        "btn_photo": "📷 Фото объекта",
        "btn_ai": "💬 Консультация",
        "btn_contact": "☎️ Связаться",
        "btn_lang": "🌐 Сменить язык",
        "btn_request": "Оставить заявку",
        "btn_back": "← Назад",
        "btn_menu": "🏠 Меню",
        "btn_skip": "Пропустить",
        "btn_yes": "Да",
        "btn_no": "Нет",

        "services_title": "Какая услуга вас интересует?",
        "svc_inspect_title": "🔍 Осмотр недвижимости",
        "svc_inspect_desc": "Профессиональная оценка состояния объекта перед покупкой, арендой или ремонтом — выезд специалиста, технический отчёт и чёткие рекомендации.",
        "svc_plumb_title": "🚿 Сантехнические работы",
        "svc_plumb_desc": "Монтаж, замена и ремонт сантехники любой сложности — от устранения протечек до полной разводки труб. Гарантия на все работы.",
        "svc_bath_title": "🛁 Ванная под ключ",
        "svc_bath_desc": "Полный ремонт ванной под ключ: проект, демонтаж, сантехника, плитка и сдача готового результата. Один подрядчик — одна ответственность.",
        "svc_heatpump_title": "♨️ Тепловые насосы",
        "svc_heatpump_desc": "Подбор, поставка и установка тепловых насосов для отопления и горячего водоснабжения — энергоэффективные решения с расчётом окупаемости.",

        "lead_objtype": "Тип объекта?",
        "obj_apartment": "Квартира",
        "obj_house": "Дом",
        "obj_commercial": "Коммерция",
        "lead_location": "Город / адрес?",
        "lead_desc": "Кратко: что нужно сделать?",
        "lead_photo": "Прикрепить фото? (необязательно)",
        "lead_contact": "Телефон или Telegram для связи?",
        "lead_done": "✅ Заявка принята — мы скоро свяжемся.",

        "emerg_desc": "🚨 Авария. Опишите коротко проблему.",
        "emerg_phone": "Телефон для немедленного звонка?",
        "emerg_done": "✅ Принято. Прямой контакт: {phone}",

        "photo_prompt": "Отправьте фото объекта.",
        "photo_more": "Фото получено. Хотите оформить заявку?",

        "ai_prompt": "💬 Задайте вопрос по ремонту, сантехнике или тепловым насосам.",
        "ai_error": "Извините, сейчас недоступно. Попробуйте позже.",
        "ai_off": "Консультация временно недоступна. Пожалуйста, оставьте заявку.",

        "contact_title": "☎️ Связаться",
        "contact_body": "Telegram: {manager}\nE-mail: {email}\nТелефон: {phone}\nСайт: {site}",
    },

    # ─────────────────────────── ENGLISH ───────────────────────────
    "en": {
        "main_title": "🏠 EUROBAUCONSULT — How can we help?",
        "btn_services": "🛠 Services",
        "btn_emergency": "🚨 Emergency",
        "btn_photo": "📷 Send photo",
        "btn_ai": "💬 Consultation",
        "btn_contact": "☎️ Contact",
        "btn_lang": "🌐 Language",
        "btn_request": "Send a request",
        "btn_back": "← Back",
        "btn_menu": "🏠 Menu",
        "btn_skip": "Skip",
        "btn_yes": "Yes",
        "btn_no": "No",

        "services_title": "Which service are you interested in?",
        "svc_inspect_title": "🔍 Property Inspection",
        "svc_inspect_desc": "Professional assessment of a property's condition before purchase, rental or renovation — on-site inspection, technical report and clear recommendations.",
        "svc_plumb_title": "🚿 Plumbing Works",
        "svc_plumb_desc": "Installation, replacement and repair of plumbing of any complexity — from fixing leaks to full pipework. All work guaranteed.",
        "svc_bath_title": "🛁 Turnkey Bathroom",
        "svc_bath_desc": "Complete turnkey bathroom renovation: design, demolition, plumbing, tiling and handover of the finished result. One contractor, one point of responsibility.",
        "svc_heatpump_title": "♨️ Heat Pumps",
        "svc_heatpump_desc": "Selection, supply and installation of heat pumps for heating and hot water — energy-efficient solutions with a payback calculation.",

        "lead_objtype": "Property type?",
        "obj_apartment": "Apartment",
        "obj_house": "House",
        "obj_commercial": "Commercial",
        "lead_location": "Location / address?",
        "lead_desc": "Briefly: what needs to be done?",
        "lead_photo": "Attach a photo? (optional)",
        "lead_contact": "Phone or Telegram for a callback?",
        "lead_done": "✅ Request received — we'll be in touch shortly.",

        "emerg_desc": "🚨 Emergency. Briefly describe the problem.",
        "emerg_phone": "Phone number for an immediate callback?",
        "emerg_done": "✅ Received. Reach us directly: {phone}",

        "photo_prompt": "Send photos of the property.",
        "photo_more": "Photo received. Would you like to submit a request?",

        "ai_prompt": "💬 Ask your question about renovation, plumbing or heat pumps.",
        "ai_error": "Sorry, currently unavailable. Please try again later.",
        "ai_off": "Consultation is temporarily unavailable. Please leave a request.",

        "contact_title": "☎️ Contact",
        "contact_body": "Telegram: {manager}\nEmail: {email}\nPhone: {phone}\nWebsite: {site}",
    },

    # ─────────────────────────── EESTI ───────────────────────────
    "et": {
        "main_title": "🏠 EUROBAUCONSULT — Kuidas saame aidata?",
        "btn_services": "🛠 Teenused",
        "btn_emergency": "🚨 Hädaabi",
        "btn_photo": "📷 Objekti foto",
        "btn_ai": "💬 Konsultatsioon",
        "btn_contact": "☎️ Kontakt",
        "btn_lang": "🌐 Keel",
        "btn_request": "Esita päring",
        "btn_back": "← Tagasi",
        "btn_menu": "🏠 Menüü",
        "btn_skip": "Jäta vahele",
        "btn_yes": "Jah",
        "btn_no": "Ei",

        "services_title": "Milline teenus teid huvitab?",
        "svc_inspect_title": "🔍 Kinnisvara ülevaatus",
        "svc_inspect_desc": "Kinnisvara seisukorra professionaalne hindamine enne ostu, üürile andmist või renoveerimist — kohapealne ülevaatus, tehniline aruanne ja selged soovitused.",
        "svc_plumb_title": "🚿 Santehnilised tööd",
        "svc_plumb_desc": "Igasuguse keerukusega santehnika paigaldus, vahetus ja remont — lekete kõrvaldamisest kuni täieliku torustiku paigalduseni. Tööde garantiiga.",
        "svc_bath_title": "🛁 Vannituba võtmed kätte",
        "svc_bath_desc": "Vannitoa täielik renoveerimine võtmed kätte: projekt, lammutus, santehnika, plaatimine ja valmis tulemuse üleandmine. Üks töövõtja — üks vastutaja.",
        "svc_heatpump_title": "♨️ Soojuspumbad",
        "svc_heatpump_desc": "Soojuspumpade valik, tarne ja paigaldus kütteks ja sooja vee tootmiseks — energiatõhusad lahendused koos tasuvusarvutusega.",

        "lead_objtype": "Objekti tüüp?",
        "obj_apartment": "Korter",
        "obj_house": "Maja",
        "obj_commercial": "Äripind",
        "lead_location": "Asukoht / aadress?",
        "lead_desc": "Lühidalt: mida on vaja teha?",
        "lead_photo": "Lisada foto? (valikuline)",
        "lead_contact": "Telefon või Telegram tagasihelistamiseks?",
        "lead_done": "✅ Päring vastu võetud — võtame peagi ühendust.",

        "emerg_desc": "🚨 Hädaolukord. Kirjeldage lühidalt probleemi.",
        "emerg_phone": "Telefoninumber kohe tagasihelistamiseks?",
        "emerg_done": "✅ Vastu võetud. Otsekontakt: {phone}",

        "photo_prompt": "Saatke objekti fotod.",
        "photo_more": "Foto saadud. Kas soovite esitada päringu?",

        "ai_prompt": "💬 Esitage küsimus renoveerimise, santehnika või soojuspumpade kohta.",
        "ai_error": "Vabandust, hetkel pole saadaval. Palun proovige hiljem.",
        "ai_off": "Konsultatsioon pole hetkel saadaval. Palun jätke päring.",

        "contact_title": "☎️ Kontakt",
        "contact_body": "Telegram: {manager}\nE-post: {email}\nTelefon: {phone}\nVeeb: {site}",
    },
}


def t(lang: str, key: str) -> str:
    """Текст по языку и ключу, с откатом на русский, затем на ключ."""
    return TEXTS.get(lang, TEXTS["ru"]).get(key) or TEXTS["ru"].get(key, key)


# Системный промпт для AI (рамки из карты диалогов)
AI_SYSTEM = {
    "de": "Du bist der Assistent von EUROBAUCONSULT, einem Premium-Unternehmen für Immobilienverwaltung und Sanierung (Markt: Deutschland/EU). Antworte kurz und fachkundig AUF DEUTSCH. Themen: Immobilien, Renovierung, Sanitär, Wärmepumpen, Objektverwaltung. Nenne KEINE konkreten Preise oder Termine — schlage stattdessen vor, eine Anfrage zu stellen. Bei Verträgen oder Zahlung verweise an den Kontakt.",
    "ru": "Ты ассистент EUROBAUCONSULT — премиальной компании по управлению недвижимостью и ремонту (рынок: Германия/ЕС). Отвечай кратко и экспертно НА РУССКОМ. Темы: недвижимость, ремонт, сантехника, тепловые насосы, управление объектами. НЕ называй конкретных цен и сроков — вместо этого предлагай оставить заявку. По договорам и оплате направляй к контактам.",
    "en": "You are the assistant of EUROBAUCONSULT, a premium property management and renovation company (market: Germany/EU). Answer briefly and expertly IN ENGLISH. Topics: real estate, renovation, plumbing, heat pumps, property management. Do NOT give specific prices or deadlines — suggest leaving a request instead. For contracts or payment, refer to the contacts.",
    "et": "Oled EUROBAUCONSULTi assistent — premium kinnisvarahaldus- ja renoveerimisettevõte (turg: Saksamaa/EL). Vasta lühidalt ja asjatundlikult EESTI KEELES. Teemad: kinnisvara, renoveerimine, santehnika, soojuspumbad, objektihaldus. ÄRA nimeta konkreetseid hindu ega tähtaegu — paku selle asemel päringu esitamist. Lepingute või maksete osas suuna kontaktide juurde.",
}
