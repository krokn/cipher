from fastapi import FastAPI
from fastapi_profiler import PyInstrumentProfilerMiddleware
from src.api.routers import all_routers

app = FastAPI(
    title="Шифр",
)

app.add_middleware(PyInstrumentProfilerMiddleware)


for router in all_routers:
    app.include_router(router)
