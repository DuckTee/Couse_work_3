from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

DB_PARAMS = {
    'dbname': os.getenv('DB_NAME', 'hh_vacancies'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'Urepim65'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

COMPANY_IDS = [
    1740,    # Яндекс
    3529,    # Сбер
    78638,   # VK
    2180,    # Ozon
    3776,    # Тинькофф
    1122462, # Wildberries
    80,      # Альфа-Банк
    39305,   # Лаборатория Касперского
    3127,    # МТС
    907345   # Авито
]
