import sqlite3
import logging


DATABASE_FILE = 'books.db'

def create_table():
    """Create the 'books' table if it doesn't exist"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS books
                     (title text, author text, year text, last_page integer)''')
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Error creating 'books' table: {e}")
    finally:
        conn.close()

def load_data():
    """Load all books from the 'books' table"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute('''SELECT * FROM books''')
        data = c.fetchall()
        return [{'title': row[0], 'author': row[1], 'year': row[2],'last_page': row[3]} for row in data]
    except sqlite3.Error as e:
        logging.error(f"Error loading data from 'books' table: {e}")
    finally:
        conn.close()

def add_book(title, author, year, last_page=0):
    """Add a book to the 'books' table"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO books (title,author,year,last_page) VALUES (?, ?, ?, ?)", (title, author, year, last_page))
        conn.commit()
        return True
    except sqlite3.Error as e:
        logging.error(f"Error adding book: {e}")
        return False
    finally:
        conn.close()


def update_books(title, author, year,last_page):
    """Update the information of a book with the given title in the 'books' table"""
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("UPDATE books SET author=?, year=?, last_page=? WHERE title=?", (author, year,last_page, title))
    conn.commit()
    conn.close()


def delete_book(title):
    """Delete a book from the 'books' table"""
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE title=?", (title,))
    conn.commit()
    conn.close()