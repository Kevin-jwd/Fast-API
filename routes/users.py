# 사용자 처리용 모델을 정의

from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn

user_router=APIRouter(
    tags=["User"]
)

users={}

# 등록 라우트
# 애플리케이션에 내장된 데이터베이스 사용
@user_router.post("/signup")
async def sign_new_user(data:User)->dict:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists."
        )
    users[data.email]=data
    return{
        "message":"User successfully registered!"
    }

# 로그인 라우트
@user_router.post("/signin")
async def sign_user_in(user:UserSignIn)->dict:
    # 아이디가 데이터베이스에 없을 때
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist."
        )
    # 비밀번호가 일치하지 않을 때
    if users[user.email].password!=user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed."
        )
    # 로그인 성공
    return{
        "message":"User signed in successfully."
    }