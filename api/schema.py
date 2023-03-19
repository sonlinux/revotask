from datetime import date as date_type

from pydantic import BaseModel


class User(BaseModel):
    username: str
    birthdate: date_type

    class Config:
        orm_mode = True
