from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/{usernames}")
def read_users():
    return {"username": "your birthday is in 8 days"}

@app.get("/username/{birthdate}")
def tell_user(birthdate: int, q: Union[str, None] = None):
    return {"birthdate": birthdate, q: "q"}