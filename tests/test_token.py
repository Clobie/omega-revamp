import unittest
from unittest.mock import patch, MagicMock
from utils.token import Token


class TestToken(unittest.TestCase):

    @patch("utils.token.tiktoken.encoding_for_model")
    def test_count_tokens_basic(self, mock_encoding_for_model):
        # Arrange
        mock_encoding = MagicMock()
        mock_encoding.encode.return_value = [1, 2, 3, 4, 5]
        mock_encoding_for_model.return_value = mock_encoding

        # Act
        result = Token.count_tokens("gpt-4", "Hello world!")

        # Assert
        self.assertEqual(result, 5)
        mock_encoding.encode.assert_called_once_with("Hello world!")
        mock_encoding_for_model.assert_called_once_with("gpt-4")

    @patch("utils.token.tiktoken.encoding_for_model")
    def test_tokens_to_usd_basic(self, mock_encoding_for_model):
        # Arrange
        mock_encoding = MagicMock()
        mock_encoding.encode.side_effect = [
            [1, 2, 3],        # context = 3 tokens
            [10, 11, 12, 13]  # result = 4 tokens
        ]
        mock_encoding_for_model.return_value = mock_encoding

        model = "gpt-4"
        context = "This is a test."
        result = "Generated response."
        cpm_context = 30.0     # $30 / million tokens
        cpm_result = 60.0      # $60 / million tokens

        # Act
        cost = Token.tokens_to_usd(model, context, result, cpm_context, cpm_result)

        # Expected cost:
        # (3 * 30 + 4 * 60) / 1_000_000 = (90 + 240) / 1_000_000 = 330 / 1_000_000 = 0.00033
        self.assertAlmostEqual(cost, 0.00033, places=8)

        # Assert calls
        self.assertEqual(mock_encoding.encode.call_count, 2)
        mock_encoding_for_model.assert_called_once_with(model)

    @patch("utils.token.tiktoken.encoding_for_model")
    def test_empty_strings(self, mock_encoding_for_model):
        mock_encoding = MagicMock()
        mock_encoding.encode.side_effect = [[], []]
        mock_encoding_for_model.return_value = mock_encoding

        # Act
        cost = Token.tokens_to_usd("gpt-4", "", "", 10.0, 10.0)

        # Assert
        self.assertEqual(cost, 0.0)

    @patch("utils.token.tiktoken.encoding_for_model")
    def test_large_token_count(self, mock_encoding_for_model):
        # Arrange
        mock_encoding = MagicMock()
        mock_encoding.encode.side_effect = [
            list(range(10000)),  # context
            list(range(20000))   # result
        ]
        mock_encoding_for_model.return_value = mock_encoding

        cost = Token.tokens_to_usd("gpt-4", "x" * 10000, "y" * 20000, 15.0, 30.0)

        # Expected: (10000 * 15 + 20000 * 30) / 1_000_000 = (150000 + 600000) / 1_000_000 = 0.75
        self.assertAlmostEqual(cost, 0.75, places=8)

    @patch("utils.token.tiktoken.encoding_for_model", side_effect=KeyError("Invalid model"))
    def test_invalid_model_raises(self, mock_encoding_for_model):
        with self.assertRaises(KeyError):
            Token.count_tokens("nonexistent-model", "some text")


if __name__ == "__main__":
	unittest.main()
