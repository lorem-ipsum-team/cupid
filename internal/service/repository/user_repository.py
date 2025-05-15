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
        query = select(User, UserPreference, UserGeo)\
            .join(UserPreference, User.id == UserPreference.id, isouter=True)\
            .join(UserGeo, User.id == UserGeo.id, isouter=True)\
            .where(User.id == user_id)\
            .limit(1)

        result = await self.__db.execute(query)
        row = result.one_or_none()

        if row is None:
            return None, None, None

        return row

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
