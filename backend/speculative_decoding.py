import torch
from typing import Dict, Any

class SpeculativeDecoding:
    def __init__(self, draft_model_selector, target_model, tokenizer, device="cuda"):
        """
        Initializes the SpeculativeDecoding class with draft and target models.

        Args:
            draft_model_selector: Instance of DraftModelSelector for speculative token generation.
            target_model: The large target LLM for verification.
            tokenizer: Tokenizer used by both models.
            device: Device to run the models on (e.g., "cuda" or "cpu").
        """
        self.draft_model_selector = draft_model_selector
        self.target_model = target_model.to(device)
        self.tokenizer = tokenizer
        self.device = device
        self.target_model.eval()

    def decode(self, input_text: str, max_tokens: int = 50) -> Dict[str, Any]:
        """
        Performs speculative decoding using the draft model and verifies with the target model.

        Args:
            input_text: The starting text for decoding.
            max_tokens: Maximum number of tokens to generate.

        Returns:
            Dict[str, Any]: The final decoded text and metadata.
        """
        input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids.to(self.device)
        generated_ids = input_ids.clone()

        for _ in range(max_tokens):
            # Step 1: Generate speculative tokens using the draft model
            draft_result = self.draft_model_selector.select_next_token(input_ids)
            speculative_token_id = draft_result["next_token_id"]
            speculative_token_prob = draft_result["next_token_prob"]

            # Step 2: Verify speculative token using the target model
            with torch.no_grad():
                logits = self.target_model(generated_ids).logits
                target_probabilities = torch.softmax(logits[:, -1, :], dim=-1)
                target_token_prob = target_probabilities[0, speculative_token_id].item()

            # Step 3: Decide whether to accept the speculative token
            if target_token_prob >= speculative_token_prob:
                # Accept the speculative token
                input_ids = torch.cat([input_ids, torch.tensor([[speculative_token_id]], device=self.device)], dim=1)
                generated_ids = torch.cat([generated_ids, torch.tensor([[speculative_token_id]], device=self.device)], dim=1)
            else:
                # Generate token directly using the target model
                target_token_id = torch.argmax(target_probabilities, dim=-1).item()
                input_ids = torch.cat([input_ids, torch.tensor([[target_token_id]], device=self.device)], dim=1)
                generated_ids = torch.cat([generated_ids, torch.tensor([[target_token_id]], device=self.device)], dim=1)

            # Stop if the model generates an end-of-sequence token
            if speculative_token_id == self.tokenizer.eos_token_id:
                break

        decoded_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        return {"decoded_text": decoded_text}

# Example usage (for testing purposes)
if __name__ == "__main__":
    from transformers import GPT2LMHeadModel, GPT2Tokenizer
    from draft_model.selection import DraftModelSelector

    # Load models and tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    draft_model = GPT2LMHeadModel.from_pretrained("gpt2")
    target_model = GPT2LMHeadModel.from_pretrained("gpt2")

    # Initialize draft model selector
    draft_model_selector = DraftModelSelector(model=draft_model, device="cpu")

    # Initialize speculative decoding
    speculative_decoder = SpeculativeDecoding(
        draft_model_selector=draft_model_selector,
        target_model=target_model,
        tokenizer=tokenizer,
        device="cpu"
    )

    # Perform speculative decoding
    input_text = "The future of AI is"
    result = speculative_decoder.decode(input_text, max_tokens=20)
    print("Decoded Text:", result["decoded_text"])