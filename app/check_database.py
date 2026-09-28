import sqlite3


connection = sqlite3.connect("movies.db")

cursor = connection.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

tables = cursor.fetchall()

print("Tablas de la base de datos:")

for table in tables:
    print(f"- {table[0]}")

connection.close()