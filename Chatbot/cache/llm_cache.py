# Chatbot/cache/color_llm_cache.py

import json
import os
from typing import Optional, Tuple, List

from Chatbot.extractors.general.utils.fuzzy_match import normalize_token


class ColorLLMCache:
    """
    Singleton class to manage caching of LLM-based RGB resolutions and simplified phrases.

    - RGB values are stored as: { "peachy beige": [243, 207, 183] }
    - Simplified phrases are stored as: { "peachy": ["light peach"] }
    """

    _instance = None

    @staticmethod
    def get_instance():
        if ColorLLMCache._instance is None:
            ColorLLMCache._instance = ColorLLMCache()
        return ColorLLMCache._instance

    def __init__(self):
        if ColorLLMCache._instance is not None:
            raise Exception("Use get_instance() instead of direct instantiation.")
        self._rgb_cache = {}
        self._simplify_cache = {}
        self._path = self._default_path()
        self.load()

    def _default_path(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
        return os.path.join(project_root, "Data", "color_llm_cache.json")

    def get_rgb(self, phrase: str) -> Optional[Tuple[int, int, int]]:
        val = self._rgb_cache.get(normalize_token(phrase))
        return tuple(val) if isinstance(val, list) else val

    def store_rgb(self, phrase: str, rgb: Tuple[int, int, int]):
        self._rgb_cache[normalize_token(phrase)] = list(rgb)

    def get_simplified(self, phrase: str) -> List[str]:
        return self._simplify_cache.get(normalize_token(phrase), [])

    def store_simplified(self, phrase: str, simplified: List[str]):
        self._simplify_cache[normalize_token(phrase)] = simplified

    def clear(self):
        self._rgb_cache.clear()
        self._simplify_cache.clear()

    def save(self):
        try:
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump({
                    "rgb": self._rgb_cache,
                    "simplified": self._simplify_cache
                }, f, indent=2)
            print(f"[💾 CACHE SAVED] → {self._path}")
        except Exception as e:
            print(f"[❌ ERROR] Saving cache → {e}")

    def load(self):
        if not os.path.exists(self._path):
            return
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._rgb_cache.update(data.get("rgb", {}))
                self._simplify_cache.update(data.get("simplified", {}))
            print(f"[📂 CACHE LOADED] ← {self._path}")
        except Exception as e:
            print(f"[❌ ERROR] Loading cache → {e}")
