# Chatbot/extractors/color/shared/constants.py

"""
constants.py
------------
Static blocklists or filters that don’t belong in vocab or dynamic config.
"""

BLOCKED_TOKENS = {
    ("light", "night"),
    ("romantic", "dramatic"),
}

COSMETIC_NOUNS = {
    "blush", "foundation", "lipstick", "concealer",
    "bronzer", "highlighter", "mascara", "eyeliner"
}

EXPRESSION_SUPPRESSION_RULES = {
    "glamorous": {"natural", "daytime"},
    "edgy": {"romantic", "soft glam"},
    "evening": {"daytime"},
    "bold": {"subtle", "neutral"},
    # Extend as needed
}
