from datetime import datetime
import random
import string
import re
import unicodedata
import secrets
import json
from typing import Any, List, Union


class Common:
    """
    Utility class for common helper functions including string manipulation,
    timestamp parsing, randomness, validation, and formatting.
    """

    _SUPERSCRIPT_MAP = str.maketrans(
        "0123456789abcdefghijklmnopqrstuvwxyz.-",
        "⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ˙ˉ"
    )
    _NORMAL_MAP = str.maketrans(
        "⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ˙ˉ",
        "0123456789abcdefghijklmnopqrstuvwxyz.-"
    )

    @staticmethod
    def roll_chance(percent: float) -> bool:
        """
        Return True with the given percent probability.
        """
        return random.random() < (percent / 100)

    @staticmethod
    def convert_to_superscript(text: str) -> str:
        """
        Convert normal characters to their superscript equivalents.
        """
        return text.translate(Common._SUPERSCRIPT_MAP)

    @staticmethod
    def convert_from_superscript(text: str) -> str:
        """
        Convert superscript characters back to normal characters.
        """
        return text.translate(Common._NORMAL_MAP)

    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """
        Generate a random alphanumeric string of given length.
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def get_unix_timestamp(date_str: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> int:
        """
        Convert a date string to a Unix timestamp (seconds since epoch).
        Raises ValueError if parsing fails.
        """
        dt = datetime.strptime(date_str, date_format)
        return int(dt.timestamp())

    @staticmethod
    def get_unix_interval(timestamp1: int, timestamp2: int) -> str:
        """
        Given two Unix timestamps in seconds, return a string representing the interval:
        '5m', 'hourly', or 'daily'.
        """
        diff = abs(timestamp1 - timestamp2)
        if diff <= 300:
            return '5m'
        elif diff <= 3600:
            return 'hourly'
        else:
            return 'daily'

    @staticmethod
    def slugify(text: str) -> str:
        """
        Convert text to a slug suitable for URLs/filenames.
        """
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        text = re.sub(r'[^\w\s-]', '', text).strip().lower()
        return re.sub(r'[-\s]+', '-', text)

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validate email format with a regex.
        """
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None

    @staticmethod
    def format_bytes(size: Union[int, float]) -> str:
        """
        Convert bytes count to human-readable string.
        """
        size = float(size)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                # Show no decimals for bytes, else 2 decimals
                if unit == 'B':
                    return f"{int(size)} {unit}"
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    @staticmethod
    def clamp(value: float, min_value: float, max_value: float) -> float:
        """
        Clamp a value between min_value and max_value.
        """
        return max(min_value, min(value, max_value))

    @staticmethod
    def now_iso() -> str:
        """
        Return current UTC time in ISO 8601 format with 'Z' suffix.
        """
        return datetime.utcnow().isoformat() + "Z"

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Replace invalid filename characters with underscores.
        """
        return re.sub(r'[<>:"/\\|?*]', '_', filename)

    @staticmethod
    def random_choice_weighted(choices: List[Any], weights: List[float]) -> Any:
        """
        Return a random element from choices based on weights.
        """
        return random.choices(choices, weights=weights, k=1)[0]

    @staticmethod
    def time_ago(past_timestamp: int) -> str:
        """
        Convert a past Unix timestamp into a human-readable "time ago" string.
        """
        now = int(datetime.utcnow().timestamp())
        diff = now - past_timestamp
        if diff < 60:
            return f"{diff}s ago"
        elif diff < 3600:
            return f"{diff // 60}m ago"
        elif diff < 86400:
            return f"{diff // 3600}h ago"
        else:
            return f"{diff // 86400}d ago"

    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        """
        Linear interpolation between a and b by fraction t (0 <= t <= 1).
        """
        return a + (b - a) * t

    @staticmethod
    def map_range(value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
        """
        Map a value from one range to another.
        """
        if in_max == in_min:
            raise ValueError("in_max and in_min cannot be the same value")
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Validate if the string is a valid HTTP, HTTPS, or FTP URL.
        """
        return re.match(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', url) is not None

    @staticmethod
    def secure_random_string(length: int = 16) -> str:
        """
        Generate a cryptographically secure random string of given length.
        """
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    @staticmethod
    def flatten_list(nested: List[List[Any]]) -> List[Any]:
        """
        Flatten a nested list by one level.
        """
        return [item for sublist in nested for item in sublist]

    @staticmethod
    def unique_list(items: List[Any]) -> List[Any]:
        """
        Return a list with unique elements preserving order.
        """
        seen = set()
        return [x for x in items if not (x in seen or seen.add(x))]

    @staticmethod
    def is_json(text: str) -> bool:
        """
        Check if the given string is valid JSON.
        """
        try:
            json.loads(text)
            return True
        except ValueError:
            return False
