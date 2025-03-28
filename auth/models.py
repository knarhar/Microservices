from sqlalchemy import Table, Column, Integer, String
from database import metadata

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(30), unique=True, nullable=False),
    Column("hashed_password", String),
    Column("email", String, nullable=False),
    Column("role", String, nullable=False, default="customer"),
    extend_existing=True,
)

refresh_tokens = Table(
    "refresh_tokens",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", String),
    Column("token", String, unique=True),
    Column("expires_at", String),
    extend_existing=True,
)
