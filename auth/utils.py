from passlib.context import CryptContext
from datetime import datetime, timedelta
import uuid
from jose import jwt
from config import SECRET_KEY, ALGORITHM
from models import refresh_tokens
from database import engine

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(username: str) -> str:
    expires = datetime.utcnow() + timedelta(days=7)
    data = {"sub": username, "exp": expires}
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    query = refresh_tokens.insert().values(user_id=username, token=token, expires_at=expires.isoformat())
    with engine.connect() as connection:
        connection.execute(query)
        connection.commit()
    return token
