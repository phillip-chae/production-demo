from fastapi import APIRouter

from .routes import ingest

router = APIRouter()
router.include_router(ingest.router)