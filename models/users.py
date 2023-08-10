# 사용자 등록 및 로그인 처리를 위한 라우팅

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event

# 사용자 모델 정의
class User(BaseModel): 
    email: EmailStr                        #  사용자 이메일
    password: str                          # 사용자 패스워드
    events: Optional[List[Event]]=None     # 해당 사용자가 생성한 이벤트. 처음에는 비어있다.

    # 샘플 데이터
    class Config:
        json_schema_extra={
            "example":{
                "email":"fastapi@packt.com",
                "username":"strong!!!",
                "events":[],
            }
        }

class UserSignIn(BaseModel):
    email:EmailStr
    password:str

    class Config:
        json_schema_extra={
            "example":{
                "email":"fastapi@packt.com",
                "password":"storng!!!",
                "events":[]
            }
        }