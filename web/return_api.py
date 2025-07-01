from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service import borrowings as borrowing_service

router = APIRouter(prefix="/return", tags=["return"])

class ReturnRequest(BaseModel):
    borrower: str
    title: str

@router.post("/")
def return_book(return_req: ReturnRequest) -> bool:
    """도서를 반납합니다."""
    success = borrowing_service.return_book(return_req.borrower, return_req.title)
    if not success:
        raise HTTPException(status_code=400, detail="도서 반납에 실패했습니다.")
    return success 