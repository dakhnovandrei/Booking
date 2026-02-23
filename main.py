from fastapi import FastAPI
from authx import AuthXConfig, AuthX



config = AuthXConfig()
config.JWT_SECRET_KEY = 'SECRET_KEY'
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=config)


app = FastAPI()


@app.on_event('startup')
async def on_startup():
    db = SessionLocal()
    try:
        pass
    except Exception as e:
        print(f'ERROR {e}')
    finally:
        db.close()