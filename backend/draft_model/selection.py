from typing import Any, Dict
import torch
import torch.nn as nn
from tensorrt_optimization import TensorRTOptimizer

class DraftModelSelector:
    def __init__(self, model: nn.Module, input_shape: tuple, device: str = "cuda"):
        """
        Initializes the DraftModelSelector with the given model and device.

        Args:
            model (nn.Module): The lightweight draft model.
            input_shape (tuple): The input shape for the model.
            device (str): The device to run the model on (e.g., "cuda" or "cpu").
        """
        self.device = device
        self.trt_optimizer = TensorRTOptimizer(model, input_shape)
        self.engine = self.trt_optimizer.build_engine()

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
            logits = self.trt_optimizer.infer(input_ids).cpu()

            # Apply softmax to get probabilities
            probabilities = torch.softmax(logits[:, -1, :], dim=-1)

            # Select the token with the highest probability
            next_token_id = torch.argmax(probabilities, dim=-1).item()
            next_token_prob = probabilities[0, next_token_id].item()

        return {
            "next_token_id": next_token_id,
            "next_token_prob": next_token_prob,
            "probabilities": probabilities.tolist(),
        }