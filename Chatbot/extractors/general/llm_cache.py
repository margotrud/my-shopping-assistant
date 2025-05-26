# Chatbot/cache/color_llm_cache.py

import json
import os

_rgb_cache = {}
_simplify_cache = {}

import os

# Always resolve relative to this script's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
CACHE_FILE_PATH = os.path.join(PROJECT_ROOT, "Data", "color_llm_cache.json")


def get_cached_rgb(phrase: str):
    return _rgb_cache.get(phrase.lower().strip())


def store_rgb_to_cache(phrase: str, rgb: tuple):
    _rgb_cache[phrase.lower().strip()] = rgb


def get_cached_simplified(phrase: str):
    return _simplify_cache.get(phrase.lower().strip())


def store_simplified_to_cache(phrase: str, simplified: list):
    _simplify_cache[phrase.lower().strip()] = simplified


def clear_caches():
    _rgb_cache.clear()
    _simplify_cache.clear()




def get_full_cache():
    return {
        "rgb": _rgb_cache.copy(),
        "simplified": _simplify_cache.copy()
    }


def save_cache_to_file(path: str = CACHE_FILE_PATH):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({
                "rgb": _rgb_cache,
                "simplified": _simplify_cache
            }, f, indent=2)
        print(f"[💾 CACHE SAVED] → {path}")
    except Exception as e:
        print(f"[❌ ERROR] Saving cache → {e}")


def load_cache_from_file(path: str = CACHE_FILE_PATH):
    if not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            _rgb_cache.update(data.get("rgb", {}))
            _simplify_cache.update(data.get("simplified", {}))
        print(f"[📂 CACHE LOADED] ← {path}")
    except Exception as e:
        print(f"[❌ ERROR] Loading cache → {e}")
