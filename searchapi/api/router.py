from fastapi import APIRouter

from .v1.routes.image import router as image_router

router = APIRouter()
router.include_router(image_router)