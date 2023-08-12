# 데이터베이스 추상화와 설정에 사용되는 파일

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from pydantic import BaseSettings

from models.users import User
from models.events import Event

async def initialize_database(self):      # 데이터베이스 초기화
    client=AsyncIOMotorClient(self.DATABASE_URL)
    await init_beanie(database=client.get_default_database(),document_models=[Event,User])

class Config:
    env_file=".env"
