from typing import List, Dict
from data import books as book_data

def register_book(title: str, author: str) -> bool:
    """도서를 등록합니다."""
    return book_data.add_book(title, author)

def get_available_books() -> List[Dict[str, str]]:
    """대출 가능한 도서 목록을 조회합니다."""
    return book_data.get_available_books()

def delete_book(book_id: int) -> bool:
    """도서를 삭제합니다."""
    return book_data.delete_book(book_id) 