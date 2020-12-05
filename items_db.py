import sqlite3

connection = sqlite3.connect('items.db')


with open('items.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute("INSERT INTO items (name, details, contact, category, price, pic) VALUES (?, ?, ?, ?, ?, ?)",
            ('Avocado', 'A very tasty fruit', 'iloveavocado@avocado.com', 'Food', 2.12, 'avocado.png')
            )
connection.commit()
connection.close()
