import unittest
from unittest.mock import patch, MagicMock
import torch
from backend.draft_model.selection import DraftModelSelector

class TestDraftModelSelector(unittest.TestCase):

    @patch('backend.draft_model.selection.TensorRTOptimizer')
    def setUp(self, mock_trt_optimizer):
        self.mock_trt_optimizer = mock_trt_optimizer.return_value
        self.mock_trt_optimizer.build_engine.return_value = MagicMock()
        self.mock_trt_optimizer.infer.return_value = torch.tensor([[[0.1, 0.9]]])

        self.model = MagicMock()
        self.input_shape = (1, 10)
        self.selector = DraftModelSelector(self.model, self.input_shape, device='cpu')

    def test_select_next_token(self):
        input_ids = torch.tensor([[1, 2, 3]])
        result = self.selector.select_next_token(input_ids)

        self.assertEqual(result['next_token_id'], 1)
        self.assertAlmostEqual(result['next_token_prob'], 0.9)

if __name__ == '__main__':
    unittest.main()