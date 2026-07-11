from fastapi import FastAPI
from inference_pipeline import app as inference_app

app = FastAPI()

# Mount the inference pipeline as a sub-application
app.mount("/api", inference_app)