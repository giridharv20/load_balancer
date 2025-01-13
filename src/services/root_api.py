import httpx

from fastapi import APIRouter, Request, HTTPException
from starlette.responses import JSONResponse

from src.container.container import container as ctx

router = APIRouter()

#  Middleware to intercept incoming requests
@router.api_route("/", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "TRACE"])
async def handle_all_methods(request: Request):
    service = request.url.path.split("/")[1]
    if service == "urls":
        return None

    # getting the next server by means of a round-robin iterator
    service_url = ctx.get("UrlService").get_service_url(service)
    if service_url:
        service_url += request.url.path
        if request.query_params:
            service_url += f"?{request.query_params}"
        try:
            response = await _route_request(service_url, request)
            return response
        except Exception as e:
            print(e)
    else:
        raise HTTPException(status_code=404, detail="Url not found or registered.")

# Route calls
async def _route_request(service_url, request):
    # to test in pytest use http server - call and response can be set
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=service_url,
            headers=request.headers.raw,
            content=await request.body()
        )

    return JSONResponse(
        content=response.json(),  # Convert response to JSON
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get("Content-Type", "application/json")
    )
