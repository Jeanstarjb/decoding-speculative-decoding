import unittest
from unittest.mock import patch, MagicMock
from backend.inference_pipeline import inference
from backend.inference_api import InferenceRequest

class TestIntegrationPipeline(unittest.TestCase):

    @patch('backend.inference_pipeline.SpeculativeDecoding')
    def test_inference_pipeline(self, mock_speculative_decoding):
        mock_decoder = mock_speculative_decoding.return_value
        mock_decoder.decode.return_value = {
            'decoded_text': 'This is a test response.'
        }

        request = InferenceRequest(input_text='Test input', max_tokens=5)
        response = inference(request)

        self.assertEqual(response['decoded_text'], 'This is a test response.')
        mock_decoder.decode.assert_called_once_with('Test input', max_tokens=5)

if __name__ == '__main__':
    unittest.main()