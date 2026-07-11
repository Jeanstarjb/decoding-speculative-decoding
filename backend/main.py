from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
from inference_pipeline import app as inference_app
from monitoring import log_request, log_error
import time

app = FastAPI()

# Mount the inference pipeline as a sub-application
app.mount("/api", inference_app)

# Add Prometheus metrics endpoint
prometheus_app = make_asgi_app()
app.mount("/metrics", prometheus_app)

@app.middleware("http")
async def add_monitoring_middleware(request: Request, call_next):
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