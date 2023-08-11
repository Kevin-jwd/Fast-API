from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from typing import List
from database.connection import conn

from routes.users import user_router
from routes.events import event_router

import uvicorn

# 인스턴스 생성
app=FastAPI()

# 라우트 등록
app.include_router(user_router,prefix="/user")
app.include_router(event_router, prefix="/event")

# 시작 시 데이터베이스 생성
@app.on_event("startup")
def on_startup():
    conn()

# "/" 으로 접속한 경우 "event" 로 리다이렉트
@app.get("/")
async def home():
    return RedirectResponse(url="/event/")   # 상태 코드 307(리다이렉트) 반환

# 8000번 포트에서 애플리케이션을 실행하도록 설정
if __name__=="__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000, reload=True)

