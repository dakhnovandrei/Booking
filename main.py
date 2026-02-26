from fastapi import FastAPI
from authx import AuthXConfig, AuthX
from api.auth import router
from core.database import engine, Base

config = AuthXConfig()
config.JWT_SECRET_KEY = 'SECRET_KEY'
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=config)

app = FastAPI()

app.include_router(router, prefix='/api/auth')


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
