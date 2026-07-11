from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from draft_model.selection import DraftModelSelector
from speculative_decoding import SpeculativeDecoding

app = FastAPI()

# Initialize models and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
draft_model = GPT2LMHeadModel.from_pretrained("gpt2")
target_model = GPT2LMHeadModel.from_pretrained("gpt2")

# Initialize draft model selector
draft_model_selector = DraftModelSelector(model=draft_model, device="cuda" if torch.cuda.is_available() else "cpu")

# Initialize speculative decoding
speculative_decoder = SpeculativeDecoding(
    draft_model_selector=draft_model_selector,
    target_model=target_model,
    tokenizer=tokenizer,
    device="cuda" if torch.cuda.is_available() else "cpu"
)

class DecodeRequest(BaseModel):
    input_text: str
    max_tokens: int = 50

@app.post("/speculative-decode")
def speculative_decode(request: DecodeRequest):
    """
    Endpoint to perform speculative decoding.

    Args:
        request (DecodeRequest): Input text and max tokens for decoding.

    Returns:
        dict: Decoded text and metadata.
    """
    try:
        result = speculative_decoder.decode(request.input_text, max_tokens=request.max_tokens)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))