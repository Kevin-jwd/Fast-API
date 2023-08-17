# authenticate 의존 라이브러리가 포함되며 인증 및 권한을 위해 라우트에 주입

# Depends : oauth2_scheme을 의존 라이브러리 함수에 주입
# OAuth2PasswordBearer : 보안 로직이 존재한다는 것을 애플리케이션에 알려줌
# verify_access_token : 앞서 정의한 검증 함수로 토큰의 유효성을 확인
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import verify_access_token

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/user/signin")

async def authenticate(token: str= Depends(oauth2_scheme)) -> str:
    # 토큰이 유효하지 않다면 verify_access_token() 함수에 정의된 오류 메시지 반환
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sign in for access"
        )
    
    # 토큰이 유효하면 디코딩한 후 페이로드의 사용자 필드를 반환    
    decoded_token=verify_access_token(token)
    return decoded_token["user"]