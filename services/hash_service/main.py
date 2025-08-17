from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio

from app.api import hash_routes 
from app.worker.hash_generator import HashGenerator


worker = HashGenerator()


@asynccontextmanager
async def lifespan(app: FastAPI):
    worker_task = asyncio.create_task(worker.add_hashes_to_pool())
    try:
        yield
    finally:
        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            pass

app = FastAPI(lifespan=lifespan)



origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(hash_routes.router, prefix='/posts', tags=['Posts'])