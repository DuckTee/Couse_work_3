# Проект: Анализ вакансий с hh.ru и работа с PostgreSQL

## Описание
Учебный проект для сбора данных о компаниях и вакансиях с сайта через публичный API, их сохранения в базу данных PostgreSQL и анализа с помощью SQL-запросов.
В проекте реализованы:
- Получение информации о 10 компаниях и их вакансиях с hh.ru
- Загрузка данных в PostgreSQL (автоматическое создание БД и таблиц)
- Класс DBManager для работы с вакансиями и компаниями
- Удобный консольный интерфейс для пользователя

## Описание модулей проекта
### 1. `api.py`
Назначение: обеспечивает взаимодействие с публичным API hh.ru.

Задачи:
- Получение информации о работодателе по его ID.
- Получение списка вакансий конкретной компании.


Основные классы и функции:

- class HHApi — статический класс с методами:
- get_company_info(company_id: int) -> dict — возвращает данные о компании.
- get_vacancies(company_id: int) -> List[Dict] — возвращает список вакансий компании, реализует постраничную загрузку.

Использование:

Этот модуль служит источником данных для дальнейшей загрузки в базу данных.
Обеспечивает надежное получение данных о компаниях и вакансиях.

### 2. `config.py`
Назначение: 

Хранит конфигурационные параметры проекта:

- параметры подключения к базе данных (DB_PARAMS)
- список ID компаний (COMPANY_IDS), выбранных для анализа

Особенности:
- Использует python-dotenv для загрузки переменных окружения.
- Позволяет легко менять параметры без изменения кода.

### 3. `db.py`
Назначение:

Обеспечивает создание базы данных и таблиц, если они еще не существуют.

Задачи:

- Создать базу данных PostgreSQL (если не создана).
- Создать таблицы companies и vacancies с необходимыми связями и ограничениями.

Основные функции:

create_database() — создает базу данных и таблицы.

Особенности:
- Использует psycopg2 для подключения и выполнения SQL-запросов.
- Обеспечивает автоматическую подготовку структуры базы данных перед загрузкой данных.

### 4. `db_manager.py`
Назначение:

Класс DBManager — основной интерфейс для работы с данными в базе данных.

Задачи:

- Получение списка компаний и количества вакансий.
- Получение всех вакансий с деталями.
- Расчет средней зарплаты.
- Получение вакансий с зарплатой выше средней.
- Поиск вакансий по ключевому слову.

Методы:

- get_companies_and_vacancies_count()
- get_all_vacancies()
- get_avg_salary()
- get_vacancies_with_higher_salary()
- get_vacancies_with_keyword(keyword: str)

Особенности:

Использует SQL-запросы с JOIN, AVG, LIKE.
Обеспечивает закрытие соединения при необходимости.

### 5. `main.py`
Назначение:

Точка входа и пользовательский интерфейс.

Задачи:

- Создать базу и таблицы (при необходимости).
- Предложить пользователю выбрать действие через меню.
- Взаимодействовать с DBManager для получения и отображения данных.
- Обеспечить удобную человекочитаемую выдачу информации.

Особенности:

- Реализует цикл меню.
- Позволяет запускать различные аналитические запросы.
- Обеспечивает интерактивность и удобство использования.