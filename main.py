from fastapi import FastAPI
from routes.users import user_router
from routes.events import event_router
from database.connection import Settings
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 인스턴스 생성
app=FastAPI()
settings=Settings()

# 라우트 등록
app.include_router(user_router,prefix="/user")
app.include_router(event_router, prefix="/event")

# 출처 등록

origins=["*"]

# CORSMiddleware 클래스를 FastAPI에서 임포트한 다음 origins 배열을 등록하고 add_middleware()메서드를 사용해 미들웨어를 등록한다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def init_db():
    await settings.initialize_database()

# 8000번 포트에서 애플리케이션을 실행하도록 설정
if __name__=="__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000, reload=True)

