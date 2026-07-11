import unittest
from unittest.mock import patch, MagicMock
from backend.speculative_decoding import SpeculativeDecoding

class TestSpeculativeDecoding(unittest.TestCase):

    @patch('backend.speculative_decoding.RedisCache')
    def setUp(self, mock_redis_cache):
        self.mock_redis_cache = mock_redis_cache.return_value
        self.mock_redis_cache.get.return_value = None
        self.mock_redis_cache.set = MagicMock()

        self.draft_model_selector = MagicMock()
        self.target_model = MagicMock()
        self.tokenizer = MagicMock()
        self.tokenizer.return_tensors = 'pt'
        self.tokenizer.eos_token_id = 50256
        self.tokenizer.decode = lambda ids, skip_special_tokens: ' '.join(map(str, ids))

        self.decoder = SpeculativeDecoding(
            draft_model_selector=self.draft_model_selector,
            target_model=self.target_model,
            tokenizer=self.tokenizer,
            device='cpu',
            redis_host='localhost'
        )

    def test_decode(self):
        self.draft_model_selector.select_next_token.return_value = {
            'next_token_id': 42,
            'next_token_prob': 0.8
        }

        self.target_model.return_value.logits = torch.tensor([[[0.1, 0.9]]])
        self.tokenizer.return_tensors = lambda text: {'input_ids': [1, 2, 3]}

        result = self.decoder.decode('test input', max_tokens=3)
        self.assertIn('decoded_text', result)
        self.assertTrue(len(result['decoded_text']) > 0)

if __name__ == '__main__':
    unittest.main()