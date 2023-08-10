from fastapi import FastAPI
from routes.users import user_router

import uvicorn

# 인스턴스 생성
app=FastAPI()
# 라우트 등록
app.include_router(user_router,prefix="/user")

# 8000번 포트에서 애플리케이션을 실행하도록 설정
if __name__=="__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000, reload=True)

    