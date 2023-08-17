# 사용자 처리용 모델을 정의

from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn
from database.connection import Database
from auth.hash_password import HashPassword

user_router=APIRouter(
    tags=["User"]
)

user_database=Database(User)
hash_password=HashPassword()

# 등록 라우트
# 애플리케이션에 내장된 데이터베이스 사용
@user_router.post("/signup")
# 사용자 모델 (User)을 함수에 전달해 email 필드를 추출
# User 클래스가 의존 라이브러리, 이를 sign_user_up()함수에 주입
async def sign_new_user(user:User)->dict:
    user_exist=await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists."
        )
    # 패스워드를 해싱해서 데이터베이스에 저장
    hashed_password=hash_password.create_hash(user.password)
    user.password=hashed_password
    await user_database.save(user)
    return{
        "message":"User successfully registered!"
    }

# 로그인 라우트
@user_router.post("/signin")
async def sign_user_in(user:UserSignIn)->dict:
    user_exist=await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist."
        )
    
    if user_exist.password == user.password:
        return {
            "message" : "User signed in successfully."
        }
    # 로그인 성공
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalied details passed."
    )