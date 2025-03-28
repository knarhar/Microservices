from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth_router
from database import engine, metadata
from starlette.middleware.sessions import SessionMiddleware

from dotenv import dotenv_values

env = dotenv_values(".env")

# Create tables
metadata.drop_all(engine)  # Удалит таблицы
metadata.create_all(engine)

app = FastAPI(title="Auth API")

origins = [
    "http://localhost:63342",  # Allow your frontend origin
    "http://localhost:3000",   # If you have another frontend (e.g., React, Vue, etc.)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows the specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.add_middleware(
    SessionMiddleware,
    secret_key=env["SECRET_KEY"],
    session_cookie="session_cookie",
    max_age=3600,  # 1 hour
    same_site="Lax",
    https_only=True  # In production
)
# Include authentication routes
app.include_router(auth_router, prefix="/auth")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
