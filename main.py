from fastapi import FastAPI

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