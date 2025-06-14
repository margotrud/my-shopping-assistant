"""
Color Extractor Package Init
----------------------------
Provides package-level access to shared vocab sets and key extractor modules.
"""

from .shared.vocab import known_tones, all_webcolor_names

__all__ = [
    "known_tones",
    "all_webcolor_names",
]
