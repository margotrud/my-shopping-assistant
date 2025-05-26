import webcolors
from matplotlib.colors import XKCD_COLORS

# Load CSS3 and XKCD color names
css3 = set(webcolors.CSS3_NAMES_TO_HEX.keys())
xkcd = set(name.replace("xkcd:", "") for name in XKCD_COLORS.keys())

# Add fallback cosmetic tones not in webcolors
cosmetic_fallbacks = {"nude"}  # Expand if needed

# Shared vocabularies
all_webcolor_names = set(name.lower() for name in css3)             # CSS3 only
known_tones = set(name.lower() for name in css3.union(xkcd).union(cosmetic_fallbacks))  # Full tone set
