from fastapi import FastAPI
from data import get_db
from web import books as book_web
from web import borrowings as borrow_web
from web import return_api as return_web

app = FastAPI(title="도서 대출 관리 시스템", version="1.0.0")

get_db()

app.include_router(book_web.router)
app.include_router(borrow_web.router)
app.include_router(return_web.router)

@app.get("/")
def read_root():
    return {"message": "도서 대출 관리 시스템 API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
