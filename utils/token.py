import tiktoken

class Token:
    """
    Utility class for token counting and cost estimation based on OpenAI tokenization.

    Methods:
        - tokens_to_usd: Estimate USD cost for tokens used by a model given input and output texts.
        - count_tokens: Count the number of tokens in a given text for a specific model.
    """

    @staticmethod
    def tokens_to_usd(model, context, result, cpm_context, cpm_result) -> float:
        """
        Calculate cost in USD for tokens consumed by a given model.

        Parameters:
            model (str): Model name for tokenizer (e.g., "gpt-4", "gpt-3.5-turbo").
            context (str): Input text to encode (prompt tokens).
            result (str): Output text to encode (completion tokens).
            cpm_context (float): Cost per million tokens for context tokens.
            cpm_result (float): Cost per million tokens for result tokens.

        Returns:
            float: Estimated cost in USD rounded to 8 decimal places.
        """
        encoding = tiktoken.encoding_for_model(model)
        t_context = len(encoding.encode(context))
        t_result = len(encoding.encode(result))
        cost = ((cpm_context * t_context) + (cpm_result * t_result)) / 1_000_000.0
        return round(cost, 8)

    @staticmethod
    def count_tokens(model, text) -> int:
        """
        Count the number of tokens in a given text for a specific model.

        Parameters:
            model (str): Model name for tokenizer.
            text (str): Text to tokenize.

        Returns:
            int: Number of tokens.
        """
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
