import psycopg2
from psycopg2.extras import execute_batch
from config import DB_CONFIG


def get_connection():
    """Возвращает подключение к PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)


def create_table():
    """Создает таблицу weather, если она не существует."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather (
                    city TEXT,
                    temperature FLOAT,
                    humidity FLOAT,
                    timestamp TIMESTAMP
                )
            """)
            conn.commit()


def save_to_db(df):
    """Пакетная вставка данных из DataFrame в PostgreSQL."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # Преобразуем DataFrame в список кортежей
            data = df[[
                "city",
                "temperature",
                "humidity",
                "timestamp"]].to_records(index=False).tolist()

            # Пакетная вставка
            execute_batch(
                cursor, """
                INSERT INTO weather (city, temperature, humidity, timestamp)
                VALUES (%s, %s, %s, %s)
                """,
                data,
                page_size=100  # Количество записей в одном пакете
            )
            conn.commit()


def test_connection():
    """Проверяет подключение к БД."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                print("Подключение к PostgreSQL успешно!")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
