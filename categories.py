import sqlite3

connection = sqlite3.connect('categories.db')


with open('categories.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute("INSERT INTO categories (name) VALUES (?)",
            ('Food',)
            )
connection.commit()
connection.close()
