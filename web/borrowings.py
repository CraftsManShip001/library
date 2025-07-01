from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from service import borrowings as borrowing_service

router = APIRouter(prefix="/borrows", tags=["borrows"])

class BorrowRequest(BaseModel):
    borrower: str
    title: str

class BorrowerBooksResponse(BaseModel):
    borrower: str
    books: List[str]

class MonthlyBookResponse(BaseModel):
    borrower: str
    title: str
    author: str



@router.post("/")
def borrow_book(borrow: BorrowRequest) -> bool:
    """도서를 대출합니다."""
    success = borrowing_service.borrow_book(borrow.borrower, borrow.title)
    if not success:
        raise HTTPException(status_code=400, detail="도서 대출에 실패했습니다.")
    return success

@router.get("/month/{borrow_month}", response_model=List[MonthlyBookResponse])
def get_books_by_month(borrow_month: str):
    """특정 월에 대출된 도서 목록을 조회합니다."""
    return borrowing_service.get_books_by_month(borrow_month)

@router.get("/borrowers/{borrower}/books", response_model=BorrowerBooksResponse)
def get_borrower_books(borrower: str):
    """대출자의 대출한 도서 목록을 조회합니다."""
    return borrowing_service.get_borrower_books(borrower)

