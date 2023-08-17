# JWT 문자열을 인코딩, 디코딩하는 함수

import time
from datetime import datetime

from fastapi import HTTPException, status
# JWT 를 인코딩, 디코딩하는 라이브러리
from jose import jwt, JWTError
from database.connection import Settings

settings=Settings()

# 토큰 생성용 함수
def create_access_token(user: str):
    # 문자열 하나를 받아서 payload 딕셔너리에 연결
    # payload 딕셔너리는 사용자명과 만료 시간을 포함하며 JWT가 디코딩될 때 반환됨.
    payload={
        "user":user,
        "expires":time.time() + 3600        # 생성시점에서 한 시간 후
    }

    # encode() 메서드는 세 개의 인수를 받으며 payload를 암호화한다.
    # 페이로드 : 값이 저장된 딕셔너리로, 인코딩할 대상
    # 키 : 페이;로드를 사인하기 위한 키
    # 알고리즘 : 페이로드를 사인 및 암호화하는 알고리즘, 기본값인 HS256 알고리즘을 가장 많이 사용
    token=jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

# 애플리케이션에 전달된 토큰을 검증하는 함수 (토큰을 문자열로 받는다.)
def verify_access_token(token:str):
    try:
        data=jwt.decode(token,settings.SECRET_KEY, algorithms=["HS256"])
        expire=data.get("expires")

        # 토큰의 만료 시간이 존재하는지 여부 확인 (없으면 유요한 토큰이 존재하지 않는다고 판단)
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied."
            )
        
        # 토큰이 유효한지 (만료 시간이 지나지 않았는지) 여부 확인
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired!"
            )
        return data
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token."
        )