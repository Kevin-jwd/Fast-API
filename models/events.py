# 이벤트 처리용 모델을 정의
from beanie import Document
from typing import Optional, List
from pydantic import BaseModel

# 이벤트 모델
class Event(Document):
    title: str          # 이벤트 타이틀
    image: str          # 이벤트 이미지 배너의 링크
    description: str    # 이벤트 설명
    tags: List[str]     # 그룹화를 위한 이벤트 태그
    location: str       # 이벤트 위치

    # Config 서브 클래스 : 문서화할 때 샘플 데이터를 보여주기 위한 용도
    # 샘플 데이터를 정의하고, API를 통해 신규 이벤트를 생성할 때 참고할 수 있다.
    class Config:
        json_schema_extra={
            "example":{
                "title":"FastAPI Book Launch",
                "image":"https://linktomyimage.com/image.png",
                "description":"We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags":["python","fastapi","book","launch"],
                "location":"Google Meet"
            }
        }

    class Settings:
        name="events"

# UPDATE 처리를 위한 pydantic 모델
class EventUpdate(BaseModel):
    title: Optional[str]          # 이벤트 타이틀
    image: Optional[str]          # 이벤트 이미지 배너의 링크
    description: Optional[str]    # 이벤트 설명
    tags: Optional[List[str]]     # 그룹화를 위한 이벤트 태그
    location: Optional[str]       # 이벤트 위치

    # Config 서브 클래스 : 문서화할 때 샘플 데이터를 보여주기 위한 용도
    # 샘플 데이터를 정의하고, API를 통해 신규 이벤트를 생성할 때 참고할 수 있다.
    class Config:
        json_schema_extra={
            "example":{
                "title":"FastAPI Book Launch",
                "image":"https://linktomyimage.com/image.png",
                "description":"We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags":["python","fastapi","book","launch"],
                "location":"Google Meet"
            }
        }