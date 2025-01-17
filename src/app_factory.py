from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from src.services.url_service.url_service_api import router as url_service_router
from src.services.root_api import router as root_router


def create_app():
    app = FastAPI()
    app.include_router(url_service_router)
    app.include_router(root_router, prefix="")

    # look to adding a router for "/<any_param>" so that exclusion logic is moved out
    @app.middleware("http")
    async def intercept_all_calls(request: Request, call_next):
        try:
            response = await root_router.routes[0].endpoint(request)
            if response is None:
                response = await call_next(request)

        except HTTPException as http_ex:
            return JSONResponse(
                content={"detail": http_ex.detail},
                status_code=http_ex.status_code
            )
        except Exception as ex:
            return JSONResponse(
                content={"detail": str(ex)},
                status_code=500
            )

        return response

    return app
