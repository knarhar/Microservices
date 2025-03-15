from fastapi import FastAPI
from auth.routes import auth_router
from auth.database import engine, metadata

# Create tables
metadata.create_all(engine)

app = FastAPI(title="Auth API")

# Include authentication routes
app.include_router(auth_router, prefix="/auth")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
