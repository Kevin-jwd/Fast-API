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

async def init_db():
    test_settings=Settings()
    test_settings.DATABASE_URL="mongodb://localhost:27017/testdb"

    await test_settings.initialize_database()

@pytest.fixture(scope="session")
async def default_client():
    await init_db()
    async with httpx.AsyncClient(app=app, base_url="http://app") as client:
        yield client
        # 리소스 정리 -> 테스트 세션이 끝나면 데이터베이스가 비어 있도록
        await Event.find_all().delete()
        await User.find_all().delete()