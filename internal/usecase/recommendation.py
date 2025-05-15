import random
from typing import Annotated
from uuid import UUID
from fastapi import Depends, HTTPException, status
from scipy.spatial.distance import cosine
from internal.config.settings import settings
from internal.entity.userdata import User, UserDescription, UserPhoto, UserPreference
from internal.schema.recommendation import FetchRecommendedUsersResponse
from internal.service.repository.user_repository import UserRepository


class RecommendationUsecase:
    def __init__(self,
                 user_repo: Annotated[UserRepository, Depends(UserRepository)]):
        self.__user_repo = user_repo
        self.__fetch_factor = 5
        self.__radius = settings.ST_DWITHIN_KM * 1000

    async def fetch_recommended_users(self,
                                      user_id: UUID, limit: int) -> FetchRecommendedUsersResponse:
        user, prefs, geo = await self.__user_repo.get_user_data_by_id(user_id)

        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 'User not found')

        if geo is None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, 'Location data not available')

        nearby = await self.__user_repo.get_nearby_users(
            user, geo, limit * self.__fetch_factor, self.__radius)

        nearby = random.sample(nearby, min(limit, len(nearby)))

        if prefs is not None:
            nearby = self.__sort_by_cosine(nearby, prefs)

        return FetchRecommendedUsersResponse(users=list(map(lambda n: n[0].id, nearby)))

    def __sort_by_cosine(self,
                         users: list[tuple[User, UserPhoto, UserDescription]],
                         prefs: UserPreference):

        sorted_users = sorted(
            users,
            key=lambda u: cosine(u[1].photo, prefs.photo) +
            cosine(u[2].tags, prefs.tags),
        )

        return sorted_users
