import asyncio                 # 활성 루프 세션을 만들어서 테스트가 단일 스레드로 실행되도록 한다.
import httpx                   # HTTP CRUD 처리를 실행하기 위한 비동기 클라이언트 역할
import pytest                  # pytest 라이브러리는 픽스처 정의를 위해 사용

from main import app
from database.connection import Settings
from models.events import Event
from models.users import User

# 루프 세션 픽스처 정의
@pytest.fixture(scope="session")
def event_loop():
    loop=asyncio.get_event_loop()
    yield loop
    loop.close()