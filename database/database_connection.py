import psycopg2

from data import DATABASE_URL


def connect_to_database():
    """
    Connects to the database and returns the connection object.
    """
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Успешное подключение к базе данных")
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при подключении к базе данных:", error)
