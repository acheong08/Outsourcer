import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute("INSERT INTO accounts (username, password) VALUES (?, ?)",
            ('Admin', '38a7744f5523335db845ff1976bf4747')
            )
cur.execute("INSERT INTO items (name, details, contact, price, pic) VALUES (?, ?, ?, ?, ?)",
            ('Avocado', 'A very tasty fruit', 'iloveavocado@avocado.com', 2.12, 'avocado.png')
            )
connection.commit()
connection.close()
