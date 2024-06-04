from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from .database import create_database_client
from .routers import health_router, prediction_router, price_router, production_router
from ..models.model_registry import download_model_registry
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from .helpers.cron_log_predictions import save_daliy_predictions

app = FastAPI()
client = create_database_client()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(prediction_router)
app.include_router(price_router)
app.include_router(production_router)

jobstores = {
    'default': MemoryJobStore()
}
scheduler = AsyncIOScheduler(jobstores=jobstores, timezone="UTC")


@scheduler.scheduled_job('cron', day_of_week='mon-sun', hour=13, minute=0, second=0)
def scheduled_job_1():
    save_daliy_predictions(client)


# download model registry
@app.on_event("startup")
async def startup_event():
    download_model_registry()
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
