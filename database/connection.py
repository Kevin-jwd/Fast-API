# 데이터베이스 추상화와 설정에 사용되는 파일

from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any, List, Optional
from pydantic import BaseSettings, BaseModel

from models.users import User
from models.events import Event

# async def initialize_database(self):      # 데이터베이스 초기화
#     client=AsyncIOMotorClient(self.DATABASE_URL)
#     await init_beanie(database=client.get_default_database(),document_models=[Event,User])

class Settings(BaseSettings):
    DATABASE_URL:Optional[str]=None

    async def initialize_database(self):
        client=AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(), document_models=[Event,User])

    class Config:
        env_file=".env"
        
class Database:
    def __init__(self,model):
        self.model=model

    # 생성 처리 : 레코드 하나를 데이터베이스 컬렉션에 추가
    async def save(self,document) -> None:
        await document.create()
        return
    
    # 조회 처리 : 데이터베이스 컬렉션에서 단일 레코드를 불러오거나 전체 레코드를 불러오는 메서드
    # ID를 인수로 받아 일치하는 레코드를 불러온다.
    async def get(self, id:PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False
    
    # 인수가 없으며 모든 레코드를 불러온다.
    async def get_all(self) -> List[Any]:
        docs=await self.model.find_all().to_list()
        return docs
    
    # 변경 처리 : 기존 레코드를 변경하는 메서드
    async def update(self, id:PydanticObjectId, body: BaseModel) -> Any:
        doc_id=id
        des_body=body.dict()
        des_body={k:v for k,v in des_body.items() if v is not None}
        update_query={"$set":{
            field: value for field, value in des_body.items()
        }}

        doc=await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc
    
    # 삭제 처리 : 데이터베이스에서 레코드를 삭제하는 메서드
    async def delete(self, id:PydanticObjectId) -> bool:
        doc=await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True
    