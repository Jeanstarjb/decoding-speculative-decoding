from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from inference_pipeline import inference

app = FastAPI()

class InferenceRequest(BaseModel):
    input_text: str
    max_tokens: int = 50

@app.post("/inference")
async def perform_inference(request: InferenceRequest):
    """
    Endpoint to perform inference using the speculative decoding pipeline.

    Args:
        request (InferenceRequest): Input text and max tokens for decoding.

    Returns:
        dict: Decoded text and metadata.
    """
    try:
        result = inference(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))