from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from service import books as book_service

router = APIRouter(prefix="/books", tags=["books"])

class BookRequest(BaseModel):
    title: str
    author: str

@router.post("/")
def register_book(book: BookRequest) -> bool:
    """도서를 등록합니다."""
    success = book_service.register_book(book.title, book.author)
    if not success:
        raise HTTPException(status_code=400, detail="도서 등록에 실패했습니다.")
    return success

@router.get("/")
def get_available_books() -> List[Dict[str, str]]:
    """대출 가능한 도서 목록을 조회합니다."""
    return book_service.get_available_books()

@router.delete("/{book_id}")
def delete_book(book_id: int) -> bool:
    """도서를 삭제합니다."""
    success = book_service.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=400, detail="도서 삭제에 실패했습니다.")
    return success 