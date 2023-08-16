# 패스워드를 암호화하는 함수를 포함
# 이 함수는 계정을 등록할 때 또는 로그인 시 패스워드를 비교할 때 사용된다.

# bcrypt를 사용해 문자열을 해싱할 수 있도록 CryptContext를 임포트한다.
from passlib.context import CryptContext

# 코드는 pwd_context 변수에 저장되며 이 변수를 사용해 해싱에 필요한 함수들을 호출한다.
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashPassword:
    # 문자열을 해싱한 값을 반환
    def create_hash(self,password: str):
        return pwd_context.hash(password)
    # 일반 텍스트 패스워드와 해싱한 패스워드를 인수로 받아 두 값이 일치하는지 비교
    # 일치 여부에 따라 boolean 값을 반환
    def verify_hash(self, plain_password:str, hashed_password:str):
        return pwd_context.verify(plain_password, hashed_password)