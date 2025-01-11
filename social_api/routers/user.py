import logging
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from social_api.models.user import UserIn
from social_api.security import (
    get_user,
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_subject_for_token_type,
    create_confirmation_token,
)
from social_api.database import database, user_table
from social_api import tasks

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserIn, background_tasks: BackgroundTasks, request: Request
):
    existing_user = await get_user(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email is already exists",
        )
    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(email=user.email, password=hashed_password)
    logger.debug(query)
    await database.execute(query)

    logger.debug("Submitting background task to send email")
    background_tasks.add_task(
        tasks.send_user_registration_email,
        user.email,
        confirmation_url=request.url_for(
            "confirm_email", token=create_confirmation_token(user.email)
        ),
    )
    return {"detail": "User created successfully. Please confirm your email."}


# @router.post("/token", status_code=status.HTTP_201_CREATED)
# async def login(user: UserIn):
#     user = await authenticate_user(user.email, user.password)
#     access_token = create_access_token(user.email)
#     return {"access_token": access_token, "token_type": "bearer"}


# (Optional) OAuth Password Bearer and Swagger Auth
@router.post("/token", status_code=status.HTTP_201_CREATED)
async def login(from_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(from_data.username, from_data.password)
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/confirm/{token}")
async def confirm_email(token: str):
    email = get_subject_for_token_type(token, "confirmation")
    query = (
        user_table.select().where(user_table.c.email == email).values(is_confirmed=True)
    )
    logger.debug(query)
    await database.execute(query)
    return {"detail": "Email confirmed"}
