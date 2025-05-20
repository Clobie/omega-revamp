# utils/common.py

from datetime import datetime
import random
import string
import re
import unicodedata
import secrets
import json

class Common:
    """
    Utility class for common helper functions including string manipulation,
    timestamp parsing, randomness, validation, and formatting.
    """

    def __init__(self):
        self.superscript_mapping = str.maketrans(
            "0123456789abcdefghijklmnopqrstuvwxyz.-",
            "⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ˙ˉ"
        )

    def chance(self, percent: float) -> bool:
        return random.random() < (percent / 100)

    def to_superscript(self, text: str) -> str:
        return text.translate(self.superscript_mapping)

    def remove_superscript(self, text: str) -> str:
        superscripts = "⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ˙ˉ"
        return ''.join(c for c in text if c not in superscripts)

    def generate_random_string(self, length: int = 10) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def get_unix_timestamp(date_str: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> int:
        try:
            dt = datetime.strptime(date_str, date_format)
            return int(dt.timestamp())
        except ValueError as e:
            return f"Error parsing date: {e}"
            raise

    @staticmethod
    def get_unix_interval(timestamp1: int, timestamp2: int) -> str:
        diff = abs(timestamp1 - timestamp2) / 1000
        if diff <= 300:
            return '5m'
        elif diff <= 3600:
            return 'hourly'
        else:
            return 'daily'

    def slugify(self, text: str) -> str:
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        text = re.sub(r'[^\w\s-]', '', text).strip().lower()
        return re.sub(r'[-\s]+', '-', text)

    def is_valid_email(self, email: str) -> bool:
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None

    def format_bytes(self, size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    def clamp(self, value: float, min_value: float, max_value: float) -> float:
        return max(min_value, min(value, max_value))

    def now_iso(self) -> str:
        return datetime.utcnow().isoformat() + "Z"

    def sanitize_filename(self, filename: str) -> str:
        return re.sub(r'[<>:"/\\|?*]', '_', filename)

    def random_choice_weighted(self, choices: list, weights: list) -> any:
        return random.choices(choices, weights=weights, k=1)[0]

    def time_ago(self, past_timestamp: int) -> str:
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

    def lerp(self, a: float, b: float, t: float) -> float:
        return a + (b - a) * t

    def map_range(self, value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def is_valid_url(self, url: str) -> bool:
        return re.match(r'^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$', url) is not None

    def secure_random_string(self, length: int = 16) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def flatten_list(self, nested: list) -> list:
        return [item for sublist in nested for item in sublist]

    def unique_list(self, items: list) -> list:
        seen = set()
        return [x for x in items if not (x in seen or seen.add(x))]

    def is_json(self, text: str) -> bool:
        try:
            json.loads(text)
            return True
        except ValueError:
            return False