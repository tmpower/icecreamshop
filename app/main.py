from fastapi import FastAPI, Depends

from app.database import init_db
from app.routers import authentication


app = FastAPI()
app.include_router(authentication.router)


@app.on_event('startup')
async def on_startup():
    await init_db()


@app.get('/ping')
async def ping():
    return {'ping': 'pong'}


@app.get('/protected')
async def protected_endpoint(
    current_user: dict = Depends(authentication.get_current_user),
):
    return {'message': 'This is a protected endpoint', 'user': current_user}
