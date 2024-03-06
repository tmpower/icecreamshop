import logging
from fastapi import FastAPI, Depends

from app.database import init_db
from app.redis import queue
from app.routers import authentication, order
from app.services.authentication import get_current_user


app = FastAPI()
app.include_router(authentication.router)
app.include_router(order.router)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.on_event('startup')
async def on_startup():
    await init_db()


@app.get('/ping')
async def ping():
    return {'ping': 'pong'}


@app.get('/protected')
async def protected_endpoint(
    current_user: dict = Depends(get_current_user),
):
    logger.info(f'accessed protected endpoint: {current_user}')
    return {'message': 'This is a protected endpoint', 'user': current_user}
