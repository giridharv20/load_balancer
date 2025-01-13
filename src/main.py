import uvicorn
import threading

from src.services.health_check.health_checker import HealthCheck

from src.container_factory import create_container

from src.app_factory import create_app

container = create_container()
app = create_app()
health_check = HealthCheck(container)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host='0.0.0.0', port=8080, reload=True)


@app.on_event("startup")
async def startup_event():
    threading.Thread(target=health_check.run_health_check, daemon=True).start()
