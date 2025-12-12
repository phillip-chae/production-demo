from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from ingestapi.container import Container
from ingestapi.service.ingest import IngestService
from .. import version

tag = "ingest"
prefix = f"/api/{version}/ingest"
router = APIRouter(prefix=prefix, tags=[tag])

@router.post(
    "", 
    name="Ingest Data", 
    summary="Ingest data for processing"
)
@inject
async def create_ingest(
    file: UploadFile = File(..., description="Image to be ingested for image search"),
    # injected dependencies
    ingest_service: IngestService = Provide[Container.ingest_service]
):
    try:
        file_bytes = await file.read()
        res = await ingest_service.create_ingest(
            file_bytes,
            file_name=file.filename if file.filename else "unknown"
        )
        return JSONResponse(content={"task_id": res})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        await file.close()
    
@router.get(
    "/{task_id}", 
    name="Get Ingest Status", 
    summary="Get the status of an ingest task"
)
@inject
async def get_ingest(
    task_id: str, 
    ingest_service: IngestService = Provide[Container.ingest_service]
):
    try:
        res = await ingest_service.read_ingest(task_id)
        if res is None:
            raise HTTPException(status_code=404, detail="ingest task not found")
        return JSONResponse(content=res)
    
    except HTTPException as he:
        raise he
    except Exception:
        raise HTTPException(status_code=500, detail="internal Server Error")