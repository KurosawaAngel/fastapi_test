from typing import Annotated, AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_test.data.gateway.cat import CatGateway


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    engine = request.app.state.engine
    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        yield session


async def get_cat_gateway(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CatGateway:
    return CatGateway(session)
