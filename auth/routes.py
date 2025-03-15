from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from auth.database import engine
from auth.models import users
from auth.schemas import UserCreate, UserLogin
from auth.utils import hash_password, verify_password, create_access_token

auth_router = APIRouter()


@auth_router.post("/register")
async def register(user: UserCreate):
    hashed_password = hash_password(user.password)
    query = users.insert().values(username=user.username, hashed_password=hashed_password)

    try:
        with engine.connect() as connection:
            connection.execute(query)
            connection.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")

    return {"message": "User registered successfully"}


@auth_router.post("/login")
async def login(user: UserLogin):
    query = select(users).where(users.c.username == user.username)

    with engine.connect() as connection:
        result = connection.execute(query).fetchone()

        if not result or not verify_password(user.password, result.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        access_token = create_access_token({"sub": user.username})
        refresh_token = create_access_token(
            {"sub": user.username})  # Refresh tokens should ideally have a different expiry

        return {"access_token": access_token, "refresh_token": refresh_token}
