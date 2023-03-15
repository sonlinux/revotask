from typing import Union

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    birthdate: str


class User(UserBase):
    id: int
    username: str
    birthdate: str

    class Config:
        orm_mode = True

