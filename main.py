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


def view_tasks():
    tasks = load_tasks()
    if len(tasks) == 0:
        print("Список задач пуст.")
    else:
        for task in tasks:
            print(f"{task[0]}. {task[1]} — [{task[2]}]")


def add_task():
    title = input("Введите название задачи: ")
    priority = input("Введите приоритет (Низкий/Средний/Высокий): ")

    with psycopg2.connect(**CONNECT_DB) as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute('INSERT INTO tasks (title, priority) VALUES (%s, %s)', (title, priority))
                conn.commit()
                print("Задача добавлена.")
            except Exception as e:
                print(f"Ошибка добавления: {e}")


def delete_task():
    view_tasks()
    try:
        task_id = int(input("Введите ID задачи для удаления: "))
        try:
            with psycopg2.connect(**CONNECT_DB) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))

                    if cursor.rowcount > 0:
                        print("Задача удалена")
                    else:
                        print("Задача с таким ID не найдена")
                    conn.commit()
                    cursor.close()
        except Exception as e:
            print(f"Ошибка удаления: {e}")

    except ValueError:
        print("Введено некорректное значение")


def update_task():
    view_tasks()

    title = input("Введите название задачи: ")
    priority = input("Введите приоритет (Низкий/Средний/Высокий): ")

    try:
        task_id = int(input("Введите ID задачи для обновления: "))
        try:
            with psycopg2.connect(**CONNECT_DB) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('UPDATE tasks SET title = %s, priority = %s WHERE id = %s',
                                   (title, priority, task_id,))

                    if cursor.rowcount > 0:
                        print("Задача обновлена")
                    else:
                        print("Задача с таким ID не найдена")
                    conn.commit()
                    cursor.close()
        except Exception as e:
            print(f"Ошибка обновления: {e}")

    except ValueError:
        print("Введено некорректное значение")
