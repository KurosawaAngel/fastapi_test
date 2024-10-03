from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from fastapi_test.api.depends import get_cat_gateway
from fastapi_test.data.gateway.cat import CatGateway

from .models import Cat, CreateCatBody, UpdateCatBody

router = APIRouter()


@router.get("/cat", status_code=status.HTTP_200_OK)
async def get_cats(
    gateway: Annotated[CatGateway, Depends(get_cat_gateway)], breed: str | None = None
) -> list[Cat]:
    return await gateway.get_cats(breed)


@router.delete(
    "/cat/{cat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": None}},
)
async def delete_cat(
    cat_id: int,
    gateway: Annotated[CatGateway, Depends(get_cat_gateway)],
):
    result = await gateway.delete_cat(cat_id)
    await gateway.commit()

    if result < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/cat", status_code=status.HTTP_201_CREATED)
async def create_cat(
    cat: CreateCatBody,
    gateway: Annotated[CatGateway, Depends(get_cat_gateway)],
) -> int:
    id = await gateway.create_cat(
        name=cat.name, color=cat.color, age=cat.months, breed=cat.breed
    )
    await gateway.commit()
    return id


@router.patch(
    "/cat/{cat_id}",
    status_code=status.HTTP_200_OK,
    responses={404: {"model": None}},
)
async def patch_cat(
    cat_id: int,
    cat: UpdateCatBody,
    gateway: Annotated[CatGateway, Depends(get_cat_gateway)],
) -> Cat:
    res = await gateway.update_cat(cat_id=cat_id, **cat.model_dump(exclude_none=True))
    await gateway.commit()

    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.get(
    "/cat/{cat_id}", status_code=status.HTTP_200_OK, responses={404: {"model": None}}
)
async def get_cat(
    cat_id: int, gateway: Annotated[CatGateway, Depends(get_cat_gateway)]
) -> Cat:
    res = await gateway.get_cat(cat_id)
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return res


@router.get("/breads", status_code=status.HTTP_200_OK)
async def get_breads(
    gateway: Annotated[CatGateway, Depends(get_cat_gateway)],
) -> list[str]:
    return await gateway.get_breads()
