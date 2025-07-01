from typing import List, Dict, Any
from data import books as book_data
from cache import borrower as borrower_cache

def borrow_book(borrower: str, title: str) -> bool:
    """도서를 대출합니다."""
    # 데이터베이스에서 대출 처리
    if book_data.borrow_book(borrower, title):
        # Redis에 대출자 정보 저장
        borrower_cache.add_borrowed_book(borrower, title)
        return True
    return False

def get_books_by_month(borrow_month: str) -> List[Dict[str, str]]:
    """특정 월에 대출된 도서 목록을 조회합니다."""
    return book_data.get_books_by_month(borrow_month)

def get_borrower_books(borrower: str) -> Dict[str, Any]:
    """대출자의 대출한 도서 목록을 조회합니다."""
    books = borrower_cache.get_borrower_books(borrower)
    return {
        "borrower": borrower,
        "books": books
    }

def return_book(borrower: str, title: str) -> bool:
    """도서를 반납합니다."""
    # 데이터베이스에서 반납 처리
    if book_data.return_book(borrower, title):
        # Redis에서 대출자 정보 삭제
        borrower_cache.remove_borrowed_book(borrower, title)
        return True
    return False