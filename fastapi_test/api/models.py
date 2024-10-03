from pydantic import BaseModel


class Cat(BaseModel):
    id: int
    name: str
    color: str
    months: int
    breed: str
    description: str


class CreateCatBody(BaseModel):
    name: str
    color: str
    months: int
    breed: str
    description: str


class UpdateCatBody(BaseModel):
    name: str | None = None
    color: str | None = None
    months: int | None = None
    breed: str | None = None
    description: str | None = None
