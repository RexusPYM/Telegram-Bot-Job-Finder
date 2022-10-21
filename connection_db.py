import sqlite3

db = sqlite3.connect('job_finder.db', check_same_thread=False)
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT NOT NULL,
    search_size INT NOT NULL
    )""")
db.commit()


def add_info_search_size_test(user_id: int, search_size: int):
    sql.execute(
        f"""SELECT id,
        IIF(EXISTS(id),
            UPDATE users SET search_size = '{search_size}' WHERE id = '{user_id}',
            INSERT INTO users(id, search_size) VALUES ('{user_id}', '{search_size}'))
        FROM users WHERE users.id = '{user_id}'; """)

    # sql.execute(
    #     f"""SELECT
    #         IIF(EXISTS(SELECT id FROM users WHERE users.id = '{user_id}'),
    #             UPDATE users SET search_size = '{search_size}' WHERE id = '{user_id}',
    #             INSERT INTO users(id, search_size) VALUES ('{user_id}', '{search_size}'))""")


def add_search_size(user_id: int, search_size: int):
    sql.execute(f"INSERT INTO users(id, search_size) VALUES ('{user_id}', '{search_size}')")
    db.commit()


def update_search_size(user_id: int, search_size: int):
    sql.execute(f"UPDATE users SET search_size = '{search_size}' WHERE id = '{user_id}'")
    db.commit()


def get_info_search_size(user_id: int):
    sql.execute(f"SELECT search_size FROM users WHERE users.id = '{user_id}'")
    return sql.fetchone()[0]


def check_user(user_id: int) -> bool:
    sql.execute(f"SELECT id FROM users WHERE users.id = '{user_id}'")
    if sql.fetchone():
        return True
    else:
        return False
