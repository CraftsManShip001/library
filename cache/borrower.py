import redis
from typing import List, Dict

redis_client = redis.Redis(host="localhost", port=6379, db=0)

def add_borrowed_book(borrower: str, title: str) -> bool:
    try:
        key = f"borrower:{borrower}:books"
        redis_client.sadd(key, title)
        return True
    except redis.ConnectionError:
        print("Redis connection error")
        return False
    except Exception as e:
        print(f"Redis error: {e}")
        return False

def get_borrower_books(borrower: str) -> List[str]:
    try:
        key = f"borrower:{borrower}:books"
        books = redis_client.smembers(key)
        return [book.decode('utf-8') for book in books]
    except Exception:
        return []

def remove_borrowed_book(borrower: str, title: str) -> bool:
    try:
        key = f"borrower:{borrower}:books"
        redis_client.srem(key, title)
        return True
    except Exception:
        return False

