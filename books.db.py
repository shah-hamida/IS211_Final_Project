import sqlite3
conn = sqlite3.connect("books.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    isbn TEXT,
    title TEXT,
    author TEXT,
    pages INTEGER,
    rating REAL
)
""")

conn.commit()
conn.close()
