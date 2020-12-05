import sqlite3

connection = sqlite3.connect('accounts.db')


with open('accounts.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute("INSERT INTO accounts (username, password) VALUES (?, ?)",
            ('Admin', 'e3afed0047b08059d0fada10f400c1e5')
            )
connection.commit()
connection.close()
