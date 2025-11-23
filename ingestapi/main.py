from fastapi import FastAPI, HTTPException, Request

from ingestapi.config import service_name
from ingestapi.container import Container
from ingestapi.api.router import router
app = FastAPI(
    title= "Ingest API",
    description="API for ingesting data for processing",
    version="1.0.0",
)
container = Container()
container.wire(packages=[
    "ingestapi.api",
])
app.container = container # type: ignore

app.include_router(router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Guards internal exceptions from leaking implementation details
    if exc.status_code >= 500:
        return HTTPException(status_code=500, detail="Internal Server Error")
    return exc

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)