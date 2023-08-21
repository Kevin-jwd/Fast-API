import httpx
import pytest

from auth.jwt_handler import create_access_token
from models.events import Event

@pytest.fixture(scope="module")
async def access_token() -> str:
    return create_access_token("testuser@packt.com")

# 이벤트를 데이터베이스에 추가하는 픽스처
# CRUD 라우트 테스트에 대한 사전 테스트를 진행하는 데 사용
@pytest.fixture(scope="module")
async def mock_event() -> Event:
    new_event=Event(
        creator="testuser@packt.com",
        title="FastAPI Book Launch",
        image="https://linktomyimage.com/image.png",
        description="We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
        tags=["python","fastapi","book","launch"],
        location="Google Meet"
    )

    await Event.insert_one(new_event)

    yield new_event

# 조회 라우트 테스트
# /event(이벤트 라우트)의 GET 메서드 테스트 함수를 작성
# 이벤트가 데이터베이스에 추가되는지 테스트
@pytest.mark.asyncio
async def test_get_events(default_client:httpx.AsyncClient, mock_event: Event) -> None:
    response = await default_client.get("/event/")

    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)

# /event/{id} 라우트 테스트 함수
# 단일 이벤트 추출 라우트를 테스트
@pytest.mark.asyncio
async def test_get_event(default_client:httpx.AsyncClient, mock_event: Event) -> None:
    url=f"/event/{str(mock_event.id)}"
    response = await default_client.get(url)

    assert response.status_code == 200
    assert response.json()["creator"] == mock_event.creator
    assert response.json()["_id"] == str(mock_event.id)

# 생성 라우트 테스트
# 앞서 만든 픽스처를 사용해 접속 토큰을 추출하고 테스트 함수 정의
# 이 함수는 서버로 전송될 요청 페이로드를 생성
# 요청 페이로드에는 콘텐츠 유형과 인증 헤더가 포함
@pytest.mark.asyncio
async def test_post_event(default_client: httpx.AsyncClient, access_token: str) -> None:
    payload ={
        "title" : "FastAPI Book Launch",
        "image" : "http://linktomyimage.com/image.png",
        "description" : "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
        "tags" : ["python", "fastapi" ,"book", "launch"],
        "location"  : "Google Meet"
    }
    headers = {
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {access_token}"
    }
    test_response={
        "message" : "Event created successfully."
    }
    response = await default_client.post("/event/new", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response

# 데이터베이스에 저장된 이벤트 개수 (2개) 를 확인
@pytest.mark.asyncio 
async def test_get_events_count(default_client: httpx.AsyncClient) -> None:
    response = await default_client.get("/event/")

    events=response.json()

    assert response.status_code == 200
    assert len(events) == 2

# 변경 라우트 테스트
# mock_event 픽스처에서 추출한 ID를 사용해 데이터베이스에 저장된 해당 이벤트를 수정
# 그 다음 요청 페이로드와 헤더를 정의하고 response 변수에 요청 결과를 저장
@pytest.mark.asyncio
async def test_update_event(default_client: httpx.AsyncClient, mock_event: Event, access_token: str) -> None:
    test_payload={
        "title" : "Updated FastAPI event"
    }
    headers={
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {access_token}"
    }
    url=f"/event/{str(mock_event.id)}"

    response = await default_client.put(url, json=test_payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == test_payload["title"]
    # assert response.json()["title"] == "This test should fail"