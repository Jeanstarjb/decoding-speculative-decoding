from typing import Any, Dict
import torch
import torch.nn as nn

class DraftModelSelector:
    def __init__(self, model: nn.Module, device: str = "cuda"):
        """
        Initializes the DraftModelSelector with the given model and device.

        Args:
            model (nn.Module): The lightweight draft model.
            device (str): The device to run the model on (e.g., "cuda" or "cpu").
        """
        self.model = model.to(device)
        self.device = device
        self.model.eval()

    def select_next_token(self, input_ids: torch.Tensor, **kwargs) -> Dict[str, Any]:
        """
        Selects the next token using the draft model.

        Args:
            input_ids (torch.Tensor): The input token IDs.

        Returns:
            Dict[str, Any]: The next token and additional metadata.
        """
        with torch.no_grad():
            input_ids = input_ids.to(self.device)
            logits = self.model(input_ids, **kwargs).logits

            # Apply softmax to get probabilities
            probabilities = torch.softmax(logits[:, -1, :], dim=-1)

            # Select the token with the highest probability
            next_token_id = torch.argmax(probabilities, dim=-1).item()
            next_token_prob = probabilities[0, next_token_id].item()

        return {
            "next_token_id": next_token_id,
            "next_token_prob": next_token_prob,
            "probabilities": probabilities.cpu().tolist(),
        }

# Example usage (for testing purposes)
if __name__ == "__main__":
    from transformers import GPT2LMHeadModel, GPT2Tokenizer

    # Load a small, lightweight GPT-2 model for demonstration purposes
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    # Initialize the DraftModelSelector
    selector = DraftModelSelector(model=model, device="cpu")

    # Prepare input
    input_text = "The quick brown fox"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    # Select the next token
    result = selector.select_next_token(input_ids)
    print("Next Token ID:", result["next_token_id"])
    print("Next Token Probability:", result["next_token_prob"])
    print("Probabilities:", result["probabilities"])