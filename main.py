from fastapi import FastAPI
import logging

from .db import Base, engine
from .routers import addresses

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API")

app.include_router(addresses.router)