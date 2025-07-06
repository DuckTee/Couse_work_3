from api import HHApi
from db import create_database
from db_manager import DBManager
from config import COMPANY_IDS, DB_PARAMS

def fill_database():
    """Заполняет БД данными о компаниях и вакансиях."""
    import psycopg2

    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    for hh_id in COMPANY_IDS:
        company = HHApi.get_company_info(hh_id)
        cur.execute("""
            INSERT INTO companies (hh_id, name, url)
            VALUES (%s, %s, %s)
            ON CONFLICT (hh_id) DO NOTHING;
        """, (company['id'], company['name'], company['alternate_url']))
        conn.commit()

        cur.execute("SELECT company_id FROM companies WHERE hh_id = %s;", (company['id'],))
        company_id = cur.fetchone()[0]

        vacancies = HHApi.get_vacancies(hh_id)
        for v in vacancies:
            salary_from = v['salary']['from'] if v['salary'] and v['salary']['from'] else None
            salary_to = v['salary']['to'] if v['salary'] and v['salary']['to'] else None
            cur.execute("""
                INSERT INTO vacancies (company_id, title, salary_from, salary_to, url, description)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, (
                company_id,
                v['name'],
                salary_from,
                salary_to,
                v['alternate_url'],
                v.get('snippet', {}).get('responsibility', '')
            ))
        conn.commit()
    cur.close()
    conn.close()

def print_menu():
    print("Меню:")
    print("1. Компании и количество вакансий")
    print("2. Все вакансии")
    print("3. Средняя зарплата")
    print("4. Вакансии с зарплатой выше средней")
    print("5. Вакансии по ключевому слову")
    print("0. Выход")

def main():
    create_database()
    print("База данных и таблицы созданы.")
    print("Заполнить базу данных? (y/n)")
    if input().lower() == 'y':
        fill_database()
        print("База данных заполнена.")

    db = DBManager()
    while True:
        print_menu()
        choice = input("Выберите действие: ")
        if choice == '1':
            for name, count in db.get_companies_and_vacancies_count():
                print(f"{name}: {count} вакансий")
        elif choice == '2':
            for c, t, f, to, url in db.get_all_vacancies():
                print(f"{c} | {t} | {f or '-'} - {to or '-'} | {url}")
        elif choice == '3':
            avg = db.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {int(avg)} руб.")
        elif choice == '4':
            for c, t, f, to, url in db.get_vacancies_with_higher_salary():
                print(f"{c} | {t} | {f or '-'} - {to or '-'} | {url}")
        elif choice == '5':
            kw = input("Введите ключевое слово: ")
            for c, t, f, to, url in db.get_vacancies_with_keyword(kw):
                print(f"{c} | {t} | {f or '-'} - {to or '-'} | {url}")
        elif choice == '0':
            db.close()
            print("Выход.")
            break
        else:
            print("Некорректный выбор!")

if __name__ == '__main__':
    main()
