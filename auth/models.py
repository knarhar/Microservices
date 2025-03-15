from sqlalchemy import Table, Column, Integer, String
from auth.database import metadata

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(30), unique=True, nullable=False),
    Column("hashed_password", String, nullable=False)
)
