"""
Color Extractor Package Init
----------------------------
Exposes all key extractor logic via flat imports,
including tones, modifiers, phrase extraction, and helpers.
"""

# ── Public color vocab sets ─────────────────────────────

import webcolors
from matplotlib.colors import XKCD_COLORS

# CSS3 + XKCD names
css3 = set(webcolors.CSS3_NAMES_TO_HEX.keys())
xkcd = set(name.replace("xkcd:", "") for name in XKCD_COLORS.keys())

# Fallback additions (can expand later)
cosmetic_fallbacks = {"nude"}  # Expand if needed

# Final vocab sets
all_webcolor_names = set(name.lower() for name in css3)             # CSS3 only
known_tones = set(name.lower() for name in css3.union(xkcd).union(cosmetic_fallbacks))  # Full tone set

# ── Key extraction entry point ───────────────────────────
from .phrase_extractor import (
    extract_phrases_from_segment,
    extract_all_descriptive_color_phrases
)

# ── Low-level logic modules (used internally or for testing) ──
from .compound_extraction import extract_compound_phrases
from .standalone_extraction import extract_standalone_phrases, extract_lone_tones
from .fallback_extraction import extract_suffix_fallbacks
from .tokenizer import singularize, tokenize_text
from .modifier_resolution import resolve_modifier_with_suffix_fallback, should_suppress_compound