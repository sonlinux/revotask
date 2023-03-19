from datetime import date as DateType

from fastapi import FastAPI, status, HTTPException, Depends
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


@app.post("/hello/{username}")
def create_user(
    username: str, birthdate: DateType, session: Session = Depends(get_session)
):
    validate_username = has_letters_only(username)
    validate_date = is_past_date(birthdate)

    if not (validate_username and validate_date):
        return {
            status.HTTP_400_BAD_REQUEST: "Username must contain letters only and Birthdate must be in the past."
        }

    user_obj = session.query(User).filter(User.username == username).first()
    if user_obj:
        return {
            user_obj.username: "Username already exists, make sure to pass a unique username ID"
        }
    else:
        new_user = User(username=username, birthdate=birthdate)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return status.HTTP_204_NO_CONTENT


@app.get("/hello/{username}", status_code=status.HTTP_200_OK)
def read_user(username: str, session: Session = Depends(get_session)):
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
def update_user(
    username: str, birthdate: DateType, session: Session = Depends(get_session)
):
    validate_date = is_past_date(birthdate)

    user_query = session.query(User).filter(User.username == username)
    user_obj = user_query.first()

    if not validate_date:
        return "Birthdate must be in the past."

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User item with username `{username}` not found",
        )

    else:
        payload = UserSchema(username=username, birthdate=birthdate)
        update_data = payload.dict(exclude_unset=True)
        user_query.update(update_data, synchronize_session=False)

        session.commit()
        session.refresh(user_obj)
        return user_obj
