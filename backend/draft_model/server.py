from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from .selection import DraftModelSelector

app = FastAPI()

# Initialize the draft model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
draft_model_selector = DraftModelSelector(model=model, device="cuda" if torch.cuda.is_available() else "cpu")

class DraftRequest(BaseModel):
    input_text: str

@app.post("/draft")
def generate_draft(request: DraftRequest):
    """
    Endpoint to generate the next token using the draft model.

    Args:
        request (DraftRequest): The input text for the draft model.

    Returns:
        dict: The next token and its probability.
    """
    try:
        input_ids = tokenizer(request.input_text, return_tensors="pt").input_ids
        result = draft_model_selector.select_next_token(input_ids)
        next_token = tokenizer.decode([result["next_token_id"]])

        return {
            "input_text": request.input_text,
            "next_token": next_token,
            "next_token_prob": result["next_token_prob"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))