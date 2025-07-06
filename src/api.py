import requests
from typing import List, Dict

class HHApi:
    """Класс для работы с API hh.ru"""

    BASE_URL = "https://api.hh.ru"

    @staticmethod
    def get_company_info(company_id: int) -> dict:
        """Получить информацию о компании по id."""
        resp = requests.get(f"{HHApi.BASE_URL}/employers/{company_id}")
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def get_vacancies(company_id: int) -> List[Dict]:
        """Получить список вакансий компании по id."""
        vacancies = []
        page = 0
        while True:
            params = {'employer_id': company_id, 'page': page, 'per_page': 50}
            resp = requests.get(f"{HHApi.BASE_URL}/vacancies", params=params)
            resp.raise_for_status()
            data = resp.json()
            vacancies.extend(data['items'])
            if page >= data['pages'] - 1:
                break
            page += 1
        return vacancies
