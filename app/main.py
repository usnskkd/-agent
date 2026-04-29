from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import api_router, page_router
from app.core.scheduler import scheduler_service
from app.db.base import SessionLocal, init_db
from app.services.automation_service import automation_service


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    scheduler_service.start()
    db = SessionLocal()
    try:
        automation_service.sync_jobs(db)
    finally:
        db.close()
    yield
    scheduler_service.shutdown()


app = FastAPI(
    title="Multi-Agent Operations Automation",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(page_router)
app.include_router(api_router, prefix="/api")
