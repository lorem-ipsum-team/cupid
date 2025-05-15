from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from internal.schema.recommendation import FetchRecommendedUsersRequest, FetchRecommendedUsersResponse
from internal.service.authentication.user import authorized_user_id
from internal.usecase.recommendation import RecommendationUsecase

router = APIRouter(tags=['recommendation'])


@router.get('/fetch', response_model=FetchRecommendedUsersResponse)
async def fetch_recommended_users(query: Annotated[FetchRecommendedUsersRequest,
                                                   Depends(FetchRecommendedUsersRequest)],
                                  user_id: Annotated[UUID, Depends(authorized_user_id)],
                                  usecase: Annotated[RecommendationUsecase,
                                                     Depends(RecommendationUsecase)]):
    return await usecase.fetch_recommended_users(user_id, query.limit)
