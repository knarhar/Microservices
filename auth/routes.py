import uuid

from fastapi import APIRouter, HTTPException, Request
from authlib.integrations.starlette_client import OAuth
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from dotenv import dotenv_values
from sqlalchemy.orm import Session

from google.oauth2 import id_token
from google.auth.transport import requests

from database import engine
from models import users, refresh_tokens
from schemas import UserCreate, UserLogin
from utils import hash_password, verify_password, create_access_token, create_refresh_token

auth_router = APIRouter()


@auth_router.post("/register")
async def register(user: UserCreate):
    hashed_password = hash_password(user.password)
    new_user = users.insert().values(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role if user.role else "customer"
    )

    with Session(engine) as session:
        try:
            session.execute(new_user)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    return {"message": "User registered successfully"}


@auth_router.post("/login")
async def login(user: UserLogin):
    query = select(users).where(users.c.username == user.username)

    with engine.connect() as connection:
        result = connection.execute(query).fetchone()

        if not result or not verify_password(user.password, result.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        access_token = create_access_token({"sub": user.username})
        refresh_token = create_refresh_token(
            username=user.username)

        return {"access_token": access_token, "refresh_token": refresh_token}


# TODO: Create logout route, by blacklisting refresh token
@auth_router.post("/refresh")
async def refresh_token(old_token: str):
    query = select(refresh_tokens).where(refresh_tokens.c.token == old_token)

    with engine.connect() as connection:
        result = connection.execute(query).fetchone()
        if not result:
            raise HTTPException(status_code=400, detail="Invalid refresh token")

        new_access_token = create_access_token({"sub": result.user_id})
        return {"access_token": new_access_token}


env = dotenv_values()
oauth = OAuth()
oauth.register(
    name="google",
    client_id=env["GOOGLE_CLIENT_ID"],
    client_secret=env["GOOGLE_CLIENT_SECRET"],
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    token_url=env["GOOGLE_TOKEN_URL"],  # Hardcoded from JSON
    redirect_url="http://localhost:8001/auth/google/callback/",
    client_kwargs={"scope": "openid profile email"},
)


@auth_router.post("/google")
async def auth_google(request: Request):
    data = await request.json()
    token = data.get("id_token")
    if not token:
        raise HTTPException(status_code=400, detail="Token is missing.")

    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), env["GOOGLE_CLIENT_ID"])
        email = id_info.get("email")

        if not email:
            raise HTTPException(status_code=400, detail="Email не найден в токене")

        with Session(engine) as session:
            query = select(users).where(users.c.email == email)
            result = session.execute(query).fetchone()

            if not result:
                new_user = users.insert().values(
                    email=email,
                    username=email.split("@")[0],
                    hashed_password=None
                )
                try:
                    session.execute(new_user)
                    session.commit()
                except IntegrityError as e:
                    session.rollback()
                    raise HTTPException(status_code=400, detail=str(e))

        access_token = create_access_token({"sub": email.split("@")[0]})
        refresh_token = create_refresh_token(username=email.split("@")[0])

        return {"message": "Authenticated successfully.", "access_token": access_token, "refresh_token": refresh_token}
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный токен")


@auth_router.get("/google/callback")
async def auth_callback(request: Request):
    query_state = request.query_params.get("state")
    session_state = request.session.get("oauth_state")  # Don't pop, just compare
    if not session_state or query_state != session_state:
        raise HTTPException(status_code=400, detail="State mismatch: Possible CSRF attempt")

    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token exchange failed: {str(e)}")

    user_info = await oauth.google.parse_id_token(request, token)
    email = user_info.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Google account has no email")

    return {"email": email, "token": token}
