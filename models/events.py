# 이벤트 처리용 모델을 정의
from sqlmodel import JSON, SQLModel, Field, Column
from typing import Optional,List

# 이벤트 모델 -> SQLModel의 테이블 클래스 사용
class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)             
    title: str          # 이벤트 타이틀
    image: str          # 이벤트 이미지 배너의 링크
    description: str    # 이벤트 설명
    tags: List[str] = Field(default=None, primary_key=True)           
    location: str       # 이벤트 위치

    # Config 서브 클래스 : 문서화할 때 샘플 데이터를 보여주기 위한 용도
    # 샘플 데이터를 정의하고, API를 통해 신규 이벤트를 생성할 때 참고할 수 있다.
    class Config:
        arbitary_types_allowed=True
        json_schema_extra={
            "example":{
                "title":"FastAPI Book Launch",
                "image":"https://linktomyimage.com/image.png",
                "description":"We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags":["python","fastapi","book","launch"],
                "location":"Google Meet"
            }
        }

# UPDATE 처리의 바디 유형으로 사용할 SQLModel 클래스
class EventUpdate(SQLModel):
    title:Optional[str]
    image:Optional[str]
    description:Optional[str]
    tags:Optional[str]
    location:Optional[str]

    class Config:
        json_schema_extra={
            "exmaple":{
                "title":"FastAPI Book Launch",
                "image":"https://linktomyimage.com/image.png",
                "description":"We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags":["python","fastapi","book","launch"],
                "locaiton":"Google Meet"
            }
        }
