import os

import nltk
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
CATALOG_ID = os.getenv("CATALOG_ID")

NARRATION_COST_PER_THOUSAND = 1.32
NARRATION_PRICE_URL = 'https://cloud.yandex.ru/docs/speechkit/pricing#prices'


# Глобальные константы
RUSSIAN_WORDS_REGEX = "^[а-яА-ЯёЁ0-9]+$"
IGNORED_WORDS = ['sil']
CHANNELS = 1
SAMPLE_WIDTH = 2
FRAME_RATE = 16000

# Загрузка пакетов nltk
nltk.download('punkt')

REPLACEMENTS = {
    'Балун': 'Б+аллоун',
    'Лукаш': 'Л+укаш',
    'Палив': 'П+алив',
    'Водичк': 'В+одичк',
    'Марек': 'М+арек',
    'Горжин': 'Горж+ин',
    'Клаген': 'Кл+аген',
    'Головатенко': 'Голов+атенко',
    'Ванек': 'В+анек',
    'Голечек': 'Г+олечек',
    'Водичка': 'В+одичка',
    'Польда': 'П+ольда',
    'Подскали': 'П+одскали',
    'Водражка': 'В+одражка',
    'Вышеград': 'В+ышеград',
    'Барушко': 'Барушк+о',
    'Крамарж': 'Кр+амарж',
    'Кралуп': 'Кр+алуп',
    'Жижков': 'Ж+ижков',
    'Крамарж': 'Кр+амарж',
    'Розделов': 'Розд+елов',
    'Витуничи': 'Вит+уничи',
    'Яношек': '+Яношек',
    'Вомач': 'В+омач'
}
