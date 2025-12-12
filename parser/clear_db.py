import psycopg2
from config import DATABASE_CONFIG

def clear_database():
    """
    Очищает все таблицы в базе данных, описанные в main_parser.py.
    Использует TRUNCATE ... CASCADE для очистки связанных данных.
    """
    
    # Список таблиц для очистки
    # Порядок не важен при использовании CASCADE, но для наглядности перечислены все
    tables = [
        "film_watch_provider",
        "film_still",
        "similar_film",
        "film_stuff",
        "film_country",
        "film_genre",
        "media",
        "stuff",
        "film",
        "genre",
        "country"
    ]
    
    connection = None
    try:
        # Подключение к БД
        print("🔌 Подключение к базе данных...")
        connection = psycopg2.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()
        
        print("🧹 Начало очистки таблиц...")
        
        # Формируем список таблиц через запятую
        tables_string = ", ".join(tables)
        
        # Выполняем TRUNCATE для всех таблиц сразу с опцией CASCADE
        # CASCADE удалит данные из зависимых таблиц, если они есть (хотя мы и так перечислили все)
        # и сбросит счетчики identity (RESTART IDENTITY)
        query = f"TRUNCATE TABLE {tables_string} RESTART IDENTITY CASCADE;"
        
        cursor.execute(query)
        connection.commit()
        
        print(f"✅ Успешно очищены таблицы: {tables_string}")
        
    except Exception as e:
        print(f"❌ Ошибка при очистке базы данных: {e}")
        if connection:
            connection.rollback()
            
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("🔌 Соединение с базой данных закрыто")

if __name__ == "__main__":
    confirm = input("⚠️  Вы уверены, что хотите удалить ВСЕ данные из таблиц парсера? (y/n): ")
    if confirm.lower() == 'y':
        clear_database()
    else:
        print("❌ Операция отменена")
