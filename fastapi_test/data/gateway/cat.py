from typing import Sequence

from sqlalchemy import delete, insert, select, update

from ..models import Cat
from .base import BaseGateway


class CatGateway(BaseGateway):
    __slots__ = ()

    async def delete_cat(self, cat_id: int) -> int:
        result = await self.session.execute(delete(Cat).where(Cat.id == cat_id))
        return result.rowcount

    async def get_cats(self, breed: str | None = None) -> Sequence[Cat]:
        query = select(Cat).order_by(Cat.id)

        if breed:
            query = query.where(Cat.breed == breed)
        res = await self.session.scalars(query)
        return res.all()

    async def create_cat(self, name: str, color: str, age: int, breed: str) -> int:
        return await self.session.scalar(
            insert(Cat)
            .values(name=name, color=color, months=age, breed=breed)
            .returning(Cat.id)
        )

    async def update_cat(
        self,
        cat_id: int,
        **values,
    ) -> Cat | None:
        query = update(Cat).where(Cat.id == cat_id).values(**values).returning(Cat)
        res = await self.session.scalar(query)
        return res

    async def get_cat(self, cat_id: int) -> Cat:
        return await self.session.get(Cat, cat_id)

    async def get_breads(self) -> Sequence[str]:
        query = select(Cat.breed).distinct()
        res = await self.session.scalars(query)
        return res.all()
