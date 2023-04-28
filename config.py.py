import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS stock (
                name text,
                quantity integer,
                cost integer
                ) """)

    conn.commit()

    conn1 = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                password TEXT,
                role TEXT
                ) """)

    conn.commit()
