from fastapi import FastAPI
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
from inference_api import app as inference_api_app
from monitoring import log_request, log_error
import time

app = FastAPI()

# Mount the inference API as a sub-application
app.mount("/api", inference_api_app)

# Add Prometheus metrics endpoint
prometheus_app = make_asgi_app()
app.mount("/metrics", prometheus_app)

@app.middleware("http")
async def add_monitoring_middleware(request, call_next):
    start_time = time.time()
    endpoint = request.url.path
    try:
        response = await call_next(request)
        status = 'success' if response.status_code == 200 else 'failure'
        log_request(endpoint, status, start_time)
        return response
    except Exception as e:
        log_error(endpoint, str(e))
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})