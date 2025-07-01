import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

def add_book(title: str, author: str) -> bool:
    try:
        conn = sqlite3.connect("./mydb.db")
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO books (title, author, available) VALUES (?, ?, 1)",
            (title, author)
        )
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def get_available_books() -> List[Dict[str, str]]:
    try:
        conn = sqlite3.connect("./mydb.db")
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT title, author FROM books WHERE available = 1"
        )
        
        books = []
        for row in cursor.fetchall():
            books.append({
                "title": row[0],
                "author": row[1]
            })
        
        conn.close()
        return books
    except Exception:
        return []

def delete_book(book_id: int) -> bool:
    try:
        conn = sqlite3.connect("./mydb.db")
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT available FROM books WHERE book_id = ?",
            (book_id,)
        )
        
        result = cursor.fetchone()
        if not result or result[0] != 1:
            conn.close()
            return False
        
        cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def borrow_book(borrower: str, title: str) -> bool:
    try:
        conn = sqlite3.connect("./mydb.db")
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT book_id FROM books WHERE title = ? AND available = 1",
            (title,)
        )
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            return False
        
        book_id = result[0]
        
        cursor.execute(
            "UPDATE books SET available = 0 WHERE book_id = ?",
            (book_id,)
        )
        
        cursor.execute(
            "INSERT INTO borrowings (book_id, borrower) VALUES (?, ?)",
            (book_id, borrower)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def get_books_by_month(borrow_month: str) -> List[Dict[str, str]]:
    try:
        conn = sqlite3.connect("./mydb.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.borrower, bk.title, bk.author 
            FROM borrowings b
            JOIN books bk ON b.book_id = bk.book_id
            WHERE strftime('%Y-%m', b.borrowed_at) = ?
        ''', (borrow_month,))
        
        books = []
        for row in cursor.fetchall():
            books.append({
                "borrower": row[0],
                "title": row[1],
                "author": row[2]
            })
        
        conn.close()
        return books
    except Exception:
        return []

def return_book(borrower: str, title: str) -> bool:
    try:
        conn = sqlite3.connect("./mydb.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.borrow_id, bk.book_id 
            FROM borrowings b
            JOIN books bk ON b.book_id = bk.book_id
            WHERE b.borrower = ? AND bk.title = ? AND b.returned_at IS NULL
        ''', (borrower, title))
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            return False
        
        borrowing_id, book_id = result
        return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute(
            "UPDATE borrowings SET returned_at = ? WHERE borrow_id = ?",
            (return_date, borrowing_id)
        )
        
        cursor.execute(
            "UPDATE books SET available = 1 WHERE book_id = ?",
            (book_id,)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False 