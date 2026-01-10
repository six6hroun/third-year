import sqlite3
def get_db():
    conn = sqlite3.connect('C:\\учеба\\Интерпретируемые языки программирования\\datebase\\dakotawar.db')
    conn.row_factory = sqlite3.Row
    return conn
