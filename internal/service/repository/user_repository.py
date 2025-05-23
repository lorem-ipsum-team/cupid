from typing import Annotated, Tuple
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select
from geoalchemy2.functions import ST_DWithin
from internal.entity.userdata import User, UserDescription, UserGeo, UserPhoto, UserPreference
from internal.service.database import AsyncSession, async_session


class UserRepository:
    def __init__(self, db: Annotated[AsyncSession, Depends(async_session)]):
        self.__db = db

    async def get_user_data_by_id(self,
                                  user_id: UUID) -> Tuple[User, UserPreference, UserGeo]:
        user_query = select(User)\
            .where(User.id == user_id)\
            .limit(1)

        pref_query = select(UserPreference)\
            .where(UserPreference.id == user_id)\
            .limit(1)

        geo_query = select(UserGeo)\
            .where(UserGeo.id == user_id)\
            .limit(1)

        user = await self.__db.scalars(user_query)
        pref = await self.__db.scalars(pref_query)
        geo = await self.__db.scalars(geo_query)

        return user.one_or_none(), pref.one_or_none(), geo.one_or_none()

    async def get_nearby_users(self, user: User, geo: UserGeo, limit: int, radius: float):
        query = select(User, UserPhoto, UserDescription)\
            .join(UserPhoto, User.id == UserPhoto.id)\
            .join(UserDescription, User.id == UserDescription.id)\
            .join(UserGeo, User.id == UserGeo.id)\
            .where(ST_DWithin(
                UserGeo.location,
                geo.location,
                radius
            ))\
            .where(User.gender != user.gender)\
            .order_by(UserGeo.geo_updated.desc())\
            .limit(limit)

        result = await self.__db.execute(query)
        rows = result.all()
        return rows
