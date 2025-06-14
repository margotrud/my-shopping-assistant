# Chatbot/extractors/color/shared/vocab.py

"""
vocab.py
--------
Centralized vocabularies for tones, modifiers, and web colors.
"""

import webcolors
from matplotlib.colors import XKCD_COLORS

# Base vocab sets
css3 = set(webcolors.CSS3_NAMES_TO_HEX.keys())
xkcd = set(name.replace("xkcd:", "") for name in XKCD_COLORS.keys())

# Cosmetic tones not found in CSS/XKCD
cosmetic_fallbacks = {"nude"}

# Public shared vocab sets
all_webcolor_names = set(name.lower() for name in css3)
known_tones = set(name.lower() for name in css3.union(xkcd).union(cosmetic_fallbacks))
