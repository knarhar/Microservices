from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    role: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str