from fastapi import FastAPI

from app.database import init_db
from app.redis import queue
from app.routers import authentication, order, stats


app = FastAPI()

app.include_router(authentication.router)
app.include_router(order.router)
app.include_router(stats.router)


@app.on_event('startup')
async def on_startup():
    await init_db()


@app.get('/healthcheck')
async def ping():
    return {'status': 'OK!'}
