from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from searchapi.container import Container
from searchapi.service.image import ImageService
from .. import version

tag = "image"
prefix = f"/api/{version}/{tag}"
router = APIRouter(prefix=prefix, tags=[tag])

@router.get(
    "/search", 
    name="Search Image", 
    summary="Search for similar images"
)
@inject
async def get_search(
    text: str = Query(..., description="Text to be used for image search"),
    # injected dependencies
    svc: ImageService = Provide[Container.svc]
):
    try:
        return await svc.create_search(text)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))