import webcolors
from matplotlib.colors import XKCD_COLORS

css3 = set(webcolors.CSS3_NAMES_TO_HEX.keys())
css21 = set(webcolors.CSS21_NAMES_TO_HEX.keys())
xkcd = set(name.replace("xkcd:", "") for name in XKCD_COLORS.keys())

# 👇 No need to add mint/peach manually anymore
cosmetic_fallbacks = {"nude", "ash", "ink", "almond", "champagne"}  # Only keep what’s missing from XKCD/CSS

# ✅ This ensures 'mint', 'peach', 'lavender', etc. are all present
known_tones = set(name.lower() for name in css3.union(css21).union(xkcd).union(cosmetic_fallbacks))

all_webcolor_names = set(name.lower() for name in css3.union(css21))

print("terracotta" in known_tones)
print("earthy" in known_tones)
