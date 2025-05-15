from typing import Annotated
from uuid import UUID
from fastapi import Depends
from internal.schema.recommendation import FetchRecommendedUsersResponse
from internal.service.database import AsyncSession, async_session


class RecommendationUsecase:
    def __init__(self, db: Annotated[AsyncSession, Depends(async_session)]):
        self.__db = db

    async def fetch_recommended_users(self,
                                      user_id: UUID, limit: int) -> FetchRecommendedUsersResponse:
        pass
