from uuid import UUID
from fastapi import Query
from pydantic import BaseModel, Field


class FetchRecommendedUsersRequest(BaseModel):
    limit: int = Field(gt=0, lt=101)

    def __call__(self, limit: int = Query(...)):
        return FetchRecommendedUsersRequest(limit=limit)


class FetchRecommendedUsersResponse(BaseModel):
    users: list[UUID]
