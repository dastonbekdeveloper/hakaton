import sqlite3

def init_db():
    with sqlite3.connect('users.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                phone TEXT
            )
        ''')

def add_user(user_id, username, first_name,phone ):
    if bool(get_user(user_id)):
        pass
    else:
        with sqlite3.connect('users.db') as conn:
            conn.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, phone)
                VALUES (?, ?, ?,?)
            ''', (user_id, username, first_name,phone))
def get_user(user_id):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()
init_db()