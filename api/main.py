from fastapi import FastAPI, status, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from .models import User
from .schema import User as UserSchema
from .database import Base, engine, get_session
from .utils import days_left, has_letters_only, is_past_date


Base.metadata.create_all(engine)

app = FastAPI(
    title="RevoTask",
    description="An API to tell the user how many days to their birthday.",
)


@app.get("/", include_in_schema=False)
async def docs_route():
    return RedirectResponse(url="/redoc")


@app.post("/hello", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserSchema, session: Session = Depends(get_session)):
    validate_username = has_letters_only(payload.username)
    validate_date = is_past_date(payload.birthdate)

    if not (validate_username and validate_date):
        return "Username must contain letters only and Birthday must be in the past."

    user_obj = session.query(User).filter(User.username == payload.username).first()
    if user_obj:
        return {
            user_obj.username: "Username already exists, make sure to pass a unique username ID"
        }
    else:
        new_user = User(**payload.dict())
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return {"status": "success", "user": new_user}


@app.get("/hello/{username}")
def get_user(username: str, session: Session = Depends(get_session)):
    user_obj = session.query(User).filter(User.username == username).first()

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail=f"204 No Content"
        )

    days_to_birthday = days_left(user_obj.birthdate)

    if days_to_birthday > 0:
        return (
            f"Hello, {user_obj.username}! Your birthday is in {days_to_birthday} day(s)"
        )
    else:
        return f"Hello, {user_obj.username}! Happy birthday!"


@app.patch("/hello/{username}")
def update_user(payload: UserSchema, session: Session = Depends(get_session)):
    validate_username = has_letters_only(payload.username)
    validate_date = is_past_date(payload.birthdate)

    user_query = session.query(User).filter(User.username == payload.username)
    user_obj = user_query.first()

    if not (validate_username and validate_date):
        return "Username must contain letters only and Birthday must be in the past."

    if not user_obj:
        raise HTTPException(
            status_code=404,
            detail=f"user item with username {payload.username} not found",
        )

    else:
        update_data = payload.dict(exclude_unset=True)
        user_query.filter(User.username == payload.username).update(
            update_data, synchronize_session=False
        )

        session.commit()
        session.refresh(user_obj)
        return {"status": "success", "user": user_obj}
