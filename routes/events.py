# 이벤트 처리용 모델을 정의

from fastapi import APIRouter, Body, HTTPException, status
from models.events import Event
from typing import List

event_router=APIRouter(
    tags=["Events"]
)

events=[]

# 모든 이벤트를 추출하는 라우트
@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events

# 특정 ID의 이벤트 추출하는 라우트
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id:int) -> Event:
    for event in events:
        if event.id==id:
            return event
        # 해당 ID의 이벤트가 없을 때
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist."
    )
    
# 이벤트 생성 라우트
@event_router.post("/new")
async def create_event(body:Event=Body(...)) -> dict:
    events.append(body)
    return{
        "message":"Event created successfully."
    }

# 데이터베이스에 있는 단일 이벤트 삭제
@event_router.delete("/{id}")
async def delete_event(id:int) -> dict:
    for event in events:
        if event.id==id:
            events.remove(event)
            return{
                "message":"Event deleted successfully."
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist."
    )

# 전체 이벤트 삭제
@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {
        "message":"Events deleted successfully."
    }
