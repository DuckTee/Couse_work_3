import psycopg2
from typing import List, Tuple, Optional
from config import DB_PARAMS

class DBManager:
    """Класс для работы с базой данных вакансий и компаний."""

    def __init__(self, db_params: dict = DB_PARAMS):
        """Инициализация подключения к БД."""
        self.conn = psycopg2.connect(**db_params)

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Список всех компаний и количество вакансий у каждой."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, COUNT(v.vacancy_id)
                FROM companies c
                LEFT JOIN vacancies v ON c.company_id = v.company_id
                GROUP BY c.name
                ORDER BY c.name;
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """Список всех вакансий с названием компании, вакансии, зарплатой и ссылкой."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.company_id
                ORDER BY c.name;
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """Средняя зарплата по всем вакансиям (по salary_from и salary_to)."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2.0)
                FROM vacancies
                WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL;
            """)
            result = cur.fetchone()
            return result[0] if result else 0

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """Вакансии с зарплатой выше средней."""
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.company_id
                WHERE ((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2.0) > %s
                ORDER BY ((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2.0) DESC;
            """, (avg_salary,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """Вакансии, в названии которых есть ключевое слово."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.company_id
                WHERE LOWER(v.title) LIKE %s
                ORDER BY c.name;
            """, (f'%{keyword.lower()}%',))
            return cur.fetchall()

    def close(self):
        """Закрыть соединение с БД."""
        self.conn.close()
