import psycopg2

CONNECT_DB = {
    'user': 'postgres',
    'password': 'admin',
    'database': 'task_manager_db',
    'host': 'localhost',
    'port': 5432, }


def init_database():
    with psycopg2.connect(**CONNECT_DB) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS tasks
                           (
                               id       SERIAL PRIMARY KEY,
                               title    TEXT NOT NULL,
                               priority TEXT NOT NULL
                           )
                           ''')
            conn.commit()
            cursor.close()


def load_tasks():
    with psycopg2.connect(**CONNECT_DB) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, title, priority FROM tasks')
            task_list = cursor.fetchall()
        return task_list

