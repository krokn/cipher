from fastapi import FastAPI
from src.api.routers import all_routers
import logging

app = FastAPI(
    title="Шифр",
)

for router in all_routers:
    app.include_router(router)
