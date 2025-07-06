import psycopg2
from config import DB_PARAMS

def create_database():
    """Создаёт базу данных и таблицы."""
    conn = psycopg2.connect(dbname='postgres', user=DB_PARAMS['user'],
                            password=DB_PARAMS['password'], host=DB_PARAMS['host'])
    conn.autocommit = True
    cur = conn.cursor()
    # Создать БД, если не существует
    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_PARAMS['dbname']}';")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {DB_PARAMS['dbname']};")
    cur.close()
    conn.close()

    # Создать таблицы
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            company_id SERIAL PRIMARY KEY,
            hh_id INTEGER UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            url TEXT
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES companies(company_id),
            title VARCHAR(255) NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            url TEXT,
            description TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
