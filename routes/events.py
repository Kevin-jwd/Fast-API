# 이벤트 처리용 모델을 정의

from fastapi import APIRouter, Body, HTTPException, status
from models.events import Event, EventUpdate
from typing import List
from beanie import PydanticObjectId
from database.connection import Database

event_router=APIRouter(
    tags=["Events"]
)
event_database=Database(Event)

events=[]

# 모든 이벤트를 추출하는 라우트
@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events=await event_database.get_all()
    print("GET호출되었습니다.")
    return events

# 특정 ID의 이벤트 추출하는 라우트
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id:PydanticObjectId) -> Event:
    event=await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist."
        )
    return event

# 이벤트 생성 라우트
@event_router.post("/new")
async def create_event(body:Event) -> dict:
    await event_database.save(body)
    return{
        "message":"Event created successfully."
    }

# UPDATE 라우트
@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body:EventUpdate) -> Event:
    print("PUT 호출되었습니다.")
    updated_event=await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist."
        )

    return updated_event


# 데이터베이스에 있는 단일 이벤트 삭제
@event_router.delete("/{id}")
async def delete_event(id:PydanticObjectId) -> dict:
    event=await event_database.delete(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist."
        )
    return {
        "message" : "Event deleted successfully."
    }

# 전체 이벤트 삭제
@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {
        "message":"Events deleted successfully."
    }
